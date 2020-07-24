# Generated by Django 3.0.6 on 2020-07-24 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=225)),
                ('link', models.CharField(max_length=225)),
                ('admin', models.ManyToManyField(related_name='controlling', to='rooms.UserProfile')),
                ('participate', models.ManyToManyField(blank=True, related_name='classes', to='rooms.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('credit', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='rooms.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='rooms.Exam')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_answers', to='rooms.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='rooms.Room'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('exam_answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='rooms.ExamAnswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='rooms.Question')),
            ],
        ),
    ]