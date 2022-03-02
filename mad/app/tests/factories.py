import factory
from django.contrib.auth.models import User

from mad.app.models import Diagnose, Patient


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("first_name")
    password = factory.PostGenerationMethodCall("set_password", "admin")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class DiagnoseFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("first_name")

    class Meta:
        model = Diagnose


class PatientFactory(factory.django.DjangoModelFactory):
    date_of_birth = factory.Faker("date")

    class Meta:
        model = Patient

    @factory.post_generation
    def diagnoses(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for diagnose in extracted:
                self.diagnoses.add(diagnose)
