import django_filters
from .models import Message, User

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(
        field_name="sender", queryset=User.objects.all()
    )
    start_date = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["sender", "start_date", "end_date"]
