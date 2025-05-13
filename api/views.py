from django.db.models import Count, F, Q, Value, CharField
from django.db.models.functions import TruncMonth, Lower, Concat
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from datetime import datetime, date


class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]  # Allow unauthenticated users to log in

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            year, created = Year.objects.get_or_create(year=now().year)
            return Response(
                {
                    "token": token.key,
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "year": {"id": year.id, "year": year.year},
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """Retrieve users (admin can see all, normal users see only themselves)."""
        user = request.user
        if user.is_staff:
            users = User.objects.all()  # Admins can see all users
        else:
            users = User.objects.filter(id=user.id)  # Normal users see only themselves

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    Handles retrieving and updating a specific user.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, user_id, request):
        """Ensure users can only access their own profile unless they are admin."""
        if request.user.is_staff:
            return get_object_or_404(User, id=user_id)  # Admin can access any user
        return get_object_or_404(
            User, id=request.user.id
        )  # Normal users can access only themselves

    def get(self, request, user_id):
        """Retrieve a specific user."""
        user = self.get_object(user_id, request)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, user_id):
        user = self.get_object(user_id, request)

        old_password = request.data.get("old_password")
        if old_password and not check_password(old_password, user.password):
            return Response(
                {"old_password": "Incorrect password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data
        new_password = make_password(data["password"])
        data["password"] = new_password
        serializer = UserSerializer(
            user, data=data, partial=True
        )  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YearListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Year.objects.order_by("year")
    serializer_class = YearSerializer


class YearRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    lookup_field = "year"


class TribeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer


class TribeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer
    lookup_field = "name"


class HealthStatusListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = HealthStatus.objects.all()
    serializer_class = HealthStatusSerializer


class HealthStatusRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = HealthStatus.objects.all()
    serializer_class = HealthStatusSerializer
    lookup_field = "name"


class SocialStatusListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = SocialStatus.objects.all()
    serializer_class = SocialStatusSerializer


class SocialStatusRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = SocialStatus.objects.all()
    serializer_class = SocialStatusSerializer
    lookup_field = "name"


class ProfessionListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class ProfessionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    lookup_field = "name"


class HandlerListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Handler.objects.all()
    serializer_class = HandlerSerializer


class HandlerRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Handler.objects.all()
    serializer_class = HandlerSerializer
    lookup_field = "pk"


class HandlerFilter(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = HandlerListSerializer

    def get(self, request: Request, *args, **kwargs):
        sort = request.query_params.getlist("sort", ["-id"])
        search = request.query_params.get("search", "")
        types = request.query_params.getlist("types", [])

        handler_query = Handler.objects.annotate(
            full_name=Concat(
                "lastName",
                Value(" "),
                "firstName",
                Value(" "),
                output_field=CharField(),
            ),
        )
        query = Q(full_name__icontains=search) & Q(type__in=types)
        queryset = handler_query.filter(query)
        queryset = queryset.order_by(*case_insensitive_sort(queryset, sort))
        queryset = queryset.distinct()

        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class HandlerFamiliesList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = FamilyCreateSerializer

    def get(self, request: Request, *args, **kwargs):
        try:
            year = request.query_params.get(
                "year", str(Year.objects.order_by("year").last().year)
            )
            id = request.query_params.get("id", "")
            if id:
                handler = Handler.objects.get(pk=id)
                familiyList = handler.family_set.filter(year__year=year)
                serializer = FamilyListSerializer(instance=familiyList, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data={"error": "no id"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                data={"error": e.__str__()}, status=status.HTTP_400_BAD_REQUEST
            )


class FamilyListCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = FamilyCreateSerializer

    def get(self, request: Request, *args, **kwargs):
        year = request.query_params.get(
            "year", str(Year.objects.order_by("year").last().year)
        )
        familiyList = Family.objects.filter(year__year=year)
        serializer = FamilySerializer(instance=familiyList, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FamilyRetrieve(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request: Request, id, *args, **kwargs):
        try:
            familiy = Family.objects.get(pk=id)
            serializer = FamilySerializer(instance=familiy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={"error": "no id"}, status=status.HTTP_400_BAD_REQUEST)


class FamilyRetrieveUpdateDestroy(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request: Request, id, *args, **kwargs):
        try:
            familiy = Family.objects.get(pk=id)
            serializer = FamilyCreateSerializer(instance=familiy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={"error": "no id"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, id, *args, **kwargs):
        data = request.data
        if data:
            familiy = Family.objects.get(pk=id)
            serializer = FamilyCreateSerializer(familiy, data=data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"error": "no data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        familiy = Family.objects.get(pk=id)
        familiy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FamilySortFilterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = FamilyListSerializer

    def get(self, request: Request, year, *args, **kwargs):
        sort = request.query_params.getlist("sort", ["-id"])
        search = request.query_params.get("search", "")
        professions = request.query_params.getlist("p", [])
        socials = request.query_params.getlist("s", [])
        healths = request.query_params.getlist("h", [])
        min_age = int(request.query_params.get("min_age", 0))
        max_age = int(request.query_params.get("max_age", 1000))
        min_children_age = int(request.query_params.get("min_children_age", 0))
        max_children_age = int(request.query_params.get("max_children_age", 1000))
        today = now().date()
        has_children = request.query_params.get("has_children", "")
        get_children = request.query_params.get("get_children", "")

        if not get_children:
            family_query = Family.objects.annotate(
                full_name=Concat(
                    "lastName",
                    Value(" "),
                    "firstName",
                    Value(" "),
                    "father",
                    Value(" "),
                    "grandFather",
                    output_field=CharField(),
                ),
                spouces_full_name=Concat(
                    "spouces__lastName",
                    Value(" "),
                    "spouces__firstName",
                    output_field=CharField(),
                ),
                child_full_name=Concat(
                    "lastName",
                    Value(" "),
                    "children__firstName",
                    Value(" "),
                    "firstName",
                    Value(" "),
                    "father",
                    Value(" "),
                    "grandFather",
                    output_field=CharField(),
                ),
                handler_full_name=Concat(
                    "handler__lastName",
                    Value(" "),
                    "handler__firstName",
                    output_field=CharField(),
                ),
                personincustody_full_name=Concat(
                    "personincustody__lastName",
                    Value(" "),
                    "personincustody__firstName",
                    output_field=CharField(),
                ),
            ).only("id", "lastName", "firstName", "father", "grandFather")

            query = (
                Q(full_name__icontains=search)
                | Q(tribe__name__icontains=search)
                | Q(phoneNumber1__icontains=search)
                | Q(phoneNumber2__icontains=search)
                | Q(barcode__icontains=search)
                | Q(healthStatus__name__icontains=search)
                | Q(address__icontains=search)
                | Q(child_full_name__icontains=search)
                | Q(handler_full_name__icontains=search)
                | Q(spouces_full_name__icontains=search)
                | Q(personincustody_full_name__icontains=search)
            )

            # Apply additional filters only if they are provided
            if socials:
                query &= Q(socialStatus__name__in=socials)
            if professions:
                query &= Q(profession__name__in=professions)
            if healths:
                query &= Q(healthStatus__name__in=healths)

            query &= Q(
                day_of_birth__gte=today.replace(year=today.year - max_age - 1),
                day_of_birth__lte=today.replace(year=today.year - min_age),
            )

            if has_children:
                query &= Q(
                    children__day_of_birth__gte=today.replace(
                        year=today.year - max_children_age
                    ),
                    children__day_of_birth__lte=today.replace(
                        year=today.year - min_children_age
                    ),
                )

            queryset = (
                family_query.filter(year__year=year)
                .filter(query)
                .distinct()
                .order_by(*sort)
            )

            serializer = self.serializer_class(instance=queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            children_query = Child.objects.annotate(
                child_full_name=Concat(
                    "family__lastName",
                    Value(" "),
                    "firstName",
                    Value(" "),
                    "family__firstName",
                    Value(" "),
                    "family__father",
                    Value(" "),
                    "family__grandFather",
                    output_field=CharField(),
                ),
            ).only("id", "firstName", "family__lastName", "family__firstName")

            query = Q(child_full_name__icontains=search) & Q(
                day_of_birth__gte=today.replace(year=today.year - max_children_age),
                day_of_birth__lte=today.replace(year=today.year - min_children_age),
            )

            queryset = children_query.filter(query).distinct().order_by(*sort)

            serializer = ChildListSerializer(instance=queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChildList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ChildListSerializer

    def get(self, request: Request, *args, **kwargs):
        id = request.query_params.get("id", "")
        if id:
            try:
                family = Family.objects.get(pk=id)
                childrenList = family.children.all()
                serializer = ChildListSerializer(instance=childrenList, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except family.DoesNotExist:
                return Response({"error": "no id"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no id"}, status=status.HTTP_200_OK)


class ChildCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ChildSerializer

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    lookup_field = "pk"


class ChildRetrieve(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Child.objects.all()
    serializer_class = ChildListSerializer
    lookup_field = "pk"


class SpouceListCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SpouceSerializer

    def get(self, request: Request, *args, **kwargs):
        id = request.query_params.get("id", "")
        if id:
            try:
                family = Family.objects.get(pk=id)
                spoucesList = family.spouces.all()
                serializer = SpouceListSerializer(instance=spoucesList, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except family.DoesNotExist:
                return Response(
                    {"message": "wrong id Porvided"}, status=status.HTTP_200_OK
                )
        else:
            return Response({"message": "No id Porvided"}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpouceUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Spouce.objects.all()
    serializer_class = SpouceSerializer
    lookup_field = "pk"


class SpouceRetrieve(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Spouce.objects.all()
    serializer_class = SpouceListSerializer
    lookup_field = "pk"


class PersonInCustodyListCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = PersonInCustodySerializer

    def get(self, request: Request, *args, **kwargs):
        id = request.query_params.get("id", "")
        if id:
            list = Family.objects.get(pk=id).personincustody_set.all()
            serializer = PersonInCustodyListSerializer(instance=list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no id"}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonInCustodyUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PersonInCustody.objects.all()
    serializer_class = PersonInCustodySerializer
    lookup_field = "pk"


class PersonInCustodyRetrieve(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = PersonInCustody.objects.all()
    serializer_class = PersonInCustodyViewSerializer
    lookup_field = "pk"


class DocumentListCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request: Request, *args, **kwargs):
        family_id = request.query_params.get("family_id", "")
        if family_id:
            list = Family.objects.get(pk=family_id).files.all()
            serializer = self.serializer_class(instance=list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            list = Document.objects.all()
            serializer = self.serializer_class(instance=list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        try:
            file = request.data["file"]
            owner = Family.objects.get(pk=request.data["owner"])
            document = Document.objects.create(file=file, owner=owner)
            return Response(
                data=self.serializer_class(document).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": e.__str__()}, status=status.HTTP_400_BAD_REQUEST)


class DocumentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = "pk"


class DeliveryListCreate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DeliverySerializer

    def get(self, request: Request, *args, **kwargs):
        id = request.query_params.get("id", "")
        if id:
            list = Family.objects.get(pk=id).delivery_set.all().order_by("date")
            serializer = DeliveryListSerializer(instance=list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no id"}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    lookup_field = "pk"


class DeliveryFilter(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DeliveryFilterSerializer

    def get(self, request: Request, *args, **kwargs):
        product_id = request.query_params.get("product_id", None)
        sort = request.query_params.getlist("sort", ["date"])
        search = request.query_params.get("search", "")
        today = date.today()
        start_of_year = date(today.year, 1, 1)

        since = request.query_params.get("since", start_of_year)
        till = request.query_params.get("till", today)

        delivery_query = Delivery.objects.annotate(
            beneficiary_full_name=Concat(
                "beneficiary__lastName", Value(" "), "beneficiary__firstName"
            )
        )
        query = (
            Q(occasion__icontains=search)
            | Q(product__category__icontains=search)
            | Q(product__type__icontains=search)
            | Q(beneficiary_full_name__icontains=search)
        )
        if since and till:
            query = query & (Q(date__gte=since) & Q(date__lte=till))
        elif since:
            query = query & (Q(date__gte=since))
        elif till:
            query = query & (Q(date__lte=till))

        if product_id:
            query = query & Q(product__id=product_id)

        queryset = delivery_query.filter(query)
        queryset = queryset.order_by(*case_insensitive_sort(queryset, sort))
        queryset = queryset.distinct()

        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductDeliveryList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DeliverySerializer

    def get(self, request: Request, *args, **kwargs):
        id = request.query_params.get("id", "")
        if id:
            list = Product.objects.get(pk=id).delivery_set.all().order_by("date")
            serializer = DeliveryListSerializer(instance=list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no id"}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"


class ProductFilter(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductSerializer

    def get(self, request: Request, *args, **kwargs):
        sort = request.query_params.getlist("sort", ["-id"])
        search = request.query_params.get("search", "")

        query = Q(category__icontains=search) | Q(type__icontains=search)
        queryset = Product.objects.filter(query)
        queryset = queryset.order_by(*case_insensitive_sort(queryset, sort))
        queryset = queryset.distinct()

        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StatsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, year: int, *args, **kwargs):

        today = now().date()
        months = [(today.year, today.month - i) for i in range(12)]
        months = [(y - (m <= 0), m + 12 if m <= 0 else m) for y, m in months]
        months = [datetime(year, month, 1).date() for year, month in months]

        queryset = (
            Delivery.objects.annotate(month=TruncMonth("date"))
            .filter(month__gte=months[-1])
            .values(month=F("month"))
            .annotate(total=Count("id"))
            .order_by("month")
        )
        queryset_dict = {entry["month"]: entry["total"] for entry in queryset}
        query = [
            {"month": month, "total": queryset_dict.get(month, 0)} for month in months
        ]
        query.reverse()
        last_12_months_deliveries = {"months": [], "totals": []}
        for item in query:
            last_12_months_deliveries["months"].append(str(item["month"]).split("-")[1])
            last_12_months_deliveries["totals"].append(item["total"])

        queryset = (
            Donation.objects.annotate(month=TruncMonth("date"))
            .filter(month__gte=months[-1])
            .values(month=F("month"))
            .annotate(total=Count("id"))
            .order_by("month")
        )
        queryset_dict = {entry["month"]: entry["total"] for entry in queryset}
        query = [
            {"month": month, "total": queryset_dict.get(month, 0)} for month in months
        ]
        query.reverse()
        last_12_months_donations = {"months": [], "totals": []}
        for item in query:
            last_12_months_donations["months"].append(str(item["month"]).split("-")[1])
            last_12_months_donations["totals"].append(item["total"])

        last_20_years = list(
            Year.objects.order_by("-year")[:20].values_list("year", flat=True)
        )
        queryset = (
            Family.objects.annotate(year_=F("year__year"))
            .values("year_")
            .annotate(total=Count("id"))
            .order_by("year_")
        )
        queryset_dict = {entry["year_"]: entry["total"] for entry in queryset}
        query = [
            {"year_": year, "total": queryset_dict.get(year, 0)}
            for year in last_20_years
        ]
        query.reverse()
        last_20_years_families = {"years": [], "totals": []}
        for item in query:
            last_20_years_families["years"].append(str(item["year_"]))
            last_20_years_families["totals"].append(item["total"])

        queryset = HealthStatus.objects.annotate(total=Count("family")).values(
            "name", "total"
        )
        health_status = {"status": [], "totals": []}
        for item in queryset:
            if item["total"] > 0:
                health_status["status"].append(item["name"])
                health_status["totals"].append(item["total"])

        queryset = SocialStatus.objects.annotate(total=Count("family")).values(
            "name", "total"
        )
        social_status = {"status": [], "totals": []}
        for item in queryset:
            if item["total"] > 0:
                social_status["status"].append(item["name"])
                social_status["totals"].append(item["total"])

        queryset = Profession.objects.annotate(total=Count("family")).values(
            "name", "total"
        )
        proffession_status = {"status": [], "totals": []}
        for item in queryset:
            if item["total"] > 0:
                proffession_status["status"].append(item["name"])
                proffession_status["totals"].append(item["total"])

        queryset = Tribe.objects.annotate(total=Count("family")).values("name", "total")
        tribes = {}
        for item in queryset:
            tribes[item["name"]] = item["total"]

        stats = {
            "totals": [
                list(
                    Family.objects.filter(year__year=year)
                    .aggregate(
                        total=Count("id"),
                    )
                    .values()
                )[0],
                list(
                    Child.objects.filter(family__year__year=year)
                    .aggregate(
                        total=Count("id"),
                    )
                    .values()
                )[0],
                list(
                    Spouce.objects.filter(family__year__year=year)
                    .aggregate(
                        total=Count("id"),
                    )
                    .values()
                )[0],
                list(
                    PersonInCustody.objects.filter(family__year__year=year)
                    .aggregate(
                        total=Count("id"),
                    )
                    .values()
                )[0],
                list(
                    Handler.objects.aggregate(
                        total=Count("id"),
                    ).values()
                )[0],
            ],
            "don_delv": {
                "months": (last_12_months_donations["months"]),
                "donations": (last_12_months_donations["totals"]),
                "deliveries": (last_12_months_deliveries["totals"]),
            },
            "families": (last_20_years_families),
            "status": {
                "health": (health_status),
                "social": (social_status),
                "profession": (proffession_status),
            },
            "tribes": (tribes),
        }
        return Response(stats)


class DonationListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer


class DonationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    lookup_field = "pk"


class ProductDonationList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DonationFilterSerializer

    def get(self, request: Request, *args, **kwargs):
        id = request.query_params.get("id", "")
        if id:
            list = Product.objects.get(pk=id).donation_set.all().order_by("date")
            serializer = self.serializer_class(instance=list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "no id"}, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationFilter(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = DonationFilterSerializer

    def get(self, request: Request, *args, **kwargs):
        product_id = request.query_params.get("product_id", None)
        sort = request.query_params.getlist("sort", ["date"])
        search = request.query_params.get("search", "")
        today = date.today()
        start_of_year = date(today.year, 1, 1)

        since = request.query_params.get("since", start_of_year)
        till = request.query_params.get("till", today)

        query = (
            Q(donor__icontains=search)
            | Q(product__category__icontains=search)
            | Q(product__type__icontains=search)
        )
        if since and till:
            query = query & (Q(date__gte=since) & Q(date__lte=till))
        elif since:
            query = query & (Q(date__gte=since))
        elif till:
            query = query & (Q(date__lte=till))

        if product_id:
            query = query & Q(product__id=product_id)

        queryset = Donation.objects.filter(query)
        queryset = queryset.order_by(*case_insensitive_sort(queryset, sort))
        queryset = queryset.distinct()

        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PrintFamilyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, id, *args, **kwargs):
        data = {}

        family = get_object_or_404(Family, id=id)
        data["info"] = FamilySerializer(family).data

        if data["info"]["handler"] is not None:
            handler = get_object_or_404(Handler, id=data["info"]["handler"])
            data["info"].pop("handler")
            data["handler"] = HandlerSerializer(handler).data
        else:
            data["handler"] = None

        spouces = Spouce.objects.filter(family=family)
        data["spouces"] = SpouceListSerializer(spouces, many=True).data

        children = Child.objects.filter(family=family)
        data["children"] = ChildListSerializer(children, many=True).data

        custodies = PersonInCustody.objects.filter(family=family)
        data["custodies"] = PersonInCustodyListSerializer(custodies, many=True).data

        return Response(data)


class FamiliesBulkDeleteAPIView(APIView):
    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = Family.objects.filter(id__in=ids).delete()
        return Response(
            {"message": f"Deleted {deleted} objects"}, status=status.HTTP_200_OK
        )


class ChildrenBulkDeleteAPIView(APIView):
    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = Child.objects.filter(id__in=ids).delete()
        return Response(
            {"message": f"Deleted {deleted} objects"}, status=status.HTTP_200_OK
        )


class HandlersBulkDeleteAPIView(APIView):
    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = Handler.objects.filter(id__in=ids).delete()
        return Response(
            {"message": f"Deleted {deleted} objects"}, status=status.HTTP_200_OK
        )


class ProductsBulkDeleteAPIView(APIView):
    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = Product.objects.filter(id__in=ids).delete()
        return Response(
            {"message": f"Deleted {deleted} objects"}, status=status.HTTP_200_OK
        )


class DonationsBulkDeleteAPIView(APIView):
    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = Donation.objects.filter(id__in=ids).delete()
        return Response(
            {"message": f"Deleted {deleted} objects"}, status=status.HTTP_200_OK
        )


class DeliveriesBulkDeleteAPIView(APIView):
    def delete(self, request):
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "No IDs provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = Delivery.objects.filter(id__in=ids).delete()
        return Response(
            {"message": f"Deleted {deleted} objects"}, status=status.HTTP_200_OK
        )


def case_insensitive_sort(queryset, fields):
    ci_fields = []
    model = queryset.model  # Dynamically get the model from queryset

    for field in fields:
        is_desc = field.startswith("-")
        field_name = field[1:] if is_desc else field

        try:
            field_type = model._meta.get_field(field_name).get_internal_type()

            # Apply LOWER only to text-based fields
            if field_type in ["CharField", "TextField"]:
                annotated_field = Lower(field_name)
                ci_fields.append(
                    annotated_field.desc() if is_desc else annotated_field.asc()
                )
            else:
                ci_fields.append(field)  # Keep original field for non-text fields
        except:
            ci_fields.append(field)  # If the field does not exist, keep it as is

    return ci_fields
