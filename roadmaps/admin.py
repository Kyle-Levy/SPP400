from django.contrib import admin


class SystemAdmin(admin.ModelAdmin):
    filter_horizontal = ('procedures', )
