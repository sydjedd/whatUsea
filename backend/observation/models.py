from django.db import models
from referential import models as referentialModel

class Observation(models.Model):
    id = models.AutoField(primary_key = True)
    ilot = models.CharField(max_length = 32, null = False)
    ilot_distance = models.PositiveIntegerField(null = False)
    date_time = models.DateTimeField(null = False)
    quality = models.ForeignKey(referentialModel.Quality, models.DO_NOTHING, null = False)
    species = models.ForeignKey(referentialModel.Species, models.DO_NOTHING, null = False)
    mammel_apnea_duration = models.PositiveSmallIntegerField(null = True)
    animal_length = models.PositiveSmallIntegerField(null = True)
    fish_single = models.BooleanField(null = True)
    fish_number = models.PositiveSmallIntegerField(null = True)

    class Meta:
        db_table = 'observation'
        ordering = ['id']
