from django.contrib import admin

from .models import File, FileTag


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'uploaded_by')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ('tags',)

admin.site.register(File, FileAdmin)


class FileTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(FileTag, FileTagAdmin)
