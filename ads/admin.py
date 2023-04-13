from django.contrib import admin

from ads.models import Ad, Category, Selection


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'is_published')
    search_fields = ('name', 'description')
    list_filter = ('is_published',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    pass


