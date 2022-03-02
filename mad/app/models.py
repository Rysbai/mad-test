from django.db import models


class Diagnose(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Patient(models.Model):
    date_of_birth = models.DateField()
    diagnoses = models.ManyToManyField(Diagnose)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_of_birth)

    class Meta:
        ordering = ("-created_at",)
