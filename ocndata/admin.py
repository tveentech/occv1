from django.contrib.messages import constants as messages
from django.contrib import admin
from datetime import date
from models import *
from forms import *


class AccountHeadAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'relation_category',)
	list_filter = ('is_active', 'relation_category', 'created_by',)
	search_fields = ['name']
	exclude = ('created_by',)

	def save_model(self, request, obj, form, change):
		if obj.pk is None:
			obj.created_by = request.user
		obj.save()

admin.site.register(AccountHead, AccountHeadAdmin)


class ClientAdmin(admin.ModelAdmin):
	list_display = ('account_head', 'first_name', 'last_name',
					'phone1', 'email1',)
	list_filter = ('is_active', 'created_by',)
	search_fields = ['account_head__name', 'first_name', 'last_name',
					 'company_name']
	save_on_top = True

	fieldsets = (
		('Client Info', {
			'fields': ('account_head', 'reference',
					   ('first_name', 'last_name'),
					   'company_name',)
		}),
		('Contact Details', {
			'fields': (('phone1', 'phone2'),
					   ('email1', 'email2'),
					   ('address1', 'address2'),
					   'remarks', 'is_active',)
		}),
	)

	def formfield_for_foreignkey(self, account_head, request, **kwargs):
		kwargs['queryset'] = AccountHead.objects.filter(relation_category='C')
		return super(ClientAdmin, self).formfield_for_foreignkey(account_head,
																 request,
																 **kwargs) 

	def save_model(self, request, obj, form, change):
		if obj.pk is None:
			obj.created_by = request.user
		obj.save()

admin.site.register(Client, ClientAdmin)


class VendorAdmin(admin.ModelAdmin):
	list_display = ('account_head', 'company_name', 'first_name',
					'phone1', 'email1',)
	list_filter = ('is_active', 'created_by',)
	search_fields = ['account_head__name', 'first_name', 'last_name',
					 'company_name']
	save_on_top = True

	fieldsets = (
		('Vendor Info', {
			'classes': ('wide', 'extrapretty',),
			'fields': ('account_head', 'reference', 'company_name',)
		}),
		('Contact Details', {
			'fields': (
				('first_name', 'last_name'),
				('phone1', 'phone2'),
				('email1', 'email2'),
				('address1', 'address2'),
				'remarks', 'is_active',)
		}),
	)

	def formfield_for_foreignkey(self, account_head, request, **kwargs):
		kwargs['queryset'] = AccountHead.objects.filter(relation_category='V')
		return super(VendorAdmin, self).formfield_for_foreignkey(account_head,
																 request,
																 **kwargs)

	def save_model(self, request, obj, form, change):
		if obj.pk is None:
			obj.created_by = request.user
		obj.save()

admin.site.register(Vendor, VendorAdmin)


def submit_to_accounts(self, request, queryset):
	if queryset.filter(is_submit_to_accounts=True):
		message_bit = 'FAILED: One or more of the selected dockets have \
already been submitted to accounts. Kindly review the selection and try \
submitting again.'
		self.message_user(request,'%s' % message_bit, level=messages.ERROR)
	else:
		rows_updated = queryset.update(is_submit_to_accounts=True)
		if rows_updated == 1:
			message_bit = 'SUCCESS: 1 Docket was submitted to Accounts'
		else:
			message_bit = 'SUCCESS: %s Dockets were submitted to \
Accounts' % rows_updated
		self.message_user(request,'%s' % message_bit)
submit_to_accounts.short_description = 'Submit selected dockets to Accounts'


def return_to_operations(self, request, queryset):
	if queryset.filter(is_submit_to_accounts=False):
		message_bit = 'FAILED: One or more of the selected dockets have \
already been returned to operations. Kindly review the selection and try \
returning again.'
		self.message_user(request,'%s' % message_bit, level=messages.ERROR)
	else:
		rows_updated = queryset.update(is_submit_to_accounts=False)
		if rows_updated == 1:
			message_bit = 'SUCCESS: 1 Docket was returned to Operations'
		else:
			message_bit = 'SUCCESS: %s Dockets were returned to \
Operations' % rows_updated
		self.message_user(request,'%s' % message_bit)
return_to_operations.short_description = 'Return selected dockets to Operations'


def mark_void(self, request, queryset):
	if queryset.filter(is_void=True):
		message_bit = 'FAILED: Item has already been marked as \
void. Kindly review the selection and try again.'
		self.message_user(request,'%s' % message_bit, level=messages.ERROR)
	else:
		rows_updated = queryset.update(is_void=True)
		if rows_updated == 1:
			message_bit = 'SUCCESS: 1 Item marked as Void'
		else:
			message_bit = 'SUCCESS: %s Items were marked as Void' % rows_updated
		self.message_user(request,'%s' % message_bit)
mark_void.short_description = 'Mark as Void'

