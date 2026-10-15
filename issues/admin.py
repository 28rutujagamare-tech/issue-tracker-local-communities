from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'location', 'created_by', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'created_by')

    # Automatically set created_by to the logged-in user
    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
