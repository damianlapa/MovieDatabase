# Generated by Django 2.2.6 on 2020-03-18 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('year', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MoviePersonRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=64)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movie_database.Movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movie_database.Person')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='movie_database.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='movie_database.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='screenplay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='movie_database.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='starring',
            field=models.ManyToManyField(through='movie_database.MoviePersonRole', to='movie_database.Person'),
        ),
    ]