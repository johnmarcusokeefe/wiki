from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("results/", views.results, name="results"),
    path("edit/", views.edit, name="edit"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("create/", views.create, name="create"),
    path("random/", views.random_page, name="random_page")
]
