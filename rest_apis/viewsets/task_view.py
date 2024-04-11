from rest_framework import status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_apis.serial.task_serial import TaskSerializer, TaskInputSerializer
from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework import permissions
from rest_apis.models import Task

class TaskViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TaskSerializer

    @swagger_auto_schema(tags=['Task API'], request_body=TaskInputSerializer)
    def create(self, request, *args, **kwargs):
        data=request.data
        task = Task.objects.create(name=data['name'], description=data['description'], trigger=data['trigger'], user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=['Task API'])
    def list(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Task API'])
    def retrieve(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"message": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['Task API'], request_body=TaskInputSerializer)
    def update(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"message": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        task.name = data['name']
        task.description = data['description']
        task.trigger = data['trigger']
        task.save()
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['Task API'])
    def destroy(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"message": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
