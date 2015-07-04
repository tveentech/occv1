from django.contrib import admin
from models import *


class OnlineSystemAdmin(admin.ModelAdmin):
	list_display = ('id', 'title_website', 'agent_id', 'agent_password_masked',
					'user_id', 'user_password_masked', 'status', 'remarks',)
	list_filter = ('is_active', 'product_type', 'destination',)
	search_fields = ['title', 'website', 'product_type',
					 'destination', 'remarks']
	exclude = ('created_by', 'last_updated_by',)
	save_on_top = True

	fieldsets = (
		('Meta', {
			'fields': ('is_active', ('title', 'website'),)
		}),
		('Credentials', {
			'fields': (('agent_id', 'agent_password'),
					   ('user_id', 'user_password'),)
		}),
		(None, {
			'fields': (('product_type', 'destination'),
					   'remarks',)
		}),
	)

	def title_website(self, obj):
		if obj.website:
			result = u'<a href="%s" target="_blank">%s</a>' % (obj.website,
															   obj.title)
		else:
			result = obj.title
		return result
	title_website.allow_tags = True
	title_website.short_description = 'Online System'

	def agent_password_masked(self, obj):
		result = ''
		if obj.agent_password:
			length_of_agent_password = len(obj.agent_password)
			result = '<span title="%s">%s</span>' % (obj.agent_password,
												'*' * length_of_agent_password)
		return result
	agent_password_masked.allow_tags = True
	agent_password_masked.short_description = 'Agent Password'

	def user_password_masked(self, obj):
		result = ''
		if obj.user_password:
			length_of_user_password = len(obj.user_password)
			result = '<span title="%s">%s</span>' % (obj.user_password,
												'*' * length_of_user_password)
		return result
	user_password_masked.allow_tags = True
	user_password_masked.short_description = 'Agent Password'

	def status(self, obj):
		if obj.is_active:
			result = '<img src="/static/admin/img/icon-yes.gif" \
title="Created at %s\nCreated by %s\n\nLast Updated at %s\nLast Updated \
by %s">' % (\
	obj.created_at.strftime('%d %b %y'),
	obj.created_by,
	obj.last_updated_at.strftime('%d %b %y'),
	obj.last_updated_by)
		else:
			result = '<img src="/static/admin/img/icon-no.gif" \
title="Created at %s\nCreated by %s\n\nLast Updated at %s\nLast Updated \
by %s">' % (\
	obj.created_at.strftime('%d %b %y'),
	obj.created_by,
	obj.last_updated_at.strftime('%d %b %y'),
	obj.last_updated_by)

		return result
	status.allow_tags = True
	status.short_description = 'Status'

	def save_model(self, request, obj, form, change):
		if obj.pk is None:
			obj.created_by = request.user
		obj.last_updated_by = request.user
		obj.save()

admin.site.register(OnlineSystem, OnlineSystemAdmin)


class CreditCardAdmin(admin.ModelAdmin):
	list_display = ('nickname', 'name_on_card', 'card_number_masked',
					'card_type', 'credit_days_available',
					'actual_available_amount',
					'remarks', 'last_updated_details', 'is_active',)
	list_filter = ('is_active', 'issuing_bank', 'card_type', 'name_on_card',)
	search_fields = ['issuing_bank', 'card_type', 'card_number',
					 'name_on_card', 'nickname', 'remarks',]
	ordering = ('-is_active',
				'-credit_days_available',
				'-actual_available_amount',)
	exclude = ('last_updated_by',)
	save_on_top = True

	fieldsets = (
		('Card details', {
			'fields': ('is_active',
					   ('issuing_bank', 'card_type'),
					   ('card_number', 'name_on_card'), 'nickname')
		}),
		('Credit cyle', {
			'fields': (('next_statement_generation_date',
					   'next_payment_date',
					   'credit_days_available'),)
		}),
		('Amount', {
			'fields': (('pending_amount', 'current_available_amount',),)
		}),
		('Credentials', {
			'classes': ('collapse',),
			'fields': ('website',
					   ('username', 'password'),
					   ('email', 'phone'),
					   'total_limit',)
		}),
		(None, {
			'fields': ('remarks',)
		}),
	)

	def card_number_masked(self, obj):
		result = '<span title="%s">%s</span>' % (\
			obj.card_number,
			obj.card_number[:4] + '*'*8 + obj.card_number[-4:])
		return result
	card_number_masked.allow_tags = True
	card_number_masked.short_description = 'Card Number'

	def last_updated_details(self, obj):
		result = '%s by %s' % (\
			obj.last_updated_at.strftime('%d %b %y @ %H:%M'),
			obj.last_updated_by)
		return result
	last_updated_details.allow_tags = True
	last_updated_details.short_description = 'Last Updated'

	def save_model(self, request, obj, form, change):
		# calculate actual available amount
		obj.actual_available_amount = obj.current_available_amount - obj.pending_amount

		# assign current user to last_updated_by field
		obj.last_updated_by = request.user
		obj.save()

admin.site.register(CreditCard, CreditCardAdmin)
