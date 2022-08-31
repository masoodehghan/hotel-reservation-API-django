from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHostOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.host_id == request.user.id)


class IsGalleryHost(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return bool(obj.content_object.hotel.host_id == request.user.id)

        except AttributeError:
            return bool(obj.content_object.host_id == request.user.id)


class IsRoomHostOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(obj.hotel.host_id == request.user.id)
