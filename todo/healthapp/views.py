from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Health
from .serializer import HealthSerializer


# Create your views here.
class HealthViews:
    @api_view(["GET"])
    def get_data(request):
        params_name = request.GET.get("name")
        params_age = request.GET.get("age")

        filters = Q()

        # check if name or age is exist params search
        if params_name:
            filters &= Q(name=params_name)
        if params_age:
            filters &= Q(age=params_age)

        all_data = Health.objects.filter(filters)
        serializer = HealthSerializer(all_data, many=True)

        if not serializer.data:
            return Response(
                {"message": "No data available"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(["POST"])
    def post_data(request):
        serializer = HealthSerializer(data=request.data)
        # check if name is exist
        exits_name = Health.objects.filter(name=request.data["name"]).exists()

        if exits_name:
            return Response(
                {"message": "Name already exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["PUT"])
    def update_data(request, pk):
        try:
            data = Health.objects.get(pk=pk)
        except Health.DoesNotExist:
            return Response(
                {"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = HealthSerializer(data, data=request.data)
        # only check name is exist and not same with the current data
        current_db_name = Health.objects.get(pk=pk).name
        exits_name = Health.objects.filter(name=request.data["name"]).exists()
        if exits_name and request.data["name"] != current_db_name:
            return Response(
                {"message": "Name already exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
