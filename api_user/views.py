from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from api_user import serializers
from core.models import Profile, User
from core import ownpermissions
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,ownpermissions.ProfilePermission,)

    def get_queryset(self):
        try:
            is_friend = Profile.objects.get(userpro=self.request.user)
        except Profile.DoesNotExist:
            is_friend = None
            return

        friend_filter = Q()
        for friend in is_friend.friends.all():
            friend_filter = friend_filter | Q(userpro=friend)

        return self.queryset.filter(friend_filter)

    def perform_create(self,serializer):
        try:
            serializer.save(userpro=self.request.user)
        except IntegrityError:
            raise ValidationError("User can have only one own profile")
