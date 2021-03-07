# Generated by Django 3.1.7 on 2021-03-07 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210307_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='health_insurance',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='known_health_disorder',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='physically_disabled',
            field=models.BooleanField(default=False),
        ),
    ]
