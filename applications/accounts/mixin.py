from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy


class LoginRequiredMixin(object):
    """ makes sure only logged in users can access the view extending this MIXIN """

    @method_decorator(login_required(login_url=reverse_lazy('user:login')))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AdminRequiredMixin(object):
    """ makes sure only logged in admin-type users can access the view extending this MIXIN """

    @method_decorator(login_required(login_url=reverse_lazy('user:login')))
    @method_decorator(user_passes_test(lambda u: u.is_admin, login_url=reverse_lazy('user:login')))
    def dispatch(self, *args, **kwargs):
        return super(AdminRequiredMixin, self).dispatch(*args, **kwargs)


class NonAdminRequiredMixin(object):
    """ makes sure only logged in non-admin-type users can access the view extending this MIXIN """

    @method_decorator(login_required(login_url=reverse_lazy('user:login')))
    @method_decorator(user_passes_test(lambda u: not u.is_admin, login_url=reverse_lazy('user:login')))
    def dispatch(self, *args, **kwargs):
        return super(NonAdminRequiredMixin, self).dispatch(*args, **kwargs)
