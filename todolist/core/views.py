from re import T
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated 
from rest_framework import generics
from .serializers import TodoSerializer
from todo.models import Todo
from django.shortcuts import get_object_or_404
from rest_framework.decorators import (
    api_view, renderer_classes , permission_classes
)

from store.models import Product

# class base view for single and list items
class TodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,*args, **kwargs):
        single_todo = Todo.objects.all().first()
        all_todos = Todo.objects.all()
        serializer = TodoSerializer(all_todos,many=True)

        return Response(serializer.data)

    def post(self, request,*args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer._errors)

# function base view for list items
@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def todo_list_view(request, format=None):
    todos = TodoSerializer(Todo.objects.all(),many=True)
    return Response(todos.data)

# function base view for single item
@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def todo_detail_view(request, pk, format=None):
    todo = get_object_or_404(Todo, pk=pk)
    serializer = TodoSerializer(todo)
    return Response(serializer.data)

# class base view for list items
class TodoList(generics.ListAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

#class base view for single item
class TodoDetail(generics.RetrieveAPIView):
    def get_serializer_class(self):
        return TodoSerializer

    def get_queryset(self):
        product = Product(name='Dell',price=2.000,description='product under dell laptops')
        product.save(using='stores')
        todo = Todo.objects.all()
        return todo
