from django.db import models

# Create your models here.
class PageAdmin(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{'x' if self.is_active else ' '}] {str(self.email)} - {self.name}"
