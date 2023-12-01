from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe

from core.models import Category, Car, CarImage, CarAttribute, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


class CarAdminForm(forms.ModelForm):
    overview = forms.CharField(widget=forms.Textarea, label='Описание', help_text='Просто описание')

    class Meta:
        model = Car
        fields = '__all__'


class CarImageStackedInline(admin.TabularInline):

    model = CarImage
    extra = 1


class CarAttributeStackedInline(admin.TabularInline):

    model = CarAttribute
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'price', 'category', 'is_published', 'get_image')
    list_display_links = ('id', 'model',)
    list_filter = ('category', 'owner', 'is_published',)
    search_fields = ('model', 'overview',)
    readonly_fields = ('created_at', 'updated_at', 'get_big_image',)
    form = CarAdminForm
    inlines = [CarImageStackedInline, CarAttributeStackedInline]

    @admin.display(description='Изображение')
    def get_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="150px">')
        return '-'

    @admin.display(description='Изображение')
    def get_big_image(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" width="100%">')
        return '-'

