from django.db import models
from django.contrib.auth.models import User
from perfis.models import Perfil
from datetime import datetime


class Reacao(models.Model):
    """
    Classe que representa a reacao de um usario a uma postage
    Attributes:
        post: ForeignKey com referencia para Post e related_name = reacaoes
        perfil: ForeingKey para Perfil e related_name = reacaoes
        reacao: Choice ('gostei', 'nao gostei')
        data_reacao: DateTimeField default now()
    """
    
    post = models.ForeignKey('Post', related_name='reacoes', on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, related_name='reacoes', on_delete=models.CASCADE)
    CHOICES = (
        ('gostei', 'Gostei'),
        ('nao gostei', 'Não gostei')
    )
    reacao = models.CharField(max_length=10, choices=CHOICES)
    data_reacao = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = ('post', 'perfil')


class Comentario(models.Model):
    """
    Classe que representa um comentario de um usuario em uma postagem
    Attributes:
        texto: CharField(max_length=255)
        perfil: FokeingKey com referencia para Perfil 
        post: Post a qual esta sendo feito o comentario com related_name = comentarios
        data_comentario: DateTimeField default now()
    """

    texto = models.CharField(max_length=255)
    perfil = models.ForeignKey(Perfil, related_name='comentarios', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comentarios', on_delete=models.CASCADE)
    data_comentario = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['data_comentario']


class Post(models.Model):
    """
    Classe que representa uma postagem de um usário
    Attributes:
        texto: TextField
        foto: ImageField
        perfil:  Chave Estrangeira para Perfil com related_name = postagens
        data_post:  DateTimeField com auto_now = True
        perfis_marcados: ManyToMany com Perfil
        visivel: BooleanField default True (postagem visivel pro amigos)
        qnt_gostei:  int 
        qnt_nao_gostei:  int
        qnt_comentario: int
    """

    texto = models.TextField(blank=True)
    foto = models.ImageField(upload_to='images/postagens', max_length=None, null=True)
    perfil = models.ForeignKey(Perfil, related_name='postagens', on_delete=models.CASCADE)
    data_post = models.DateTimeField(default=datetime.now)
    perfis_marcados = models.ManyToManyField(Perfil)
    visivel = models.BooleanField(default=True)

    class Meta:
        ordering = ['data_post']

    def __str__(self):
        etc = ''
        if len(self.texto) > 20:
            etc = '...'
        return '{} - {}'.format(self.perfil, self.texto[:20] + etc)

    @property
    def qnt_gostei(self):
        """Metodo Property com a quantidade de Reacao do tipo 'gostei' do post"""

        return self.get_gostei_all().count()

    @property
    def qnt_nao_gostei(self):
        """Metodo Property com a quantidade de Reacao do tipo 'nao gostei' do post"""

        return self.get_nao_gostei_all().count()

    @property
    def qnt_comentarios(self):
        """Metodo Property com a quantidade de Comentaio"""

        return self.get_comentarios().count()

    def reagir(self, perfil, reacao):
        """
        Metodo  para um perfil fazer uma reacao ao post
        Args:
            perfil: instancia de Perfil
            reacao: str com o tipo da reacao
        Retruns:
            instancia de Reacao com a nova reacao criada
        """

        return Reacao.objects.create(post=self, perfil=perfil, reacao=reacao)

    def remover_reacao(self, perfil, reacao):
        """
        Metodo  para remover a reacao de um perfil do post
        Args:
            perfil: instancia de Perfil
            reacao: str com o tipo da reacao
        """

        reacao = Reacao.objects.get(post=self, perfil=perfil, reacao=reacao)
        reacao.delete()

    def gostar(self, perfil):
        """
        Metodo  para um perfil fazer uma reacao de 'gostei'
        Args:
            perfil: instancia de Perfil
        Retruns:
            instancia de Reacao com a nova reacao do tipo 'gostei' criada
        """

        return self.reagir(perfil, 'gostei')

    def get_gostei_all(self):
        """
        Metodo para pegar todas as reacoes do tipo 'gostei' do post
        Rerturns:
            QuerySet com todos Reacoes do tipo 'gostei' feitas ao post
        """

        return self.reacoes.filter(reacao='gostei')

    def remover_gostar(self, perfil):
        """
        Metodo para remover a reacao do tipo 'gostei' que um perfil fez ao post
        Args:
            perfil: instancia de Perfil
        """

        self.remover_reacao(perfil, 'gostei')

    def nao_gostar(self, perfil):
        """
        Metodo  para um perfil fazer uma reacao de 'nao gostei'
        Args:
            perfil: instancia de Perfil
        Retruns:
            instancia de Reacao com a nova reacao do tipo 'nao gostei' criada
        """

        return self.reagir(perfil, 'nao gostei')

    def get_nao_gostei_all(self):
        """
        Metodo para pegar todas as reacoes do tipo 'nao gostei' do post
        Rerturns:
            QuerySet com todos Reacoes do tipo 'nao gostei' feitas ao post
        """

        return self.reacoes.filter(reacao='nao gostei')

    def remover_nao_gostar(self, perfil):
        """
        Metodo para remover a reacao do tipo 'nao gostei' que um perfil fez ao post
        Args:
            perfil: instancia de Perfil
        """

        self.remover_reacao(perfil, 'nao gostei')

    def get_comentarios(self):
        """
        Metodo para pegar todos os comentario do post
        Rerturns:
            QuerySet com todos os Comentarios feitos ao post
        """

        return self.comentarios.all()

    def perfil_reagiu_gostei(self, perfil):
        """
        Metodo que verifica se o perfil ja fez uma reacao do tipo 'gostei' ao post
        Args:
            perfil: instancia de Perfil
        Returns:
            boolean: True se perfila ja reagiu com 'gostei', False se nao reagaiu ainda
        """

        return self.get_gostei_all().filter(perfil=perfil).exists()

    def perfil_reagiu_nao_gostei(self, perfil):
        """
        Metodo que verifica se o perfil ja fez uma reacao do tipo 'nao gostei' ao post
        Args:
            perfil: instancia de Perfil
        Returns:
            boolean: True se perfila ja reagiu com 'nao gostei', False se nao reagaiu ainda 
        """

        return self.get_nao_gostei_all().filter(perfil=perfil).exists()

    def comentar(self, perfil, comentario):
        """
        Metodo  para um perfil fazer um comentario ao post
        Args:
            perfil: instancia de Perfil
            comentario: str (max_lenth=255)
        Retruns:
            instancia de Comentario com o nova comentario feito ao post
        """

        return Comentario.objects.create(post=self, perfil=perfil, texto=comentario)

    def marcar_alguem(self):
        """
        Funcão para retornar os perfis que estao sendo marcados no texto de uma postagem
        Returns:
            list() com todas instancias de Perfil marcado
        """
        texto = self.texto

        amigos = self.perfil.contatos.all()
        listar_marcados = []

        indice = texto.find('@')
        while indice != -1:
            username = texto[indice:].split()[0].replace('@', '')
            try:
                user = User.objects.get(username=username)
                if user.perfil and user.perfil in amigos:
                    listar_marcados.append(user.perfil)
            except User.DoesNotExist:
                pass
            texto = texto[indice + 1:]
            indice = texto.find('@')

        self.perfis_marcados.set(listar_marcados)
        return listar_marcados

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Post, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        self.marcar_alguem()
