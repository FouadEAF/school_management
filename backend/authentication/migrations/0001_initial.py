# Generated by Django 4.1.13 on 2024-07-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activation_code', models.CharField(max_length=5)),
                ('expires_at', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
