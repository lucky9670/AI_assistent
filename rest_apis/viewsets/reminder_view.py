from rest_framework import status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_apis.serial.reminder_serial import ReminderSerializer, ReminderInputSerializer
from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework import permissions
from rest_apis.models import Reminder

class ReminderViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ReminderSerializer

    @swagger_auto_schema(tags=['Reminder API'], request_body=ReminderInputSerializer)
    def create(self, request, *args, **kwargs):
        data=request.data
        reminder = Reminder.objects.create(title=data['title'], description=data['description'], due_date=data['due_date'], user=request.user)
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=['Reminder API'])
    def list(self, request):
        queryset = Reminder.objects.all()
        serializer = ReminderSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Reminder API'])
    def retrieve(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(pk=pk)
        except Reminder.DoesNotExist:
            return Response({"message": "Reminder not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Reminder API'], request_body=ReminderInputSerializer)
    def update(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(pk=pk)
        except Reminder.DoesNotExist:
            return Response({"message": "Reminder not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        reminder.title = data['title']
        reminder.description = data['description']
        reminder.due_date = data['due_date']
        reminder.save()
        serializer = ReminderSerializer(reminder)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['Reminder API'])
    def destroy(self, request, pk=None):
        try:
            reminder = Reminder.objects.get(pk=pk)
        except Reminder.DoesNotExist:
            return Response({"message": "Reminder not found."}, status=status.HTTP_404_NOT_FOUND)
        reminder.delete()
        return Response({"message": "Reminder deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
