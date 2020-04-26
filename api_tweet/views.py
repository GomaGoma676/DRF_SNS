from rest_framework import authentication, permissions
from api_tweet import serializers
from core.models import Tweet
from rest_framework import viewsets
from core import ownpermissions

class TweetViewSet(viewsets.ModelViewSet):

    queryset = Tweet.objects.all()
    serializer_class = serializers.TweetSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, ownpermissions.TweetPermission,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)