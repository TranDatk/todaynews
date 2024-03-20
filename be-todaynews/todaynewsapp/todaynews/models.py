from django.db import models
from django.contrib.auth.models import AbstractUser

class ItemBase(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')
    email = models.CharField(max_length=255, null=False, unique=True)
    tel = models.CharField(max_length=255, null=True, unique=True)

class Category(ItemBase):
    class Meta:
        db_table = 'category'

    name = models.CharField(max_length=255, null=True, unique=False)
    description = models.TextField(null=True, blank=True)

class Article(ItemBase):
    class Meta:
        db_table = 'article'
    title = models.CharField(max_length=255, null=True, unique=False)
    view = models.IntegerField(default=0)
    author = models.CharField(max_length=255, null=True, unique=False)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                related_name="article_user")
    fk_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                 related_name="article_category")

class PartArticle(ItemBase):
    class Meta:
        db_table = 'partarticle'
        ordering = ['index']
    index = models.IntegerField(default=0)
    heading = models.CharField(max_length=255, null=True, unique=False)
    content = models.TextField(null=True, blank=True)
    description_photo = models.CharField(max_length=255, null=True, unique=False)
    photo = models.ImageField(upload_to='photos/%Y/%m')
    fk_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True,
                                related_name="partarticle_article")

class Favorite(ItemBase):
    class Meta:
        db_table = 'favorite'

    fk_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True,
                                   related_name="favorite_article")
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                     related_name="favorite_user")

class Comment(ItemBase):
    class Meta:
        db_table = 'comment'

    comment_text = models.TextField(null=True, blank=True)
    fk_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                     related_name="comment_user")
    fk_article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True,
                                 related_name="comment_article")