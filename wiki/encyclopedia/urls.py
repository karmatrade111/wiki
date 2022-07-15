from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:TITLE>", views.title, name="TITLE"),
    path("/newPage", views.newPage, name="newPage"),
    path("/edit/<str:title>", views.edit, name="edit"),
    path("/success/<str:title>", views.success, name="success")
]
