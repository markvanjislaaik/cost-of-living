from rest_framework.serializers import ModelSerializer
from base.models import Expenses


class ExpensesSerializer(ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'