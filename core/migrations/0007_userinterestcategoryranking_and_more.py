# Generated by Django 5.1 on 2024-09-28 02:26

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_interestcategory_interest_usercategoryranking_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInterestCategoryRanking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importance', models.IntegerField(help_text='Importance ranking from 1 (least important) to 5 (most important)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.interestcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interest_category_rankings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'category')},
            },
        ),
        migrations.DeleteModel(
            name='UserCategoryRanking',
        ),
    ]
