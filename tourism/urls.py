from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('spots/', views.tourist_spots, name='tourist_spots'),
    path('spots/<int:spot_id>/reserve/', views.book_reservation, name='book_reservation'),
    path('map/', views.map_view, name='map_view'),
    path('reserve/<int:spot_id>/', views.book_reservation, name='book_reservation'),
    path('book/<int:spot_id>/', views.book_reservation, name='book_reservation'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('reservation-success/<int:pk>/', views.reservation_success, name='reservation_success'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('officials-dashboard/', views.officials_dashboard, name='officials_dashboard'),
    path('officials/delete-reservation/<int:pk>/', views.delete_reservation_official, name='delete_reservation_official'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
