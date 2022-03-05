"""newblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blog.views import main_page, show_post, register, endreg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', main_page, name='home'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    # path('register/', RegisterUser.as_view(), name='register')
    # path('personalArea/', personalArea, name='personalArea'),
    path('register/', register, name="register"),
    path('activation_code_form/', endreg, name="endreg"),
]


admin.site.site_header = 'Администрирование Блога'
admin.site.index_title = 'Редактирование Блога'
admin.site.site_title = 'Администрирование Блога'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
