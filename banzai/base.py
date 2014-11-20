from lxml import etree

from banzai.settings import (BANZAI_API_DOMAIN, BANZAI_API_VERSION,
                             BANZAI_API_KEY)


class MailPackage(object):

    def __init__(self, email_from, name_from, subject, message, send_at=None,
                 headers=[], attach_images='0', description=''):
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

    def add_user(self, email_to, name_to='', header={}, fields={}):
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
        pass

    def xml_tostring(self):
        self._generate()
        return etree.tostring(self._xml, encoding='UTF-8',
                              xml_declaration=True)

    def _generate(self):
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
        self.package_obj = package_obj
        self._api_key = BANZAI_API_KEY
        self._api_url = 'http://{0}/api/{1}/'.format(BANZAI_API_DOMAIN,
                                                     BANZAI_API_VERSION)

    def add(self):
        pass

    def fast_add(self):
        pass

    def check(self):
        pass

    def status(self):
        pass

    def report(self):
        pass

    def report_fbl(self):
        pass

    def stop(self):
        pass
