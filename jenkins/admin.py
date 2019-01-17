from django.contrib import admin
from jenkins import models
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
    list_filter = ('username',)
    search_fields = ('username',)
    # raw_id_fields = ('consult_course',)
    # filter_horizontal = ('tags',)
    # list_editable = ('status',)
    list_per_page = 5

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Project)
admin.site.register(models.Permiss)