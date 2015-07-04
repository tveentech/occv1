from django.contrib import admin
from models import *


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


class PaymentReminderAdmin(admin.ModelAdmin):
	list_display = ('id', 'void_flag_based_item_title', 'payment_due_date',
					'currency_and_amount', 'payment_owner',
					'is_paid', 'remarks',)
	list_filter = ('is_paid', 'payment_due_date', 'is_void', 'payment_date',)
	exclude = ('is_void', 'created_by',)
	actions = [mark_void, remove_void]
	search_fields = ['item_title', 'amount', 'remarks']

	def void_flag_based_item_title(self, obj):
		result = obj.item_title
		if obj.is_void:
			return u'<div style="text-decoration:line-through">%s\
</div>' % result
		return result
	void_flag_based_item_title.allow_tags = True
	void_flag_based_item_title.short_description = 'Item'


	def currency_and_amount(self, obj):
		return u'%s %s' % (obj.currency_type, obj.amount)
	currency_and_amount.allow_tags = True
	currency_and_amount.short_description = 'Amount'


	def get_actions(self, request):
		actions = super(PaymentReminderAdmin, self).get_actions(request)

		# remove DELETE SELECTED action for non SuperUser
		if not request.user.is_superuser:
			del actions['delete_selected']

		return actions


	def queryset(self, request):
		qs = super(PaymentReminderAdmin, self).queryset(request)

		# show items which have been created by current user only
		if request.user.groups.filter(name='OPERATIONS').count():
			return qs.filter(payment_owner=request.user)
		else:
			return qs


	def save_model(self, request, obj, form, change):
		# assign current user as author while saving for first time
		if obj.pk is None:
			obj.created_by = request.user
		obj.save()

admin.site.register(PaymentReminder, PaymentReminderAdmin)
