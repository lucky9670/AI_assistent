from django.contrib import admin
from .models import *

# Register your models here.
class UserFormAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'username', 'email', 'phone', 'address', 'gender', 'image', 'prefrence', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')

admin.site.register(User, UserFormAdmin)
admin.site.register(Task)
admin.site.register(Reminder)
admin.site.register(Activity)
admin.site.register(ScheduleTask)