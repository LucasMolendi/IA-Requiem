from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.species})"


class PlantReading(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField(auto_now_add=True)

    # Données capteurs
    humidity = models.FloatField()
    air_humidity = models.FloatField()
    temperature = models.FloatField()
    light_level = models.FloatField()

    # Résultat analyse
    health_score = models.FloatField(null=True, blank=True)
    health_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.plant.name} - {self.timestamp}"


class AIAdvice(models.Model):
    reading = models.OneToOneField(PlantReading, on_delete=models.CASCADE)
    advice_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conseil pour {self.reading.plant.name}"