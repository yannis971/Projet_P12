from rest_framework.exceptions import PermissionDenied

def route_permissions(permission):
    """ django-rest-framework permission decorator for custom methods """
    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            if self.request.user.has_perm(permission):
                return drf_custom_method(self, *args, **kwargs)
            else:
                raise PermissionDenied()
        return _decorator
    return decorator
