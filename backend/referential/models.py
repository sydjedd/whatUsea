from django.db import models


class Quality(models.Model):
    id = models.AutoField(primary_key = True)
    libelle = models.CharField(max_length = 30, null = False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.id + ' ' + self.libelle

class Family(models.Model):
    id = models.AutoField(primary_key = True)
    libelle = models.CharField(max_length = 30, null = False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.id + ' ' + self.libelle

class Species(models.Model):
    id = models.AutoField(primary_key = True)
    libelle = models.CharField(max_length = 30, null = False)
    family = models.ForeignKey(Family, models.DO_NOTHING, null = False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.id + ' ' + self.libelle
