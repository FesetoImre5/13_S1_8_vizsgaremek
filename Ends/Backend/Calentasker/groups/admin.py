from django.contrib import admin
from .models import Group, GroupMember

class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 1
    readonly_fields = ('joined_at',)

class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupMemberInline]
    list_display = ('groupname', 'created_by_userid', 'created_at', 'active')
    search_fields = ('groupname',)
    readonly_fields = ('created_at',)

admin.site.register(Group, GroupAdmin)
# Optionally register GroupMember separately if needed, but inline is usually better
admin.site.register(GroupMember)
