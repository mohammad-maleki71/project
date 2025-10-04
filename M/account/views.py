from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
from .models import User, OtpCode
import random
from utils import send_otp_code
from django.contrib import messages


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password2': form.cleaned_data['password2'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('account:verify_code')
        return render(request, self.template_name, {'form': form})


class VerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'account/verify_code.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['full_name'], user_session['password2'])
                code_instance.delete()
                messages.success(request, 'you registered successfully', 'success')
            else:
                messages.error(request, 'this code is wrong', 'error')
                return redirect('account:verify_code')
        return redirect('home:home')



