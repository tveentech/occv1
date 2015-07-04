from django.contrib import admin
from models import *
from ocndata.models import AccountHead


class PrivilegeProgramAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'remarks', 'is_active',)
	list_filter = ('is_active',)
	search_fields = ['title']

admin.site.register(PrivilegeProgram, PrivilegeProgramAdmin)


class PrivilegeAccountAdmin(admin.ModelAdmin):
	list_display = ('id', 'guest', 'program_type', 'number', 'tier',
					'points', 'last_updated_at', 'remarks', 'is_active',)
	list_filter = ('is_active', 'program_type',)
	search_fields = ['guest__first_name', 'guest__last_name', 'number', 'remarks']
	save_on_top = True

	fieldsets = (
		('Program details', {
			'fields': ('is_active', 'guest',
					   ('program_type', 'tier'),
					   ('number', 'points'),
					   'last_updated_at',)
		}),
		('Credentials', {
			'classes': ('collapse',),
			'fields': ('website',
					   ('username', 'password'),
					   ('email', 'phone'),
					   'dob',)
		}),
		(None, {
			'fields': ('remarks',)
		}),
	)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		#if db_field.name == 'guest':
		#    kwargs['queryset'] = Client.objects.filter(relation_category='C')
		return super(PrivilegeAccountAdmin, self).formfield_for_foreignkey(
			db_field, request, **kwargs)

admin.site.register(PrivilegeAccount, PrivilegeAccountAdmin)
