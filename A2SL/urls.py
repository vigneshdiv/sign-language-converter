from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('animation/',views.animation_view,name='animation'),
    path('reflex/',views.reflex_view,name='reflex'),
    path('',views.home_view,name='home'),
]