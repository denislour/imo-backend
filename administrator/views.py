from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.models import User, Product
from common.serializers import UserSerializer
from common.authen import JWTAuthentication
from .serializers import ProductSerializer


class AmbassadorAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        serializer = UserSerializer(ambassadors, many=True)

        return Response(serializer.data)


class ProductGenericAPIView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """
    Generic API will allow create API thanks to class base view
    - RetrieveModelMixin allow us inherit retrieve function to return detail one model's records
    - ListModelMixin allow us using list function to return list all model's record
    - CreateModelMixin allow us using create function create one model's record
    - UpdateModelMixin allow us using partial_update to update value of one model's record
    - DestroyModelMixin allow us using destroy to delete one model's record
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        if pk is not None:
            return self.retrieve(request, pk)
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        return self.partial_update(request, pk)

    def delete(self, request, pk=None):
        return self.destroy(request, pk)
