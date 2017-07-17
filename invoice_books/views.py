from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import TemplateView


class IndexView(TemplateView):

    template_name = 'project/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'project/dashboard.html'


class TestView(TemplateView):

    template_name = "invoice_pdf/default.html"

    def get_context_data(self, **kwargs):
        return {
            'company': {
                'logo_1': 'images/logo_1.png',
                'logo_2': 'images/logo_2.jpg',
                'name': 'My Company',
                'address_line_1': 'Add line 1',
                'address_line_2': 'Add line 2',
                'phone': '09188182',
                'GSTIN': 'My 09AAZFMHYU89',
            }
        }
