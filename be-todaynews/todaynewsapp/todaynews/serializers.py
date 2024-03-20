from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class UserSerializer(ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password' : {'write_only':'true'}
        }

    def validate(self, data):
        if 'password' not in data or 'username' not in data or data['password'] == '' or data['username'] == '':
            raise serializers.ValidationError("Mật khẩu không được để trống")

        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email đã tồn tại trong hệ thống")

        username = data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Tên người dùng đã tồn tại trong hệ thống")
        return data

    def get_avatar(self, user):
        if user.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % user.avatar.name)

            return '/static/%s' % user.avatar.name

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PartArticleSerializer(ModelSerializer):
    class Meta:
        model = PartArticle
        fields = '__all__'

class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'