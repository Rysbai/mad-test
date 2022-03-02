from typing import TypeVar, List, Union, Generic

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from mad.app.exceptions import MadNotFound
from mad.app.models import Patient

T = TypeVar("T")


class BaseModelRepository(Generic[T]):
    model: models.Model

    def __init__(self, model: T):
        self.model = model

    def get_by_id(self, instance_id: int or str) -> T:
        try:
            return self.model.objects.get(id=instance_id)
        except models.ObjectDoesNotExist:
            raise MadNotFound()

    def create(self, **data) -> T:
        instance = self.model(**data)
        instance.save()
        return instance

    def update_one(self, instance_id: int, **update_data):
        self.model.objects.filter(id=instance_id).update(**update_data)

    def all(self) -> Union[QuerySet, List[T]]:
        return self.model.objects.all()


class PatientRepository(BaseModelRepository):
    def get_last_three(self):
        return self.model.objects.all()[:3]

    @classmethod
    def factory(cls) -> "PatientRepository":
        return cls(Patient)


class UserRepository(BaseModelRepository):
    def get_by_username(self, username: str):
        try:
            return self.model.objects.get(username=username)
        except models.ObjectDoesNotExist:
            raise MadNotFound()

    @classmethod
    def factory(cls) -> "UserRepository":
        return cls(User)
