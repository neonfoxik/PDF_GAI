
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('button_name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='имя кнопки а также колбэк дата')),
                ('button_group', models.CharField(max_length=20, verbose_name='имя группы кнопок')),
                ('button_text', models.CharField(max_length=100, verbose_name='текст кнопки')),
            ],
            options={
                'verbose_name': 'Кнопка',
                'verbose_name_plural': 'Кнопки',
            },
        ),
        migrations.CreateModel(
            name='ButtonGroup',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Имя группы кнопок')),
                ('parent_button', models.CharField(max_length=20, verbose_name='Имя родительской кнопки')),
                ('is_main_group', models.BooleanField(default=False)),
                ('is_document', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Группа кнопок',

    ]
