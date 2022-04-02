# Generated by Django 4.0.3 on 2022-04-01 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('code', models.CharField(blank=True, default=None, max_length=124, null=True, unique=True)),
                ('user_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('language_code', models.CharField(blank=True, default=None, help_text="Telegram client's lang", max_length=8, null=True)),
                ('deep_link', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('is_stopped', models.BooleanField(default=False)),
            ],
        ),
    ]