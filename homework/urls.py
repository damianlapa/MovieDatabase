"""homework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from movie_database.views import AddPerson, AddGenre, MainPage, AddMovie, Movies, MovieDetails, Persons, EditPerson
from movie_database.views import EditMovie, SearchMovie, DeleteMovie, DeletePerson

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-person', AddPerson.as_view(), name='add-person'),
    path('add-genre', AddGenre.as_view(), name='add-genre'),
    path('main-page', MainPage.as_view(), name='main-page'),
    path('add-movie', AddMovie.as_view(), name='add-movie'),
    path('movies', Movies.as_view(), name='movies'),
    path('movie-details/<int:movie_id>', MovieDetails.as_view(), name='movie-details'),
    path('persons', Persons.as_view(), name='persons'),
    path('edit-person/<int:person_id>', EditPerson.as_view(), name='person-edit'),
    path('edit-movie/<int:movie_id>', EditMovie.as_view(), name='movie-edit'),
    path('search-movie', SearchMovie.as_view(), name='search-movie'),
    path('del-movie/<int:movie_id>', DeleteMovie.as_view(), name='delete-movie'),
    path('del-person/<int:person_id>', DeletePerson.as_view(), name='delete-person')

]