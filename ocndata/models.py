import datetime
from django.db import models
from django.contrib.auth.models import User


class AccountHead(models.Model):
	RELATION_CATEGORIES = (
		('C', 'Client'),
		('V', 'Vendor'),
	)

	name = models.CharField(max_length=255, blank=False)
	relation_category = models.CharField(verbose_name='Account Type',
										 max_length=1,
										 choices=RELATION_CATEGORIES,
										 default='C')

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)

	is_active = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.name)

	class Meta:
		unique_together = ['name', 'relation_category']
		ordering = ['name']


class CommonAccountType(models.Model):
	account_head = models.ForeignKey('AccountHead')
	reference = models.CharField(max_length=255, blank=True)
	last_name = models.CharField(max_length=255, blank=True)
	phone1 = models.CharField(max_length=255, blank=True)
	phone2 = models.CharField(max_length=255, blank=True)
	email1 = models.CharField(max_length=255, blank=True)
	email2 = models.CharField(max_length=255, blank=True)
	address1 = models.CharField(max_length=255, blank=True)
	address2 = models.CharField(max_length=255, blank=True)
	remarks = models.TextField(blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)

	is_active = models.BooleanField(default=True)

	class Meta:
		abstract = True


class Client(CommonAccountType):
	first_name = models.CharField(max_length=255, blank=False)
	company_name = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return u'%s (%s)' % (self.account_head, self.first_name)

	class Meta:
		unique_together = ['account_head', 'first_name']
		ordering = ['account_head']


class Vendor(CommonAccountType):
	first_name = models.CharField(max_length=255, blank=True)
	company_name = models.CharField(max_length=255, blank=False)

	def __unicode__(self):
		return u'%s (%s)' % (self.account_head, self.company_name)

	class Meta:
		unique_together = ['account_head', 'company_name']
		ordering = ['account_head']


DESTINATION_TYPE_CHOICES = (
	('D', 'Domestic'),
	('I', 'International'),
)

MEAL_PLAN_CHOICES = (
	('EP', 'Room Only'),
	('CP', 'Room + Breakfast'),
	('MAP', 'Room + Breakfast + Dinner'),
	('AP', 'Room + All Meals'),
	('DU', 'Day Use'),
	('AU', 'All Inclusive'),
	('OTH', 'Others'),
)

PAYMENT_MODE_CHOICES = (
	('CREDIT', 'Credit'),
	('CCVBICICIVisa', 'Credit Card VB ICICI Visa (5002)'),
	('CCVBICICIAmex', 'Credit Card VB ICICI Amex (83004)'),
	('CCVBHDFC', 'Credit Card VB HDFC (9197)'),
	('CCVBINDUSIND', 'Credit Card VB IndusInd AMEX (10005)'),
	('CCVB/AKBAMEX', 'Credit Card VB/AKB AMEX (22019)'),
	('CCVBAMEXJET', 'Credit Card VB AMEX JET (51008)'),
	#('CCVBAMEXRES', 'Credit Card VB AMEX RESERVE (52006)'),
	('CCGSHDFCJET', 'Credit Card GS HDFC JET (9643)'),
	('CCVBAMEXCHRG', 'Credit Card VB/AKB AMEX CHARGE (41018)'),
	('CCAKBAMEXJET', 'Credit Card AKB AMEX JET (31000)'),
	('CCAKBHDFCJET', 'Credit Card AKB HDFC JET (2076)'),
	('CCAKBICICIAMXJT', 'Credit Card AKB ICICI AMEX JET (35007)'),
	('CCAB/SBAMEX', 'Credit Card AB/SB AMEX (02018)'),
	('CCAB/SBAMEXJET', 'Credit Card AB/SB AMEX JET (61010)'),
	('CCABAMEX', 'Credit Card AB AMEX (21004)'),
	('CCABAMEXJET', 'Credit Card AB AMEX JET (91008)'),
	('CCABSBI', 'Credit Card AB SBI (9295)'),
	('CCABHDFC', 'Credit Card AB HDFC (3748)'),
	('CCABICICIAmex', 'Credit Card AB ICICI Amex (00008)'),
	('CCABSTANCHART', 'Credit Card AB StanChart (5244)'),
	('CCABINDUSIND', 'Credit Card AB/AKB IndusInd (8207)'),
	('CCSBSBI', 'Credit Card SB SBI (6497)'),
	('CCSBJETHDFC', 'Credit Card SB JET HDFC (7682)'), 
	('NEFTOTHDFC', 'NEFT Oceana HDFC'),
	('NEFTOTICICI', 'NEFT Oceana ICICI'),
	('NEFTOTINDIAN', 'NEFT Oceana Indian Bank'),
	('CASH', 'Cash'),
	('REMITTANCE', 'Remittance'),
	('CHEQUE', 'Cheque'),
	('DD', 'Demand Draft'),
	('NBOTHDFC', 'Net Banking Oceana HDFC'),
	('NBOTICICI', 'Net Banking Oceana ICICI'),
	('NBOTINDIAN', 'Net Banking Oceana Indian Bank'),
	('OTH', 'Others'),
	('CCVBAMEXCHRG', 'Credit Card VB AMEX CHARGE CARD (41018)'),
	('CCSONAMHDFCJET', 'Credit Card AKB SONAM HDFC JET (8539)'),
)


