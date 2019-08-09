from axes.helpers import get_client_ip_address
from axes.utils import reset
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import AxesCaptchaForm


class RegistrationView(CreateView):
    template_name = 'account/register.html'
    form_class = UserCreationForm
    success_url = '/'


class CaptchaView(FormView):
    template_name = 'account/captcha.html'
    form_class = AxesCaptchaForm
    success_url = '/'

    def form_valid(self, form):
        ip = get_client_ip_address(self.request)
        reset(ip=ip)
        return HttpResponseRedirect(reverse_lazy('login'))


register_view = RegistrationView.as_view()
captcha_view = CaptchaView.as_view()
