"""
Module for customized decorators
"""
from rest_framework.exceptions import PermissionDenied


def route_permissions(permission_required):
    """Decorator that performs a method if the user has the permission
    required to perform that method
    """

    def decorator(drf_custom_method):
        """
        the wrapper method
        """

        def _decorator(self, *args, **kwargs):
            """
            the inner method
            """
            if self.request.user.has_perm(permission_required):
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()

        return _decorator

    return decorator