class CommonDocket(models.Model):
	booking_date = models.DateField(blank=False)
	booking_reference = models.CharField(max_length=255, blank=True)
	account_head = models.ForeignKey('Client')
	guest_name = models.TextField(blank=False)
	no_of_guests = models.IntegerField(blank=False, default=1)
	vendor = models.ForeignKey('Vendor')
	payment_mode = models.CharField(max_length=15,
									choices=PAYMENT_MODE_CHOICES)
	purchase = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
	sale = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
	profit = models.DecimalField(max_digits=10, decimal_places=2, null=True,
								 blank=True)
	invoice_no = models.IntegerField(null=True, blank=True)
	purchase_invoice_no = models.CharField(max_length=255, blank=True)
	invoice_dispatch_date = models.DateField(null=True, blank=True)
	remarks = models.TextField(blank=True)
	tally_narration = models.TextField(blank=True)
	log = models.TextField(blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)

	is_void = models.BooleanField(default=False)
	is_submit_to_accounts = models.BooleanField(verbose_name=
												'Submit to Accounts',
												default=False)
	is_purchase_received = models.BooleanField(verbose_name=
											   'Purchase Received',
											   default=False)
	is_invoice_created = models.BooleanField(verbose_name=
											 'Invoice Created',
											 default=False)
	is_tally_entered = models.BooleanField(verbose_name=
										   'Entered in Tally',
										   default=False)

	class Meta:
		abstract = True
		ordering = ['-booking_date']


class AirTicketDocket(CommonDocket):
	airlines = models.CharField(max_length=255, blank=True)
	sector = models.CharField(max_length=255, blank=False)
	destination_country = models.CharField(max_length=255, blank=True)
	destination_type = models.CharField(max_length=1,
										choices=DESTINATION_TYPE_CHOICES,
										blank=True)
	start_date = models.DateField(null=True, blank=True)
	return_date = models.DateField(null=True, blank=True)
	basic_fare = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
	pnr = models.CharField(max_length=255, blank=False)

	def __unicode__(self):
		return u'(%d) %s | %s | %s | %s | %s' % (self.id, self.account_head,
												 self.guest_name, self.sector,
												 self.start_date,
												 self.return_date)
	

class HotelDocket(CommonDocket):
	hotel = models.CharField(max_length=255, blank=False)
	destination_city = models.CharField(max_length=255, blank=False)
	destination_country = models.CharField(max_length=255, blank=True)
	destination_type = models.CharField(max_length=1,
										choices=DESTINATION_TYPE_CHOICES,
										blank=True)
	check_in = models.DateField(blank=False)
	check_out = models.DateField(blank=False)
	duration = models.IntegerField(null=True, blank=True)
	meal_plan = models.CharField(max_length=3,
								 choices=MEAL_PLAN_CHOICES,
								 default='CP')
	hotel_confirmation_no = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return u'%s, %s' % (self.account_head, self.hotel)


