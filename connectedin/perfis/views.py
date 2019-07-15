from django.shortcuts import render
from .models import Perfil, Convite
from django.shortcuts import redirect
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from postagem.forms import FormPost


@login_required
def index(request):    
    perfil = get_perfil_logado(request)
    postagens = list(perfil.postagens.all().order_by('data_post'))
    for contato in perfil.contatos.filter(is_active=True):
        postagens += list(contato.postagens.all())
    postagens.sort(key=lambda post: post.data_post, reverse=True)

    if not perfil.is_active:
        return redirect('reativar_perfil')
    
    return render(request, 'index.html',
                  {'perfis': Perfil.objects.all(),
                   'perfil_logado': get_perfil_logado(request),
                   'form_post': FormPost(),
                   'postagens': postagens})


@login_required
def reativar_perfil(request):
    if request.POST:
        print(request.POST.keys())
        if not 'reativar' in request.POST.keys():
            logout(request)
            return redirect('login')
        
        perfil_logado = get_perfil_logado(request)
        perfil_logado.is_active = True
        perfil_logado.save()
        return redirect('index')

    return render(request, 'reativar_perfil.html', {'perfil_logado': get_perfil_logado(request)})
    

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
def desativar_perfil(request):
    perfil_logado = get_perfil_logado(request)
    perfil_logado.is_active = False
    perfil_logado.save()
    logout(request)

    return redirect('login')


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
def pesquisar_usuarios(request, nome):
    perfis_econtrados = Perfil.objects.filter(nome__startswith=nome, is_active=True)
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
