from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:filename>", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("edit/", views.edit, name="edit"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("create/", views.create, name="create"),
    path("create/<str:title>", views.create, name="create"),
    path("random/", views.random_page, name="random_page")
]
