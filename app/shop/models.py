from django.db import models


class Item(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.IntegerField()
	currency = models.CharField(max_length=10, default='usd')

	def __str__(self):
		return f"{self.name} ({self.price} {self.currency})"
