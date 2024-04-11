from django_filters import rest_framework as filters
from rest_apis.models import Activity
from rest_apis.serial.activity_serial import ActivitySerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from lib.pagination import CustomPageNumberPagination
from rest_framework import permissions
from knox.auth import TokenAuthentication

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class CompanyDetailsFilterClass(filters.FilterSet):
    id = NumberInFilter(field_name='id', lookup_expr='in', required=False, distinct=True)
    name = filters.CharFilter(method='filterName', required=False),

    class Meta:
        model = Activity
        fields = ['id', 'name']

    def filterName(self, querset, name, value):
        querset = querset.filter(name__name=value)   
        return querset

class ActivityView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ActivitySerializer
    filter_class = CompanyDetailsFilterClass
    filterset_fields = ['id', 'name']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Activity.objects.all()

    def create(self, request, *args, **kwargs):
        data=request.data
        activity = Activity.objects.filter(name=data['name']).count()
        if activity:
            return Response({'message': "This activity is already exist"}, status=status.HTTP_400_BAD_REQUEST)

        activity = Activity.objects.create(name=data['name'], description=data['description'])
        serializer = ActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

