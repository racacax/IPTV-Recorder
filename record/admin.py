from django.contrib import admin

from record.models import UserData


# Register your models here.
class UserDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserData, UserDataAdmin)
