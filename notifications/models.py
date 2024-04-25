from sqlite3 import OperationalError

from django.contrib.auth.models import User
from django.db import models

import thriftpy2
from thriftpy2.rpc import make_client
timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService
from datetime import datetime
from django.contrib import messages



class Notification(models.Model):
    objects = None
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    @staticmethod
    def send_notification(recipient, alert):
        print("THis is receipent", recipient)
        try:
            client = make_client(Timestamp, '127.0.0.1', 9090)
            timestamp = datetime.fromtimestamp(int(str(client.getCurrentTimestamp())))
            notification = Notification.objects.create(recipient=recipient, message=alert, timestamp=timestamp)
            return notification
        except OperationalError:
            print("Transfer operation is not possible now.")

    class Meta:
        ordering = ['-timestamp']
