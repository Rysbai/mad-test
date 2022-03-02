from mad.app.models import Diagnose, Patient
from mad.app.serializers import DiagnoseSerializer, PatientSerializer


class BaseSerializerChecker:
    model_class = None
    FIELDS: list or dict
    serializer_class = None

    @classmethod
    def assert_equal(cls, first, second):
        if first is None or second is None:
            assert first is None and second is None
            return

        if isinstance(first, cls.model_class):
            first = cls.serializer_class(first).data
        if isinstance(second, cls.model_class):
            second = cls.serializer_class(second).data

        assert isinstance(cls.FIELDS, (dict, list))
        fields = cls.FIELDS if type(cls.FIELDS) == dict else {field: None for field in cls.FIELDS}

        for field_name, checker in fields.items():
            actual = first[field_name]
            expected = second[field_name]
            if checker:
                if checker == "self":
                    checker = cls.assert_equal
                checker(actual, expected)
                continue

            assert actual == expected

        assert set(fields.keys()) == set(first.keys())
        assert set(fields.keys()) == set(second.keys())

    @classmethod
    def assert_equal_list(cls, first: list, second: list):
        for f, s in zip(first, second):
            cls.assert_equal(f, s)


class DiagnoseSerializerChecker(BaseSerializerChecker):
    model_class = Diagnose
    serializer_class = DiagnoseSerializer
    FIELDS = ["id", "name"]


class PatientSerializerChecker(BaseSerializerChecker):
    model_class = Patient
    serializer_class = PatientSerializer
    FIELDS = {
        "id": None,
        "date_of_birth": None,
        "created_at": None,
        "diagnoses": DiagnoseSerializerChecker.assert_equal_list,
    }
