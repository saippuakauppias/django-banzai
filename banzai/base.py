import hashlib
from lxml import etree
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile

import requests

from banzai.models import Package, Report
from banzai.settings import (BANZAI_API_DOMAIN, BANZAI_API_VERSION,
                             BANZAI_API_KEY)


class MailPackage(object):

    def __init__(self, email_from, name_from, subject, message, send_at=None,
                 headers=[], attach_images=u'0', description=u''):
        self.email_from = email_from
        self.name_from = name_from
        self.subject = subject
        self.message = message
        self.send_at = send_at
        self.headers = headers
        self.attach_images = attach_images
        self.description = description

        self._users_data = []
        self._xml = etree.Element('list')
        self._generation_complete = False
        self._package = None

    def add_user(self, email_to, name_to=u'', header={}, fields={}):
        if self._generation_complete:
            raise RuntimeError('Impossibly add user, because '
                               'generation already complete!')
        self._users_data.append({
            'email_to': email_to,
            'name_to': name_to,
            'header': header,
            'fields': fields
        })

    def save(self):
        if self._package is None:
            file_name = '{0}#{1}'.format(datetime.now(), settings.SECRET_KEY)
            file_name = hashlib.md5(file_name).hexdigest()
            file_name = '{0}.xml'.format(file_name)

            package_obj = Package(
                emails_all=len(self._users_data),
                description=self.description
            )
            xml_content = ContentFile(self.xml_tostring())
            package_obj.file.save(file_name, xml_content)
            package_obj.save()
            self._package = package_obj
        return self._package

    def xml_tostring(self):
        self._generate()
        return etree.tostring(self._xml, encoding='UTF-8',
                              xml_declaration=True)

    def _generate(self):
        if self._generation_complete:
            return
        body_tag = etree.Element('body')

        data_tag = etree.Element('Data')
        data_tag.text = etree.CDATA(self.message)
        body_tag.append(data_tag)
        del data_tag

        email_from_tag = etree.Element('EmailFrom')
        email_from_tag.text = etree.CDATA(self.email_from)
        body_tag.append(email_from_tag)
        del email_from_tag

        name_from_tag = etree.Element('NameFrom')
        name_from_tag.text = etree.CDATA(self.name_from)
        body_tag.append(name_from_tag)
        del name_from_tag

        subject_tag = etree.Element('Subject')
        subject_tag.text = etree.CDATA(self.subject)
        body_tag.append(subject_tag)
        del subject_tag

        attach_images_tag = etree.Element('AttachImages')
        attach_images_tag.text = etree.CDATA(self.attach_images)
        body_tag.append(attach_images_tag)
        del attach_images_tag

        if self.send_at is not None:
            send_at_tag = etree.Element('SendAt')
            send_at_str = self.send_at.strftime('%Y/%m/%d %H:%M')
            send_at_tag.text = etree.CDATA(send_at_str)
            body_tag.append(send_at_tag)
            del send_at_tag, send_at_str

        for header in self.headers:
            header_tag = etree.Element('Header')
            header_tag.attrib['name'] = header['name']
            header_tag.attrib['value'] = header['value']
            body_tag.append(header_tag)
            del header_tag

        self._xml.append(body_tag)
        del body_tag

        users_tag = etree.Element('users')
        for user in self._users_data:
            current_user_tag = etree.Element('user')

            email_to_tag = etree.Element('EmailTo')
            email_to_tag.text = etree.CDATA(user['email_to'])
            current_user_tag.append(email_to_tag)
            del email_to_tag

            if user['name_to']:
                name_to_tag = etree.Element('NameTo')
                name_to_tag.text = etree.CDATA(user['name_to'])
                current_user_tag.append(name_to_tag)
                del name_to_tag

            if user['header']:
                header_tag = etree.Element('Header')
                header_tag.attrib['name'] = user['header']['name']
                header_tag.attrib['value'] = user['header']['value']
                current_user_tag.append(header_tag)
                del header_tag

            for field in user['fields']:
                field_tag = etree.Element(field['name'])
                field_tag.text = etree.CDATA(field['value'])
                current_user_tag.append(field_tag)
                del field_tag

            users_tag.append(current_user_tag)
            del current_user_tag

        self._xml.append(users_tag)
        del users_tag

        self._generation_complete = True


