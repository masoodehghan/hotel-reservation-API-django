from rest_framework.permissions import BasePermission


class IsHost(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(obj.content_object.host_id == request.user.id)
