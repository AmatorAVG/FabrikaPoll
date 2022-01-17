# Generated by Django 2.2.26 on 2022-01-17 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название')),
                ('start_at', models.DateTimeField(verbose_name='дата старта')),
                ('finish_at', models.DateTimeField(verbose_name='дата окончания')),
                ('description', models.TextField(verbose_name='описание')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('T', 'Ответ текстом'), ('S', 'Ответ с выбором одного варианта'), ('P', 'Ответ с выбором нескольких вариантов')], db_index=True, default='T', max_length=2)),
                ('text', models.CharField(max_length=200)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.Survey', verbose_name='опрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='AnswerOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=200)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='core.Question', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'вариант ответа',
                'verbose_name_plural': 'варианты ответа',
                'unique_together': {('question', 'option')},
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('author', models.IntegerField(verbose_name='ID пользователя')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Question')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='AnswerItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_items', to='core.Answer', verbose_name='Ответ')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='core.AnswerOptions', verbose_name='вариант ответа')),
            ],
            options={
                'verbose_name': 'выбранный вариант ответа',
                'verbose_name_plural': 'выбранные варианты ответа',
                'unique_together': {('answer', 'option')},
            },
        ),
    ]
