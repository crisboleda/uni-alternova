# Generated by Django 5.1.6 on 2025-02-09 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subjects", "0002_alter_subject_required_subjects"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="required_subjects",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                to="subjects.subject",
                verbose_name="required subjects",
            ),
        ),
    ]
