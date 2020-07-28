from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page"),
    path("search", views.search, name="search"),
    path("add_page", views.add_page, name="add_page"),


]
