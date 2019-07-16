from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.base import View
from perfis.models import Perfil
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.decorators import login_required
from perfis.views import get_perfil_logado
from django.contrib import messages
from django.core.paginator import Paginator


class RegistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)

        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['nome'],
                                               email=dados_form['email'],
                                               password=dados_form['senha'])
            perfil = Perfil(nome=dados_form['nome'],
                            telefone=dados_form['telefone'],
                            nome_empresa=dados_form['nome_empresa'],
                            usuario=usuario)
            perfil.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form})


@login_required
def pagina_de_superusuario(request):
    perfil = get_perfil_logado(request)
    if not perfil.usuario.is_superuser:
        messages.error(request, 'Você não tem autorização para entrar nesta página.')
        return redirect('index')
    
    perfis_bd = Perfil.objects.all()
    paginator = Paginator(perfis_bd, 15)
    page = request.GET.get('page')
    task = paginator.get_page(page)

    context = {
        'perfil_logado': get_perfil_logado(request), 
        'perfis_bd': task,
        'range_paginator': range(1, task.paginator.num_pages + 1),
        'current_page': int(page) if page else 1
    }
    return render(request, 'super_usuario.html', context)