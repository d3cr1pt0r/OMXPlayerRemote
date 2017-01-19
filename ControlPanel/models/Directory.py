from django.db import models

class Directory(models.Model):
    name = models.CharField(max_length=100)
    last_watched_file = models.ForeignKey('File', blank=True, null=True, on_delete=models.SET_NULL, related_name='last_watched_file')
