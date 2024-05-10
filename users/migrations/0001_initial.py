# Generated by Django 5.0.2 on 2024-05-10 12:29

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrator', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='note')),
                ('date', models.DateField(help_text='date.png', verbose_name='date')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('file', models.FileField(blank=True, null=True, upload_to=users.models.save_record_file, verbose_name='file')),
                ('is_validate', models.BooleanField(default=False, verbose_name='validate?')),
                ('field_1', models.PositiveIntegerField(default=0, help_text='bath.png', verbose_name='Bath & Body products')),
                ('field_2', models.PositiveIntegerField(default=0, help_text='beauty.png', verbose_name='Beauty and cosmetics products')),
                ('field_3', models.PositiveIntegerField(default=0, help_text='books.png', verbose_name='Books and stationery')),
                ('field_4', models.PositiveIntegerField(default=0, help_text='electronics.png', verbose_name='Electronics')),
                ('field_5', models.PositiveIntegerField(default=0, help_text='kitchen.png', verbose_name='Kitchen gadgets and cookware')),
                ('field_6', models.PositiveIntegerField(default=0, help_text='musical.png', verbose_name='Musical instruments and accessories')),
                ('field_7', models.PositiveIntegerField(default=0, help_text='pet-shop.png', verbose_name='Pet supplies and accessories')),
                ('field_8', models.PositiveIntegerField(default=0, help_text='sports.png', verbose_name='Sports Goods & Equipment')),
                ('field_9', models.PositiveIntegerField(default=0, help_text='tools.png', verbose_name='Tools and hardware')),
                ('field_10', models.PositiveIntegerField(default=0, help_text='toys.png', verbose_name='Toys and games')),
                ('field_11', models.PositiveIntegerField(default=0, help_text='video-games.png', verbose_name='Video Games and Consoles')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.departments', verbose_name='department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='uploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=255, verbose_name='subject')),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='note')),
                ('date', models.DateField(verbose_name='upload date')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='added at')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('file', models.FileField(blank=True, null=True, upload_to=users.models.save_uploadFile, verbose_name='file')),
                ('is_validate', models.BooleanField(default=False, verbose_name='validated?')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.departments', verbose_name='Department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Account Owner')),
            ],
        ),
    ]
