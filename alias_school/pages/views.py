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

    @action(methods=['get'], detail=True)
    def schedule(self, request, pk=None):
        schedule_teacher = (ClassTime.objects
            .filter(group__teacher = pk).order_by('isoweekday')
            .values('id',
                    'isoweekday',
                    'start_time',
                    'end_time',
                    'class_room__name',
                    'group__name',)
        )
        return Response({'schedule': [c for c in schedule_teacher]})

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(methods=['get'], detail=True)
    # Возможность получить по методу detail=True - pk
    # pk - будет использоваться для получения всех групп в которых есть ученики этих классов
    def grades(self, request, pk=None):
        groups = (Group.objects
        .filter(grade__name = pk)
        .select_related('teacher')
        .prefetch_related('grade').values('id',
                                          'name',
                                          'teacher__first_name',
                                          'teacher__last_name',
                                          )
        )
        list_of_grade = []
        for group in groups:
            one_group = Group.objects.get(pk=group['id'])
            group['grade'] = one_group.grade_in()
            class_times = (ClassTime.objects
                           .filter(group = group['id'])
                           .all().values('isoweekday',
                                         'start_time',
                                         'end_time',
                                         'class_room__name',)
            )
            group['classtime'] = {'classtime': [c for c in class_times]}
            list_of_grade.append(group)
        return Response({'groups': [c for c in list_of_grade]})


class ClassTimeViewSet(viewsets.ModelViewSet):
    queryset = ClassTime.objects.all()
    serializer_class = ClassTimeSerializer

    @action(methods=['get'], detail=True)
    def group(self, request, pk=None):  # путь будет classtime/{pk}/название функции в данном случае /group
        class_times = (ClassTime.objects.filter(group = pk)
                       .all().order_by('isoweekday')
                       .values('id',
                                     'isoweekday',
                                     'start_time',
                                     'end_time',
                                     'group_id',
                                     'class_room__name'
                                     ))
        return Response({'classtime': [c for c in class_times]})