from django.db import models
from ocndata.models import Client


class PrivilegeProgram(models.Model):
	title = models.CharField(max_length=255)
	remarks = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.title)

	class Meta:
		unique_together = ['title']


class PrivilegeAccount(models.Model):
	number = models.CharField(max_length=255)
	tier = models.CharField(max_length=255, blank=True)

	points = models.IntegerField(null=True, blank=True)
	last_updated_at = models.DateField()

	website = models.URLField(max_length=255, blank=True)
	username = models.CharField(max_length=255, blank=True)
	password = models.CharField(max_length=255, blank=True)
	email = models.EmailField(max_length=255, blank=True)
	phone = models.CharField(max_length=255, blank=True)
	dob = models.DateField(null=True, blank=True)

	remarks = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	guest = models.ForeignKey(Client)
	program_type = models.ForeignKey(PrivilegeProgram)


	def __unicode__(self):
		return u'%s' % (self.guest)

	class Meta:
		unique_together = ['guest', 'number']
