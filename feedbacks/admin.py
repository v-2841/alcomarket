from django.contrib import admin

from feedbacks.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'name', 'email', 'is_processed')
    ordering = ('is_processed', '-created_at')
    date_hierarchy = 'created_at'


admin.site.register(Feedback, FeedbackAdmin)
