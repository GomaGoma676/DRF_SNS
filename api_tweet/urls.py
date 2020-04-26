from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_tweet import views

app_name = 'tweet'

router = DefaultRouter()
router.register('new', views.TweetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]