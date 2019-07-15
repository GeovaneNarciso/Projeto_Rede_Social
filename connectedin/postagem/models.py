from django.db import models
from perfis.models import Perfil
from datetime import datetime    


class Reacao(models.Model):
    post = models.ForeignKey('Post', related_name='reacoes', on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    CHOICES = (
        ('gostei', 'Gostei'),
        ('nao gostei', 'Não gostei')
    )
    reacao = models.CharField(max_length=10, choices=CHOICES)
    
    class Meta:
        unique_together = ('post', 'perfil')


class Comentario(models.Model):
    texto = models.CharField(max_length=255)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comentarios', on_delete=models.CASCADE)
    data_comentario = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['data_comentario']

class Post(models.Model):
    '''
    Classe que representa uma postagem de um usário
    Attributes:
        texto = TextField
        foto = ImageField
        perfil = Chave Estrangeira para Perfil com related_name = postagens
        data_post = DateTimeField com auto_now = True
        qnt_gostei = int 
        qnt_nao_gostei = int
        qnt_comentario = int
    '''
    texto = models.TextField(blank=True)
    foto = models.ImageField(upload_to='images/postagens', max_length=None, null=True)
    perfil = models.ForeignKey(Perfil, related_name='postagens', on_delete=models.CASCADE)
    data_post = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ['data_post']
        
    @property
    def qnt_gostei(self):
        return self.get_gostei_all().count()
    
    @property
    def qnt_nao_gostei(self):
        return self.get_nao_gostei_all().count()

    @property
    def qnt_comentarios(self):
        return self.get_comentarios().count()

    def reagir(self, perfil, reacao):
        return Reacao.objects.create(post=self, perfil=perfil, reacao=reacao)

    def remover_reacao(self, perfil, reacao):
        reacao = Reacao.objects.get(post=self, perfil=perfil, reacao=reacao)
        reacao.delete()

    def gostar(self, perfil):
        return self.reagir(perfil, 'gostei')
    
    def get_gostei_all(self):
        return self.reacoes.filter(reacao='gostei')
    
    def remover_gostar(self, perfil):
        self.remover_reacao(perfil, 'gostei')
    
    def nao_gostar(self, perfil):
        return self.reagir(perfil, 'nao gostei')

    def get_nao_gostei_all(self):
        return self.reacoes.filter(reacao='nao gostei')
    
    def remover_nao_gostar(self, perfil):
        self.remover_reacao(perfil, 'nao gostei')

    def get_comentarios(self):
        return self.comentarios.all()
    
    def perfil_reagiu_gostei(self, perfil):
        return self.get_gostei_all().filter(perfil=perfil).exists()
    
    def perfil_reagiu_nao_gostei(self, perfil):
        return self.get_nao_gostei_all().filter(perfil=perfil).exists()
    
    def comentar(self, perfil, comentario):
        Comentario.objects.create(post=self, perfil=perfil, texto=comentario)