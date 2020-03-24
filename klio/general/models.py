from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from tags.models import Tag

User = get_user_model()


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(help_text='Date to be shown in article.')
    start_date = models.DateTimeField(help_text='Date to make article visible on site.')
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(blank=True)
    tag = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'))
    content = RichTextField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:50]

    class Meta:
        ordering = ['-activity', '-date']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class Banner(models.Model):
    YELLOW = 'yellow'
    RED = 'red'
    WHITE = 'white'
    BLACK = 'black'
    BTN_COLORS = [
        (YELLOW, 'Yellow'),
        (RED, 'Red'),
        (WHITE, 'White'),
        (BLACK, 'Black'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    img = models.ImageField(blank=False, help_text=_('Upload image 1200x675 px.'))
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    link = models.URLField(blank=True)
    btn = models.BooleanField(default=True)
    btn_text = models.CharField(max_length=32, blank=True, null=False)
    btn_color = models.CharField(max_length=10, choices=BTN_COLORS, default=WHITE)
    start_date = models.DateTimeField(help_text='From what date banner should be visible on a site?')
    deadline = models.DateTimeField(help_text='When banner should disappear from a site?')
    activity = models.BooleanField(default=True)

    def __str__(self):
        return "#{0} {1}".format(self.id, self.name)

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')


class CallbackInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    """ Automatically uploaded for registered users. """
    name = models.CharField(max_length=32, blank=False)
    """ Automatically uploaded for registered users. """
    phone = models.CharField(max_length=20, blank=False,
                             help_text='Enter the phone in the format +7(XXX)XXX-XX-XX.')
    comment = models.TextField(blank=False)

    def __str__(self):
        return _("Callback") + " #{0}".format(self.id)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Callback info')
        verbose_name_plural = _('Callback info')


class Menu(models.Model):
    HEADER, FOOTER, LEFTBAR = 'header', 'footer', 'leftbar'
    MENU_POSITIONS = [
        (HEADER, 'Header'),
        (FOOTER, 'Footer'),
        (LEFTBAR, 'Leftbar'),
    ]

    name = models.CharField(max_length=32, blank=False, null=False)
    position = models.CharField(max_length=10, choices=MENU_POSITIONS)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'name']
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')


# TODO: Remove slug and add actual relation to object or leave free link.
class MenuItem(models.Model):
    CATEGORY, PRODUCT_LIST, PAGE, ARTICLE, NEWS, EXTERNAL = \
        'category', 'products', 'page', 'article', 'news', 'external'
    RELATED_OBJ_TYPES = [
        (CATEGORY, 'Category'),
        (PRODUCT_LIST, 'Product list'),
        (PAGE, 'Page'),
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
        (EXTERNAL, 'External'),
    ]

    name = models.CharField(max_length=64, blank=False, null=False)
    slug = models.SlugField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(blank=False, default=1)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=False, related_name='items')
    related_type = models.CharField(max_length=10, choices=RELATED_OBJ_TYPES, default=CATEGORY)
    """ Use this field to link an outer site. """
    link = models.URLField(blank=True)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['menu', 'order', 'name']
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')


# TODO: Add meta info to all objects.
# class MetaMixin(models.AbstractModel):
#     meta_title = models.CharField()
#     meta_desc = models.CharField()
#     meta_keywords = models.CharField()


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(help_text='Date to be shown in article.')
    start_date = models.DateTimeField(help_text='Date to make article visible on site.')
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(blank=True)
    tag = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'))
    content = RichTextField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:50]

    class Meta:
        ordering = ['-activity', '-date']
        verbose_name = _('News')
        verbose_name_plural = _('News')


class Page(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    slug = models.SlugField()
    content = RichTextField()
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'name']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class SubscriberInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    """ Automatically uploaded for registered users. """
    name = models.CharField(max_length=32, blank=False)
    """ Automatically uploaded for registered users. """
    email = models.EmailField(blank=False)

    def __str__(self):
        return _("Subscription") + " #{0}".format(self.id)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Subscriber info')
        verbose_name_plural = _('Subscriber info')
