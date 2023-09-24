from django.contrib import admin
from .models import User,Customer,Profile,Admin,Task
# Register your models here.
class AdminDisplay(admin.ModelAdmin):
    list_display = ('username','email', 'password')
admin.site.register(User, AdminDisplay)
from django.contrib import admin
from .models import User
# Register your models here.
class AdminDisplay(admin.ModelAdmin):
    list_display = ('email','username')
admin.site.register(Customer, AdminDisplay)
class AdminDisplay(admin.ModelAdmin):
    list_display = ('email','username')
admin.site.register(Admin, AdminDisplay)
class AdminDisplay(admin.ModelAdmin):
    list_display = ('image',)
admin.site.register(Profile, AdminDisplay)

class AdminDisplay(admin.ModelAdmin):
    list_display = ('title','description')
admin.site.register(Task, AdminDisplay)