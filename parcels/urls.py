from django.urls import path, reverse

from parcels import views as parcel_views

app_name = 'parcels'

urlpatterns = [
    path('cost-calculator/', parcel_views.CostCalculatorView.as_view(), name='cost_calculator'),
    path('parcels/', parcel_views.ParcelListView.as_view(), name='list'),
    path('parcels/<int:pk>/', parcel_views.ParcelDetailView.as_view(), name='detail'),
    path('parcels/<int:pk>/issue/create', parcel_views.IssueCreateView.as_view(), name='create_issue'),
    path('parcels/create/', parcel_views.ParcelCreateView.as_view(), name='create'),
    path('parcels/track', parcel_views.ParcelTrackView.as_view(), name='track'),
    path('parcels/<int:pk>/update', parcel_views.ParcelUpdateView.as_view(), name='update'),
    path('parcels/<int:pk>/delete', parcel_views.ParcelDeleteView.as_view(), name='delete'),
]
