import datetime
from django.db import models


class Teacher(models.Model):
    """Учителя +++++ добавить фото пользователя"""
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=25, verbose_name='Фамилия')
    email = models.EmailField(blank=True, null=True, verbose_name='Почта')
    town = models.CharField(max_length=100, verbose_name='Город')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return '{} {} {}'.format(self.pk, self.first_name, self.last_name)


class Grade(models.Model):
    """Класс в котором учатся ученики,
    0 - дошкольник, 12 - студент, 13 - взрослый"""
    name = models.SmallIntegerField()

    def __str__(self) -> str:
        return f'{self.name}'


class Group(models.Model):
    """Группы с кол-вом учеников, вариантом оплаты занятия"""

    name = models.CharField(max_length=100)
    quota = models.IntegerField()
    sublease = models.BooleanField(default=False)  # Субаренда
    price = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    is_online = models.BooleanField(default=False)  # False - офлайн

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель')
    grade = models.ManyToManyField(Grade, related_name='group_grade', through='GroupGrade')

    def __str__(self):
        return f'{self.name} учитель: {self.teacher.first_name} {self.teacher.last_name} класс(ы): {self.grade_in()}'
    
    def grade_in(self):
        """Получаем текстом список классов который учатся в этой группе (0 1 2)"""
        grades = GroupGrade.objects.filter(group=self.pk).all().values('grade__name').order_by('grade__name')
        grade_list = ''
        for grade in grades:
            grade_list += f"{str(grade['grade__name'])} "
        return grade_list.strip()
    
    def text(self):
        group_text = f'{self.pk}. {self.name} ({self.grade_in()})'
        group_text += f'\n{self.teacher.first_name} {self.teacher.last_name}'
        return group_text


class GroupGrade(models.Model):
    """Отношения многие ко многим группы и класс ученика который учатся в этих группах"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name='Класс')

    def __str__(self):
        return f'{self.group.name} - класс: {self.grade.name}'


class User(models.Model):
    """Ученики"""
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=25, verbose_name='Фамилия')
    town = models.CharField(max_length=100, verbose_name='Город')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='группа')


class ClassRoom(models.Model):
    """Кабинет может быть онлайн"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name


class ClassTime(models.Model):
    """Время занятий, занятия могут идти одна за одной"""
    isoweekday = models.SmallIntegerField()  # день недели 1-пн, 7-вс
    start_time = models.TimeField()
    end_time = models.TimeField()

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
        