from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect, redirect, render, resolve_url
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from accounts.models import *
from .forms import UserRegistrationForm, UserAddressForm, OTPCheckForm, LoginForm, passwordForm,UserInformationForm
from banking_system import settings
from accounts.forms import UserFingerprintForm
import os
from checker.app import *
import math, random
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth import signals
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from axes.decorators import axes_dispatch
from accounts import forms
from django.views.generic.edit import FormView
from axes.models import AccessAttempt, AccessLog
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers  import make_password
from django.http import JsonResponse
from django.core import serializers

User = get_user_model()

# class UserRegistrationView(TemplateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'accounts/user_registration.html'

#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return HttpResponseRedirect(
#                 reverse_lazy('transactions:transaction_report')
#             )
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         registration_form = UserRegistrationForm(self.request.POST)
#         address_form = UserAddressForm(self.request.POST)
#         try:
#             if registration_form.is_valid() and address_form.is_valid():
#                 user = registration_form.save()
#                 address = address_form.save(commit=False)
#                 address.user = user
#                 address.save()
#                 login(self.request, user)
#                 messages.success(
#                     self.request,
#                     (
#                         f'Thank You For Creating A Bank Account. '
#                         f'Your Account Number is {user.account.account_no}. '
#                     )
#                 )
#                 return HttpResponseRedirect(
#                     reverse_lazy('transactions:deposit_money')
#                 )
#         except:
#             messages.error(request,"Something is wrong")
#             return self.render_to_response(
#                 self.get_context_data(
#                     registration_form=registration_form,
#                     address_form=address_form
#                 )
#             )

#     def get_context_data(self, **kwargs):
#         if 'registration_form' not in kwargs:
#             kwargs['registration_form'] = UserRegistrationForm()
#         if 'address_form' not in kwargs:
#             kwargs['address_form'] = UserAddressForm()

#         return super().get_context_data(**kwargs)



class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)
        formss = UserInformationForm(request.POST,request.FILES,)
        # information_form = UserInformationForm(self.request.POST,self.request.FILES)
        if registration_form.is_valid() and formss.is_valid() and address_form.is_valid():
            # if registration_form.is_valid() and address_form.is_valid() and information_form.is_valid():
            print("if")
            user = registration_form.save(commit=False)
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            form_data = forms.save(commit=False)
            form_data.user = user
            form_data.fingerprint_images = request.FILES['image']
            form_data.account_no=(
                user.id +
                settings.ACCOUNT_NUMBER_START_FROM
            )
            form_data.save()
            new_user = authenticate(username=registration_form.cleaned_data['email'], password=registration_form.cleaned_data['password1'])
            login(self.request, new_user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )
        else:
            registration_form = UserRegistrationForm()
            address_form = UserAddressForm()
            formss = UserInformationForm()
            return HttpResponse("Form is not valid")

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                forms = forms,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'formss' not in kwargs:
            kwargs['formss'] = UserInformationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()
        return super().get_context_data(**kwargs)


