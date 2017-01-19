from django.db import models

class File(models.Model):
    name = models.CharField(max_length=100, blank=False, default='')
    path = models.CharField(max_length=500, blank=False, default='')
    watched = models.BooleanField(default=False, blank=True)
    directory = models.ForeignKey('Directory', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def lastWatched(self):
        if self.directory.last_watched_file is not None:
            if self.directory.last_watched_file.id == self.id:
                return True
        return False
