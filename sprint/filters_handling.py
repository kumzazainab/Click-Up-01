from datetime import timedelta, date


def filter_status_logic(queryset, status_filter_type, status):
    if status_filter_type == 'is' and status:
        return queryset.filter(status__name__iexact=status)
    if status_filter_type == 'is_not' and status:
        return queryset.exclude(status__name__iexact=status)
    if status_filter_type == 'active':
        return queryset.exclude(status__name__iexact='Complete')
    if status_filter_type == 'closed':
        return queryset.filter(status__name__iexact='Complete')
    return queryset


def filter_due_date_logic(queryset, value):
        today = date.today()
        if value == 'today':
            return queryset.filter(due_date=today)
        elif value == 'yesterday':
            return queryset.filter(due_date=today - timedelta(days=1))
        elif value == 'tomorrow':
            return queryset.filter(due_date=today + timedelta(days=1))
        return queryset


def filter_priority_logic(queryset,value):
        if value.startswith('is:'):
            priority_value = value.split(':')[1].lower()
            return queryset.filter(priority=priority_value)
        if value.startswith('is_not:'):
            priority_value = value.split(':')[1].lower()
            return queryset.exclude(priority=priority_value)
        if value == 'is_set':
            return queryset.exclude(priority__isnull=True).exclude(priority='')
        if value == 'is_not_set':
            return queryset.filter(priority__isnull=True) | queryset.filter(priority='')
        return queryset


def filter_assignee_logic(queryset, value, request_user):
    if value.startswith('is:'):
        if value.split(':')[1] == 'me':
            return queryset.filter(assigned_to=request_user)
    elif value.startswith('is_not:'):
        if value.split(':')[1] == 'me':
            return queryset.exclude(assigned_to=request_user)
    elif value == 'is_set':
        return queryset.exclude(assigned_to__isnull=True)
    elif value == 'is_not_set':
        return queryset.filter(assigned_to__isnull=True)
    return queryset


def filter_tags_logic(queryset, value):
    if value.startswith('is:'):
        tag_value = value.split(':')[1].strip().lower()
        return queryset.filter(tags__name__iexact=tag_value).distinct()
    elif value.startswith('is_not:'):
        tag_value = value.split(':')[1].strip().lower()
        return queryset.exclude(tags__name__iexact=tag_value).distinct()
    elif value == 'is_set':
        return queryset.filter(tags__isnull=False).distinct()
    elif value == 'is_not_set':
        return queryset.filter(tags__isnull=True).distinct()
    return queryset