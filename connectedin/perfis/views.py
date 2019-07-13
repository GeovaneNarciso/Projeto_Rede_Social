from django.shortcuts import render
from .models import Perfil, Convite
from django.shortcuts import redirect
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

@login_required
def index(request):
    return render(request, 'index.html',
                  {'perfis': Perfil.objects.all(),
                   'perfil_logado': get_perfil_logado(request)})


@login_required
def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'perfil_logado': get_perfil_logado(request),
                   'ja_eh_contato': ja_eh_contato})


@login_required
def convidar(request, perfil_id):
    perfil_convidado = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.convidar(perfil_convidado)
    return redirect('index')


@login_required
def get_perfil_logado(request):
    return request.user.perfil


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


@login_required
def rejeitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.delete()
    return redirect('index')


@login_required
def desfazer_amizade(request, id_contato):
    contato_remove = Perfil.objects.get(id=id_contato)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.contatos.remove(contato_remove)
    
    return redirect('index')


@login_required
def alterar_senha(request):
    perfil_logado = get_perfil_logado(request).usuario
    senha_atual = request.POST['senha_atual']
    if check_password(senha_atual, perfil_logado.password):
        perfil_logado.set_password(request.POST['senha_nova'])
        perfil_logado.save()    
    return redirect('index')


@login_required
def dar_super_usuario(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id).usuario
    perfil.is_superuser = True
    perfil.save()
    return redirect('index')

@login_required
def retirar_super_usuario(request, perfil_id):
    print('pwidos')
    perfil = Perfil.objects.get(id=perfil_id).usuario
    perfil.is_superuser = False
    perfil.save()
    return redirect('index')


@login_required
def pesquisar_usuarios(request):
    perfis_econtrados = Perfil.objects.filter(nome__startswith=request.POST['nome_pesquisar'])        
    context = {'perfis_econtrados': perfis_econtrados, 'perfil_logado': get_perfil_logado(request)}
    return render(request, 'pesquisar_perfil.html', context)


@login_required
def bloquear(request, perfil_id):
    bloquear = Perfil.objects.get(id=perfil_id)
    get_perfil_logado(request).bloqueados.add(bloquear)
    return redirect('index')


@login_required
def desbloquear(request, perfil_id):
    bloquear = Perfil.objects.get(id=perfil_id)
    get_perfil_logado(request).bloqueados.remove(bloquear)
    return redirect('index')
