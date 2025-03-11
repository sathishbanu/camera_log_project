from django.shortcuts import render
from django.http import HttpResponse
from .models import CameraLog
import openpyxl
from io import BytesIO
from datetime import datetime

def log_list(request):
    # Sample list of all available camera names - replace with actual data if available
    all_cameras = CameraLog.objects.values_list('camera_id', flat=True).distinct()  # Unique camera IDs from logs
    
    # Get filter parameters from the request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_cameras = request.GET.getlist('camera_id')  # Get list of selected camera IDs
    status = request.GET.get('status')

    # Filter logs based on parameters
    logs = CameraLog.objects.all()
    
    if start_date:
        logs = logs.filter(timestamp__date__gte=start_date)
    if end_date:
        logs = logs.filter(timestamp__date__lte=end_date)
    if selected_cameras:
        logs = logs.filter(camera_id__in=selected_cameras)  # Filter logs by selected cameras
    if status:
        logs = logs.filter(status=status)

    return render(request, 'camera_log/log_list.html', {
        'logs': logs,
        'start_date': start_date,
        'end_date': end_date,
        'all_cameras': all_cameras,
        'selected_cameras': selected_cameras,
        'status': status
    })

def download_logs(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    camera_id = request.GET.get('camera_id')
    status = request.GET.get('status')

    # Filter logs
    logs = CameraLog.objects.all()

    # Check and apply valid filters
    if start_date and start_date != "None":  # Ensure the value is not None
        logs = logs.filter(timestamp__date__gte=start_date)
    if end_date and end_date != "None":  # Ensure the value is not None
        logs = logs.filter(timestamp__date__lte=end_date)
    if camera_id and camera_id != "None":  # Ensure the value is not None
        logs = logs.filter(camera_id=camera_id)
    if status and status != "None":  # Ensure the value is not None
        logs = logs.filter(status=status)

    # Create Excel file
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Camera Logs"
    ws.append(["Timestamp", "Camera ID", "Status", "Start Time", "End Time", "Duration (mins)"])

    for log in logs:
        ws.append([
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            log.camera_id,
            log.status,
            log.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            log.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            log.duration
        ])

    # Save to in-memory file
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Send the file as a response
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=CameraLogs_{datetime.now().strftime("%Y%m%d")}.xlsx'
    return response
