from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('trips/new', views.new),
    path('trips/create', views.create),
    path('trips/<int:trip_id>', views.trip),
    path('trips/edit/<int:trip_id>', views.edit),
    path('trips/update/<int:trip_id>', views.update),
    path('trips/join/<int:trip_id>', views.join),
    path('trips/cancel/<int:trip_id>', views.cancel),
    path('trips/destroy/<int:trip_id>', views.destroy)
]