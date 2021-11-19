from django.contrib import contenttypes
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


# Category +
# Product +
# Cart_product +
# Customer +
# Cart+
# Order
# Employee
#

class Product(models.Model):
    class Meta:
        abstract = True  # делает продукт не создаваемым в миграции, исп для  наследование

    category = models.ForeignKey('Category', verbose_name=' Категория', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, verbose_name='Наименование продукта')
    description = models.TextField(verbose_name='Описание', )
    price = models.DecimalField(verbose_name='Стоимость', max_digits=9, decimal_places=2)
    count = models.IntegerField(verbose_name='Количество товара')
    image = models.ImageField(verbose_name=' Изображение', upload_to='media/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Продукт: {}'.format(self.title)


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    ram = models.CharField(verbose_name='ОЗУ', max_length=255)
    video_card = models.CharField(max_length=255, verbose_name='Видео карта')
    battery_life = models.CharField(verbose_name='Время работы от аккумулятора', max_length=255)
    cpu = models.CharField(verbose_name='Процессор', max_length=255)

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)


class SmartDevice(Product):
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    memory = models.CharField(max_length=255, verbose_name='Память')
    ram = models.CharField(verbose_name='ОЗУ', max_length=255)
    cpu = models.CharField(verbose_name='Процессор', max_length=255)

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)


class Category(models.Model):
    name = models.CharField(max_length=156, verbose_name='Наименование категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Category', kwargs={'slug': self.slug})


class Cart(models.Model):
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Владелец')
    product = models.ManyToManyField('CartProduct', blank=True, related_name='relate_product', )
    final_price = models.DecimalField(verbose_name='Конечная стоимость', max_digits=9,
                                      decimal_places=2)

    def __str__(self):
        return self.owner

    def get_absolute_url(self):
        return reverse('Cart', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='relate_cart', verbose_name='Корзина')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # помогает увидеть все модели от продукта
    object_id = models.PositiveIntegerField()  # идентификатор инстанса этой модели
    content_object = GenericForeignKey('content_type', 'object_id')
    final_price = models.DecimalField(verbose_name='Конечная стоимость', max_digits=9,
                                      decimal_places=2)  # decimal_places количество символов после запятой
    qty = models.PositiveIntegerField(default=1)  # количество

    def __str__(self):
        return 'Продукт: {} (для корзины)'.format(self.product.title)


class Customer(models.Model):
    slug = models.SlugField(unique=True, verbose_name='ссылка')
    address = models.CharField(max_length=255, verbose_name='Адресс')
    user = models.ForeignKey(User, max_length=255, on_delete=models.CASCADE, verbose_name=' Пользователь')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')

    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)


class Employee(models.Model):
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=255, verbose_name='Адрес')
    user = models.CharField(max_length=255, verbose_name=' Пользователь')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
