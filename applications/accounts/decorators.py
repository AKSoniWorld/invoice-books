from django.contrib.auth.decorators import user_passes_test


def anonymous_required(function=None, redirect_url=None):
    """  Decorator for views that checks that the user is anonymous """
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_url,
        redirect_field_name=''
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
