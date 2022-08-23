
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

from paymeuz.serializers import SubscribeSerializer
from paymeuz.models import Transaction
from paymeuz.config import *
from paymeuz.methods import *





class CardCreateApiView(APIView):

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data)

        return Response(result)

    def card_create(self, validated_data):
        data = dict(
            id=validated_data['id'],
            method=CARD_CREATE,
            params=dict(
                card=dict(
                    number=validated_data['params']['card']['number'],
                    expire=validated_data['params']['card']['expire'],
                ),
                amount=validated_data['params']['amount'],
                save=validated_data['params']['save']
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CREATE)
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        result = self.card_get_verify_code(token)

        return result

    def card_get_verify_code(self, token):
        data = dict(
            method=CARD_GET_VERIFY_CODE,
            params=dict(
                token=token
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CREATE)
        result = response.json()
        if 'error' in result:
            return result

        result.update(token=token)
        return result


class CardVerifyApiView(APIView):

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data)

        return Response(result)

    def card_verify(self, validated_data):
        data = dict(
            id=validated_data['id'],
            method=CARD_VERIFY,
            params=dict(
                token=validated_data['params']['token'],
                code=validated_data['params']['code'],
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CREATE)
        result = response.json()

        return result


class PaymentApiView(APIView):

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['params']['token']
        result = self.receipts_create(token, serializer.validated_data)

        return Response(result)

    def receipts_create(self, token, validated_data):
        key_2 = validated_data['params']['account'][KEY_2] if KEY_2 else None
        data = dict(
            id=validated_data['id'],
            method=RECEIPTS_CREATE,
            params=dict(
                amount=validated_data['params']['amount'],
                account=dict(
                    KEY_1 = validated_data['params']['account'][KEY_1],
                    KEY_2 = key_2,
                )
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_RECEIPT)
        result = response.json()
        if 'error' in result:
            return result

        trans_id = result['result']['receipt']['_id']
        trans = Transaction()
        trans.create_transaction(
            trans_id=trans_id,
            request_id=result['id'],
            amount=result['result']['receipt']['amount'],
            account=result['result']['receipt']['account'],
            status=trans.PROCESS,
        )
        result = self.receipts_pay(trans_id, token)
        return result

    def receipts_pay(self, trans_id, token):
        data = dict(
            method=RECEIPTS_PAY,
            params=dict(
                id=trans_id,
                token=token,
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_RECEIPT)
        result = response.json()
        trans = Transaction()

        if 'error' in result:
            trans.update_transaction(
                trans_id=trans_id,
                status=trans.FAILED,
            )
            return result

        trans.update_transaction(
            trans_id=result['result']['receipt']['_id'],
            status=trans.PAID,
        )

        return result