class PackageDocket(CommonDocket):
	hotel = models.CharField(max_length=255, blank=False)
	destination_city = models.CharField(max_length=255, blank=False)
	destination_country = models.CharField(max_length=255, blank=True)
	destination_type = models.CharField(max_length=1,
										choices=DESTINATION_TYPE_CHOICES,
										blank=True)
	check_in = models.DateField(blank=False)
	check_out = models.DateField(blank=False)
	duration = models.IntegerField(null=True, blank=True)
	meal_plan = models.CharField(max_length=3,
								 choices=MEAL_PLAN_CHOICES,
								 default='CP')
	package_inclusions = models.CharField(max_length=255, blank=False)
	package_confirmation_no = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return u'%s, %s' % (self.account_head, self.hotel)


class VisaDocket(CommonDocket):
	VISA_TYPE_CHOICES = (
		('T', 'Tourist'),
		('TT', 'Tourist Tatkal'),
		('TR', 'Transit'),
		('B', 'Business'),
		('BT', 'Business Tatkal'),
	)

	destination_country = models.CharField(max_length=255, blank=False)
	visa_type = models.CharField(max_length=2,
								 choices=VISA_TYPE_CHOICES,
								 default='T')

	def __unicode__(self):
		return u'%s, %s' % (self.account_head, self.destination_country)


class TravelInsuranceDocket(CommonDocket):
	INSURANCE_PROVIDER_CHOICES = (
		('BJ', 'Bajaj Allianz'),
		('AIG', 'Tata AIG'),
		('LOM', 'ICICI Lombard'),
		('OTH', 'Others'),
	)
	insurance_provider = models.CharField(max_length=3,
										  choices=INSURANCE_PROVIDER_CHOICES)
	insurance_plan = models.CharField(max_length=30, blank=False)
	destination_country = models.CharField(max_length=255, blank=False)
	policy_no = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return u'%s, %s' % (self.account_head, self.destination_country)


class CreditNoteDocket(models.Model):
	CREDIT_NOTE_TYPE_CHOICES = (
		('T', 'Air Ticket'),
		('H', 'Hotel'),
		('P', 'Package'),
		('V', 'Visa'),
		('I', 'Travel Insurance'),
	)

	booking_date = models.DateField(blank=False)
	credit_note_type = models.CharField(max_length=1,
										choices=CREDIT_NOTE_TYPE_CHOICES,
										default='T',
										blank=False)
	old_docket_no = models.IntegerField(blank=False)
	new_purchase = models.DecimalField(max_digits=10, decimal_places=2,
									   blank=False)
	new_sale = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
	new_profit = models.DecimalField(max_digits=10, decimal_places=2,
									 null=True, blank=True)
	new_payment_mode = models.CharField(max_length=15,
										choices=PAYMENT_MODE_CHOICES,
										blank=True)

	invoice_no = models.IntegerField(null=True, blank=True)
	purchase_invoice_no = models.CharField(max_length=255, blank=True)
	invoice_dispatch_date = models.DateField(blank=True, null=True)
	remarks = models.TextField(blank=True)
	tally_narration = models.TextField(blank=True)
	log = models.TextField(blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User)

	is_void = models.BooleanField(default=False)
	is_submit_to_accounts = models.BooleanField(verbose_name=
												'Submit to Accounts',
												default=False)
	is_purchase_received = models.BooleanField(verbose_name=
											   'Purchase Received',
											   default=False)
	is_invoice_created = models.BooleanField(verbose_name=
											 'Invoice Created',
											 default=False)
	is_tally_entered = models.BooleanField(verbose_name=
										   'Entered in Tally',
										   default=False)
	def __unicode__(self):
		return u'%s (%s)' % (self.credit_note_type, self.old_docket_no)
