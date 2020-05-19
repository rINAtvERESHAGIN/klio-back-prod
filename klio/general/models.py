from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from tags.models import Tag

User = get_user_model()


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'),
                                  help_text=_('Leave blank to fill automatically with name.'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'),
                                        help_text=_('Leave blank to fill automatically with name.'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'),
                                     help_text=_('Leave blank to fill automatically with words taken from name.'))
    date = models.DateTimeField(help_text=_('Date to be shown in article.'), verbose_name=_('published'))
    start_date = models.DateTimeField(blank=True, null=True,
                                      help_text=_("""Date to make article visible on site.
                                                  Leave this blank to show the article immediately."""),
                                      verbose_name=_('start date'))
    deadline = models.DateTimeField(blank=True, null=True,
                                    help_text=_("""Show article until this date.
                                                Article will appear forever if this field blank."""),
                                    verbose_name=_('deadline'))
    title = models.CharField(max_length=256, blank=False, null=False, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('author'))
    img = models.ImageField(verbose_name=_('image'), upload_to='articles')
    tags = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'), verbose_name=_('tags'))
    abstract = models.TextField(verbose_name=_('abstract'), max_length=256,
                                help_text=_('Short description - 256 symbols max.'))
    content = RichTextField(verbose_name=_('content'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', '-date']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        return self.title[:50]

    def clean(self):
        if self.start_date and self.deadline and self.start_date >= self.deadline:
            raise ValidationError(_("Deadline must be more than start date"))

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.title
        if not self.meta_keywords:
            self.meta_keywords = ', '.join(self.title.split())
        super(Article, self).save(*args, **kwargs)


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
    img = models.ImageField(blank=False, upload_to='banners', verbose_name=_('image'),
                            help_text=_('Upload image 1200x675 px.'))
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

    class Meta:
        ordering = ['-activity', 'order']
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return "#{0} {1}".format(self.id, self.name)


class CallbackInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('user'))
    """ Automatically uploaded for registered users. """
    name = models.CharField(max_length=32, blank=False, verbose_name=_('name'))
    """ Automatically uploaded for registered users. """
    phone = models.CharField(max_length=20, blank=False, verbose_name=_('phone'),
                             help_text=_('Enter the phone in the format +7(XXX)XXX-XX-XX.'))
    comment = models.TextField(blank=False, verbose_name=_('comment'))

    class Meta:
        ordering = ['-date']
        verbose_name = _('Callback info')
        verbose_name_plural = _('Callback info')

    def __str__(self):
        return _("Callback") + " #{0}".format(self.id)


class Menu(models.Model):
    HEADER, SUBHEADER, FOOTER, LEFTBAR = 'header', 'subheader', 'footer', 'leftbar'
    MENU_POSITIONS = [
        (HEADER, _('Header')),
        (SUBHEADER, _('Subheader')),
        (FOOTER, _('Footer')),
        (LEFTBAR, _('Leftbar')),
    ]

    name = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('name'))
    position = models.CharField(max_length=10, choices=MENU_POSITIONS, verbose_name=_('position'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'name']
        unique_together = ('name', 'position')
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')

    def __str__(self):
        return self.name

    def clean(self):
        if self.activity:
            active_menus = Menu.objects.filter(activity=True, position=self.position).exclude(name=self.name)
            if active_menus.exists():
                raise ValidationError(_("""Active menu for selected position is already exists.
                                        Please, deactivate it first."""))


# TODO: Remove slug and add actual relation to object or leave free link.
class MenuItem(models.Model):
    ROOT, CATEGORY, PRODUCT_LIST, PAGE, ARTICLE, NEWS, SPECIAL, EXTERNAL = \
        'root', 'category', 'products', 'page', 'article', 'news', 'special', 'external'
    RELATED_OBJ_TYPES = [
        (ROOT, _('Root object')),
        (CATEGORY, _('Category')),
        (PRODUCT_LIST, _('Product list')),
        (PAGE, _('Info page')),
        (ARTICLE, _('Article')),
        (NEWS, _('News')),
        (SPECIAL, _('Special')),
        (EXTERNAL, _('External link')),
    ]

    name = models.CharField(max_length=64, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(blank=True, verbose_name=_('slug'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name=_('parent'))
    icon = models.FileField(blank=True, upload_to='menu/items/icons', verbose_name=_('icon'),
                            help_text=_('Pay attention! Visible ONLY in HEADER SUBMENU! Preferred format - SVG.'))
    order = models.PositiveIntegerField(blank=False, default=1, verbose_name=_('order'))
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=False, related_name='items', verbose_name=_('menu'))
    related_type = models.CharField(max_length=10, choices=RELATED_OBJ_TYPES, default=CATEGORY,
                                    verbose_name=_('related type'),
                                    help_text=_("""
        Root object - /{object}
        Category - /categories/{object}
        Product list - /categories/{object}/products
        Info page - /info/{object}
        Article - /articles/{object}
        News - /news/{object}
        Special - /specials/{object}
        External link - {link}
                                    """))
    """ Use this field to link an outer site. """
    link = models.URLField(blank=True, verbose_name=_('External link'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['menu', 'order', 'name']
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')

    def __str__(self):
        return self.name


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'),
                                  help_text=_('Leave blank to fill automatically with name.'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'),
                                        help_text=_('Leave blank to fill automatically with name.'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'),
                                     help_text=_('Leave blank to fill automatically with words taken from name.'))
    date = models.DateTimeField(help_text=_('Date to be shown in news.'), verbose_name=_('date'))
    start_date = models.DateTimeField(blank=True, null=True,
                                      help_text=_("""Date to make news visible on site.
                                                  Leave this blank to show the news item immediately."""),
                                      verbose_name=_('start date'))
    deadline = models.DateTimeField(blank=True, null=True,
                                    help_text=_("""Show news item until this date.
                                                News item will appear forever if this field blank."""),
                                    verbose_name=_('deadline'))
    title = models.CharField(max_length=256, blank=False, null=False, verbose_name=_('title'))
    slug = models.SlugField(verbose_name=_('slug'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('author'))
    img = models.ImageField(verbose_name=_('image'), upload_to='news')
    tags = models.ManyToManyField(Tag, help_text=_('At least 1 tag is required.'), verbose_name=_('tags'))
    abstract = models.TextField(verbose_name=_('abstract'), max_length=256,
                                help_text=_('Short description - 256 symbols max.'))
    content = RichTextField(verbose_name=_('content'))
    activity = models.BooleanField(default=False, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', '-date']
        verbose_name = _('News item')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.title[:50]

    def clean(self):
        if self.start_date and self.deadline and self.start_date >= self.deadline:
            raise ValidationError(_("Deadline must be more than start date"))

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description:
            self.meta_description = self.title
        if not self.meta_keywords:
            self.meta_keywords = ', '.join(self.title.split())
        super(News, self).save(*args, **kwargs)


class Page(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('modified'))
    meta_title = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('meta title'),
                                  help_text=_('Leave blank to fill automatically with name.'))
    meta_description = models.CharField(max_length=1024, blank=True, null=True, verbose_name=_('meta description'),
                                        help_text=_('Leave blank to fill automatically with name.'))
    meta_keywords = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('meta keywords'),
                                     help_text=_('Leave blank to fill automatically with words taken from name.'))
    name = models.CharField(max_length=32, blank=False, null=False, verbose_name=_('name'))
    slug = models.SlugField(verbose_name=_('slug'))
    content = RichTextUploadingField(verbose_name=_('content'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        ordering = ['-activity', 'name']
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = self.name
        if not self.meta_description:
            self.meta_description = self.name
        if not self.meta_keywords:
            self.meta_keywords = ', '.join(self.name.split())
        super(Page, self).save(*args, **kwargs)


class SiteSettings(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, null=False, related_name='additional_info')
    description = RichTextUploadingField(blank=True, verbose_name=_('description'))
    activity = models.BooleanField(default=True, verbose_name=_('activity'))

    class Meta:
        unique_together = ('site', 'description')
        verbose_name = _('Site settings')
        verbose_name_plural = _('Site settings')

    def __str__(self):
        return 'Дополнительная информация по сайту #{0}'.format(self.id)

    def save(self, *args, **kwargs):
        if self.activity:
            current_settings = SiteSettings.objects.filter(activity=True).first()
            if current_settings:
                current_settings.activity = False
                current_settings.save()
        super(SiteSettings, self).save(*args, **kwargs)


class SubscriberInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('user'))
    """ Automatically uploaded for registered users. """
    email = models.EmailField(blank=False, unique=True)

    class Meta:
        ordering = ['-date']
        verbose_name = _('Subscriber info')
        verbose_name_plural = _('Subscriber info')

    def __str__(self):
        return _("Subscription") + " #{0}".format(self.id)
