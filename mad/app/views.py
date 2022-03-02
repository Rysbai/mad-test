from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from mad.app.repositories import PatientRepository
from mad.app.serializers import PatientSerializer, LoginViaUsernameAndPasswordSerializer
from mad.app.services import LoginViaUsernameAndPasswordService


class LoginViaUsernameAndPasswordAPIView(APIView):
    def post(self, request):
        serializer = LoginViaUsernameAndPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = LoginViaUsernameAndPasswordService.factory().execute(**serializer.validated_data)
        return Response({"token": token})


class PatientListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PatientSerializer

    def get_queryset(self):
        return PatientRepository.factory().get_last_three()