def UserRegistrationView1(request):
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        address_form = UserAddressForm(request.POST)
        forms = UserInformationForm(request.POST,request.FILES,)
        # information_form = UserInformationForm(request.POST,request.FILES)
        if registration_form.is_valid() and address_form.is_valid() and forms.is_valid():
            user = registration_form.save(commit=False)
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            form_data = forms.save(commit=False)
            form_data.user = user
            form_data.account_no=(
                user.id +
                settings.ACCOUNT_NUMBER_START_FROM
            )
            form_data.fingerprint_images = request.FILES['image']
            form_data.save()
            # user = authenticate(email=user.email, password= user.password)
            # login(request,user)
            # information = information_form.save(False)
            # information.user = user
            # information.fingerprint_images =  request.FILES['image']
            # information.account_no=(
            #     user.id +
            #     settings.ACCOUNT_NUMBER_START_FROM
            # )
            # information.save()
            # login(request, user)
            messages.success(
                request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return redirect('transactions:deposit_money')
        # else:
        #     return redirect('accounts:register')

    else:
        registration_form = UserRegistrationForm()
        address_form = UserAddressForm()
        forms = UserInformationForm()
    context_dict = {'registration_form': registration_form,'address_form':address_form,'forms':forms }

    return render (request,'accounts/user_registration.html',context_dict)

class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = True
    # def get_success_url(self):
    #     url = self.get_redirect_url()
    #     return url or resolve_url(settings.LOGIN_REDIRECT_URL)


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

def InformationRegister(request):
    if request.method == 'POST':
        forms = UserInformationForm(request.POST,request.FILES,)
        if forms.is_valid():
            form_data = forms.save(commit=False)
            user= User.objects.first()
            form_data.user = User.objects.get(email='ti@tee.com')
            form_data.account_no=(
                user.id +
                settings.ACCOUNT_NUMBER_START_FROM
            )
            form_data.save()
            user = authenticate(email=user.email, password = user.password)
            login(request, user)
            messages.success(
                request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return redirect('transactions:deposit_money')
    else:
        forms = UserInformationForm()
    context_dict = {'forms': forms, }

    return render (request,'accounts/checkfingerprint.html',context_dict)

def checkFingerprintupload(request):
    if request.method == 'POST':
        forms = UserFingerprintForm(request.POST,request.FILES,)
        if forms.is_valid():
            form_data = forms.save(commit=False)
            form_data.image = request.FILES['image']
            form_data.save()
            myImage = request.FILES['image']
            attemptUser = AccessAttempt.objects.last()
            try:
                user = UserBankAccount.objects.get(email=attemptUser.username)
                print(str(user.fingerprint_images), str(myImage))
                a = checker(str(user.fingerprint_images), "checkimages/"+str(myImage))
                if a == 1:
                    return redirect('accounts:password_change')
                else:
                    messages.error(request, "Authentication Failed.")
            except UserBankAccount.DoesNotExist as e:
                messages.error(request,"User Bank Account Doesnot Exist.")
    else:
        forms = UserFingerprintForm()
    context_dict = {'forms': forms, }

    return render (request,'accounts/checkfingerprint.html',context_dict)

    
        #     ser_instance = serializers.serialize('json', [ forms, ])
        #     if a == 1:
        #         return JsonResponse({"forms": ser_instance}, status=200)
        #         # return redirect('accounts:OTP')
        #     else:
        #         messages.error(request, "invalid fingerprint.")    
        # else:
        #     forms = UserFingerprintForm()
        #     return JsonResponse({"forms": forms}, status=400)
# https://www.pluralsight.com/guides/work-with-ajax-django
    # some error occured
    # return JsonResponse({"error": ""}, status=400)
  

def generateOTP() : 
    digits = "0123456789"
    OTP = "" 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP

otp = generateOTP()
def OTPCheck(request):
    if request.method == 'POST':
        forms = OTPCheckForm(request.POST,request.FILES,)
        if forms.is_valid():
            gotOtp= forms.cleaned_data.get("otp")
            print(otp,gotOtp)
            if int(otp) == int(gotOtp):
                result = "matches"
                return redirect('accounts:password_change')
            else:
                result = "doesn't match"
                messages.error(request, f'Invalid OTP!')
                return redirect('accounts:OTP')

    else:
        forms = OTPCheckForm()
        result = 0
    attemptUser = AccessAttempt.objects.first()
    context = {'o':result,'forms': forms,'otp': otp,'uSir':attemptUser.username}
    return render (request,'accounts/otp.html',context)

# @csrf_exempt
def passwordChange(request):
    if request.method == 'POST':
        forms = passwordForm (request.POST)
        # forms = UserFingerprintForm(request.POST,request.FILES,)
        if forms.is_valid():
            password1 = forms.cleaned_data['password1']
            password2 = forms.cleaned_data['password2']
            attemptUser = AccessAttempt.objects.last()
            if password1 == password2:
                try:
                    theuser = User.objects.filter(email = attemptUser.username)
                    for object in theuser:
                        object.password = make_password(password1)
                        object.save()
                    attemptUser.delete()
                    messages.success(request, f'Password changed successfully!')
                    return redirect('accounts:user_login')
                except User.DoesNotExist as e:
                    messages.error(request, f'User Doesnot Exist')
            else:
                messages.error(request,"Passwords Donot Match.")
            
    else:
        forms = passwordForm()
    context = {'forms': forms, }
    return render (request,'accounts/password_change_form.html',context)


# def reset_confirm(request, key):
#     """
#     Complete the password reset procedure.
#     """
#     attemptUser = AccessAttempt.objects.first()
#     # key = get_object_or_404(ConfirmationKey, key=key)
#     if request.method == 'POST':
#         form = SetPasswordForm(user=theuser.id, data=request.POST)
#         if form.is_valid():
#             form.save()
#             # key.delete()
#             messages.info(request, "Thank you! Your password has been reset. Please log in below.")
#             return redirect('accounts:user_login')
#     else:
#         form = SetPasswordForm(user=theuser.id)
#     return render(request, 'accounts/password_change_form.html', {
#         'title': 'Set Password',
#         'form': form,
#         'description': "Please enter a new password for your account.",
#         'action': 'Continue',
#     })

class LoginView(FormView):
    """login view"""

    form_class = forms.LoginForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_login.html'

    def form_valid(self, form): 
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            # messages.add_message(self.request, messages.INFO, 'Wrong credentials\
            #                     please try again')
            return HttpResponseRedirect(reverse_lazy('accounts:login'))