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

admin.site.register(User)
admin.site.register(ClassTime)
admin.site.register(ClassRoom)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupGrade)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Teacher)

# class GroupInline(admin.TabularInline):
#     model = Group.grade.through

# @admin.register(Grade)
# class GradeAdmin(admin.ModelAdmin):
#     model = Grade
#     inlines = [
#         GroupInline,
#     ]



