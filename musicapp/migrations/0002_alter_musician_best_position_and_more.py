# Generated by Django 5.0.4 on 2024-05-11 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("musicapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="musician",
            name="best_position",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="musician",
            name="current_position",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="musician",
            name="end_date_best_position",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="musician",
            name="points",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="musician",
            name="points_semester",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="musician",
            name="points_year",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="musician",
            name="rating",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="musician",
            name="start_date_best_position",
            field=models.DateField(null=True),
        ),
    ]