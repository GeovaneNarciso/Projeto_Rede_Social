from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from perfis.views import get_perfil_logado
from .models import Post
from .forms import FormPost


@login_required
def nova_postagem(request):
    if request.POST: 
        post = Post()
        post.perfil = get_perfil_logado(request)
        form = FormPost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return redirect('index')


@login_required
def curtir_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    perfil = get_perfil_logado(request)

    if post.perfil_reagiu_gostei(perfil):  # ja curtiu
        post.remover_gostar(perfil) # romover gostei
    else:
        if post.perfil_reagiu_nao_gostei(perfil):  # ja tinha um nao gostei
            post.remover_nao_gostar(perfil)  # romove nao gostei
        post.gostar(perfil)
    
    return redirect('index')


@login_required
def nao_curtir_postagem(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    perfil = get_perfil_logado(request)

    if post.perfil_reagiu_nao_gostei(perfil):  # ja tinha um nao gostei
        post.remover_nao_gostar(perfil)
    else:
        if post.perfil_reagiu_gostei(perfil):  # ja curtiu
            post.remover_gostar(perfil) # romover gostei
        post.nao_gostar(perfil)
    
    return redirect('index')


@login_required
def comentar(request, id_postagem):
    post = Post.objects.get(id=id_postagem)
    
    for key in request.POST.keys():
        print(key)
        print(request.POST[key])

    post.comentar(
        get_perfil_logado(request),
        request.POST['comentario']
    )

    return redirect('index')