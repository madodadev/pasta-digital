from django.urls import path
from . import views

urlpatterns = [
    path('<int:modulo>/', views.resultados, name='resultados-modulo'),
    path('setResultados/', views.setResultados),
    path('ri1/<int:modulo>/<int:estudante>/', views.estudanteResultados, name='estudate-resultados'),
    path('pauta/<int:modulo>/', views.pautaDoc, name='pauta-modulo'),
]