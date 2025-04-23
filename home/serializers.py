from rest_framework import serializers
from django.core.validators import RegexValidator

class ValidateQueryParams(serializers.Serializer):
    search = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[\u0621-\u064A\u0660-\u0669 a-zA-Z0-9\s]{3,30}$",
                message="Search must be 0–200 characters and contain valid characters."
            )
        ]
    )
