from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.editor, name='editor'),
    path('modern/', login_required(TemplateView.as_view(template_name='editor/modern_editor.html')), name='modern_editor'),
    path('studio/', login_required(TemplateView.as_view(template_name='editor/studio_editor.html')), name='studio_editor'),
    path('snippet/<int:pk>/', views.snippet_detail, name='snippet_detail'),
    path('snippet/create/', views.create_snippet, name='create_snippet'),
    path('snippet/<int:pk>/delete/', views.delete_snippet, name='delete_snippet'),
    path('history/', views.execution_history, name='execution_history'),
    path('profile/', views.profile, name='profile'),
]
