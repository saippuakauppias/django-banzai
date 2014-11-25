django-banzai
=============

Python API Wrapper for `get-n-post.ru <http://get-n-post.ru/>`_ service.

Requirements
------------

`requests <https://pypi.python.org/pypi/requests>`_ and `lxml <https://pypi.python.org/pypi/lxml>`_.

Installation
------------

Installing with pip::

    $ pip install django-banzai

Add ``banzai`` in ``INSTALLED_APPS``.

Fill your API key in ``BANZAI_API_KEY`` settings.

Usage
-----

Send email with django compatible syntax::

    from banzai.base import send_mail

    send_mail('subject', 'mail body', 'from@myprojectand.me', ['to@lovely.users'])

Or send emails with get-n-post principles::

    from banzai.mail import MailPackage
    from banzai.api import BanzaiAPI

    mail_package = MailPackage(email_from, name_from, subject, message)
    mail_package.add_recipients(recipient_list)
    package = mail_package.save()

    banzai_api_obj = BanzaiAPI(package)
    package = banzai_api_obj.add()
