# Generated by Django 3.1.7 on 2021-03-01 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('playername', models.CharField(max_length=100, unique=True)),
                ('live_sts', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'player',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerQuestions',
            fields=[
                ('srno', models.AutoField(primary_key=True, serialize=False)),
                ('choice', models.IntegerField()),
            ],
            options={
                'db_table': 'player_questions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerQuizdet',
            fields=[
                ('srno', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
            ],
            options={
                'db_table': 'player_quizdet',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TbQuestions',
            fields=[
                ('questionid', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'tb_questions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblChoices',
            fields=[
                ('questionid', models.OneToOneField(db_column='questionid', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='quiz.tbquestions')),
                ('choice1', models.CharField(blank=True, max_length=100, null=True)),
                ('choice2', models.CharField(blank=True, max_length=100, null=True)),
                ('choice3', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tbl_choices',
                'managed': False,
            },
        ),
    ]