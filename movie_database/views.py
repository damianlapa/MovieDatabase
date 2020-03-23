from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from django.views import View
from django.http import HttpResponse
from movie_database.models import Person, Genre, Movie, MoviePersonRole
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt


class AddPerson(View):
    def get(self, request):
        return render(request, "add_person.html")

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        new_person = Person()
        new_person.first_name = first_name
        new_person.last_name = last_name
        new_person.save()
        return redirect("/persons")


class AddGenre(View):
    def get(self, request):
        return render(request, "add_genre.html")

    def post(self, request):
        genres = Genre.objects.all()
        genre = request.POST.get("genre")
        for item in genres:
            if genre == item.name:
                statement = "Genre {} is already in database!".format(item.name)
                return render(request, "statement.html", {"statement": statement})

        new_genre = Genre()
        new_genre.name = genre
        new_genre.save()
        statement = "Genre {} added!".format(new_genre)

        return render(request, "statement.html", {"statement": statement})


class MainPage(View):
    def get(self, request):
        movie_num = 0
        person_num = 0
        movies = Movie.objects.all()
        persons = Person.objects.all()

        for movie in movies:
            movie_num += 1

        for person in persons:
            person_num += 1

        return render(request, "main_page.html", context={"movie_num": movie_num, "person_num": person_num})

    def post(self, request):
        pass


class AddMovie(View):
    def get(self, request):
        persons = Person.objects.all()
        genres = Genre.objects.all()
        return render(request, "add_movie.html", context={"persons": persons, "genres": genres})

    def post(self, request):

        title = request.POST.get("title")
        director_id = int(request.POST.get("director"))
        director = Person.objects.get(id=director_id)
        screenplay_id = int(request.POST.get("screenplay"))
        screenplay = Person.objects.get(id=screenplay_id)
        starring_id = int(request.POST.get("starring"))
        starring = Person.objects.get(id=starring_id)
        role = request.POST.get("role")
        year = int(request.POST.get("year"))
        rating = float(request.POST.get("rating"))
        genre = Genre.objects.get(id=int(request.POST.get("genre")))

        new_movie = Movie()
        new_movie.title = title
        new_movie.director_id = director.id
        new_movie.screenplay_id = screenplay.id
        new_movie.year = year
        new_movie.rating = rating

        new_movie.save()

        new_movie.genre.add(genre)
        MoviePersonRole.objects.create(movie=new_movie, person=starring, role=role)

        return redirect("/movies")


class Movies(View):
    def get(self, request):
        movies = Movie.objects.all().order_by('year')
        if request.session["sorted"] == 1:
            movies = Movie.objects.all().order_by('rating')
        elif request.session["sorted"] == 2:
            movies = Movie.objects.all().order_by('-rating')
        elif request.session["sorted"] == 0 or request.session["sorted"] is None:
            movies = Movie.objects.all().order_by('year')
        return render(request, "movies.html", {"movies": movies})

    def post(self, request):
        action = request.POST.get("action")
        delete = request.POST.get("delete_id")
        if delete:
            movie = Movie.objects.get(id=int(delete))
            movie.delete()
            return redirect("/movies")
        if action == "Ascending":
            request.session["sorted"] = 1
            movies = Movie.objects.all().order_by('rating')
            return render(request, "movies.html", {"movies": movies})
        elif action == "Descending":
            request.session["sorted"] = 2
            movies = Movie.objects.all().order_by('-rating')
            return render(request, "movies.html", {"movies": movies})
        elif action == "Default(by date)":
            request.session["sorted"] = 0
            movies = Movie.objects.all().order_by('year')
            return render(request, "movies.html", {"movies": movies})


