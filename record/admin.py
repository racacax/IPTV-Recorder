from django.contrib import admin

from record.models import UserData, Playlist, RecordingMethod, Recording


# Register your models here.
class DefaultAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserData, DefaultAdmin)
admin.site.register(Playlist, DefaultAdmin)
admin.site.register(RecordingMethod, DefaultAdmin)
admin.site.register(Recording, DefaultAdmin)
