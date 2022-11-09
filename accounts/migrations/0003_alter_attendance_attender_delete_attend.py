# Generated by Django 4.1.2 on 2022-10-18 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0002_attendance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="attender",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(name="Attend",),
    ]