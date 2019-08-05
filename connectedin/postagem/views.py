from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from perfis.views import get_perfil_logado, index
from .models import Post, Comentario
from .forms import FormPost
from postagem import feedback


@login_required
def nova_postagem(request):
    if request.POST:
        if request.FILES or request.POST['texto']:
            post = Post()
            post.perfil = get_perfil_logado(request)
            form = FormPost(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, feedback.POSTAGEM_SUCESS)
            else:
                messages.error(request, feedback.POSTAGEM_ERROR)
                messages.error(request, form.errors)
        else:
            messages.error(request, feedback.POSTAGEM_EMPTY)
    return redirect('index')


@login_required
def curtir_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    perfil = get_perfil_logado(request)

    if post.perfil_reagiu_gostei(perfil):
        post.remover_gostar(perfil)
        messages.success(request, feedback.GOSTEI_REMOVE_SUCESS)
    else:
        if post.perfil_reagiu_nao_gostei(perfil):
            post.remover_nao_gostar(perfil)
            messages.error(request, feedback.GOSTEI_REMOVE_SUCESS)
        post.gostar(perfil)
        messages.success(request, feedback.GOSTEI_ADD_SUCESS)
    
    return redirect('index')


@login_required
def nao_curtir_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    perfil = get_perfil_logado(request)

    if post.perfil_reagiu_nao_gostei(perfil):
        post.remover_nao_gostar(perfil)
        messages.success(request, feedback.DISLIKE_REMOVE_SUCESS)
    else:
        if post.perfil_reagiu_gostei(perfil):
            post.remover_gostar(perfil)
        post.nao_gostar(perfil)
        
        messages.info(request, feedback.GOSTEI_REMOVE_SUCESS)
        messages.success(request, feedback.DESLIKE_ADD_SUCESS)
    
    return redirect('index')


@login_required
def comentar(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    
    if post.comentar(get_perfil_logado(request), request.POST['comentario']):
        messages.success(request, feedback.COMENTARIO_SUCESS)
    else:
        messages.error(request, feedback.COMENTARIO_ERROR)

    return redirect('index')


@login_required
def excluir_postagem(request, id_postagem):

    post = Post.objects.get(id=id_postagem)
    if post.perfil == get_perfil_logado(request):
        post.delete()
        messages.success(request, feedback.POSTAGEM_EXCLUIDA_SUCESS)
    elif get_perfil_logado(request).usuario.is_superuser:
        post.delete()
        messages.success(request, feedback.POSTAGEM_EXCLUIDA_SUCESS)
    else:
        messages.error(request, feedback.POSTAGEM_PERFIL_NAO_TEM_AUTORIZACAO)
    
    return redirect('index')


@login_required
def editar_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    form = FormPost(request.POST, request.FILES, instance=post)
    if form.is_valid():
        form.save()    
        messages.success(request, feedback.POSTAGEM_EDITAR_SUCESS)
    else:
        messages.error(request, feedback.POSTAGEM_EDITAR_ERROR)
    return redirect('index')


@login_required
def remover_comentario(request, id_comentario):
    comentario = Comentario.objects.filter(id=id_comentario)
    if comentario.exists():
        comentario.delete()
        messages.success(request, feedback.COMENTARIO_REMOVER_SUCESS)
    else:
        messages.error(request, feedback.COMENTARIO_NOT_FOUND)

    return redirect('index')
