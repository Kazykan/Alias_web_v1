from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import Teacher, Group


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'