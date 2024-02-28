from django.db import models

# Create your models here.
class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=20)

class RequestLog(models.Model):
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.url} - {self.timestamp}"