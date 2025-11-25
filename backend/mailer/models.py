from django.conf import settings
from django.db import models

class Mailer(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    context = models.JSONField()
    template = models.URLField()
    sent_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} → {self.email}"
