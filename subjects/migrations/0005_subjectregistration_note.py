# Generated by Django 5.1.6 on 2025-02-10 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subjects", "0004_alter_subject_required_subjects"),
    ]

    operations = [
        migrations.AddField(
            model_name="subjectregistration",
            name="note",
            field=models.FloatField(default=0.0, verbose_name="note"),
        ),
    ]
