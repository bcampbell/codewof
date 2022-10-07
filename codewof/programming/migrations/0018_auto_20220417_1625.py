# Generated by Django 3.2.11 on 2022-04-17 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0017_question_difficulty_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(default='Program', max_length=100),
        ),
        migrations.CreateModel(
            name='QuestionContexts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('name', models.CharField(max_length=500)),
                ('css_class', models.CharField(max_length=30)),
                ('number', models.PositiveSmallIntegerField()),
                ('hint', models.TextField()),
                ('indent_level', models.PositiveSmallIntegerField(default=0)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='programming.questioncontexts')),
            ],
            options={
                'ordering': ['number', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ProgrammingConcepts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('css_class', models.CharField(max_length=30)),
                ('number', models.PositiveSmallIntegerField()),
                ('hint', models.TextField()),
                ('indent_level', models.PositiveSmallIntegerField(default=1)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='programming.programmingconcepts')),
            ],
            options={
                'ordering': ['number', 'name'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='concepts',
            field=models.ManyToManyField(related_name='concepts', to='programming.ProgrammingConcepts'),
        ),
        migrations.AddField(
            model_name='question',
            name='contexts',
            field=models.ManyToManyField(related_name='contexts', to='programming.QuestionContexts'),
        ),
    ]