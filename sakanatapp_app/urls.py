from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register_page', views.register_page),
    path('login_page', views.login_page),
    path('home', views.search_page),
    path('about', views.about_page),
    path('contact_page', views.contact_page),
    path('register', views.register_user),
    path('login', views.login_user),
    path('success', views.success_login),
    path('logout', views.logout_user),
    path('add_apartment' , views.add_apartment),
    path('apartment_form', views.apartment_form),
    path('search', views.search),
    path('<int:apartment_id>', views.Apartment_detail),
    path('success/<int:apartment_id>/delete' , views.delete), 
    path('edit_apartment/<int:apartment_id>', views.edit_page),
    path('edit_apartment', views.update_apartment),
    path('chalet_form', views.chalet_form),
    path('add_chalet', views.add_chalet),
    path('chalet/<int:chalet_id>', views.chalet_detail),







]