from django.urls import path

from . import views

urlpatterns = [
    path("health", views.health),
    path("auth/register", views.RegisterView.as_view()),
    path("auth/login", views.LoginView.as_view()),
    path("notes", views.NoteListView.as_view()),
    path("notes/<int:note_id>", views.NoteDetailView.as_view()),
]
