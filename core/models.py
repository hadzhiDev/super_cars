from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django_resized import ResizedImageField

from utils.models import TimeStampAbstractModel


class Category(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'

class Brand(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    name = models.CharField(verbose_name = 'Имя марка', max_length=150, unique=True)

    def __str__(self):
        return f'{self.name}'


class Car(TimeStampAbstractModel):

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    model = models.CharField(max_length=150, verbose_name='Модель',)
    brand = models.ForeignKey(Brand, verbose_name = 'Марка', on_delete=models.CASCADE, related_name='cars',)
    year = models.IntegerField(verbose_name='год выпуска')
    overview = models.CharField(max_length=1000, verbose_name='Краткое описание', help_text='Просто описание')
    owner = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='Владелец', null=True)
    price = models.DecimalField(verbose_name='Цена автомобиля', max_digits=10, decimal_places=2, default=0.0)
    color = models.CharField(max_length=100, verbose_name='Цвет автомобиля')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата добавление')
    is_published = models.BooleanField('публичность', default=True)
    category = models.ForeignKey('core.Category', models.PROTECT, "cars", verbose_name='категория',
                                 help_text='Выберите категорию')

    def clean(self):
        if len(self.model) < 3:
            raise ValidationError({'model': ['Model name must be at least 3 characters']})

    @property
    def image(self):
        if self.images.first():
            return self.images.first().image
        return None

    def __str__(self):
        return f'{self.brand.name} - {self.model}'


class CarImage(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'изображение автомобиля'
        verbose_name_plural = 'изображении автомобили'
        ordering = ('-created_at',)

    car = models.ForeignKey('core.Car', models.CASCADE, 'images', verbose_name='автомобиль')
    image = ResizedImageField('изображение', upload_to='cars_images/', force_format='WEBP', quality=90)

    def __str__(self):
        return f'{self.car.model}'


class CarAttribute(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'атрибут автомобиля'
        verbose_name_plural = 'атрибуты автомобили'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=50)
    value = models.CharField('значение', max_length=50)
    car = models.ForeignKey('core.Car', models.CASCADE, 'attributes', verbose_name='товар')

    def __str__(self):
        return f'{self.name} - {self.value}'