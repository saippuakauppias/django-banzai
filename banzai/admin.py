from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from banzai.models import Package, Report, ReportFBL


class ReportInline(admin.StackedInline):

    extra = 0
    model = Report
    verbose_name = _('report')
    readonly_fields = ('status', 'email', 'reject_code', 'reject_message',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReportFBLInline(admin.StackedInline):

    extra = 0
    model = ReportFBL
    verbose_name = _('feedback list report')
    readonly_fields = ('status', 'email',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PackageAdmin(admin.ModelAdmin):

    list_display = ('id', 'description', 'status', 'pack_id', 'emails_all',
                    'emails_correct',)
    readonly_fields = ('file', 'status', 'pack_id', 'emails_all',
                       'emails_correct', 'description',)
    inlines = (ReportInline, ReportFBLInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Package, PackageAdmin)
