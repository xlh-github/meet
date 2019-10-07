# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-09-11 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='会议室名称')),
            ],
            options={
                'verbose_name_plural': '会议室',
            },
        ),
        migrations.CreateModel(
            name='ReserveRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='预定日期')),
                ('timeline', models.IntegerField(choices=[(1, '8.00'), (2, '9.00'), (3, '10.00'), (4, '11.00'), (5, '12.00'), (6, '13.00'), (7, '14.00'), (8, '15.00'), (9, '16.00'), (10, '17.00'), (11, '18.00'), (12, '19.00'), (13, '20.00')], verbose_name='预定时间')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.MeetingRoom', verbose_name='预定房间')),
            ],
            options={
                'verbose_name_plural': '预订记录表',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='reserverecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.UserInfo', verbose_name='预订人'),
        ),
        migrations.AlterUniqueTogether(
            name='reserverecord',
            unique_together=set([('data', 'timeline', 'room')]),
        ),
    ]