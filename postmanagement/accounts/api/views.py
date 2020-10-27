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


class UserLoginApiView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        # data = serializer.data
        if serializer.is_valid():
            # serializer.save()
            return Response({
                'data':serializer.data,
                "message": "Login successfully"
            }, status=HTTP_200_OK)
        error_keys = list(serializer.errors.keys())
        print(error_keys)
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0]}, status=400)
        return Response(serializer.errors, status=400)


class UserApiView(CreateAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        qs = User.objects.all()
        data = UserSerializer(qs, many=True).data
        return Response({"message":"Promo code list","data":data},status=HTTP_200_OK)

    def put(self, request, pk):
        saved_promo = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data
        serializer = UserSerializer(instance=saved_promo, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            promo_saved = serializer.save()
        return Response({"success": "Promo Code '{}' updated successfully".format(promo_saved.coupon_code)})

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User {} created successfully".format(serializer.data.get('username')),"data":serializer.data},status=HTTP_200_OK)
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



