from rest_framework import permissions
from rest_framework.permissions import BasePermission

from posts.models import Post, Comment, Reaction


class IsOwnerOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Post):
            return request.user == obj.author

        if isinstance(obj, Reaction):
            return request.user == obj.author

        if isinstance(obj, Comment):
            return request.user == obj.commenter

        return False
