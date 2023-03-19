from django.forms import model_to_dict
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import TeacherSerializer, GroupSerializer

from .models import Teacher, Group


class HomePageView(TemplateView):
    template_name = 'pages/index.html'


class TeacherViewSet(viewsets.ModelViewSet):
    """ModelViewSet - CRUD метод, ReadOnlyModelViewSet - чтение"""
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = (IsAuthenticated, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


    @action(methods=['get'], detail=True)
    # Возможность получить по методу detail=True - pk
    # pk - будет использоваться для получения всех групп в которых есть ученики этих классов
    def grade(self, request, pk=None):
        # groups = Group.objects.filter(grade=pk).all().values()
        # return Response({'groups': groups})
        groups = Group.objects.filter(grade=pk).all()
        return Response({'groups': [c.text() for c in groups]})