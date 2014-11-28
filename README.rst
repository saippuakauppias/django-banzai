django-banzai
=============

API обёртка на Python над сервисом `get-n-post.ru <http://get-n-post.ru/>`_.

Зависимости
-----------

Пакету требуются: `requests <https://pypi.python.org/pypi/requests>`_ и `lxml <https://pypi.python.org/pypi/lxml>`_.

Установка и настройка
---------------------

Установить пакет из PyPI::

    $ pip install django-banzai

Добавить приложение ``banzai`` в ваши ``INSTALLED_APPS``.

Заполнить в настройках ``BANZAI_API_KEY`` - API-ключ, сгенерированный сервисом для вашего IP-адреса.

Использование
-------------

Отправить email с django-совместимым синтаксисом::

    from banzai.base import send_mail

    send_mail('subject', 'mail body', 'from@myprojectand.me', ['to@lovely.users'])

Или отправить email согласно принципам get-n-post::

    from banzai.mail import MailPackage
    from banzai.api import BanzaiAPI

    mail_package = MailPackage(email_from, name_from, subject, message)
    mail_package.add_recipients(recipient_list)
    package = mail_package.save()

    banzai_api_obj = BanzaiAPI(package)
    package = banzai_api_obj.add()