class MovieDetails(View):
    def get(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        director = Person.objects.get(id=movie.director_id)
        screenplay = Person.objects.get(id=movie.screenplay_id)
        genre = movie.genre.all()[0]
        starring = movie.starring.all()[0]
        role = MoviePersonRole.objects.get(movie=movie, person=starring).role
        return render(request, "movie_details.html", context={"movie": movie, "director": director,
                                                              "screenplay": screenplay, "genre": genre,
                                                              "starring": starring, "role": role})


class Persons(View):
    def get(self, request):
        persons = Person.objects.all().order_by('last_name')
        return render(request, "persons.html", {"persons": persons})

    def post(self, request):
        delete = request.POST.get("delete_id")
        if delete:
            person = Movie.objects.get(id=int(delete))
            person.delete()
            return redirect("/persons")


class EditPerson(View):
    def get(self, request, person_id):
        person = Person.objects.get(id=person_id)
        return render(request, "edit_person.html", {"person": person})
    def post(self, request, person_id):
        person = Person.objects.get(id=person_id)
        person.first_name = request.POST.get("first_name")
        person.last_name = request.POST.get("last_name")
        person.save()
        statement = "{} edited".format(person)
        return render(request, "statement.html", {"statement": statement})


class EditMovie(View):
    def get(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        movies = Movie.objects.all()
        title = movie.title
        starring = movie.starring.all()[0]
        persons = Person.objects.all()
        role = MoviePersonRole.objects.get(movie=movie, person=starring).role
        genres = Genre.objects.all()
        genre = movie.genre.all()[0]
        return render(request, "edit_movie.html", {"movie": movie, "movies": movies, "mid": movie_id,
                                                   "persons": persons, "starring": starring, "role": role,
                                                   "genres": genres, "movie_genre": genre, "title": title})
    def post(self, request, movie_id):
        title = request.POST.get("title")
        director_id = int(request.POST.get("director"))
        director = Person.objects.get(id=director_id)
        screenplay_id = int(request.POST.get("screenplay"))
        screenplay = Person.objects.get(id=screenplay_id)
        starring_id = int(request.POST.get("starring"))
        starring = Person.objects.get(id=starring_id)
        role = request.POST.get("role")
        year = int(request.POST.get("year"))
        rating = float(request.POST.get("rating"))
        genre = Genre.objects.get(id=int(request.POST.get("genre")))

        edited_movie = Movie.objects.get(id=movie_id)
        edited_movie.title = title
        edited_movie.director_id = director.id
        edited_movie.screenplay_id = screenplay.id
        edited_movie.year = year
        edited_movie.rating = rating

        edited_movie.starring.clear()
        edited_movie.genre.clear()

        edited_movie.save()

        edited_movie.genre.add(genre)
        MoviePersonRole.objects.create(movie=edited_movie, person=starring, role=role)

        return redirect("/movies")

class SearchMovie(View):
    def get(self, request):
        return render(request, "search_movie.html")

    def post(self, request):
        title = request.POST.get("title", None)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        year_from = request.POST.get("year_from", None)
        year_to = request.POST.get("year_to", None)
        genres = request.POST.get("genre", None)
        rating_bottom = request.POST.get("bottom_rate", None)
        ratting_top = request.POST.get("top_rate", None)

        movies = Movie.objects.all()
        persons = Person.objects.all()

        if title:
            movies = movies.filter(title=title)

        if year_from.isdigit():
            movies = movies.filter(year__gte=year_from)

        if year_to.isdigit():
            movies = movies.filter(year__lte=year_to)

        if rating_bottom.isdigit():
            movies = movies.filter(rating__gte=rating_bottom)

        if ratting_top.isdigit():
            movies = movies.filter(rating__lte=ratting_top)

        filtered_movies = []

        if first_name:
            persons = persons.filter(first_name=first_name)

        if last_name:
            persons = persons.filter(last_name=last_name)

        if first_name or last_name:

            for person in persons:
                movies2 = movies.filter(director=person)
                movies3 = movies.filter(screenplay=person)
                movies4 = person.movie_set.all()
                for movie in movies4:
                    filtered_movies.append(movie.id)
                for movie in movies2:
                    filtered_movies.append(movie.id)
                for movie in movies3:
                    filtered_movies.append(movie.id)

            filtered_movies = set(filtered_movies)

            movies = []

            for movie_id in filtered_movies:
                movies.append(Movie.objects.get(id=movie_id))

        if genres:
            genres_split = genres.replace(" ", "").split(",")

            filtered_movies_by_genres = []

            for genre_object in genres_split:
                try:
                    genres_movie = Genre.objects.get(name=genre_object)
                    genre_movies = genres_movie.movie_set.all()
                    for movie in genre_movies:
                        if movie in movies:
                            filtered_movies_by_genres.append(movie.id)
                except Genre.DoesNotExist:
                    pass

            movies = []

            for movie_id in filtered_movies_by_genres:
                movies.append(Movie.objects.get(id=movie_id))

        search = True

        return render(request, "movies.html", {"movies": movies, "search": search})


class DeleteMovie(View):
    def post(self, request, movie_id):
        movie = Movie.objects.get(id=int(movie_id))
        title = movie.title
        movie.delete()
        return render(request, "del_movie.html", {"title": title})


class DeletePerson(View):
    def post(self, request, person_id):
        person = Person.objects.get(id=int(person_id))
        name = person
        try:
            person.delete()
        except ProtectedError:
            statement = "Person can't be delete!"
            return render(request, "statement.html", {"statement": statement})

        return render(request, "del_person.html", {"name": name})
