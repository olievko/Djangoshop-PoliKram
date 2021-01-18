"""djangoshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from home.views import selectlanguage, selectcurrency, savelangcur
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('selectlanguage', selectlanguage, name='selectlanguage'),
    path('selectcurrency', selectcurrency, name='selectcurrency'),
    path('savelangcur', savelangcur, name='savelangcur'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += i18n_patterns(
    path('entrance-admin/', admin.site.urls),
    path('', include('ecomapp.urls')),
    path('user/',   include('user.urls')),
    path('home/', include('home.urls')),
    path('city/', include('city.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('currencies/', include('currencies.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)