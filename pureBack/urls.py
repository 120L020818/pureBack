"""pureBack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from . import controller_login
from . import controller_register
from . import controller_self
from . import controller_request

urlpatterns = [
    # url(r'api/login', allpages.login_controller)
    url(r'api/login', controller_login.login_controller),
    url(r'api/ecode', controller_register.register_email),
    url(r'api/register', controller_register.register_format),
    url(r'api/self', controller_self.self_controller),
    url(r'api/request', controller_request.request_controller),
]
