from django.db import models
from django.contrib.auth.models import User


class PaymentReminder(models.Model):
	item_title = models.CharField(max_length=255, blank=False)
	payment_due_date = models.DateField(blank=False, help_text='YYYY-MM-DD')
	currency_type = models.CharField(max_length=255, blank=False,
									 help_text='INR, USD, EUR, AUD, SGD, etc')
	amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False,
								 help_text='12345.78')
	payment_owner = models.ForeignKey(User, related_name='payment_owner')
	remarks = models.TextField(blank=True)

	payment_date = models.DateField(null=True, blank=True,
									help_text='YYYY-MM-DD')
	is_paid = models.BooleanField(default=False)
	is_void = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='created_by')

	def __unicode__(self):
		return u'To pay "%s %s" for "%s" by "%s"' % (self.currency_type,
													 self.amount,
													 self.item_title,
													 self.payment_due_date)

	class Meta:
		ordering = ['is_void', 'is_paid', 'payment_due_date',]
