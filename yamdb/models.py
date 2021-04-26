from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime as dt

User = get_user_model()


class Category(models.Model):
    """Categories of works."""
    name = models.CharField('Категория', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Genres of works."""
    name = models.CharField('Жанр', max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Creative works."""
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    year = models.PositiveSmallIntegerField(
        'Дата выхода',
        db_index=True,
        default=dt.now().year,
        validators=[MaxValueValidator(limit_value=dt.now().year)]
    )
    category = models.ForeignKey(
        Category, blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='title_category'
    )
    genre = models.ManyToManyField(
        Genre, blank=True,
        verbose_name='Жанр',
        related_name='title_genre'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['-year']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Text user reviews of titles."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Отзывы',
        related_name='review'
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Отзывы',
        related_name='review')
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=10)
        ]
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['title']

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Comment model for reviews."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Комментарии',
        related_name='comment'
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Комментарии',
        related_name='comment')
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['review']

    def __str__(self):
        return self.text
