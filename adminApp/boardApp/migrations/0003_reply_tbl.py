# Generated by Django 4.1.7 on 2023-03-30 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boardApp', '0002_board_tbl'),
    ]

    operations = [
        migrations.CreateModel(
            name='reply_tbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_writer', models.CharField(max_length=500)),
                ('reply_txt', models.CharField(max_length=500)),
                ('board_id', models.ForeignKey(db_column='board_id', on_delete=django.db.models.deletion.CASCADE, to='boardApp.board_tbl')),
            ],
        ),
    ]
