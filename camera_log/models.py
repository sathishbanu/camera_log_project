from django.db import models

class CameraLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    camera_id = models.CharField(max_length=100)
    status = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField()  # Duration in minutes

    def __str__(self):
        return f"Camera {self.camera_id}: {self.status}"
