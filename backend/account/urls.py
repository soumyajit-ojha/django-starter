from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
path('register-user/', RegistrationView.as_view(), name='register'),
    path('signin-user/', LoginView.as_view(), name='login'),
    path('logout-user/', LogoutView.as_view(), name='logout'),
    path('account/<user_id>/', AccountView.as_view(), name='account'),
    path('<int:user_id>/account/', AccountView.as_view(), name='edit_account'),
    path("upload-cropped-image/", UploadCroppedImageView.as_view(), name="crop_image"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)