from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from PIL import Image
from .models import *


class ImageAdminForm(ModelForm):
    MIN_RESIZE = (400, 400)
    MAX_RESIZE = (1200, 1100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображение с минимальным разрешением {}x{}'.format(
            *self.MIN_RESIZE)

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        print(img)
        min_height, min_width = self.MIN_RESIZE
        max_height, max_width = self.MAX_RESIZE
        print(min_height)
        print(min_width)
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Загружанное изображение меньше минимального')
        elif img.height > max_height or img.width > max_width:
            raise ValidationError('Загружанное изображение ,больше максимального')
        return image


class NotebookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartDeviceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartDevice, SmartDeviceAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Customer)
admin.site.register(Employee)
