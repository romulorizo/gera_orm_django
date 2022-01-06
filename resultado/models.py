from django.db import models

class Atividade(models.Model):
    id = models.IntegerField( primary_key=True )
    nome = models.TextField(  )
    data_criacao = models.DateTimeField( auto_now_add=True )
    data_atualizacao = models.DateTimeField( auto_now=True )
    class Meta:
        db_table = "atividade"
    def __str__(self):
        return self.nome

class Producao(models.Model):
    id = models.IntegerField( primary_key=True )
    id_pai = models.IntegerField( null=True )
    nivel = models.IntegerField(  )
    nome = models.TextField(  )
    data_criacao = models.DateTimeField( auto_now_add=True )
    data_atualizacao = models.DateTimeField( auto_now=True )
    class Meta:
        db_table = "producao"
    def __str__(self):
        return self.nome

class ConsumoConsolidado(models.Model):
    id = models.IntegerField( primary_key=True )
    municipio = models.ForeignKey( Municipio, on_delete=models.PROTECT, related_name='consumoConsolidado_municipio', db_column='municipio_id' )
    tipo_diesel = models.ForeignKey( Tipo_Diesel, on_delete=models.PROTECT, related_name='consumoConsolidado_tipo_diesel', db_column='tipo_diesel_id' )
    data = models.DateTimeField(  )
    volume = models.FloatField(  )
    abastecimento = models.IntegerField(  )
    data_criacao = models.DateTimeField( auto_now_add=True )
    data_atualizacao = models.DateTimeField( auto_now=True )
    class Meta:
        db_table = "consumo_consolidado"
    def __str__(self):
        return self.tipo_diesel

class ProducaoAtividade(models.Model):
    producao = models.ForeignKey( Producao, on_delete=models.PROTECT, related_name='producaoAtividade_producao', db_column='producao_id' )
    atividade = models.ForeignKey( Atividade, on_delete=models.PROTECT, related_name='producaoAtividade_atividade', db_column='atividade_id' )
    data_criacao = models.DateTimeField( auto_now_add=True )
    data_atualizacao = models.DateTimeField( auto_now=True )
    class Meta:
        db_table = "producao_atividade"
        unique_together = [('producao', 'atividade')]
    def __str__(self):
        return self.producao
