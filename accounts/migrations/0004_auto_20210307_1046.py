# Generated by Django 3.1.7 on 2021-03-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='klass',
            name='teachers',
            field=models.ManyToManyField(related_name='teachers', to='accounts.Teacher'),
        ),
        migrations.AlterField(
            model_name='klass',
            name='klass_name',
            field=models.CharField(choices=[('stage 1', 'Primary One'), ('stage 2', 'Primary Two'), ('stage 3', 'Primary Three'), ('stage 4', 'Primary Four'), ('stage 5', 'Primary Five'), ('stage 6', 'Primary Six'), ('jhs 1', 'Junior High 1'), ('jhs 2', 'Junior High 2'), ('jhs 3', 'Junior High 3')], max_length=10),
        ),
    ]
