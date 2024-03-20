# Generated by Django 4.2.11 on 2024-03-20 06:54

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(upload_to='uploads/%Y/%m')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('tel', models.CharField(max_length=255, null=True, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('view', models.IntegerField(default=0)),
                ('author', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='PartArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('index', models.IntegerField(default=0)),
                ('heading', models.CharField(max_length=255, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('description_photo', models.CharField(max_length=255, null=True)),
                ('photo', models.ImageField(upload_to='photos/%Y/%m')),
                ('fk_article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partarticle_article', to='todaynews.article')),
            ],
            options={
                'db_table': 'partarticle',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('fk_article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorite_article', to='todaynews.article')),
                ('fk_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='favorite_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('comment_text', models.TextField(blank=True, null=True)),
                ('fk_article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_article', to='todaynews.article')),
                ('fk_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comment',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='fk_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_category', to='todaynews.category'),
        ),
        migrations.AddField(
            model_name='article',
            name='fk_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='article_user', to=settings.AUTH_USER_MODEL),
        ),
    ]