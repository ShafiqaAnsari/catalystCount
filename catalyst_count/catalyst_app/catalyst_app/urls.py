from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'myapp'
urlpatterns = [
    path('home/', views.homePage, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    # path('logout/', views.logout_view, name = 'logout'),
    path('query-builder/', views.query_builder, name = 'query-builder'),
    path('users/', views.users_detail, name = 'users'),

    
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
