from functools import wraps
from django.shortcuts import redirect

def user_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # If the user is not logged in, store the previous URL in the session and redirect to the login page.
            request.session['next_url'] = request.get_full_path()
            return redirect('attendances:user_login')
        else:
            # If the login is successful and next_url is present in the session, delete it.
            if 'next_url' in request.session:
                del request.session['next_url']
        return view_func(request, *args, **kwargs)
    return _wrapped_view