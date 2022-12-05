from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import TestModel
from api.serializers.test import TestSerializer
from api.utils import error_response, response


class CreateTestView(CreateAPIView):
    queryset = TestModel.objects.filter(is_active=True)
    serializer_class = TestSerializer


class TestAPIView(RetrieveAPIView):
    queryset = TestModel.objects.filter(is_active=True)
    serializer_class = TestSerializer
    lookup_field = "id"
    # def post(self, request: Request):
    #     data = request.data
    #     sr = TestSerializer(data=data)
    #     if sr.is_valid(raise_exception=True):
    #         md = sr.save()
    #         return Response(TestSerializer(md).data)

    #     return error_response("No se pudo crear el recurso")
