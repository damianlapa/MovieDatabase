from django.core.management import BaseCommand

from movie_database.management.commands_data.movies_data import PERSONS_DATA, GENRES_DATA, TITLES_DATA, ROLES_DATA
from movie_database.models import Person, Movie, Genre, MoviePersonRole
import random


def insert_persons():
    for first_name, last_name in PERSONS_DATA:
        Person.objects.create(first_name=first_name, last_name=last_name)


def insert_genres():
    for genre in GENRES_DATA:
        Genre.objects.create(name=genre)

def insert_movies():
    for i in range(50):
        titles = [movie.title for movie in Movie.objects.all()]
        while True:
            title = "The {} {}".format(random.choice(TITLES_DATA[0]), random.choice(TITLES_DATA[1]))
            if title not in titles:
                break
        persons = Person.objects.all()
        genres = Genre.objects.all()

        director = Person.objects.get(id=random.choice(persons).id)
        screenplay = Person.objects.get(id=random.choice(persons).id)
        starring = Person.objects.get(id=random.choice(persons).id)
        role = random.choice(ROLES_DATA)
        year = random.randint(1900, 2020)
        rating = random.randint(15, 100)/10
        genre = Genre.objects.get(id=random.choice(genres).id)

        new_movie = Movie()
        new_movie.title = title
        new_movie.director_id = director.id
        new_movie.screenplay_id = screenplay.id
        new_movie.year = year
        new_movie.rating = rating

        new_movie.save()

        new_movie.genre.add(genre)
        MoviePersonRole.objects.create(movie=new_movie, person=starring, role=role)

class Command(BaseCommand):
    help = "Insert data about movies to data base."

    def handle(self, *args, **kwargs):
        insert_persons()
        insert_genres()
        insert_movies()
        print("Data load successfully!")
