from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
        }


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ["id", "year"]


class TribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribe
        fields = ["id", "name"]


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ["id", "name"]


class SocialStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialStatus
        fields = ["id", "name"]


class HealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthStatus
        fields = ["id", "name"]


####
class HandlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handler
        fields = [
            "id",
            "lastName",
            "firstName",
            "day_of_birth",
            "type",
            "phoneNumber",
            "fullName",
        ]


class HandlerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handler
        fields = ["id", "fullName", "type", "phoneNumber", "day_of_birth"]


####
class FamilyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = [
            "id",
            "year",
            "barcode",
            "handler",
            "tribe",
            "lastName",
            "firstName",
            "father",
            "grandFather",
            "day_of_birth",
            "age",
            "idNumber",
            "healthStatus",
            "socialStatus",
            "profession",
            "phoneNumber1",
            "phoneNumber2",
            "address",
            "email",
        ]
        extra_kwargs = {
            "handler": {"allow_null": True},
        }


class FamilySerializer(serializers.ModelSerializer):
    healthStatus = serializers.StringRelatedField(
        source="healthStatus.name", read_only=True, allow_null=True
    )
    socialStatus = serializers.StringRelatedField(
        source="socialStatus.name", read_only=True, allow_null=True
    )
    profession = serializers.StringRelatedField(
        source="profession.name", read_only=True, allow_null=True
    )
    tribe = serializers.StringRelatedField(
        source="tribe.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Family
        fields = [
            "id",
            "year",
            "barcode",
            "handler",
            "tribe",
            "lastName",
            "firstName",
            "father",
            "grandFather",
            "day_of_birth",
            "age",
            "idNumber",
            "healthStatus",
            "socialStatus",
            "profession",
            "phoneNumber1",
            "phoneNumber2",
            "address",
            "email",
        ]


class FamilyListSerializer(serializers.ModelSerializer):
    # donations = serializers.StringRelatedField(source='delivery_set', read_only=True)
    # children_count = serializers.IntegerField(read_only=True)
    healthStatus = serializers.StringRelatedField(
        source="healthStatus.name", read_only=True, allow_null=True
    )
    socialStatus = serializers.StringRelatedField(
        source="socialStatus.name", read_only=True, allow_null=True
    )
    profession = serializers.StringRelatedField(
        source="profession.name", read_only=True, allow_null=True
    )
    handler = serializers.StringRelatedField(
        source="handler.fullName", read_only=True, allow_null=True
    )

    class Meta:
        model = Family
        fields = [
            "id",
            "barcode",
            "fullName",
            "father",
            "healthStatus",
            "socialStatus",
            "profession",
            "phoneNumber1",
            "age",
            "spouces_count",
            "children_count",
            "numberOfPersonInCustody",
            "handler",
        ]


###
class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        max_length=None,
        allow_empty_file=False,
        allow_null=True,
        use_url=True,
        required=False,
    )

    class Meta:
        model = Document
        # fields = '__all__'
        fields = ["id", "file", "date", "owner"]


####
class ChildSerializer(serializers.ModelSerializer):
    # healthStatus = serializers.StringRelatedField(source='healthStatus.name', read_only=True, allow_null=True)
    class Meta:
        model = Child
        # fields = '__all__'
        fields = [
            "id",
            "firstName",
            "day_of_birth",
            "gender",
            "mother",
            "healthStatus",
            "notes",
            "family",
            "age",
        ]


class ChildListSerializer(serializers.ModelSerializer):
    father = serializers.StringRelatedField(source="family", read_only=True)
    healthStatus = serializers.StringRelatedField(
        source="healthStatus.name", read_only=True, allow_null=True
    )
    barcode = serializers.StringRelatedField(
        source="family.barcode", read_only=True, allow_null=True
    )

    class Meta:
        model = Child
        # fields = '__all__'
        fields = [
            "id",
            "barcode",
            "father",
            "firstName",
            "age",
            "gender",
            "day_of_birth",
            "mother",
            "healthStatus",
            "notes",
        ]


####
class PersonInCustodySerializer(serializers.ModelSerializer):
    # healthStatus = serializers.StringRelatedField(source='healthStatus.name', read_only=True, allow_null=True)
    class Meta:
        model = PersonInCustody
        # fields = '__all__'
        fields = [
            "id",
            "lastName",
            "firstName",
            "day_of_birth",
            "gender",
            "relation",
            "healthStatus",
            "notes",
            "family",
        ]


class PersonInCustodyViewSerializer(serializers.ModelSerializer):
    healthStatus = serializers.StringRelatedField(
        source="healthStatus.name", read_only=True, allow_null=True
    )

    class Meta:
        model = PersonInCustody
        # fields = '__all__'
        fields = [
            "id",
            "lastName",
            "firstName",
            "day_of_birth",
            "gender",
            "relation",
            "healthStatus",
            "notes",
            "family",
        ]


class PersonInCustodyListSerializer(serializers.ModelSerializer):
    healthStatus = serializers.StringRelatedField(
        source="healthStatus.name", read_only=True, allow_null=True
    )

    class Meta:
        model = PersonInCustody
        # fields = '__all__'
        fields = [
            "id",
            "lastName",
            "firstName",
            "day_of_birth",
            "gender",
            "relation",
            "healthStatus",
            "notes",
        ]


###
class SpouceListSerializer(serializers.ModelSerializer):
    healthStatus = serializers.StringRelatedField(
        source="healthStatus.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Spouce
        # fields = '__all__'
        fields = [
            "id",
            "lastName",
            "firstName",
            "day_of_birth",
            "healthStatus",
            "notes",
            "family",
        ]


class SpouceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spouce
        # fields = '__all__'
        fields = [
            "id",
            "lastName",
            "firstName",
            "day_of_birth",
            "healthStatus",
            "notes",
            "family",
        ]


####
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ["id", "category", "type", "quantity"]


####
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        # fields = '__all__'
        fields = ["id", "donor", "product", "date", "quantity"]


class DonationFilterSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(source="product.category", read_only=True)
    type = serializers.StringRelatedField(source="product.type", read_only=True)

    class Meta:
        model = Donation
        # fields = '__all__'
        fields = ["id", "donor", "product", "type", "date", "quantity"]


####
class DeliveryListSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(source="product.category", read_only=True)
    type = serializers.StringRelatedField(source="product.type", read_only=True)
    beneficiary = serializers.StringRelatedField(
        source="beneficiary.fullName", read_only=True
    )

    class Meta:
        model = Delivery
        # fields = '__all__'
        fields = [
            "id",
            "occasion",
            "product",
            "type",
            "quantity",
            "date",
            "beneficiary",
        ]


class DeliveryFilterSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(source="product.category", read_only=True)
    type = serializers.StringRelatedField(source="product.type", read_only=True)
    beneficiary = serializers.StringRelatedField(
        source="beneficiary.fullName", read_only=True
    )

    class Meta:
        model = Delivery
        # fields = '__all__'
        fields = [
            "id",
            "occasion",
            "product",
            "type",
            "quantity",
            "date",
            "beneficiary",
        ]


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        # fields = '__all__'
        fields = ["id", "occasion", "product", "quantity", "date", "beneficiary"]
