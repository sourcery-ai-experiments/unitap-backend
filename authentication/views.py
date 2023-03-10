import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from authentication.models import UserProfile, Wallet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from authentication.helpers import (
    BRIGHTID_SOULDBOUND_INTERFACE,
    verify_signature_eth_scheme,
)
from authentication.serializers import ProfileSerializer, WalletSerializer
from brightIDfaucet.settings import BRIGHT_ID_INTERFACE


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        address = request.data.get("username", None)
        signature = request.data.get("password", None)
        if not address or not signature:
            return Response({"message": "Invalid request"}, status=403)

        is_sponsored = BRIGHTID_SOULDBOUND_INTERFACE.check_sponsorship(address)
        if not is_sponsored:
            if BRIGHT_ID_INTERFACE.sponsor(str(address)) is not True:
                return Response({"message": "try again later."}, status=403)
            else:
                return Response(
                    {"message": "User is being sponsored. try again later."}, status=409
                )

        verified_signature = verify_signature_eth_scheme(address, signature)
        if not verified_signature:
            return Response({"message": "Invalid signature"}, status=403)

        (
            is_meet_verified,
            meet_context_ids,
        ) = BRIGHTID_SOULDBOUND_INTERFACE.get_verification_status(address, "Meet")
        (
            is_aura_verified,
            aura_context_ids,
        ) = BRIGHTID_SOULDBOUND_INTERFACE.get_verification_status(address, "Aura")

        is_nothing_verified = True

        if meet_context_ids is not None:
            context_ids = meet_context_ids
            is_nothing_verified = False
        elif aura_context_ids is not None:
            context_ids = aura_context_ids
            is_nothing_verified = False
        else:
            context_ids = [address]

        # if is_nothing_verified:
        #     return Response(
        #         {"message": "User is not verified. try again later."}, status=403
        #     )

        first_context_id = context_ids[-1]
        profile = UserProfile.objects.get_or_create(first_context_id=first_context_id)
        user = profile.user

        # get auth token for the user
        token, bol = Token.objects.get_or_create(user=user)
        print("token", token)

        # return Response({"token": token.key}, status=200)
        # return token and profile using profile serializer for profile
        return Response(
            {"token": token.key, "profile": ProfileSerializer(profile).data}, status=200
        )


class SetWalletAddressView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        address = request.data.get("address", None)
        wallet_type = request.data.get("wallet_type", None)
        if not address or not wallet_type:
            return Response({"message": "Invalid request"}, status=403)

        # get user profile
        user_profile = request.user.profile

        try:
            # check if wallet already exists
            Wallet.objects.get(user_profile=user_profile, wallet_type=wallet_type)
            return Response(
                {"message": f"{wallet_type} wallet address already set"}, status=403
            )
        # TODO change wallet creation
        except Wallet.DoesNotExist:
            # create wallet
            Wallet.objects.create(
                user_profile=user_profile, wallet_type=wallet_type, address=address
            )
            return Response(
                {"message": f"{wallet_type} wallet address set"}, status=200
            )


class GetWalletAddressView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wallet_type = request.data.get("wallet_type", None)
        if not wallet_type:
            return Response({"message": "Invalid request"}, status=403)

        # get user profile
        user_profile = request.user.profile

        try:
            # check if wallet already exists
            wallet = Wallet.objects.get(
                user_profile=user_profile, wallet_type=wallet_type
            )
            return Response({"address": wallet.address}, status=200)

        except Wallet.DoesNotExist:
            return Response(
                {"message": f"{wallet_type} wallet address not set"}, status=403
            )


class DeleteWalletAddressView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wallet_type = request.data.get("wallet_type", None)
        if not wallet_type:
            return Response({"message": "Invalid request"}, status=403)

        # get user profile
        user_profile = request.user.profile

        try:
            # check if wallet already exists
            wallet = Wallet.objects.get(
                user_profile=user_profile, wallet_type=wallet_type
            )
            wallet.delete()
            return Response(
                {"message": f"{wallet_type} wallet address deleted"}, status=200
            )

        except Wallet.DoesNotExist:
            return Response(
                {"message": f"{wallet_type} wallet address not set"}, status=403
            )


class GetWalletsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user_profile=self.request.user.profile)


class GetProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        token, bol = Token.objects.get_or_create(user=user)
        print("token", token)

        # return Response({"token": token.key}, status=200)
        # return token and profile using profile serializer for profile
        return Response(
            {"token": token.key, "profile": ProfileSerializer(user.profile).data},
            status=200,
        )
