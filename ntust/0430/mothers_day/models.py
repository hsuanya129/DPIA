from django.db import models
from django.utils import timezone

# Create your models here.
class Cards(models.Model):
	title = models.CharField(max_length =200)
	user_name = models.CharField(max_length=200)
	content = models.TextField(blank=True)
	pub_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title
