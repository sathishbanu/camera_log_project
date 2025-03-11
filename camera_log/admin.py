from django.contrib import admin
from .models import CameraLog

# Customizing the admin interface for CameraLog
class CameraLogAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('timestamp', 'camera_id', 'status', 'start_time', 'end_time', 'duration')
    # Enable filtering options in the admin interface
    list_filter = ('camera_id', 'status', 'timestamp')
    # Add a search box for specified fields
    search_fields = ('camera_id', 'status')
    # Specify the fields to display in the detail/edit view
    fields = ('timestamp', 'camera_id', 'status', 'start_time', 'end_time', 'duration')
    # Make some fields read-only
    readonly_fields = ('duration',)

# Registering the CameraLog model with the admin site
admin.site.register(CameraLog, CameraLogAdmin)
