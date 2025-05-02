from datetime import timedelta, date
import django_filters
from todolist.models import Task
from sprint.filters_handling import filter_status_logic, filter_due_date_logic, \
    filter_priority_logic, filter_assignee_logic, filter_tags_logic


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    status_filter_type = django_filters.CharFilter(method='filter_status')
    tags_filter_type = django_filters.CharFilter(method='filter_tags')
    due_date = django_filters.DateFilter(field_name='due_date')
    due_date_filter_type = django_filters.CharFilter(method='filter_due_date')
    priority_filter = django_filters.CharFilter(method='filter_priority')
    assignee_filter_type = django_filters.CharFilter(method='filter_assignee')


    def filter_status(self, queryset, name, value):
        status = self.data.get('status', None)
        return filter_status_logic(queryset, value, status)


    def filter_due_date(self, queryset, name, value):
        return filter_due_date_logic(queryset, value)


    def filter_priority(self, queryset, name, value):
        return filter_priority_logic(queryset, value)


    def filter_assignee(self, queryset, name, value):
        return filter_assignee_logic(queryset, value, self.request.user)


    def filter_tags(self, queryset, name, value):
        return filter_tags_logic(queryset, value)


    class Meta:
        model = Task
        fields = ['status', 'tags', 'end_date', 'priority', 'assigned_to', 'status_filter_type', 'due_date_filter_type',
                  'priority_filter', 'assignee_filter_type', 'tags_filter_type',]
