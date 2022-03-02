from django.urls import path

from mad.app.views import PatientListAPIView, LoginViaUsernameAndPasswordAPIView

app_name = "app"
urlpatterns = [
    path("login", LoginViaUsernameAndPasswordAPIView.as_view(), name="login"),
    path("patients", PatientListAPIView.as_view(), name="patients"),
]
