from django.contrib import admin

from .models import GroupGrade, User, ClassTime, ClassRoom, Grade, Group, Teacher


class GroupGradeInline(admin.TabularInline):
    model = GroupGrade
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    inlines = (GroupGradeInline,)
    list_display = ('name', 'quota', 'sublease', 'teacher', 'grade_in')


class GradeAdmin(admin.ModelAdmin):
    inlines = (GroupGradeInline,)


class ClassTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'isoweekday', 'start_time', 'end_time', 'group', 'class_room',)
    search_fields = ('group', 'class_room',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'town', 'description',)
    search_fields = ('first_name', 'last_name',)


admin.site.register(User)
admin.site.register(ClassTime, ClassTimeAdmin)
admin.site.register(ClassRoom)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupGrade)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Teacher, TeacherAdmin)

# class GroupInline(admin.TabularInline):
#     model = Group.grade.through

# @admin.register(Grade)
# class GradeAdmin(admin.ModelAdmin):
#     model = Grade
#     inlines = [
#         GroupInline,
#     ]



