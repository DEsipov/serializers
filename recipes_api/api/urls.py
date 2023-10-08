from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


v1_router = DefaultRouter()
# v1_router.register('recipes', PostViewSet, basename='posts')
# v1_router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )
# v1_router.register('groups', GroupViewSet, basename='groups')
#
urlpatterns = [
    # Надо исправить: Мы обязательно делаем v1_router,
    # к которому будут по v1 подключаться все урлы для v1.
    # Вьюсеты регистрируем именно так,
    # тут тоже любят напридумывать разных странные свариантов
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
