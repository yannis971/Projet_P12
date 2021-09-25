"""
Module for customized permissions
"""
from rest_framework import permissions


class ContractPermission(permissions.BasePermission):
    """
    Custom permission to manage an instance of Contract.
    """

    _perms = dict()
    _perms["create"] = "crm_api.add_contract"
    _perms["update"] = "crm_api.change_contract"
    _perms["partial_update"] = "crm_api.change_contract"
    _perms["retrieve"] = "crm_api.view_contract"
    _perms["list"] = "crm_api.view_contract"
    _perms["destroy"] = "crm_api.delete_contract"

    def change_contract_status_only(self, request, obj):
        """
        Returns True if user has change_contract_status only
        """
        amount = -1.00
        try:
            amount = float(request.data["amount"])
        except ValueError:
            pass
        except KeyError:
            pass
        return bool(
            amount == obj.amount
            and request.data["payment_due"]
            == obj.payment_due.strftime("%Y-%m-%dT%H:%M:%SZ")
            and request.user.has_perm("crm_api.change_contract_status")
        )

    def has_object_permission(self, request, view, obj):
        """
        Returns true if user is authenticated
        and has permission to perform view.action
        """
        user_is_authenticated = bool(request.user
                                     and request.user.is_authenticated)
        if view.action == "update" or view.action == "partial_update":
            user_has_perm = bool(
                self.change_contract_status_only(request, obj)
                or request.user.has_perm(self._perms[view.action])
            )
        else:
            user_has_perm = request.user.has_perm(self._perms[view.action])
        return bool(user_is_authenticated and user_has_perm)