def remove_void(self, request, queryset):
	rows_updated = queryset.update(is_void=False)
	if rows_updated == 1:
		message_bit = 'SUCCESS: 1 Docket Removed marked as Void'
	else:
		message_bit = 'SUCCESS: %s Dockets were Removed marked as Void\
' % rows_updated

	self.message_user(request,'%s' % message_bit)
remove_void.short_description = 'Remove Marked as Void'


class AirTicketDocketAdmin(admin.ModelAdmin):
	form = AirTicketDocketAdminForm
	search_fields = ['id', 'booking_reference', 'account_head__first_name',
					 'guest_name', 'vendor__company_name',
					 'purchase', 'sale', 'basic_fare',
					 'invoice_no', 'purchase_invoice_no',
					 'airlines', 'sector', 'destination_country',
					 'pnr',]
	save_on_top = True

	actions = [submit_to_accounts, return_to_operations, mark_void,remove_void]

	list_display = ('id', 'void_flag_based_booking_date', 'guest_name',
					'sector', 'pnr', 'start_date', 'return_date',
					'invoice_no', 'purchase', 'sale',
					'vendor_shortened', 'payment_mode',
					'is_submit_to_accounts',)

	_list_filter_operations = ('created_at', 'is_submit_to_accounts',
							   'is_void', 'vendor',)
	_list_filter_accounts = ('created_at', 'is_invoice_created',
							 'is_tally_entered', 'is_purchase_received',
							 'is_void', 'created_by', 'payment_mode', 'vendor',)
	_list_filter_admin = ('is_tally_entered', 'is_purchase_received',
						  'is_submit_to_accounts', 'is_invoice_created',
						  'is_void', 'invoice_dispatch_date',
						  'payment_mode',
						  'created_at', 'created_by', 'vendor',)

	def vendor_shortened(self, obj):
		result = obj.vendor.account_head.name[:10]
		return result
	vendor_shortened.allow_tags = True
	vendor_shortened.short_description = 'Vendor'


	def void_flag_based_booking_date(self, obj):
		result = obj.booking_date
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result.strftime('%b %d, %Y')
		return result
	void_flag_based_booking_date.allow_tags = True
	void_flag_based_booking_date.short_description = 'Date'

	def changelist_view(self, request, extra_context=None):
		# set list filter based on current user status
		if request.user.is_superuser:
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='SUPPORT').count():
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='OPERATIONS').count():
			self.list_filter = self._list_filter_operations
		elif request.user.groups.filter(name='ACCOUNTS').count():
			self.list_filter = self._list_filter_accounts

		# set Default filters as per current user status

		# set is_submit_to_accounts, is_void to No in case Operations
		if request.user.groups.filter(name='OPERATIONS').count():
			if not request.GET.has_key('is_submit_to_accounts__exact'):
				q = request.GET.copy()
				q['is_submit_to_accounts__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('created_by__id__exact'):
				q = request.GET.copy()
				q['created_by__id__exact'] = '%d' % User.objects.get(username=request.user).id
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		# set is_void to No in case Accounts
		"""
		if request.user.groups.filter(name='ACCOUNTS').count():
			if not request.GET.has_key('is_invoice_created__exact'):
				q = request.GET.copy()
				q['is_invoice_created__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
		"""

		return super(AirTicketDocketAdmin, self).changelist_view(request,
															 extra_context)

	"""
	def get_readonly_fields(self, request, obj=None):
		try:
			if not request.user.is_superuser and not request.user.groups.filter(name='SUPPORT'):
				if obj:
					list_of_fields = obj._meta.get_all_field_names()
					if obj.is_void:
						pass
					return list_of_fields
					if obj.is_submit_to_accounts:
						list_of_fields.remove('is_purchase_received')
						list_of_fields.remove('invoice_no')
						list_of_fields.remove('remarks')

						return list_of_fields
				else:
					return []
			else:
				return []
		except Exception, e:
			print e
	"""

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser or \
		   request.user.groups.filter(name='ACCOUNTS') or \
		   request.user.groups.filter(name='SUPPORT'):
			self.fieldsets = (
				('Accounts Area', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('invoice_no', 'invoice_dispatch_date'),
							   ('is_purchase_received', 'purchase_invoice_no'),
							   ('is_tally_entered', 'tally_narration'),)
				}),
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('sector', 'pnr'),
							   'airlines',
							   ('guest_name', 'no_of_guests'),
							   ('start_date', 'return_date'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('basic_fare', 'purchase', 'sale'),
								'payment_mode',)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)
		elif request.user.groups.filter(name='OPERATIONS'):
			self.fieldsets = (
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('sector', 'pnr'),
							   'airlines',
							   ('guest_name', 'no_of_guests'),
							   ('start_date', 'return_date'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('basic_fare', 'purchase', 'sale'),
								'payment_mode',)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)

		return super(AirTicketDocketAdmin, self).get_form(request,
													  obj=None,
													  **kwargs)

	def queryset(self, request):
		qs = super(AirTicketDocketAdmin, self).queryset(request)

		# show dockets which have been submitted to accounts
		if request.user.groups.filter(name='ACCOUNTS').count():
			return qs.filter(is_submit_to_accounts=True)
		else:
			return qs

	def get_actions(self, request):
		actions = super(AirTicketDocketAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		# remove SUBMIT TO ACCOUNTS, REMOVE VOID action for User in
		# Accounts Group
		if request.user.groups.filter(name='ACCOUNTS').count():
			del actions['submit_to_accounts']
			del actions['remove_void']

		# remove RETURN TO OPERATIONS, REMOVE VOID action
		# for User in Operations Group
		if request.user.groups.filter(name='OPERATIONS').count():
			del actions['return_to_operations']
			del actions['remove_void']

		return actions

	def save_model(self, request, obj, form, change):
		try:
			# calculate profit while saving
			obj.profit = obj.sale - obj.purchase

			# calculate duration of stay while saving
			#obj.duration = abs((obj.check_out - obj.check_in).days)

			# mark is_invoice_created as True when Invoice No is entered
			if obj.invoice_no:
				obj.is_invoice_created = True
			else:
				obj.is_invoice_created = False

			# assign current user as author while saving for first time
			if obj.pk is None:
				obj.created_by = request.user

			obj.save()
		except Exception, e:
			print e

admin.site.register(AirTicketDocket, AirTicketDocketAdmin)


class HotelDocketAdmin(admin.ModelAdmin):
	form = HotelDocketAdminForm
	search_fields = ['id', 'booking_reference', 'account_head__first_name',
					 'guest_name', 'vendor__company_name',
					 'purchase', 'sale',
					 'invoice_no', 'purchase_invoice_no',
					 'hotel', 'destination_city', 'destination_country',
					 'hotel_confirmation_no',]
	save_on_top = True

	actions = [submit_to_accounts, return_to_operations, mark_void,remove_void]

	list_display = ('id', 'void_flag_based_booking_date', 'guest_name',
					'hotel', 'destination_city', 'check_in', 'check_out',
					'invoice_no', 'purchase', 'sale', 'payment_mode',
					'is_submit_to_accounts',)

	#list_editable = ('invoice_no', 'is_tally_entered',)

	_list_filter_operations = ('created_at', 'is_submit_to_accounts',
							   'is_void', 'vendor',)
	_list_filter_accounts = ('created_at', 'is_invoice_created',
							 'is_tally_entered', 'is_purchase_received',
							 'is_void', 'created_by', 'payment_mode', 'vendor',)
	_list_filter_admin = ('is_tally_entered', 'is_purchase_received',
						  'is_submit_to_accounts', 'is_invoice_created',
						  'is_void', 'invoice_dispatch_date',
						  'created_at', 'created_by',
						  'destination_city', 'destination_country',
						  'payment_mode', 'vendor',)

	def void_flag_based_booking_date(self, obj):
		result = obj.booking_date
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result.strftime('%b %d, %Y')
		return result
	void_flag_based_booking_date.allow_tags = True
	void_flag_based_booking_date.short_description = 'Date'

	def changelist_view(self, request, extra_context=None):
		# set list filter based on current user status
		if request.user.is_superuser:
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='SUPPORT').count():
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='OPERATIONS').count():
			self.list_filter = self._list_filter_operations
		elif request.user.groups.filter(name='ACCOUNTS').count():
			self.list_filter = self._list_filter_accounts

		# set Default filters as per current user status

		# set is_submit_to_accounts, is_void to No in case Operations
		if request.user.groups.filter(name='OPERATIONS').count():
			if not request.GET.has_key('is_submit_to_accounts__exact'):
				q = request.GET.copy()
				q['is_submit_to_accounts__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('created_by__id__exact'):
				q = request.GET.copy()
				q['created_by__id__exact'] = '%d' % User.objects.get(username=request.user).id
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		# set is_invoice_created, is_void to No in case Accounts
		"""
		if request.user.groups.filter(name='ACCOUNTS').count():
			if not request.GET.has_key('is_invoice_created__exact'):
				q = request.GET.copy()
				q['is_invoice_created__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
		"""

		return super(HotelDocketAdmin, self).changelist_view(request,
															 extra_context)

	"""
	def get_readonly_fields(self, request, obj=None):
		try:
			if not request.user.is_superuser and not request.user.groups.filter(name='SUPPORT'):
				if obj:
					list_of_fields = obj._meta.get_all_field_names()
					if obj.is_void:
						pass
					return list_of_fields
					if obj.is_submit_to_accounts:
						list_of_fields.remove('is_purchase_received')
						list_of_fields.remove('invoice_no')
						list_of_fields.remove('remarks')

						return list_of_fields
				else:
					return []
			else:
				return []
		except Exception, e:
			print e
	"""

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser or \
		   request.user.groups.filter(name='ACCOUNTS') or \
		   request.user.groups.filter(name='SUPPORT'):
			self.fieldsets = (
				('Accounts Area', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('invoice_no', 'invoice_dispatch_date'),
							   ('is_purchase_received', 'purchase_invoice_no'),
							   ('is_tally_entered', 'tally_narration'),)
				}),
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('hotel', 'meal_plan'),
								'hotel_confirmation_no',
							   'destination_city',
							   ('guest_name', 'no_of_guests'),
							   ('check_in', 'check_out'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)
		elif request.user.groups.filter(name='OPERATIONS'):
			self.fieldsets = (
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('hotel', 'meal_plan'),
								'hotel_confirmation_no',
							   'destination_city',
							   ('guest_name', 'no_of_guests'),
							   ('check_in', 'check_out'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)

		return super(HotelDocketAdmin, self).get_form(request,
													  obj=None,
													  **kwargs)

	def queryset(self, request):
		qs = super(HotelDocketAdmin, self).queryset(request)

		# show dockets which have been submitted to accounts
		if request.user.groups.filter(name='ACCOUNTS').count():
			return qs.filter(is_submit_to_accounts=True)
		else:
			return qs

	def get_actions(self, request):
		actions = super(HotelDocketAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		# remove SUBMIT TO ACCOUNTS, REMOVE VOID action for User in
		# Accounts Group
		if request.user.groups.filter(name='ACCOUNTS').count():
			del actions['submit_to_accounts']
			del actions['remove_void']

		# remove RETURN TO OPERATIONS, REMOVE VOID action
		# for User in Operations Group
		if request.user.groups.filter(name='OPERATIONS').count():
			del actions['return_to_operations']
			del actions['remove_void']

		return actions

	def save_model(self, request, obj, form, change):
		try:
			# calculate profit while saving
			obj.profit = obj.sale - obj.purchase

			# calculate duration of stay while saving
			obj.duration = abs((obj.check_out - obj.check_in).days)

			# mark is_invoice_created as True when Invoice No is entered
			if obj.invoice_no:
				obj.is_invoice_created = True
			else:
				obj.is_invoice_created = False

			# assign current user as author while saving for first time
			if obj.pk is None:
				obj.created_by = request.user

			obj.save()
		except Exception, e:
			print e

admin.site.register(HotelDocket, HotelDocketAdmin)

"""
class PackageDocketAdmin(admin.ModelAdmin):
	form = PackageDocketAdminForm
	search_fields = ['id', 'booking_reference', 'account_head__first_name',
					 'guest_name', 'vendor__company_name',
					 'purchase', 'sale',
					 'invoice_no', 'purchase_invoice_no',
					 'hotel', 'destination_city', 'destination_country',
					 'package_inclusions', 'package_confirmation_no',]
	save_on_top = True

	actions = [submit_to_accounts, return_to_operations, mark_void, remove_void]

	list_display = ('id', 'void_flag_based_booking_date', 'guest_name',
					'hotel', 'destination_city', 'check_in', 'check_out',
					'purchase', 'sale',
					'is_submit_to_accounts', 'invoice_no',)

	_list_filter_operations = ('created_at', 'is_submit_to_accounts',
							   'is_void',)
	_list_filter_accounts = ('created_at', 'is_invoice_created',
							 'is_tally_entered', 'is_purchase_received',
							 'is_void', 'created_by',)
	_list_filter_admin = ('created_at', 'created_by', 'is_submit_to_accounts',
						  'is_invoice_created', 'is_tally_entered',
						  'is_purchase_received', 'is_void',
						  'payment_mode', 'vendor',)

	def void_flag_based_booking_date(self, obj):
		result = obj.booking_date
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result.strftime('%b %d, %Y')
		return result
	void_flag_based_booking_date.allow_tags = True
	void_flag_based_booking_date.short_description = 'Date'

	def changelist_view(self, request, extra_context=None):
		# set list filter based on current user status
		if request.user.is_superuser:
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='SUPPORT').count():
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='OPERATIONS').count():
			self.list_filter = self._list_filter_operations
		elif request.user.groups.filter(name='ACCOUNTS').count():
			self.list_filter = self._list_filter_accounts

		# set Default filters as per current user status

		# set is_submit_to_accounts, is_void to No in case Operations
		if request.user.groups.filter(name='OPERATIONS').count():
			if not request.GET.has_key('is_submit_to_accounts__exact'):
				q = request.GET.copy()
				q['is_submit_to_accounts__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('created_by__id__exact'):
				q = request.GET.copy()
				q['created_by__id__exact'] = '%d' % User.objects.get(username=request.user).id
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		# set is_invoice_created, is_void to No in case Accounts

		if request.user.groups.filter(name='ACCOUNTS').count():
			if not request.GET.has_key('is_invoice_created__exact'):
				q = request.GET.copy()
				q['is_invoice_created__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		return super(PackageDocketAdmin, self).changelist_view(request,
															 extra_context)


	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser and not request.user.groups.filter(name='SUPPORT'):
			if obj:
				list_of_fields = obj._meta.get_all_field_names()
				if obj.is_void:
					return list_of_fields
				if obj.is_submit_to_accounts:
					list_of_fields.remove('is_purchase_received')
					list_of_fields.remove('invoice_no')
					list_of_fields.remove('remarks')

					return list_of_fields
			else:
				return []
		else:
			return []


	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser or \
		   request.user.groups.filter(name='ACCOUNTS') or \
		   request.user.groups.filter(name='SUPPORT'):
			self.fieldsets = (
				('Accounts Area', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('invoice_no', 'invoice_dispatch_date'),
							   ('is_purchase_received', 'purchase_invoice_no'),
							   ('is_tally_entered', 'tally_narration'),)
				}),
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('hotel', 'meal_plan'),
							   'package_confirmation_no',
							   ('destination_city', 'package_inclusions'),
							   ('guest_name', 'no_of_guests'),
							   ('check_in', 'check_out'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)
		elif request.user.groups.filter(name='OPERATIONS'):
			self.fieldsets = (
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('hotel', 'meal_plan'),
							   'package_confirmation_no',
							   ('destination_city', 'package_inclusions'),
								('guest_name', 'no_of_guests'),
							   ('check_in', 'check_out'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)

		return super(PackageDocketAdmin, self).get_form(request,
													  obj=None,
													  **kwargs)

	def queryset(self, request):
		qs = super(PackageDocketAdmin, self).queryset(request)

		# show dockets which have been submitted to accounts
		if request.user.groups.filter(name='ACCOUNTS').count():
			return qs.filter(is_submit_to_accounts=True)
		else:
			return qs

	def get_actions(self, request):
		actions = super(PackageDocketAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		# remove SUBMIT TO ACCOUNTS, REMOVE VOID action for User in
		# Accounts Group
		if request.user.groups.filter(name='ACCOUNTS').count():
			del actions['submit_to_accounts']
			del actions['remove_void']

		# remove RETURN TO OPERATIONS, REMOVE VOID action
		# for User in Operations Group
		if request.user.groups.filter(name='OPERATIONS').count():
			del actions['return_to_operations']
			del actions['remove_void']

		return actions

	def save_model(self, request, obj, form, change):
		# calculate profit while saving
		obj.profit = obj.sale - obj.purchase

		# calculate duration of stay while saving
		obj.duration = abs((obj.check_out - obj.check_in).days)

		# mark is_invoice_created as True when Invoice No is entered
		if obj.invoice_no:
			obj.is_invoice_created = True
		else:
			obj.is_invoice_created = False

		# assign current user as author while saving for first time
		if obj.pk is None:
			obj.created_by = request.user

		obj.save()

admin.site.register(PackageDocket, PackageDocketAdmin)
"""

class VisaDocketAdmin(admin.ModelAdmin):
	search_fields = ['id', 'booking_reference', 'account_head__first_name',
					 'guest_name', 'vendor__company_name',
					 'purchase', 'sale',
					 'invoice_no', 'purchase_invoice_no',
					 'destination_country',]

	save_on_top = True

	actions = [submit_to_accounts, return_to_operations, mark_void, remove_void]

	list_display = ('id', 'void_flag_based_booking_date', 'guest_name',
					'visa_type', 'destination_country',
					'purchase', 'sale', 'vendor',
					'is_submit_to_accounts',
					'invoice_no',)

	#list_editable = ('invoice_no', 'is_tally_entered',)

	_list_filter_operations = ('created_at', 'is_submit_to_accounts',
							   'is_void', 'visa_type', 'destination_country',
							   'vendor',)
	_list_filter_accounts = ('created_at', 'is_invoice_created',
							 'is_tally_entered', 'is_purchase_received',
							 'is_void', 'created_by',
							 'visa_type', 'destination_country',
							 'vendor',)
	_list_filter_admin = ('is_tally_entered', 'is_purchase_received',
						  'is_submit_to_accounts', 'is_invoice_created',
						  'is_void', 'invoice_dispatch_date',
						  'visa_type', 'destination_country',
						  'created_at', 'created_by', 'payment_mode', 'vendor',)

	def void_flag_based_booking_date(self, obj):
		result = obj.booking_date
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result.strftime('%b %d, %Y')
		return result
	void_flag_based_booking_date.allow_tags = True
	void_flag_based_booking_date.short_description = 'Date'

	def changelist_view(self, request, extra_context=None):
		# set list filter based on current user status
		if request.user.is_superuser:
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='SUPPORT').count():
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='OPERATIONS').count():
			self.list_filter = self._list_filter_operations
		elif request.user.groups.filter(name='ACCOUNTS').count():
			self.list_filter = self._list_filter_accounts

		# set Default filters as per current user status

		# set is_submit_to_accounts, is_void to No in case Operations
		if request.user.groups.filter(name='OPERATIONS').count():
			if not request.GET.has_key('is_submit_to_accounts__exact'):
				q = request.GET.copy()
				q['is_submit_to_accounts__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('created_by__id__exact'):
				q = request.GET.copy()
				q['created_by__id__exact'] = '%d' % User.objects.get(username=request.user).id
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		# set is_invoice_created, is_void to No in case Accounts
		"""
		if request.user.groups.filter(name='ACCOUNTS').count():
			if not request.GET.has_key('is_invoice_created__exact'):
				q = request.GET.copy()
				q['is_invoice_created__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
		"""

		return super(VisaDocketAdmin, self).changelist_view(request,
															 extra_context)

	"""
	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser and not request.user.groups.filter(name='SUPPORT'):
			if obj:
				list_of_fields = obj._meta.get_all_field_names()
				if obj.is_void:
					return list_of_fields
				if obj.is_submit_to_accounts:
					list_of_fields.remove('is_purchase_received')
					list_of_fields.remove('invoice_no')
					list_of_fields.remove('remarks')

					return list_of_fields
			else:
				return []
		else:
			return []
	"""

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser or \
		   request.user.groups.filter(name='ACCOUNTS') or \
		   request.user.groups.filter(name='SUPPORT'):
			self.fieldsets = (
				('Accounts Area', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('invoice_no', 'invoice_dispatch_date'),
							   ('is_purchase_received', 'purchase_invoice_no'),
							   ('is_tally_entered', 'tally_narration'),)
				}),
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('visa_type', 'destination_country'),
							   ('guest_name', 'no_of_guests'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)
		elif request.user.groups.filter(name='OPERATIONS'):
			self.fieldsets = (
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('visa_type', 'destination_country'),
								('guest_name', 'no_of_guests'),
								'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)

		return super(VisaDocketAdmin, self).get_form(request,
													  obj=None,
													  **kwargs)

	def queryset(self, request):
		qs = super(VisaDocketAdmin, self).queryset(request)

		# show dockets which have been submitted to accounts
		if request.user.groups.filter(name='ACCOUNTS').count():
			return qs.filter(is_submit_to_accounts=True)
		else:
			return qs

	def get_actions(self, request):
		actions = super(VisaDocketAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		# remove SUBMIT TO ACCOUNTS, REMOVE VOID action for User in
		# Accounts Group
		if request.user.groups.filter(name='ACCOUNTS').count():
			del actions['submit_to_accounts']
			del actions['remove_void']

		# remove RETURN TO OPERATIONS, REMOVE VOID action
		# for User in Operations Group
		if request.user.groups.filter(name='OPERATIONS').count():
			del actions['return_to_operations']
			del actions['remove_void']

		return actions

	def save_model(self, request, obj, form, change):
		# calculate profit while saving
		obj.profit = obj.sale - obj.purchase

		# mark is_invoice_created as True when Invoice No is entered
		if obj.invoice_no:
			obj.is_invoice_created = True
		else:
			obj.is_invoice_created = False

		# assign current user as author while saving for first time
		if obj.pk is None:
			obj.created_by = request.user

		obj.save()

admin.site.register(VisaDocket, VisaDocketAdmin)


class TravelInsuranceDocketAdmin(admin.ModelAdmin):
	search_fields = ['id', 'booking_reference', 'account_head__first_name',
					 'guest_name', 'vendor__company_name',
					 'purchase', 'sale',
					 'invoice_no', 'purchase_invoice_no',
					 'insurance_provider', 'insurance_plan',
					 'destination_country', 'policy_no',]
	save_on_top = True

	actions = [submit_to_accounts, return_to_operations, mark_void, remove_void]

	list_display = ('id', 'void_flag_based_booking_date', 'guest_name',
					'insurance_provider', 'destination_country',
					'purchase', 'sale',
					'is_submit_to_accounts',
					'invoice_no',)

	#list_editable = ('invoice_no', 'is_tally_entered',)

	_list_filter_operations = ('created_at', 'is_submit_to_accounts',
							   'is_void', 'insurance_provider',)
	_list_filter_accounts = ('created_at', 'is_invoice_created',
							 'is_tally_entered', 'is_purchase_received',
							 'is_void', 'created_by',
							 'insurance_provider',)
	_list_filter_admin = ('is_tally_entered', 'is_purchase_received',
						  'is_submit_to_accounts', 'is_invoice_created',
						  'is_void', 'invoice_dispatch_date',
						  'insurance_provider',
						  'created_at', 'created_by',)

	def void_flag_based_booking_date(self, obj):
		result = obj.booking_date
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result.strftime('%b %d, %Y')
		return result
	void_flag_based_booking_date.allow_tags = True
	void_flag_based_booking_date.short_description = 'Date'

	def changelist_view(self, request, extra_context=None):
		# set list filter based on current user status
		if request.user.is_superuser:
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='SUPPORT').count():
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='OPERATIONS').count():
			self.list_filter = self._list_filter_operations
		elif request.user.groups.filter(name='ACCOUNTS').count():
			self.list_filter = self._list_filter_accounts

		# set Default filters as per current user status

		# set is_submit_to_accounts, is_void to No in case Operations
		if request.user.groups.filter(name='OPERATIONS').count():
			if not request.GET.has_key('is_submit_to_accounts__exact'):
				q = request.GET.copy()
				q['is_submit_to_accounts__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('created_by__id__exact'):
				q = request.GET.copy()
				q['created_by__id__exact'] = '%d' % User.objects.get(username=request.user).id
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		# set is_invoice_created, is_void to No in case Accounts
		"""
		if request.user.groups.filter(name='ACCOUNTS').count():
			if not request.GET.has_key('is_invoice_created__exact'):
				q = request.GET.copy()
				q['is_invoice_created__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

			if not request.GET.has_key('is_void__exact'):
				q = request.GET.copy()
				q['is_void__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
		"""

		return super(TravelInsuranceDocketAdmin, self).changelist_view(request,
															 extra_context)

	"""
	def get_readonly_fields(self, request, obj=None):
		if not request.user.is_superuser and not request.user.groups.filter(name='SUPPORT'):
			if obj:
				list_of_fields = obj._meta.get_all_field_names()
				if obj.is_void:
					return list_of_fields
				if obj.is_submit_to_accounts:
					list_of_fields.remove('is_purchase_received')
					list_of_fields.remove('invoice_no')
					list_of_fields.remove('remarks')

					return list_of_fields
			else:
				return []
		else:
			return []
	"""

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser or \
		   request.user.groups.filter(name='ACCOUNTS') or \
		   request.user.groups.filter(name='SUPPORT'):
			self.fieldsets = (
				('Accounts Area', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('invoice_no', 'invoice_dispatch_date'),
							   ('is_purchase_received', 'purchase_invoice_no'),
							   ('is_tally_entered', 'tally_narration'),)
				}),
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('insurance_provider', 'insurance_plan'),
							   'policy_no',
							   'destination_country',
							   ('guest_name', 'no_of_guests'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)
		elif request.user.groups.filter(name='OPERATIONS'):
			self.fieldsets = (
				('Docket Header', {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date', 'account_head',)
				}),
				('Booking Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('insurance_provider', 'insurance_plan'),
							   'policy_no',
							   'destination_country',
							   ('guest_name', 'no_of_guests'),
							   'vendor',)
				}),
				('Payment Details', {
					'classes': ('wide', 'extrapretty',),
					'fields': (('purchase', 'sale', 'payment_mode'),)
				}),
				('Remarks', {
					#'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)

		return super(TravelInsuranceDocketAdmin, self).get_form(request,
													  obj=None,
													  **kwargs)

	def queryset(self, request):
		qs = super(TravelInsuranceDocketAdmin, self).queryset(request)

		# show dockets which have been submitted to accounts
		if request.user.groups.filter(name='ACCOUNTS').count():
			return qs.filter(is_submit_to_accounts=True)
		else:
			return qs

	def get_actions(self, request):
		actions = super(TravelInsuranceDocketAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		# remove SUBMIT TO ACCOUNTS, REMOVE VOID action for User in
		# Accounts Group
		if request.user.groups.filter(name='ACCOUNTS').count():
			del actions['submit_to_accounts']
			del actions['remove_void']

		# remove RETURN TO OPERATIONS, REMOVE VOID action
		# for User in Operations Group
		if request.user.groups.filter(name='OPERATIONS').count():
			del actions['return_to_operations']
			del actions['remove_void']

		return actions

	def save_model(self, request, obj, form, change):
		# calculate profit while saving
		obj.profit = obj.sale - obj.purchase

		# mark is_invoice_created as True when Invoice No is entered
		if obj.invoice_no:
			obj.is_invoice_created = True
		else:
			obj.is_invoice_created = False

		# assign current user as author while saving for first time
		if obj.pk is None:
			obj.created_by = request.user

		obj.save()

admin.site.register(TravelInsuranceDocket, TravelInsuranceDocketAdmin)


class CreditNoteDocketAdmin(admin.ModelAdmin):
	search_fields = ['invoice_no', 'old_docket_no',]
	save_on_top = True

	actions = [submit_to_accounts, return_to_operations, mark_void]

	list_display = ('id', 'void_flag_based_booking_date', 'credit_note_type',
					'old_docket_no', 'new_purchase', 'new_sale',
					'is_submit_to_accounts', 'invoice_no', 'is_invoice_created',
					'is_tally_entered',)

	_list_filter_operations = ('created_at', 'is_submit_to_accounts',
							   'is_void', 'credit_note_type',)
	_list_filter_accounts = ('created_at', 'is_invoice_created',
							 'is_tally_entered', 'is_purchase_received',
							 'is_void', 'created_by', 'credit_note_type',)
	_list_filter_admin = ('created_at', 'is_submit_to_accounts',
						  'is_invoice_created', 'is_tally_entered',
						  'is_purchase_received', 'is_void',
						  'created_by', 'credit_note_type',)

	list_editable = ('invoice_no', 'is_tally_entered',)

	def void_flag_based_booking_date(self, obj):
		result = obj.booking_date
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result.strftime('%b %d, %Y')
		return result
	void_flag_based_booking_date.allow_tags = True
	void_flag_based_booking_date.short_description = 'Date'

	def changelist_view(self, request, extra_context=None):
		# set list filter based on current user status
		if request.user.is_superuser:
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='SUPPORT').count():
			self.list_filter = self._list_filter_admin
		elif request.user.groups.filter(name='OPERATIONS').count():
			self.list_filter = self._list_filter_operations
		elif request.user.groups.filter(name='ACCOUNTS').count():
			self.list_filter = self._list_filter_accounts

		# set Default filters as per current user status

		# set is_submit_to_accounts to No in case Operations
		if request.user.groups.filter(name='OPERATIONS').count():
			if not request.GET.has_key('is_submit_to_accounts__exact'):
				q = request.GET.copy()
				q['is_submit_to_accounts__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
			if not request.GET.has_key('created_by__id__exact'):
				q = request.GET.copy()
				q['created_by__id__exact'] = '%d' % User.objects.get(username=request.user).id
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()

		# set is_invoice_created to No in case Accounts
		"""
		if request.user.groups.filter(name='ACCOUNTS').count():
			if not request.GET.has_key('is_invoice_created__exact'):
				q = request.GET.copy()
				q['is_invoice_created__exact'] = '0'
				request.GET = q
				request.META['QUERY_STRING'] = request.GET.urlencode()
		"""

		return super(CreditNoteDocketAdmin, self).changelist_view(request,
															 extra_context)

	"""
	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='ACCOUNTS'):
			return ['booking_date', 'credit_note_type',
					'old_docket_no',
					'new_sale', 'new_purchase', 'new_payment_mode',]
		else:
			return []
	"""

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser or \
		   request.user.groups.filter(name='ACCOUNTS') or \
		   request.user.groups.filter(name='SUPPORT'):
			self.fieldsets = (
				(None, {
					'classes': ('wide', 'extrapretty',),
					'fields': (('invoice_no', 'invoice_dispatch_date'),
							   ('is_purchase_received', 'purchase_invoice_no'),
							   ('is_tally_entered', 'tally_narration'),
							   'booking_date',)}),
				(None, {
					'fields': (('credit_note_type', 'old_docket_no'),
							   ('new_purchase', 'new_sale', 'new_payment_mode'),)
				}),
				('Remarks', {
					'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)
		elif request.user.groups.filter(name='OPERATIONS'):
			self.fieldsets = (
				(None, {
					'classes': ('wide', 'extrapretty',),
					'fields': ('booking_date',
							   ('credit_note_type', 'old_docket_no'),
							   ('new_purchase', 'new_sale',
								'new_payment_mode'),)
				}),
				('Remarks', {
					'classes': ('collapse',),
					'fields': ('remarks',)
				}),
			)

		return super(CreditNoteDocketAdmin, self).get_form(request,
													  obj=None,
													  **kwargs)

	def queryset(self, request):
		qs = super(CreditNoteDocketAdmin, self).queryset(request)

		# show dockets which have been submitted to accounts
		if request.user.groups.filter(name='ACCOUNTS').count():
			return qs.filter(is_submit_to_accounts=True)
		else:
			return qs

	def get_actions(self, request):
		actions = super(CreditNoteDocketAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		# remove SUBMIT TO ACCOUNTS action for User in Accounts Group
		if request.user.groups.filter(name='ACCOUNTS').count():
			del actions['submit_to_accounts']

		# remove RETURN TO OPERATIONS, PURCHASE RECEIVED action
		# for User in Operations Group
		if request.user.groups.filter(name='OPERATIONS').count():
			del actions['return_to_operations']

		return actions

	def save_model(self, request, obj, form, change):
		# calculate profit while saving
		obj.new_profit = obj.new_sale - obj.new_purchase

		# mark is_invoice_created as True when Invoice No is entered
		if obj.invoice_no:
			obj.is_invoice_created = True
		else:
			obj.is_invoice_created = False

		# assign current user as author while saving for first time
		if obj.pk is None:
			obj.created_by = request.user

		obj.save()

admin.site.register(CreditNoteDocket, CreditNoteDocketAdmin)
