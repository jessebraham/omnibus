# Generated by Django 2.2.6 on 2019-10-14 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("goodreads", "0002_create_series")]

    operations = [
        migrations.AddField(
            model_name="book",
            name="average_rating",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="large_image_url",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="num_pages",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="publisher",
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="ratings_count",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="small_image_url",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="book",
            name="title_without_series",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="published",
            field=models.IntegerField(null=True),
        ),
    ]
