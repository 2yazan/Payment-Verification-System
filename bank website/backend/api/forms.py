from django import forms
from django.contrib.auth.models import User




## unfinished from gemini yesterday



# class RegistrationForm(forms.ModelForm):
#     username = forms.CharField(label='Username', required=True)
#     email = forms.EmailField(label='Email', required=True)
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def clean_password2(self):
#         # Check if passwords match
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return password2

#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user


# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username', required=True)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)


