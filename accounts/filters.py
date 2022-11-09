import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class EmpFilter(django_filters.FilterSet):
	name = CharFilter(field_name='name', lookup_expr='icontains')

	class Meta:
		model = Customer
		fields = ['name']

class AttenFilter(django_filters.FilterSet):
	date = DateFilter(field_name="date", lookup_expr='icontains')
	# attender = CharFilter(field_name='name', lookup_expr='icontains')

	class Meta:
		model = Attendance
		fields = ['date']
