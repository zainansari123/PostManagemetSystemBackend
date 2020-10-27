from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.response import *
from rest_framework.status import *
from ..models import *
from .serializers import *
# from django.utils import timezone
from datetime import datetime,timedelta
from pytz import timezone
# from account.models import Driver


class TaskApiView(CreateAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        data = TaskSerializer(qs, many=True).data
        return Response({"message":"Promo code list","data":data},status=HTTP_200_OK)

    def put(self, request, pk):
        print(pk)
        task = get_object_or_404(TaskWork.objects.all(), pk=pk)
        data = request.data
        serializer = EntryUpdateSerializer(instance=task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Task updated successfully"},status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Task created successfully","data":serializer.data},status=HTTP_200_OK)
        # print(serializer)
        error_keys = list(serializer.errors.keys())
        print(error_keys)
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        promo_code = get_object_or_404(User.objects.all(), pk=pk)
        coupon = promo_code.coupon_code
        promo_code.delete()
        return Response({"message": "Promo Code {} has been deleted.".format(coupon)}, status=HTTP_200_OK)



