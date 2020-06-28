from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        """
        Checks categories.
        """

        getattr(self, '_clean_%s' % self.cleaned_data.get('kind'))()

    def _clean_unique(self):
        categories = self.cleaned_data.get('categories')
        if categories.exists():
            return self.cleaned_data
        raise ValidationError(_('Unique product should contain at least one category'))

    def _clean_parent(self):
        categories = self.cleaned_data.get('categories')
        if categories.exists():
            return self.cleaned_data
        raise ValidationError(_('Parent product should contain at least one category'))

    def _clean_child(self):
        categories = self.cleaned_data.get('categories')
        if not categories.exists():
            return self.cleaned_data
        raise ValidationError(_('Child product inherit its parent category.'))
