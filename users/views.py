from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin


from .forms import CustomUserForm


class SignUpView(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('login')
    template_name = 'signup.djhtml'
    success_message = 'Account was successfully created!'

