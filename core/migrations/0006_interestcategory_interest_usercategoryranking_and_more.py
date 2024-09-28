# Generated by Django 5.1 on 2024-09-26 19:54

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_userprofile_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Interest Categories',
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', to='core.interestcategory')),
            ],
            options={
                'verbose_name_plural': 'Interests',
                'unique_together': {('name', 'category')},
            },
        ),
        migrations.CreateModel(
            name='UserCategoryRanking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importance', models.IntegerField(help_text='Importance ranking from 1 (least important) to 5 (most important)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.interestcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_rankings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category')},
            },
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.interest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_interests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'interest')},
            },
        ),
    ]
