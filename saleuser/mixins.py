from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect 


class AdminAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an admin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)