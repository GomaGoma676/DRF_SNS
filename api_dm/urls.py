from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_dm import views

app_name = 'dm'

router = DefaultRouter()
router.register('message', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('inbox/', views.InboxListView.as_view(), name='inbox')
]