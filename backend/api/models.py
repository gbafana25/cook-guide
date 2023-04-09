from django.db import models


KEY_LENGTH = 45

# Create your models here.
class ApiKey(models.Model):
	key = models.CharField(max_length=KEY_LENGTH)
	num_requests = models.IntegerField(default=0, primary_key=False)
	current_search = models.JSONField(null=True, primary_key=False)

	def __str__(self):
		return self.key
