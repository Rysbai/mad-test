from rest_framework import serializers

from mad.app.models import Diagnose, Patient


class DiagnoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnose
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    diagnoses = DiagnoseSerializer(many=True)

    class Meta:
        model = Patient
        fields = "__all__"


class LoginViaUsernameAndPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
