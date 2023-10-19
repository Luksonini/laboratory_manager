
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def verified_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_verified:
            return redirect('calendarapp:not_verified')  # przekierowanie do widoku 'not_verified'
        return view_func(request, *args, **kwargs)
    return _wrapped_view