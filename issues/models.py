from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    CATEGORY_CHOICES = [
        ('light', 'Broken Streetlight'),
        ('garbage', 'Garbage'),
        ('road', 'Road Damage'),
        ('water', 'Water Supply'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=255)
    progress_notes = models.TextField(blank=True, null=True)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    email=models.EmailField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.title


class EmailLog(models.Model):
    issue = models.ForeignKey("Issue", on_delete=models.CASCADE, related_name="email_logs")
    sent_to = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.sent_to} about {self.issue.title} on {self.sent_at}"