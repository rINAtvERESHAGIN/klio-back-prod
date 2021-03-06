"""klio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from django.views.generic import TemplateView
from general.views import SearchListView


urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('grappelli/', include('grappelli.urls')),

    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/basket/', include('basket.urls')),
    path('api/v1/contacts/', include('contacts.urls')),
    path('api/v1/general/', include('general.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/sale/', include('sale.urls')),
    path('api/v1/tags/', include('tags.urls')),
    path('api/v1/users/', include('users.urls')),

    path('api/v1/search', SearchListView.as_view({'get': 'list'}), name='search_list'),
]

urlpatterns += [
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
