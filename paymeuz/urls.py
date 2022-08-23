from django.urls import path
from paymeuz.views import CardCreateApiView, CardVerifyApiView,PaymentApiView

urlpatterns = [
    path('card-create/', CardCreateApiView.as_view(), name='card_create'),
    path('card-verify/', CardVerifyApiView.as_view(), name='card_verify'),
    path('payment/', PaymentApiView.as_view(), name='payment'),
]