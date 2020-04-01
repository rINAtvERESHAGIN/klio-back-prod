from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from tags.models import Tag

User = get_user_model()


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    date = models.DateTimeField(help_text=_('Date to be shown in article.'), verbose_name=_('published'))
    start_date = models.DateTimeField(help_text=_('Date to make article visible on site.'),
                                      verbose_name=_('start date'))
    title = models.CharField(max_length=256, blank=False, null=False, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('author'))
    img = models.ImageField(blank=True, verbose_name=_('image'))
    tags = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'), verbose_name=_('tags'))
    abstract = models.TextField(verbose_name=_('abstract'), max_length=256,
                                help_text=_('Short description - 256 symbols max.'))
    content = RichTextField(verbose_name=_('content'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

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
        (YELLOW, _('Yellow')),
        (RED, _('Red')),
        (WHITE, _('White')),
        (BLACK, _('Black')),
    ]

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    name = models.CharField(max_length=256, blank=False, null=False, verbose_name=_('name'))
    img = models.ImageField(blank=False, help_text=_('Upload image 1200x675 px.'), verbose_name=_('image'))
    content = models.TextField(blank=True, verbose_name=_('content'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('order'))
    link = models.URLField(blank=True, verbose_name=_('link'))
    btn = models.BooleanField(default=True, verbose_name=_('button is on'))
    btn_text = models.CharField(max_length=32, blank=True, null=False, verbose_name=_('button text'))
    btn_color = models.CharField(max_length=10, choices=BTN_COLORS, default=WHITE, verbose_name=_('button color'))
    start_date = models.DateTimeField(help_text=_('From what date banner should be visible on a site?'),
                                      verbose_name=_('start date'))
    deadline = models.DateTimeField(help_text=_('When banner should disappear from a site?'),
                                    verbose_name=_('deadline'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    def __str__(self):
        return "#{0} {1}".format(self.id, self.name)

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')


class CallbackInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('user'))
    """ Automatically uploaded for registered users. """
    name = models.CharField(max_length=32, blank=False, verbose_name=_('name'))
    """ Automatically uploaded for registered users. """
    phone = models.CharField(max_length=20, blank=False, verbose_name=_('phone'),
                             help_text=_('Enter the phone in the format +7(XXX)XXX-XX-XX.'))
    comment = models.TextField(blank=False, verbose_name=_('comment'))

    def __str__(self):
        return _("Callback") + " #{0}".format(self.id)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Callback info')
        verbose_name_plural = _('Callback info')


class Menu(models.Model):
    HEADER, FOOTER, LEFTBAR = 'header', 'footer', 'leftbar'
    MENU_POSITIONS = [
        (HEADER, _('Header')),
        (FOOTER, _('Footer')),
        (LEFTBAR, _('Leftbar')),
    ]

    name = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('name'))
    position = models.CharField(max_length=10, choices=MENU_POSITIONS, verbose_name=_('position'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

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
        (CATEGORY, _('Category')),
        (PRODUCT_LIST, _('Product list')),
        (PAGE, _('Page')),
        (ARTICLE, _('Article')),
        (NEWS, _('News')),
        (EXTERNAL, _('External')),
    ]

    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(blank=True, verbose_name=_('slug'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('parent'))
    order = models.PositiveIntegerField(blank=False, default=1, verbose_name=_('order'))
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=False, related_name='items', verbose_name=_('menu'))
    related_type = models.CharField(max_length=10, choices=RELATED_OBJ_TYPES, default=CATEGORY,
                                    verbose_name=_('related type'))
    """ Use this field to link an outer site. """
    link = models.URLField(blank=True, verbose_name=_('link'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

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
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    date = models.DateTimeField(help_text=_('Date to be shown in article.'), verbose_name=_('date'))
    start_date = models.DateTimeField(help_text=_('Date to make article visible on site.'),
                                      verbose_name=_('start date'))
    title = models.CharField(max_length=256, blank=False, null=False, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('author'))
    img = models.ImageField(blank=True, verbose_name=_('image'))
    tags = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'), verbose_name=_('tags'))
    content = RichTextField(verbose_name=_('content'))
    abstract = models.TextField(verbose_name=_('abstract'), max_length=256,
                                help_text=_('Short description - 256 symbols max.'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

    def __str__(self):
        return self.title[:50]

    class Meta:
        ordering = ['-activity', '-date']
        verbose_name = _('News item')
        verbose_name_plural = _('News')


class Page(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    name = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    content = RichTextField(verbose_name=_('content'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-activity', 'name']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class SubscriberInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('user'))
    """ Automatically uploaded for registered users. """
    name = models.CharField(max_length=32, blank=False, verbose_name=_('name'))
    """ Automatically uploaded for registered users. """
    email = models.EmailField(blank=False)

    def __str__(self):
        return _("Subscription") + " #{0}".format(self.id)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Subscriber info')
        verbose_name_plural = _('Subscriber info')
