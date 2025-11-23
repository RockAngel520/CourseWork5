from rest_framework import serializers
from habits.models import Habit
from habits.validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для привычки"""

    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    associated_habit = serializers.SlugRelatedField(
        slug_field="action", queryset=Habit.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "associated_habit",
            "period",
            "reward",
            "time_to_complete",
            "is_public",
        ]
        read_only_fields = ["user"]

    def validate(self, data):
        """Валидация данных привычки"""

        habit = Habit(**data)

        if self.instance:
            for field in [
                "user",
                "place",
                "time",
                "action",
                "is_pleasant",
                "associated_habit",
                "period",
                "reward",
                "time_to_complete",
                "is_public",
            ]:
                if field not in data:
                    setattr(habit, field, getattr(self.instance, field))

        validate_habit(habit)

        return data

    def create(self, validated_data):
        """Создание привычки с автоматическим назначением текущего пользователя"""

        user = self.context["request"].user
        validated_data["user"] = user

        return super().create(validated_data)


class HabitListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка привычек"""

    user = serializers.CharField(source="user.username")
    associated_habit = serializers.CharField(source="associated_habit.action", allow_null=True)

    class Meta:
        model = Habit
        fields = ["id", "user", "action", "place", "time", "is_pleasant", "associated_habit", "period", "is_public"]
