from django.urls import path

from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('login/', views.LoginInstitucionalView.as_view(), name='login'),
    path('logout/', views.LogoutInstitucionalView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('prestamos/solicitar/', views.solicitar, name='solicitar_prestamo'),
    path('prestamos/mios/', views.mis_prestamos, name='mis_prestamos'),
    path('prestamos/devolver/<int:prestamo_id>/', views.devolver, name='devolver_prestamo'),
]
