import uuid
from django.db import models

class Pet(models.Model):
    pet_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    pet_type = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    age = models.TextField()
    name = models.CharField(max_length=100)
    owner_id = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pet_id:
            prefix = self.pet_type.upper()[:3]
            unique_number = str(uuid.uuid4().int)[:5]
            self.pet_id = f"{prefix}{unique_number}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Pets"

    def __str__(self):
        return f"{self.name} ({self.pet_id})"


class PetData(models.Model):
    pet_id = models.CharField(max_length=255, blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    sleep_hours = models.FloatField(blank=True, null=True)
    miles_travelled = models.FloatField(blank=True, null=True)
    calories_burned = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pet_data'