from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        name = self.first_name + " " + self.last_name
        return name


class Genre(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="+")
    screenplay = models.ForeignKey(Person, on_delete=models.PROTECT, related_name="+")
    starring = models.ManyToManyField(Person, through="MoviePersonRole")
    year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class MoviePersonRole(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(max_length=64)