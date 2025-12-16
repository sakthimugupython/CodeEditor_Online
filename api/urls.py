from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodeSnippetViewSet, ExecutionViewSet

router = DefaultRouter()
router.register(r'snippets', CodeSnippetViewSet, basename='snippet')
router.register(r'execution', ExecutionViewSet, basename='execution')

urlpatterns = [
    path('', include(router.urls)),
]
