from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from groups.models import GroupMember

class GroupMemberInline(admin.TabularInline):
    model = GroupMember
    extra = 1
    readonly_fields = ('joined_at',)

class CustomUserAdmin(UserAdmin):
    model = User
    # Display fields in the list view
    list_display = UserAdmin.list_display + ('profile_picture',)
    
    # Restoring standard fieldsets (which includes 'groups' and 'user_permissions')
    # and appending our custom field
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('profile_picture',)}),
    )
    
    # Add custom fields to the creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture',)}),
    )
    
    # date_joined is auto_now_add=True in our model, so it's non-editable.
    readonly_fields = UserAdmin.readonly_fields + ('date_joined',)
    
    # Allow editing application groups (GroupMember) inline
    inlines = [GroupMemberInline]

admin.site.register(User, CustomUserAdmin)
