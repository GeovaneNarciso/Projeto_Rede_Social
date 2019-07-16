from datetime import datetime
from django.shortcuts import render
from .models import Perfil, Convite
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from postagem.forms import FormPost
from postagem.models import Post
from .forms import FormFotoPerfil
from django.contrib import messages

LIMITE_PAGINATION = 15


@login_required
def index(request):
    perfil = get_perfil_logado(request)
    
    postagens = list(perfil.postagens.all().order_by('data_post'))
    bloqueados = perfil.bloqueados.all()
    for contato in perfil.contatos.filter(is_active=True):
        if contato in bloqueados:  # nao mostrar os bloqueados
            continue
        postagens += list(contato.postagens.all().filter(visivel=True))
    postagens.sort(key=lambda post: post.data_post, reverse=True)

    if not perfil.is_active:
        return redirect('reativar_perfil')

    lista_form_post = []
    for post in postagens:
        lista_form_post.append(FormPost(instance=post))

    paginator = Paginator(postagens, LIMITE_PAGINATION)
    page = request.GET.get('page')
    task = paginator.get_page(page)
    context = {
        'perfis': Perfil.objects.all(),
        'perfil_logado': get_perfil_logado(request),
        'form_post': FormPost(),
        'forms_posts': lista_form_post,
        'form_aterar_foto': FormFotoPerfil(),
        'postagens': task,
        'range_paginator': range(1, task.paginator.num_pages + 1),
        'current_page': int(page) if page else 1
    }
    return render(request, 'index.html', context)


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

        mensagem = 'Perfil reativado com sucesso. Seja bem-vindo novamente, {}!'.format(perfil_logado)
        messages.success(request, mensagem)
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

    mensagem = 'Convite enviado para {}!'.format(perfil_convidado)
    messages.success(request, mensagem)
    return redirect('index')


@login_required
def remover_convite(request, perfil_id):
    perfil_logado = get_perfil_logado(request)
    perfil_convidado = Perfil.objects.get(id=perfil_id)
    perfil_logado.remover_convite(perfil_convidado)

    mensagem = 'Convite do(a) {} foi removido com sucesso!'.format(perfil_convidado)
    messages.error(request, mensagem)
    return redirect('index')


@login_required
def get_perfil_logado(request):
    return request.user.perfil


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()

    mensagem = 'Convite do(a) {} aceito. Vocês estão conectadins!'.format(convite.convidador.nome)
    messages.success(request, mensagem)
    return redirect('index')


@login_required
def rejeitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.delete()

    mensagem = 'Convite do(a) {} rejeitado'.format(convite.convidador.nome.capitalize())
    messages.error(request, mensagem)
    return redirect('index')


@login_required
def desfazer_amizade(request, id_contato):
    contato_remove = Perfil.objects.get(id=id_contato)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.contatos.remove(contato_remove)

    mensagem = 'Amizade com {} foi desfeita com sucesso'.format(contato_remove.nome.capitalize())
    messages.error(request, mensagem)
    return redirect('index')


@login_required
def alterar_senha(request):
    perfil_logado = get_perfil_logado(request).usuario
    senha_atual = request.POST['senha_atual']
    if check_password(senha_atual, perfil_logado.password):
        perfil_logado.set_password(request.POST['senha_nova'])
        perfil_logado.save()

        mensagem = 'Senha alterada!'
    else:
        mensagem = 'Senha errada.'
    messages.success(request, mensagem)
    return redirect('index')


@login_required
def desativar_perfil(request):
    perfil_logado = get_perfil_logado(request)
    perfil_logado.is_active = False
    perfil_logado.save()
    messages.info(request, 'Perfil desativo. Aguardamos o seu retorno!')
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
    if not get_perfil_logado(request).usuario.is_superuser:
        mensagem = 'Você não tem acesso a esta função!'
        mensagem.error(request, mensagem)
        return redirect('index')
    
    perfil = Perfil.objects.get(id=perfil_id).usuario
    perfil.is_superuser = False
    perfil.save()

    mensagem = 'Super usuário retidado do(a) {}!'.format(perfil)
    messages.success(request, mensagem)
    return redirect('index')


@login_required
def pesquisar_usuarios(request, nome):
    perfis_econtrados = Perfil.objects.filter(nome__startswith=nome)

    paginator = Paginator(perfis_econtrados, LIMITE_PAGINATION)
    page = request.GET.get('page')
    task = paginator.get_page(page)

    context = {
        'perfis_econtrados': task,
        'perfil_logado': get_perfil_logado(request),
        'range_paginator': range(1, task.paginator.num_pages + 1),
        'current_page': int(page) if page else 1
    }
    return render(request, 'pesquisar_perfil.html', context)


@login_required
def bloquear(request, perfil_id):
    perfil_logado = get_perfil_logado(request)
    perfil_bloquear = Perfil.objects.get(id=perfil_id)
    if perfil_bloquear == perfil_logado:
        mensagem = 'Não é possível bloqeuar a si mesmo.'
        messages.error(request, mensagem)

    perfil_logado.bloqueados.add(perfil_bloquear)
    
    mensagem = '{} bloqueado(a) com sucesso! Esta pessoa não irá economodá-lo'.format(perfil_bloquear)
    messages.success(request, mensagem)
    return redirect('index')


@login_required
def desbloquear(request, perfil_id):
    perfil_desbloquear = Perfil.objects.get(id=perfil_id)
    get_perfil_logado(request).bloqueados.remove(perfil_desbloquear)

    mensagem = '{} desbloqueado!'.format(perfil_desbloquear)
    messages.success(request, mensagem)
    return redirect('index')


@login_required
def alterar_foto(request):
    if request.POST:
        form = FormFotoPerfil(request.POST, request.FILES, instance=get_perfil_logado(request))
        if form.is_valid():
            form.save()
            
            mensagem = 'Foto alterada com sucesso.'
            messages.success(request, mensagem)
        else:
            mensagem = 'Error ao alterar a foto.'
            messages.error(request, mensagem)
            messages.error(request, form.errors)
    return redirect('index')


@login_required
def estatisticas(request):
    perfil = get_perfil_logado(request)
    context = {'posts': [], 'reacoes': [], 'comentarios': [], 'perfil_logado': perfil}
    now = datetime.now()

    MESES = {'janeiro': 1, 'fevereiro': 2, 'marco': 3, 'abril': 4, 'maio': 5, 
             'junho': 6, 'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10,
             'novembro': 11, 'dezembro': 12}
            
    def count_meses(model, mes):
        if model == 'post':
            return perfil.postagens.filter(data_post__year=str(now.year)).filter(data_post__month=str(MESES[mes])).count()
        elif model == 'reacao':
            return perfil.reacoes.filter(data_reacao__year=str(now.year)).filter(data_reacao__month=str(MESES[mes])).count()
        elif model == 'comentario':
            return perfil.comentarios.filter(data_comentario__year=str(now.year)).filter(data_comentario__month=str(MESES[mes])).count()
    
    for key in MESES.keys():
        context['posts'].append({key: count_meses('post', key)})
        context['reacoes'].append({key: count_meses('reacao', key)})
        context['comentarios'].append({key: count_meses('comentario', key)})
    print(context['posts'])
    
    return render(request, 'estatisticas.html', context)