from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, BankAccountType, UserBankAccount, UserAddress, Images
from .constants import GENDER_CHOICE
from phonenumber_field.formfields import PhoneNumberField

class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


# class UserInformationForm(forms.ModelForm):
#     class Meta:
#         model = UserBankAccount
#         exclude = ('balance','interest_start_date','initial_deposit_date',)

#     @transaction.atomic
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             self.account_no=(user.id + settings.ACCOUNT_NUMBER_START_FROM )           
#         return user

class UserRegistrationForm(UserCreationForm):
    # account_type = forms.ModelChoiceField(
    #     queryset=BankAccountType.objects.all()
    # )
    # gender = forms.ChoiceField(choices=GENDER_CHOICE)
    # birth_date = forms.DateField()
    # phone_no = PhoneNumberField()
    # fingerprint_images = forms.ImageField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'password1': 'Pin',
            'password2': 'Pin Confirmation'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                ),
            })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        # if commit:
        #     user.save()
        #     account_type = self.cleaned_data.get('account_type')
        #     gender = self.cleaned_data.get('gender')
        #     birth_date = self.cleaned_data.get('birth_date')
        #     phone_no = self.cleaned_data.get('phone_no')
        #     fingerprint_images = self.cleaned_data.get('fingerprint_images')
        #     # print(fingerprint_images)
        #     UserBankAccount.objects.create(
        #         user=user,
        #         gender=gender,
        #         birth_date=birth_date,
        #         account_type=account_type,
        #         phone_no = phone_no,
        #         fingerprint_images = fingerprint_images,
        #         account_no=(
        #             user.id +
        #             settings.ACCOUNT_NUMBER_START_FROM
        #         )
        #     )
        # print(user)
        return user

class  UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserBankAccount
        exclude = ('balance','interest_start_date','initial_deposit_date',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                ),
            })
    
    # @transaction.atomic
    # def save(self, user, commit=True):
    #     information = super().save(commit=False)
    #     information.user = user
    #     information.account_no=(
    #         user.id +
    #         settings.ACCOUNT_NUMBER_START_FROM
    #     )
    #     information.save()
    #     return information

class UserFingerprintForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = '__all__'

class OTPCheckForm(forms.Form):
    otp = forms.IntegerField()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=4, widget=forms.PasswordInput())

class passwordForm(forms.Form):
    password1 = forms.CharField(max_length=4, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=4, widget=forms.PasswordInput())