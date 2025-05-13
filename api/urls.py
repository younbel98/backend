from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.CustomAuthToken.as_view(), name="login-view"),
    path("users/", views.UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:user_id>", views.UserDetailView.as_view(), name="user-detail"),
    path("years/", views.YearListCreate.as_view(), name="year-create-view"),
    path(
        "years/<int:year>",
        views.YearRetrieveUpdateDestroy.as_view(),
        name="year-retrieve-update-destroy-view",
    ),
    path("tribes/", views.TribeListCreate.as_view(), name="tribe-create-view"),
    path(
        "tribes/<str:name>",
        views.TribeRetrieveUpdateDestroy.as_view(),
        name="tribe-retrieve-update-destroy-view",
    ),
    path(
        "health_status/",
        views.HealthStatusListCreate.as_view(),
        name="healthStatus-create-view",
    ),
    path(
        "health_status/<str:name>",
        views.HealthStatusRetrieveUpdateDestroy.as_view(),
        name="healthStatus-retrieve-update-destroy-view",
    ),
    path(
        "social_status/",
        views.SocialStatusListCreate.as_view(),
        name="socialStatus-create-view",
    ),
    path(
        "social_status/<str:name>",
        views.SocialStatusRetrieveUpdateDestroy.as_view(),
        name="socialStatus-retrieve-update-destroy-view",
    ),
    path(
        "professions/",
        views.ProfessionListCreate.as_view(),
        name="professions-create-view",
    ),
    path(
        "professions/<str:name>",
        views.ProfessionRetrieveUpdateDestroy.as_view(),
        name="professions-retrieve-update-destroy-view",
    ),
    path("handlers/", views.HandlerListCreate.as_view(), name="handler-create-view"),
    path(
        "handlers/<int:pk>",
        views.HandlerRetrieveUpdateDestroy.as_view(),
        name="handler-retrieve-update-destroy-view",
    ),
    path("handlers/filter/", views.HandlerFilter.as_view(), name="handler-filter-view"),
    path(
        "handler-family/",
        views.HandlerFamiliesList.as_view(),
        name="handler-families-view",
    ),
    path("families/", views.FamilyListCreate.as_view(), name="family-create-view"),
    path("view/<int:id>", views.FamilyRetrieve.as_view(), name="family-retrieve-view"),
    path(
        "families/<int:id>",
        views.FamilyRetrieveUpdateDestroy.as_view(),
        name="family-retrieve-update-destroy-view",
    ),
    path(
        "families/filter/<int:year>",
        views.FamilySortFilterView.as_view(),
        name="family-filter-view",
    ),
    path("children/", views.ChildList.as_view(), name="child-list-view"),
    path("add-children/", views.ChildCreate.as_view(), name="child-create-view"),
    path(
        "view-child/<int:pk>", views.ChildRetrieve.as_view(), name="child-retrieve-view"
    ),
    path(
        "child/<int:pk>",
        views.ChildUpdateDestroy.as_view(),
        name="child-update-destroy-view",
    ),
    path("spouces/", views.SpouceListCreate.as_view(), name="spouce-create-view"),
    path(
        "view-spouce/<int:pk>",
        views.SpouceRetrieve.as_view(),
        name="spouce-retrieve-view",
    ),
    path(
        "spouces/<int:pk>",
        views.SpouceUpdateDestroy.as_view(),
        name="spouce-update-destroy-view",
    ),
    path(
        "custody/",
        views.PersonInCustodyListCreate.as_view(),
        name="person-in-custody-create-view",
    ),
    path(
        "view-custody/<int:pk>",
        views.PersonInCustodyRetrieve.as_view(),
        name="person-in-custody-retrieve-view",
    ),
    path(
        "custody/<int:pk>",
        views.PersonInCustodyUpdateDestroy.as_view(),
        name="person-in-custody-update-destroy-view",
    ),
    path("delivery/", views.DeliveryListCreate.as_view(), name="delivery-create-view"),
    path(
        "delivery/<int:pk>",
        views.DeliveryRetrieveUpdateDestroy.as_view(),
        name="delivery-retrieve-update-destroy-view",
    ),
    path(
        "delivery/filter/", views.DeliveryFilter.as_view(), name="delivery-filter-view"
    ),
    path(
        "product_deliveries/",
        views.ProductDeliveryList.as_view(),
        name="product-delivery-view",
    ),
    path("products/", views.ProductListCreate.as_view(), name="product-create-view"),
    path(
        "product/<int:pk>",
        views.ProductRetrieveUpdateDestroy.as_view(),
        name="product-retrieve-update-destroy-view",
    ),
    path("products/filter/", views.ProductFilter.as_view(), name="product-filter-view"),
    path("donations/", views.DonationListCreate.as_view(), name="donation-create-view"),
    path(
        "donation/<int:pk>",
        views.DonationRetrieveUpdateDestroy.as_view(),
        name="donation-retrieve-update-destroy-view",
    ),
    path(
        "product_donations/",
        views.ProductDonationList.as_view(),
        name="product-donation-view",
    ),
    path(
        "donations/filter/", views.DonationFilter.as_view(), name="donation-filter-view"
    ),
    path("files/", views.DocumentListCreate.as_view(), name="document-create-view"),
    path(
        "file/<int:pk>",
        views.DocumentRetrieveUpdateDestroy.as_view(),
        name="document-retrieve-update-destroy-view",
    ),
    path("stats/<int:year>", views.StatsView.as_view(), name="stats-view"),
    path("print-family/<int:id>", views.PrintFamilyView.as_view(), name="stats-view"),
    path(
        "family/delete_multiple/",
        views.FamiliesBulkDeleteAPIView.as_view(),
        name="family-bulk-delete",
    ),
    path(
        "child/delete_multiple/",
        views.ChildrenBulkDeleteAPIView.as_view(),
        name="child-bulk-delete",
    ),
    path(
        "handler/delete_multiple/",
        views.HandlersBulkDeleteAPIView.as_view(),
        name="handler-bulk-delete",
    ),
    path(
        "product/delete_multiple/",
        views.ProductsBulkDeleteAPIView.as_view(),
        name="handler-bulk-delete",
    ),
    path(
        "delivery/delete_multiple/",
        views.DeliveriesBulkDeleteAPIView.as_view(),
        name="handler-bulk-delete",
    ),
    path(
        "donation/delete_multiple/",
        views.DonationsBulkDeleteAPIView.as_view(),
        name="handler-bulk-delete",
    ),
]
