from libs import utils as libs_utils


class CompanyRequiredMixin(object):

    user_company = None

    def dispatch(self, request, *args, **kwargs):
        self.user_company = libs_utils.get_current_company(request.user)
        return super(CompanyRequiredMixin, self).dispatch(request, *args, **kwargs)
