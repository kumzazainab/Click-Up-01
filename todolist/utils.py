import re
from django.contrib.auth import get_user_model

User = get_user_model()

def extract_tagged_users(comment_text):
    tagged_usernames = re.findall(r"@(\w+)", comment_text)
    if not tagged_usernames:
        return User.objects.none()  # Empty queryset to avoid errors
    return User.objects.filter(username__in=tagged_usernames)