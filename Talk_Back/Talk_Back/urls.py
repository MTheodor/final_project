"""
URL configuration for Talk_Back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from Application.views import home, account, settings, subscriptions, liked, post, create_post, user_login, signup, user_logout

urlpatterns = [
    path('', home),
    path('account/', account),
    path('settings/', settings),
    path('subscriptions/', subscriptions),
    path('liked/', liked),
    path('post/<int:post_id>', post),
    path('create/', create_post),
    path('admin/', admin.site.urls),
    path('login/', user_login),
    path('signup/', signup),
    path('logout/', user_logout),
]
