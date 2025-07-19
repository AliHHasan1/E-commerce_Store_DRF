from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