class BanzaiAPI(object):

    def __init__(self, package_obj):
        self._package = package_obj
        self._package_url = None

        self._api_key = BANZAI_API_KEY
        self._base_api_url = 'http://{0}/api/{1}/'.format(BANZAI_API_DOMAIN,
                                                          BANZAI_API_VERSION)

    @property
    def package_url(self):
        if self._package_url is None:
            current_site = Site.objects.get_current()
            url = 'http://{0}{1}{2}'.format(
                current_site.domain,
                settings.MEDIA_URL,
                self._package.file.url
            )
            self._package_url = url
        return self._package_url

    def _api_url(self, method):
        return '{0}{1}'.format(self._base_api_url, method)

    def _parse_xml(self, data):
        parser = etree.XMLParser()
        parser.feed(data)
        return parser.close()

    def add(self):
        get_params = {'key': self._api_key, 'url': self.package_url}
        req = requests.get(self._api_url('add_package'), params=get_params)

        elem = self._parse_xml(req.content)

        pack_id = elem.find('pack_id')
        if pack_id is not None:
            self._package.pack_id = pack_id.text

        status = elem.find('status')
        if status is not None:
            self._package.status = status.text

        self._package.save()

    def fast_add(self):
        get_params = {'key': self._api_key}
        post_data = {
            'package': self._package.file.read(),
            'description': self._package.description
        }
        req = requests.post(self._api_url('fast_add_package'),
                            params=get_params, data=post_data)

        elem = self._parse_xml(req.content)

        pack_id = elem.find('pack_id')
        if pack_id is not None:
            self._package.pack_id = pack_id.text

        status = elem.find('status')
        if status is not None:
            self._package.status = status.text

        user_count = elem.find('user_count')
        if user_count is not None:
            self._package.emails_correct = user_count.text

        self._package.save()

    def check(self):
        get_params = {'key': self._api_key}
        post_data = {
            'package': self._package.file.read(),
        }
        req = requests.post(self._api_url('check_package'),
                            params=get_params, data=post_data)

        elem = self._parse_xml(req.content)

        status = elem.find('status')
        if status is not None:
            self._package.status = status.text

        user_count = elem.find('user_count')
        if user_count is not None:
            self._package.emails_correct = user_count.text

        self._package.save()

    def status(self):
        get_params = {'key': self._api_key, 'pack_id': self._package.pack_id}
        req = requests.get(self._api_url('package_status'), params=get_params)

        elem = self._parse_xml(req.content)

        status = elem.find('status')
        if status is not None:
            self._package.status = status.text

        self._package.save()

    def report(self):
        get_params = {'key': self._api_key, 'pack_id': self._package.pack_id}
        req = requests.get(self._api_url('package_report'), params=get_params)

        elem = self._parse_xml(req.content)

        items = elem.findall('item')
        for item in items:
            email = ''
            reject_code = ''
            reject_message = ''

            email_elem = item.find('email')
            if email_elem is not None:
                email = email_elem.text

            code_elem = item.find('code')
            if code_elem is not None:
                reject_code = code_elem.text

            message_elem = item.find('message')
            if message_elem is not None:
                reject_message = message_elem.text

            report_obj, _ = Report.objects.get_or_create(
                package=self._package,
                email=email,
                reject_code=reject_code,
                reject_message=reject_message,
            )
        else:
            status = elem.find('status')
            if status is not None:
                report_obj, _ = Report.objects.get_or_create(
                    package=self._package,
                    status=status.text
                )

    def report_fbl(self):
        pass

    def stop(self):
        pass
