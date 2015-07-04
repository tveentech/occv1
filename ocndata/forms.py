from models import *
from django import forms


class AirTicketDocketAdminForm(forms.ModelForm):
	def clean(self):
		form_data = self.cleaned_data

		if form_data['start_date'] and form_data['return_date']:
			if form_data['start_date'] > form_data['return_date']:
				raise forms.ValidationError('Start date cannot be After Return date')

		return form_data


class HotelDocketAdminForm(forms.ModelForm):
	def clean(self):
		form_data = self.cleaned_data

		if form_data['check_in'] and form_data['check_out']:
			if form_data['check_in'] > form_data['check_out']:
				raise forms.ValidationError('Check-in date cannot be After Check-out date')

		return form_data


class PackageDocketAdminForm(forms.ModelForm):
	def clean(self):
		form_data = self.cleaned_data

		if form_data['check_in'] and form_data['check_out']:
			if form_data['check_in'] > form_data['check_out']:
				raise forms.ValidationError('Check-in date cannot be After Check-out date')

		return form_data
