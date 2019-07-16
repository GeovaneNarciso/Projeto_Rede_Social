from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from perfis.views import get_perfil_logado, index
from .models import Post, Comentario
from .forms import FormPost


@login_required
def nova_postagem(request):
    if request.POST:
        post = Post()
        post.perfil = get_perfil_logado(request)
        form = FormPost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            if post.marcar_alguem():
                messages.success(request, 'Perfis marcados com sucesso.')
            
            messages.success(request, 'Postagem feita com sucesso.')
        else:
            messages.error(request, 'Error ao fazer a nova postagem. Por favor, tente novamente')
            messages.error(request, form.errors)
    return redirect('index')


@login_required
def curtir_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    perfil = get_perfil_logado(request)

    if post.perfil_reagiu_gostei(perfil):  # ja curtiu
        post.remover_gostar(perfil) # romover gostei
        messages.success(request, 'Gostei removido.')
    else:
        if post.perfil_reagiu_nao_gostei(perfil):  # ja tinha um nao gostei
            post.remover_nao_gostar(perfil)  # romove nao gostei
            messages.error(request, 'Nao gostei removido.')
        post.gostar(perfil)
        messages.success(request, 'Gostei adicionado.')
    
    return redirect('index')


@login_required
def nao_curtir_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    perfil = get_perfil_logado(request)

    if post.perfil_reagiu_nao_gostei(perfil):  # ja tinha um nao gostei
        post.remover_nao_gostar(perfil)
        messages.success(request, 'Não gostei removido.')
    else:
        if post.perfil_reagiu_gostei(perfil):  # ja curtiu
            post.remover_gostar(perfil) # romover gostei
        post.nao_gostar(perfil)
        
        messages.info(request, 'Gostei removido.')
        messages.success(request, 'Não gostei adicionado.')
    
    return redirect('index')


@login_required
def comentar(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    post.comentar(
        get_perfil_logado(request),
        request.POST['comentario']
    )
    messages.success(request, 'Comentário realizado com sucesso!')

    return redirect('index')

@login_required
def excluir_postagem(request, id_postagem):
    sucesso = 'Postagem deletada com sucesso'

    post = Post.objects.get(id=id_postagem)
    if post.perfil == get_perfil_logado(request):
        post.delete()
        messages.success(request, sucesso)
    elif get_perfil_logado(request).usuario.is_superuser:
        post.delete()
        messages.success(request, sucesso)
    else:
        messages.error(request, 'Você não é o dono da postagem para poder excluí-la')
    
    return redirect('index')


@login_required
def editar_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    form = FormPost(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()
        if post.marcar_alguem():
            messages.success(request, 'Perfis marcados com sucesso!')    
        messages.success(request, 'Postagem editada com sucesso!')
    else:
        messages.error(request, 'Error ao editar postagem. Por favor, tente novamente!')
    return redirect('index')


@login_required
def remover_comentario(request, id_comentario):
    Comentario.objects.get(id=id_comentario).delete()

    messages.success(request, 'Comentário removido com sucesso!')
    return redirect('index')
