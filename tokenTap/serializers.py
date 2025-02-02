from rest_framework import serializers

from core.constraints import ConstraintVerification, get_constraint
from core.serializers import (
    ChainSerializer,
    ConstraintProviderSerializer,
    UserConstraintBaseSerializer,
)
from tokenTap.models import (
    Constraint,
    TokenDistribution,
    TokenDistributionClaim,
    UserConstraint,
)

from .constants import CONTRACT_ADDRESSES


class ConstraintSerializer(UserConstraintBaseSerializer, serializers.ModelSerializer):
    class Meta(UserConstraintBaseSerializer.Meta):
        ref_name = "TokenDistributionConstraint"
        model = Constraint

    def get_params(self, constraint: UserConstraint):
        c_class: ConstraintVerification = get_constraint(constraint.name)
        return [p.name for p in c_class.param_keys()]


class DetailResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        pass


class TokenDistributionSerializer(serializers.ModelSerializer):
    chain = ChainSerializer()
    constraints = serializers.SerializerMethodField()

    class Meta:
        model = TokenDistribution
        fields = [
            "id",
            "name",
            "distributor",
            "distributor_url",
            "discord_url",
            "twitter_url",
            "email_url",
            "telegram_url",
            "image_url",
            "token_image_url",
            "token",
            "token_address",
            "decimals",
            "amount",
            "is_one_time_claim",
            "chain",
            "distribution_id",
            "contract",
            "constraints",
            "constraint_params",
            "created_at",
            "start_at",
            "deadline",
            "max_number_of_claims",
            "number_of_claims",
            "total_claims_since_last_round",
            "notes",
            "necessary_information",
            "status",
            "rejection_reason",
            "tx_hash",
            "is_active",
            "is_expired",
            "is_maxed_out",
            "is_claimable",
        ]

    def get_constraints(self, distribution: TokenDistribution):
        reversed_constraints = distribution.reversed_constraints_list
        return [
            {
                **ConstraintSerializer(c).data,
                "is_reversed": True if str(c.pk) in reversed_constraints else False,
            }
            for c in distribution.constraints.all()
        ]


class SmallTokenDistributionSerializer(serializers.ModelSerializer):
    chain = ChainSerializer()
    constraints = ConstraintSerializer(many=True)

    class Meta:
        model = TokenDistribution
        fields = [
            "id",
            "name",
            "distributor",
            "distributor_url",
            "discord_url",
            "twitter_url",
            "image_url",
            "token",
            "token_address",
            "decimals",
            "amount",
            "is_one_time_claim",
            "chain",
            "distribution_id",
            "contract",
            "constraints",
            "constraint_params",
            "created_at",
            "deadline",
            "max_number_of_claims",
            "notes",
            "token_image_url",
        ]


class PayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenDistributionClaim
        fields = ["user_wallet_address", "token", "amount", "nonce", "signature"]


class TokenDistributionClaimSerializer(serializers.ModelSerializer):
    token_distribution = SmallTokenDistributionSerializer()
    payload = serializers.SerializerMethodField()

    class Meta:
        model = TokenDistributionClaim
        fields = [
            "id",
            "token_distribution",
            "user_profile",
            "user_wallet_address",
            "created_at",
            "payload",
            "status",
            "tx_hash",
        ]

    def get_payload(self, obj):
        return PayloadSerializer(obj).data


class TokenDistributionClaimResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    signature = TokenDistributionClaimSerializer()


class CreateTokenDistributionSerializer(
    serializers.ModelSerializer, ConstraintProviderSerializer
):
    class Meta:
        model = TokenDistribution
        fields = "__all__"

        read_only_fields = [
            "pk",
            "distributor_profile",
            "distribution_id",
            "created_at",
            "status",
            "rejection_reason",
            "is_active",
        ]

    def validate(self, data):
        data = super().validate(data)
        valid_chains = list(CONTRACT_ADDRESSES.keys())
        chain_id = data["chain"].chain_id
        if chain_id not in valid_chains:
            raise serializers.ValidationError({"chain": "Invalid value"})
        data["contract"] = CONTRACT_ADDRESSES[chain_id]
        data["distributor_profile"] = self.context["user_profile"]
        return data

    def create(self, validated_data):
        validated_data = self.save_constraint_files(validated_data)
        return super().create(validated_data)
