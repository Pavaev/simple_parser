from functools import wraps

from django.http import Http404


def logout_or_404(view_func):
    """
    Decorator for view functions, that can be accessed only for
    unauthorized users
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        return view_func(request, *args, **kwargs)
    return _wrapped_view
