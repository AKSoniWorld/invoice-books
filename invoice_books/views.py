from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.staticfiles.templatetags.staticfiles import static


class TestView(TemplateView):

    template_name = "invoice/default.html"

    def get_context_data(self, **kwargs):
        return {
            'logo_1': static('images/logo_1.png'),
            'logo_2': static('images/logo_2.png'),
            'company': {
                'name': 'My Company',
                'address_line_1': 'Add line 1',
                'address_line_2': 'Add line 2',
                'GSTIN': 'My 09AAZFMHYU89',
            }
        }
