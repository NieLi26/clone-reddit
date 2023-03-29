# Generated by Django 4.1.7 on 2023-03-23 19:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("foro", "0003_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment", name="body", field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name="post", name="body", field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name="subreddit",
            name="description",
            field=ckeditor.fields.RichTextField(),
        ),
    ]
