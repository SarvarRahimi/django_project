# Generated by Django 3.1.5 on 2021-01-27 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_text', models.CharField(max_length=200, verbose_name='category text')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(verbose_name='comment text')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_text', models.CharField(max_length=100, verbose_name='label text')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.category')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_text', models.CharField(max_length=10, verbose_name='like text')),
                ('like_count', models.IntegerField(verbose_name='like count')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=200, verbose_name='post head')),
                ('body', models.TextField(verbose_name='post body')),
                ('date', models.DateField(verbose_name='post date')),
                ('images', models.ImageField(upload_to='', verbose_name='post images')),
                ('category', models.ManyToManyField(to='posting.Category')),
                ('label', models.ManyToManyField(to='posting.Label')),
                ('like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.like')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='first name')),
                ('last_name', models.CharField(max_length=100, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone_number', models.IntegerField(verbose_name='phone number')),
                ('images', models.ImageField(upload_to='', verbose_name='images')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.post')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='like',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.like'),
        ),
    ]
