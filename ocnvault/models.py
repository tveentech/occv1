from django.db import models
from django.contrib.auth.models import User


class OnlineSystem(models.Model):
	title = models.CharField(max_length=255, blank=False)
	website = models.URLField(max_length=255, blank=True)
	agent_id = models.CharField(max_length=255, blank=True)
	agent_password = models.CharField(max_length=255, blank=True)
	user_id = models.CharField(max_length=255, blank=True)
	user_password = models.CharField(max_length=255, blank=True)
	product_type = models.CharField(max_length=255, blank=True,
								help_text='Separate multiple products by comma')
	destination = models.CharField(max_length=255, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User,
								related_name='online_system_created_by')
	last_updated_at = models.DateTimeField(auto_now=True)
	last_updated_by = models.ForeignKey(User,
								related_name='online_system_last_updated_by')

	remarks = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.title)

	class Meta:
		unique_together = ['title']


class CreditCard(models.Model):
	CARD_TYPE_CHOICES = (
		('Visa', 'Visa'),
		('Master Card', 'Master Card'),
		('American Express', 'American Express'),
	)

	issuing_bank = models.CharField(max_length=255, blank=False)
	card_type = models.CharField(max_length=50, blank=False,
								 choices=CARD_TYPE_CHOICES)
	card_number = models.CharField(max_length=50, blank=False)
	name_on_card = models.CharField(max_length=50, blank=False)
	nickname = models.CharField(max_length=255, blank=False)

	website = models.URLField(max_length=255, blank=True)
	username = models.CharField(max_length=255, blank=True)
	password = models.CharField(max_length=255, blank=True)
	email = models.EmailField(max_length=255, blank=True)
	phone = models.CharField(max_length=255, blank=True)

	pending_amount = models.DecimalField(max_digits=10,
										 decimal_places=2,
										 default=0,
										 null=True, blank=True)
	current_available_amount = models.DecimalField(max_digits=10,
												   decimal_places=2,
												   default=0,
												   null=True, blank=True)
	actual_available_amount = models.DecimalField(max_digits=10,
												  decimal_places=2,
												  default=0,
												  null=True, blank=True)
	total_limit = models.DecimalField(max_digits=10,
									  decimal_places=2,
									  default=0,
									  null=True, blank=True)

	next_statement_generation_date = models.DateField(blank=True, null=True)
	next_payment_date = models.DateField(blank=True, null=True)
	credit_days_available = models.IntegerField(blank=True, null=True,
												default=0)

	last_updated_at = models.DateTimeField(auto_now=True)
	last_updated_by = models.ForeignKey(User)

	remarks = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.card_number)

	class Meta:
		unique_together = ['card_number']
		ordering = ['-is_active',
					'-credit_days_available',
					'-actual_available_amount']
