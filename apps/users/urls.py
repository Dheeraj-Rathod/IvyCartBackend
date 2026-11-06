from django.urls import path, include

from apps.users.views import RegisterView, GetUsers, RegisterUserProfileView, GetUserProfile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", GetUsers, basename="users")

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),
    path("", include(router.urls)),
    path("profile/", RegisterUserProfileView.as_view(), name='create_profile'),
    path("profile/me/", GetUserProfile.as_view(), name="get_profile"), #Used '/me' because of using JWT of logged in user to get his profile
]