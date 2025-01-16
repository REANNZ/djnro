from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic.base import TemplateView
# Uncomment the next two lines to enable the django admin interface:
from django.contrib import admin
admin.autodiscover()
import social_django.urls
import edumanage
import django
import accounts, accounts.views

urlpatterns = [
    #url(r'^accounts/', include(social_django.urls, namespace='social')),
    path("accounts/", include(social_django.urls, namespace='social')),
    # This is a new requirement for django-registration since django-registration:3.0
    path('jamie/', include('django.contrib.auth.urls')),
    #url(r'^setlang/?$', edumanage.views.set_language, name='set_language'),
    path("setlang/", edumanage.views.set_language, name='set_language'),
    #url(r'^admin/', include(admin.site.urls)),
    path("admin/", admin.site.urls),
    #url(r'^managelogin/(?P<backend>[^/]+)/$', edumanage.views.manage_login, name='manage_login'),
    re_path(r'^managelogin/(?P<backend>[^/]+)/$', edumanage.views.manage_login, name='manage_login'),
    #url(r'^login/?', edumanage.views.user_login, name="login"),
    path("login/", edumanage.views.user_login, name="login"),
    #url(r'^altlogin/?', django.contrib.auth.views.login, {'template_name': 'overview/login.html'}, name="altlogin"),
    path("altlogin/", django.contrib.auth.views.login, {'template_name': 'overview/login.html'}, name="altlogin"),
    #url(r'^logout/?', edumanage.views.user_logout, {'next_page': '/'}, name="logout"),
    path("logout/", edumanage.views.user_logout, {'next_page': '/'}, name="logout"),
    #url(r'^registration/accounts/activate/(?P<activation_key>\w+)/$', accounts.views.activate, name='activate_account'),
    re_path(r'^registration/accounts/activate/(?P<activation_key>\w+)/$', accounts.views.activate, name='activate_account'),
    #url(
    #    r'^registration/activate/complete/$',
    #    TemplateView.as_view(template_name='registration/activation_complete.html'),
    #    name='registration_activation_complete'
    #),
    path(
        "registration/activate/complete/",
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'
    ),
    #url(r'^tinymce/', include('tinymce.urls')),
    path("tinymce/", include('tinymce.urls')),
    #url(r'^', include('edumanage.urls')),
    re_path(r'^', include('edumanage.urls')),
]
