from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from habits.models import Habit
from habits.serializers import HabitSerializer, HabitListSerializer
from habits.permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с привычками"""

    serializer_class = HabitSerializer

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя, кроме публичных привычек для списка"""
        user = self.request.user

        if self.action == "list":
            # Для списка возвращаем привычки пользователя и публичные привычки
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        elif self.action == "public":
            # Для публичного списка возвращаем только публичные привычки
            return Habit.objects.filter(is_public=True)
        else:
            # Для остальных действий - только привычки пользователя
            return Habit.objects.filter(user=user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == "list":
            return HabitListSerializer
        elif self.action in ["public", "my"]:
            return HabitListSerializer
        return HabitSerializer

    def get_permissions(self):

        if self.action in ["create", "list", "public", "my"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическое назначение текущего пользователя при создании"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def public(self, request):
        """Кастомное действие для получения списка публичных привычек"""

        queryset = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my(self, request):
        """Кастомное действие для получения только своих привычек"""

        queryset = Habit.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
