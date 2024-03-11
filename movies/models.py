from django.db import models
from slugify import slugify
from datetime import datetime


class Category(models.Model):
    slug = models.SlugField(max_length=160, unique=True, primary_key=True, blank=True)
    name = models.CharField('Категория', max_length=150)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    slug = models.SlugField(max_length=160, unique=True, primary_key=True, blank=True)
    name = models.CharField(verbose_name='Имя', max_length=100)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='actors/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    slug = models.SlugField(max_length=160, unique=True, primary_key=True, blank=True)
    name = models.CharField(verbose_name='Жанр', max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    slug = models.SlugField(max_length=160, unique=True, primary_key=True, blank=True)
    title = models.CharField(verbose_name='Название', max_length=100)
    tagline = models.CharField(verbose_name='Слоган', max_length=100, default='')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField('Постер', upload_to='movies/', blank=True, null=True)
    year = models.PositiveSmallIntegerField(verbose_name='Дата выхода', default=1997)
    country = models.CharField(verbose_name='Страна', max_length=50)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    budget = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text='указать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(verbose_name='Сборы в США', default=0,
                                              help_text='указать сумму в долларах')
    fees_in_world = models.PositiveIntegerField(verbose_name='Сборы в мире', default=0,
                                                help_text='указать сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='Значение', default=0)

    def __str__(self) -> str:
        return str(self.value)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    user = models.CharField(verbose_name='Пользователь', max_length=50)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм', related_name='ratings')

    def __str__(self) -> str:
        return f'{self.user} - {self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='children')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self) -> str:
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'