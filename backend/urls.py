"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,  include
from tickets import views

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),

    # method 1
    path('no_rest_no_model/', views.no_rest_no_model),

    # method 2
    path('no_rest_model/', views.no_rest_model),

    # method 3
    path('FBV/', views.FBV_list),
    path('FBV/<int:pk>/', views.FBV_pk),

    # method 4
    path('CBV/', views.CBV_List.as_view()),
    path('CBV/<int:pk>/', views.CBV_pk.as_view()),

    # # method 5
    path('mixins/', views.mixins_list.as_view()),
    path('mixins/<int:pk>/', views.mixins_pk.as_view()),

    # # method 6
    path('generics/', views.generic_list.as_view()),
    path('generics/<int:pk>/', views.generic_pk.as_view()),

    # method 7 you must set a router above
    path('viewsets/', include(router.urls)),

    # find
    path('findmovie/', views.find_movie),

    # new reservation
    path('newreservation/', views.new_reservation),

    # basic authentication method
    path('api-auth/', include('rest_framework.urls')),

    # token authentication method
    path('api-token-auth', obtain_auth_token),

    # post pk generics
    # path('post/generics/', views.Post_list.as_view()),
    path('post/generics/<int:pk>/', views.Post_pk.as_view()),
]
