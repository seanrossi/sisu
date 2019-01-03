# Generated by Django 2.0.5 on 2018-12-14 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20181214_0308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollstats',
            name='post',
        ),
        migrations.AddField(
            model_name='pollquestions',
            name='choice1stat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pollquestions',
            name='choice2stat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pollquestions',
            name='choice3stat',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pollquestions',
            name='choice4stat',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='PollStats',
        ),
    ]
