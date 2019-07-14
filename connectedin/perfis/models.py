from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self', related_name='meus_contatos')
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='perfis/static/images/foto_perfil', max_length=None, null=True)
    bloqueados = models.ManyToManyField('self', related_name='perfis_bloqueados')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    def convidar(self, perfil_convidado):
        convite = Convite(convidador=self, convidado=perfil_convidado)
        convite.save()

    @property
    def email(self):
        return self.usuario.email


class Convite(models.Model):
    convidador = models.ForeignKey(Perfil, related_name='convites_feitos', on_delete=models.CASCADE)
    convidado = models.ForeignKey(Perfil, related_name='convites_recebidos', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('convidador', 'convidado')
    
    def aceitar(self):
        # self.convidado.contatos.add(self.convidador)
        self.convidador.contatos.add(self.convidado)
        self.delete()
