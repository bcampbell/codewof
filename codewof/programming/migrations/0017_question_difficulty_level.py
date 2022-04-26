# Generated by Django 3.2.11 on 2022-04-17 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0016_remove_question_difficulty_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='difficulty_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='programming.difficultylevel'),
        ),
    ]
