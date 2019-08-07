from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView


class RegistrationView(CreateView):
    template_name = 'auth/register.html'
    form_class = UserCreationForm
    success_url = '/'


register_view = RegistrationView.as_view()
