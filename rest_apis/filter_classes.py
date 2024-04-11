from django_filters import rest_framework as filters
from account.models import User

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class UserFilterClass(filters.FilterSet):
    user_id = NumberInFilter(field_name='id', lookup_expr='in', required=False, distinct=True)
    user_email = filters.CharFilter(method='filter_user_email',required=False),
    user_phone = filters.CharFilter(method='filter_user_phone',required=False),
    user_role = filters.NumberFilter(method='filter_user_role',required=False),

    class Meta:
        model = User
        fields = ["id", 'email', 'phone', 'role']

    def filter_user_email(self,querset, name, value):
        querset = querset.filter(user_email__email=value)
        return querset

    def filter_user_phone(self,querset, name, value):
        querset = querset.filter(user_phone__name=value)
        return querset

    def filter_user_role(self,querset, name, value):
        querset = querset.filter(user_role__role=value)
        return querset

