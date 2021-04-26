"""Command for put value from csv to database."""
import os
from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from yamdb.models import Genre, Category, Title, Comment, Review

User = get_user_model()
BASE_DATA_DIR = os.path.join(BASE_DIR, 'data/')


def create_user(fields):
    User.objects.get_or_create(
        id=fields['id'],
        username=fields['username'],
        email=fields['email'],
        role=fields['role'],
        bio=fields['description'],
        first_name=fields['first_name'],
        last_name=fields['last_name']
    )


def create_genre(fields):
    Genre.objects.get_or_create(
        id=fields['id'],
        name=fields['name'],
        slug=fields['slug']
    )


def create_category(fields):
    Category.objects.get_or_create(
        id=fields['id'],
        name=fields['name'],
        slug=fields['slug']
    )


def create_title(fields):
    Title.objects.get_or_create(
        id=fields['id'],
        name=fields['name'],
        year=fields['year'],
        category=Category.objects.get(id=fields['category'])
    )[0].genre.add(*get_genre_objects(fields['id']))


def get_genre_objects(title_id):
    with open(os.path.join(BASE_DATA_DIR, 'genre_title.csv'),
              newline='') as csvfile:
        reader = DictReader(csvfile)
        genre_id_list = [filtered_genre_title['genre_id'] for
                         filtered_genre_title in
                         list(filter(
                             lambda genre_title: genre_title['title_id']
                              == title_id, reader))]
        return list(Genre.objects.filter(pk__in=genre_id_list))


def create_review(fields):
    review = Review.objects.get_or_create(
        id=fields['id'],
        title=Title.objects.get(pk=fields['title_id']),
        text=fields['text'],
        author=User.objects.get(pk=fields['author']),
        score=fields['score'],
    )[0]
    review.pub_date = fields['pub_date']
    review.save()


def create_comment(fields):
    comment = Comment.objects.get_or_create(
        id=fields['id'],
        review=Review.objects.get(pk=fields['review_id']),
        text=fields['text'],
        author=User.objects.get(pk=fields['author']),
    )[0]
    comment.pub_date = fields['pub_date']
    comment.save()


def fill_table(csv_file, func):
    with open(os.path.join(BASE_DATA_DIR, csv_file),
              newline='') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            func(row)


MODEL_DICT = {
    'users.csv': create_user,
    'genre.csv': create_genre,
    'category.csv': create_category,
    'titles.csv': create_title,
    'review.csv': create_review,
    'comments.csv': create_comment,

}


class Command(BaseCommand):

    def handle(self, *args, **options):
        [fill_table(csv_file, func) for csv_file, func in MODEL_DICT.items()]
