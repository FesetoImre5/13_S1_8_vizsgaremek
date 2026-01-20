from django.contrib import admin
from .models import Task, Assigned, Attachments, Comment

class AssignedInline(admin.TabularInline):
    model = Assigned
    extra = 1
    readonly_fields = ('assigned_at',)

class AttachmentsInline(admin.TabularInline):
    model = Attachments
    extra = 1
    readonly_fields = ('uploaded_at',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)

class TaskAdmin(admin.ModelAdmin):
    inlines = [AssignedInline, AttachmentsInline, CommentInline]
    list_display = ('title', 'group', 'priority', 'status', 'due_date', 'created_by_userid', 'active')
    list_filter = ('status', 'priority', 'group', 'active')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Task, TaskAdmin)
admin.site.register(Assigned)
admin.site.register(Attachments)
admin.site.register(Comment)
