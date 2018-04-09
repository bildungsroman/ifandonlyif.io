from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it
    """

    def has_object_permission(self, request, view, obj):
        print("I am doing a thing!")
        if obj.user != request.user:
            print("You cannot do this thing!")
            return False
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        elif request.method in permissions.SAFE_METHODS:
            print("Returning True!")
            return True
        else:
            # Write permissions are only allowed to the owner of the ifflist.
            print("This should not be happening")
            return obj.user == request.user
