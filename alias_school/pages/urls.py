from django.urls import include, path, re_path
from .views import ClassTimeViewSet, HomePageView, TeacherViewSet, GroupViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'teacher', TeacherViewSet)
router.register(r'group', GroupViewSet)
router.register(r'classtime', ClassTimeViewSet)
print(router.urls)


urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('api/v1/', include(router.urls)),  # http://127.0.0.1:8000/api/v1/teacher/

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    
]
