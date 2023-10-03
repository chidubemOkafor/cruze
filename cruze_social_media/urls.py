from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.signin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forums/', views.forum, name='forums'),
    path('createpost/', views.createpost, name='createpost'),
    path('post/<int:pk>/', views.display_comments, name='display_comments'),
    path('profile/', views.view_profile, name='view_profile')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
