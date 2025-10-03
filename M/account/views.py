from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from .models import User


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(phone_number=cd['phone_number'], email=cd['email'], full_name=cd['full_name'], password=cd['password2'])
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


