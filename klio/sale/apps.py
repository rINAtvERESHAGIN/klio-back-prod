from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SaleConfig(AppConfig):
    name = 'sale'
    verbose_name = _('Sale App')
