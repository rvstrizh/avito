from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken import views

from users.views import UserView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDeleteView.as_view()),
    path('login/', views.obtain_auth_token), # авторизация логина(получение токина через json логин пароль
    # теперь что бы был доступ нужно прописать токет в постмане
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view())
]

