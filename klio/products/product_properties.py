from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ProductPropertiesContainer(object):
    """
    To set attributes on a product, use the `props` attribute:
        product.props.size = 70
    """

    # Checked
    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    # Checked
    def __init__(self, product):
        self.product = product
        self.initialised = False

    # Checked
    def initiate_properties(self):
        values = self.get_values().select_related('property')
        for v in values:
            setattr(self, v.property.name, v.value)
        self.initialised = True

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            self.initiate_properties()
            return getattr(self, name)
        raise AttributeError(
            _("%(obj)s has no property named '%(prop)s'") % {
                'obj': self.product.get_product_type(), 'prop': name})

    def validate_properties(self):
        for property in self.get_all_properties():
            value = getattr(self, property.name, None)
            if value is None:
                if property.required:
                    raise ValidationError(
                        _("%(prop)s property cannot be blank") %
                        {'prop': property.name})
            else:
                try:
                    property.validate_value(value)
                except ValidationError as e:
                    raise ValidationError(
                        _("%(prop)s property %(err)s") %
                        {'prop': property.name, 'err': e})

    # Checked
    def get_property_by_name(self, name):
        return self.get_all_properties().get(name=name)

    # Checked
    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for property in self.get_all_properties():
            if hasattr(self, property.name):
                value = getattr(self, property.name)
                property.save_value(self.product, value)
