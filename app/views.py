from django.shortcuts import render,redirect
from .forms import CustomerSignUpForm,ManagerSignUpForm
# Create your views here.
from django.views.generic import FormView
from .models import User
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import LoginForm,TaskForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Task
from django.views.generic.edit import UpdateView

@method_decorator(login_required, name='dispatch')

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tasks = Task.objects.filter(user=request.user)
            return render(request, "app/home.html",{'task':tasks})
        else:
            return redirect('login')

    
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  
            task.user = request.user 
            task.save()  
            return redirect('home')  
    else:
        form = TaskForm()
    
    return render(request, 'app/addTask.html', {'form': form})



def TaskUpdateView(request,id):
   
    task = Task.objects.get(id=id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('home')  
    
    return render(request, 'app/editTask.html', {'form': form, 'task':task})
    
    

def deleteTask(request,id):
   
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('home')  
    

def ProfilView(request):
    user = User.objects.get(username=request.user.username)
    form = ProfileForm(request.POST or None, request.FILES, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'app/profile.html', {'form': form, 'user': user})


    


class ManagerRegisterView(FormView):
    form_class = ManagerSignUpForm
    model = User
    template_name = "app/manager_register.html"
    success_url = "login"
    def form_valid(self, form):
        instance = form.save()
        # messages.success(self.request, 'Your account has been created. Please log in.') 
        return super().form_valid(form)
    
class CustomerRegisterView(FormView):
    form_class = CustomerSignUpForm
    model = User
    template_name = "app/customer_register.html"
    success_url = "login"
    def form_valid(self, form):
        instance = form.save()
        return super().form_valid(form)



def LoginView(request):
    error_message = "" 
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate user
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Invalid username or password. Please try again."
        else:
            error_message = "Form validation failed. Please check your input."

    else:
        form = LoginForm
    return render(request,'app/login.html',{'form':form,'error_message': error_message})
