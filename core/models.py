from django.db import models

# Create your models here.
class Pokemon(models.Model):
    id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    name = models.CharField(max_length=100)
    types = models.CharField(max_length=3000, null=True, blank=True)
    evolvesTo = models.CharField(max_length=3000, null=True, blank=True)
    evolvesFrom = models.CharField(max_length=3000, null=True, blank=True)
    baseUrl = models.CharField(max_length=3000, null=True, blank=True)
    listimg = models.CharField(max_length=3000, null=True, blank=True)
    detimg = models.CharField(max_length=3000, null=True, blank=True)
    flavor = models.CharField(max_length=3000, null=True, blank=True)
    strongAgainst = models.CharField(max_length=3000, null=True, blank=True)
    weakAgainst = models.CharField(max_length=3000, null=True, blank=True)
    noDamageTo = models.CharField(max_length=3000, null=True, blank=True)
    noDamageFrom = models.CharField(max_length=3000, null=True, blank=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.nombre