from rest_framework import viewsets, permissions, generics,status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .forms import UserRegisterForm, AdminRegisterForm, UserUpdateForm
from .models import *
from rest_framework.decorators import action
from .serializers import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

class Pagination(PageNumberPagination):
    page_size = 5

class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = Pagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'hide_user':
            return [permissions.IsAdminUser()]
        if self.action == 'register_user':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=False, url_path='update-user')
    def update_user(self, request):
        user_id = request.data.get('id')
        if not id:
            return Response({'message': 'Không có ID user.'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)

        form = UserUpdateForm(instance=user, data=request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Sửa thành công.'}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='register')
    def register_user(self, request):
        if request.user.is_superuser:
            form = AdminRegisterForm(data=request.POST)
        else:
            form = UserRegisterForm(data=request.POST)

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                response_data = {
                    'error': None,
                    'message': 'Tạo người dùng thành công',
                    'statusCode': status.HTTP_200_OK,
                }
                return Response(data=response_data, status=status.HTTP_200_OK)
            else:
                errors = dict(form.errors)
                response_data = {
                    'error': errors,
                    'message': 'Lỗi khi tạo người dùng',
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=False, url_path='change-password')
    def change_password(self, request):
        user = request.user
        data = request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not user.check_password(old_password):
            return Response({'message': 'Mật khẩu cũ không đúng'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Mật khẩu đã được thay đổi'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True,
            url_path="hide-user",
            url_name="hide-user")
    def hide_user(self, request, pk):
        try:
            u = User.objects.get(pk=pk)
            u.is_active = not u.is_active
            u.save()
        except User.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=UserSerializer(u, context={'request': request}).data, status=status.HTTP_200_OK)

class ArticleViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView,
                    generics.CreateAPIView):
    queryset = Article.objects.filter(is_active = True)
    serializer_class = ArticleSerializer
    pagination_class = Pagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy.',
                'message': 'Không tìm thấy.',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path="hide-article",
            url_name="hide-article")
    def hide_article(self, request, pk):
        try:
            t = Article.objects.get(pk=pk)
            t.is_active = False
            t.save()
        except Article.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=Article(t, context={'request': request}).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            comments = Comment.objects.filter(fk_article=article)
            serializer = CommentSerializer(comments, many=True)
            response_data = {
                'error': None,
                'message': 'Thành công',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            response_data = {
                'error': 'Không tồn tại',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

class CategoryViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView,
                    generics.CreateAPIView):
    queryset = Category.objects.filter(is_active = True)
    serializer_class = CategorySerializer
    pagination_class = Pagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy.',
                'message': 'Không tìm thấy.',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path="hide-category",
            url_name="hide-category")
    def hide_category(self, request, pk):
        try:
            t = Category.objects.get(pk=pk)
            t.is_active = False
            t.save()
        except Category.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=Category(t, context={'request': request}).data, status=status.HTTP_200_OK)

class PartArticleViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView,
                    generics.CreateAPIView):
    queryset = PartArticle.objects.filter(is_active = True)
    serializer_class = PartArticleSerializer
    pagination_class = Pagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except PartArticle.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy.',
                'message': 'Không tìm thấy.',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path="hide-partarticle",
            url_name="hide-partarticle")
    def hide_partarticle(self, request, pk):
        try:
            t = PartArticle.objects.get(pk=pk)
            t.is_active = False
            t.save()
        except PartArticle.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=PartArticle(t, context={'request': request}).data, status=status.HTTP_200_OK)

class FavoriteViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView,
                    generics.CreateAPIView):
    queryset = Favorite.objects.filter(is_active = True)
    serializer_class = FavoriteSerializer
    pagination_class = Pagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Favorite.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy.',
                'message': 'Không tìm thấy.',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path="hide-favorite",
            url_name="hide-favorite")
    def hide_favorite(self, request, pk):
        try:
            t = Favorite.objects.get(pk=pk)
            t.is_active = False
            t.save()
        except Favorite.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=Favorite(t, context={'request': request}).data, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ViewSet,
                  generics.RetrieveAPIView,
                    generics.ListAPIView,
                    generics.CreateAPIView):
    queryset = Comment.objects.filter(is_active = True)
    serializer_class = CommentSerializer
    pagination_class = Pagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = {
                'error': None,
                'message': 'Success',
                'statusCode': status.HTTP_200_OK,
                'results': serializer.data,
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            response_data = {
                'error': 'Không tìm thấy.',
                'message': 'Không tìm thấy.',
                'statusCode': status.HTTP_404_NOT_FOUND,
                'results': None,
            }
            return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True,
            url_path="hide-comment",
            url_name="hide-comment")
    def hide_comment(self, request, pk):
        try:
            t = Comment.objects.get(pk=pk)
            t.is_active = False
            t.save()
        except Comment.DoesNotExits:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=Comment(t, context={'request': request}).data, status=status.HTTP_200_OK)