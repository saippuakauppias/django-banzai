from django.db import models
from django.utils.translation import ugettext_lazy as _


STATUS_GOOD_CODES = (
    ('S001', _('The package was not found at the specified URL')),
    ('S002', _('The package is uploaded to the server')),
    ('S004', _('The package is sent')),
    ('S005', _('The package is mailed. The expected removal '
               'of information about the package from the system.')),
    ('S006', _('While sending errors occurred')),
    ('S007', _('Invalid packet format')),
    ('S008', _('Has timed out the server response')),
    ('S009', _('Package received')),
    ('S010', _('The package is checked')),
    ('S011', _('The packet is processed (formed message)')),
    ('S012', _('The package is queued for deletion')),
    ('S013', _('The package is deleted. The messages stopped.')),
    ('S015', _('The number of addressees exceeds this limit')),
    ('S018', _('The package is mailed. Package information removed.')),
    ('S019', _('The package is checked. Will be sent at the specified time.')),
)
STATUS_ERROR_CODES = (
    ('E000', _('The secret key specified in the parameters of '
               'the operation, is not recognized')),
    ('E001', _('Not given URL')),
    ('E002', _('Not transferred pack_id')),
    ('E003', _('Information about the package not found')),
    ('E004', _('Not enough traffic')),
    ('E005', _('Not paid rate')),
    ('E006', _('Incorrect data in the package')),
)
STATUS_CODES = STATUS_GOOD_CODES + STATUS_ERROR_CODES


class Package(models.Model):

    file = models.FileField(_('xml package'),
                            upload_to='django_banzai/package')
    status = models.CharField(_('status code'), choices=STATUS_CODES,
                              max_length=4, blank=True)
    pack_id = models.CharField(_('package ID'), max_length=100)

    emails_all = models.PositiveIntegerField(_('emails all'))
    emails_correct = models.PositiveIntegerField(_('emails correct'),
                                                 default=0)

    description = models.CharField(_('description'), max_length=100,
                                   blank=True)

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')

    def __unicode__(self):
        return u'ID: {0}, status: "{1}", description: "{2}"'.format(
            self.pk,
            self.status,
            self.description
        )


class Report(models.Model):

    package = models.ForeignKey(Package, verbose_name=_('package'))
    status = models.CharField(_('status code'), choices=STATUS_CODES,
                              max_length=4, blank=True)

    email = models.EmailField(_('email'))
    reject_code = models.CharField(_('reject code'), max_length=250)
    reject_message = models.TextField(_('reject message'))

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

    def __unicode__(self):
        return u'Email: {0}, Reject code: "{1}"'.format(
            self.email,
            self.reject_code
        )


class ReportFBL(models.Model):

    package = models.ForeignKey(Package, verbose_name=_('package'))
    status = models.CharField(_('status code'), choices=STATUS_CODES,
                              max_length=4, blank=True)
    email = models.EmailField(_('email'))

    class Meta:
        verbose_name = _('feedback list report')
        verbose_name_plural = _('feedback list reports')

    def __unicode__(self):
        return self.email
