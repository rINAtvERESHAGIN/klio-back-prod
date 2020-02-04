from django.db import models

from ckeditor.fields import RichTextField

from products.models import Category
from tags.models import Tag
from users.models import User


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(help_text='Date to be shown in article')
    start_date = models.DateTimeField(help_text='Date to make article visible on site')
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    img = models.ImageField()
    tag = models.ManyToManyField(Tag)
    content = RichTextField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:50]

    class Meta:
        ordering = ['activity', '-date']


class Banner(models.Model):
    WHITE = 'FFFFFF'
    BLACK = '000000'
    BTN_COLORS = [
        (WHITE, 'White'),
        (BLACK, 'Black'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    img = models.ImageField(blank=False)
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
        return "Banner #{0} (created: {1})".format(self.id, self.created)

    class Meta:
        ordering = ['activity']


class CallbackInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=32, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=False,
                             help_text='Enter the phone in the format +7(XXX)XXX-XX-XX')
    comment = models.TextField(blank=False)

    def __str__(self):
        return "Callback #{0} - {1} ({2})".format(self.id, self.date, self.name)


class Menu(models.Model):
    MENU_POSITIONS = [
        (0, 'Header'),
        (1, 'Footer'),
        (2, 'Leftbar'),
    ]

    name = models.CharField(max_length=32, blank=False, null=False)
    position = models.CharField(max_length=2, choices=MENU_POSITIONS)
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['activity']


class MenuItem(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(blank=False, default=1)
    page = models.ForeignKey('Page', on_delete=models.SET_NULL, null=True)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    link = models.URLField()
    activity = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# class MetaMixin(models.AbstractModel):
#     meta_title = models.CharField()
#     meta_desc = models.CharField()
#     meta_keywords = models.CharField()


class News(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(help_text='Date to be shown in article')
    start_date = models.DateTimeField(help_text='Date to make article visible on site')
    title = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    img = models.ImageField()
    tag = models.ManyToManyField(Tag)
    content = RichTextField()
    activity = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:50]

    class Meta:
        ordering = ['activity', '-date']


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
        ordering = ['activity', 'name']


class SubscriberInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Subscription #{0} ({1})".format(self.id, self.email)
