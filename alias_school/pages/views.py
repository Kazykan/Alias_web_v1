import pprint
from django.forms import model_to_dict
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import ClassTimeSerializer, TeacherSerializer, GroupSerializer

from .models import ClassTime, Teacher, Group


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
    def grades(self, request, pk=None):
        groups = Group.objects.filter(grade__name = pk).all().values('id', 'name', 'teacher__first_name', 'teacher__last_name')
        list_of_grade = []
        for group in groups:
            temp_group = group
            # temp_group['teacher_first_name'] = Teacher.objects.get(pk = group['teacher_id']).first_name
            # temp_group['teacher_last_name'] = Teacher.objects.get(pk = group['teacher_id']).last_name
            # grade_list = Group.objects.filter(
            # temp_group['grade'] = ' '.join([str(onegrade) for onegrade in group['grade']])
            one_group = Group.objects.get(pk=group['id'])
            temp_group['grade'] = one_group.grade_in()
            list_of_grade.append(group)
        return Response({'groups': [c for c in list_of_grade]})
        # return Response({'groups': [c for c in groups]})
        # groups = Group.objects.filter(grade=pk).all()
        # return Response({'groups': [c.text() for c in groups]})


class ClassTimeViewSet(viewsets.ModelViewSet):
    queryset = ClassTime.objects.all()
    serializer_class = ClassTimeSerializer

    @action(methods=['get'], detail=True)
    def group(self, request, pk=None):
        class_times = ClassTime.objects.filter(group = pk).all().values('id', 'isoweekday', 'start_time', 'end_time', 'group_id', 'class_room__name')
        return Response({'classtime': [c for c in class_times]})