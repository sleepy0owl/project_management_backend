# Generated by Django 3.2.4 on 2021-06-08 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('username', models.CharField(max_length=45)),
                ('email_address', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('subscription_type', models.IntegerField()),
            ],
            options={
                'db_table': 'project_users',
            },
        ),
    ]
