from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Customer, Admin,User,Task

class CustomerSignUpForm(UserCreationForm):
    username=forms.CharField(required=False)
    email=forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data['email'] 
        user.save()
        student = Customer.objects.create(user=user)
        # student.save()
        return user
    
class ManagerSignUpForm(UserCreationForm):
    username=forms.CharField(required=True)
    email=forms.EmailField(required=True)
  
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        
        user.is_admin = True
        user.email = self.cleaned_data['email'] 
        user.save()
        manager = Admin.objects.create(user=user)
        manager.save()

        return manager
  

class LoginForm(forms.ModelForm):
    email = forms.CharField(max_length=254, error_messages={'required': 'email is required'})
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': 'Password is required'})

    class Meta:
        model = User
        fields = ("email", "password")



class TaskForm(forms.ModelForm):
    title = forms.CharField(max_length=254, error_messages={'required': 'title is required'})
    description = forms.CharField(max_length=254, error_messages={'required': 'description is required'})

    class Meta:
        model = Task
        fields = ("title", "description")

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', max_length=150, widget=forms.TextInput())
    image = forms.ImageField(label='Image')  # Change to ImageField

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image")


