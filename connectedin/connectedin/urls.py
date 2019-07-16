"""connectedin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import connectedin.settings as settings
from django.conf.urls.static import static
from perfis import views
from usuarios.views import RegistrarUsuarioView, pagina_de_superusuario
from django.contrib.auth import views as v
import postagem.views
import usuarios.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('perfil/<int:perfil_id>/', views.exibir, name='exibir'),
    path('perfil/alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('perfil/alterar_foto/', views.alterar_foto, name='alterar_foto'),
    path('perfil/<int:perfil_id>/convidar/', views.convidar, name='convidar'),
    path('perfil/<int:perfil_id>/remover-convite/', views.remover_convite, name='remover_convite'),
    path('perfil/dar-superuser/<int:perfil_id>/', views.dar_super_usuario, name='dar_super_usuario'),
    path('perfil/bloquear/<int:perfil_id>/', views.bloquear, name='bloquear'),
    path('perfil/desbloquear/<int:perfil_id>/', views.desbloquear, name='desbloquear'),
    path('perfil/desativar_perfil/', views.desativar_perfil, name='desativar_perfil'),
    path('perfil/reativar_perfil/', views.reativar_perfil, name='reativar_perfil'),    
    path('perfil/retirar-superuser/<int:perfil_id>/', views.retirar_super_usuario, name='retirar_super_usuario'),
    path('perfil/pesquisar/<str:nome>/', views.pesquisar_usuarios, name='pesquisar_usuarios'),
    path('convite/<int:convite_id>/aceitar/', views.aceitar, name='aceitar'),
    path('convite/<int:convite_id>/rejeitar/', views.rejeitar, name='rejeitar'),
    path('contatos/<int:id_contato>/desfazer/', views.desfazer_amizade, name='desfazer_amizade'),
    path('perfil/nova_postagem/', postagem.views.nova_postagem, name='nova_postagem'),
    path('postagem/gostar/<int:id_postagem>/', postagem.views.curtir_postagem, name='gostar'),
    path('postagem/nao-gostar/<int:id_postagem>/', postagem.views.nao_curtir_postagem, name='nao_gostar'),
    path('postagem/comentar/<int:id_postagem>/', postagem.views.comentar, name='comentar'),
    path('postagem/excluir/<int:id_postagem>/', postagem.views.excluir_postagem, name='excluir_postagem'),
    path('postagem/editar_postagem/<int:id_postagem>/', postagem.views.editar_postagem, name='editar_postagem'),
    path('postagem/remover_comentario/<int:id_comentario>/', postagem.views.remover_comentario, name='remover_comentario'),
    path('registrar/', RegistrarUsuarioView.as_view(), name='registrar'),
    path('pagina_de_superusuario/', usuarios.views.pagina_de_superusuario, name='pagina_de_superusuario'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('login/', v.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name='logout')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
