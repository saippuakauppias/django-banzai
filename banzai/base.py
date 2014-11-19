from banzai.settings import (BANZAI_API_DOMAIN, BANZAI_API_VERSION,
                             BANZAI_API_KEY)


class MailPackage(object):

    def __init__(self, email_from, name_from, subject, message, send_at=None,
                 headers=[], attach_images=False, description=''):
        self.email_from = email_from
        self.name_from = name_from
        self.subject = subject
        self.message = message
        self.send_at = send_at
        self.headers = headers
        self.attach_images = attach_images
        self.description = description

    def add_user(self, email_to, name_to='', header={}, fields={}):
        pass

    def save(self):
        pass

    def generate(self):
        pass


class BanzaiAPI(object):

    def __init__(self, package_obj):
        self.package_obj = package_obj
        self.api_key = BANZAI_API_KEY
        self.api_url = 'http://{0}/api/{1}/'.format(BANZAI_API_DOMAIN,
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
