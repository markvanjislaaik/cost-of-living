from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from base.models import Expenses
from django.db.models import Q
from .serializers import ExpensesSerializer
from rest_framework.parsers import JSONParser

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'POST /api/token/',
        'POST /api/token/refresh/',
        'GET /api',
        'GET /api/expenses',
        'POST /api/expenses',
        'GET /api/expenses/:id',
        'GET /api/search/:keyword'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getExpenses(request):
    # user = request.user # gets username from token if JWT was customixed to contain it
    if request.method == 'GET':
        expenses = Expenses.objects.all()
        jsonified = ExpensesSerializer(expenses, many=True)
        return Response(jsonified.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['date'] = data.get('date_purchased')[:10]
        data['year_month'] = data.get('date_purchased')[:7]
        print(data)
        jsonified = ExpensesSerializer(data=data)
        if jsonified.is_valid():
            jsonified.save()
            return Response(jsonified.data, status=201)
        return Response(jsonified.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExpense(request, pk):
    expense = Expenses.objects.get(id=pk)
    jsonified = ExpensesSerializer(expense, many=False)
    return Response(jsonified.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchExpenses(request, q):

    expenses = Expenses.objects.filter(
        Q(thing__icontains=q) |
        Q(details__icontains=q) |
        Q(location__icontains=q)
    )
    jsonified = ExpensesSerializer(expenses, many=True)
    return Response(jsonified.data)