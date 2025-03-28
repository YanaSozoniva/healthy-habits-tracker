# Generated by Django 5.1.7 on 2025-03-22 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0003_alter_habit_time_to_complete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="lead_time",
            field=models.TimeField(
                blank=True,
                help_text="Укажите в какое время планируется выполнять привычку",
                null=True,
                verbose_name="Время",
            ),
        ),
    ]
