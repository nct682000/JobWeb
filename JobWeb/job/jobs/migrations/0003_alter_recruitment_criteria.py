# Generated by Django 3.2.5 on 2021-08-01 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20210801_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitment',
            name='criteria',
            field=models.ManyToManyField(null=True, related_name='recruitment_criteria', to='jobs.Criteria'),
        ),
    ]