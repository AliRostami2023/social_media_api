# Generated by Django 4.2.9 on 2025-02-03 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_comment_created_alter_comment_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hashtag',
        ),
        migrations.DeleteModel(
            name='Hashtag',
        ),
    ]
