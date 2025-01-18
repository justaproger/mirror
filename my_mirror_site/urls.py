# myproject/urls.py

from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from myapp.views import MyProxyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^(?P<path>.*)$', MyProxyView.as_view(), name='proxy'),
]
