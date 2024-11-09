from django.shortcuts import render
from django.http import JsonResponse
from .models import Task

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>/',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>/',
    }


    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request,pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    # Check if the incoming data is a list of tasks
    if isinstance(request.data, list):
        # If it is a list, serialize each item individually
        serializer = TaskSerializer(data=request.data, many=True)
    else:
        # If it's a single task, serialize as usual
        serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()  # Save either one or many tasks
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)



@api_view(['POST'])
def taskUpdate(request,pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response('Item succsesfully deleted!')
