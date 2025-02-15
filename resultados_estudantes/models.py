from django.db import models

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano_ingresso = models.IntegerField()
    nome_do_centro = models.CharField(max_length=255, null=True, blank=True)
    codigo_do_centro = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nome

class Estudante(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100, null=True, blank=True)
    ano_ingresso = models.IntegerField(null=True, blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.ano_ingresso and self.turma:
            self.ano_ingresso = self.turma.ano_ingresso
        super().save(*args, **kwargs)
        if is_new:
            modulos = Modulo.objects.filter(turma=self.turma)
            avaliacoes = Avaliacao.objects.filter(modulo__in=modulos)
            for avaliacao in avaliacoes:
                Resultado.objects.create(
                    estudante = self,
                    avaliacao = avaliacao
                )
    
    def __str__(self):
        return self.nome

class Modulo(models.Model):
    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=60, null=True, blank=True)
    nivelQNQP = models.CharField(max_length=30, null=True, blank=True)
    creditos =  models.PositiveSmallIntegerField(null=True, blank=True)
    bimestre = models.CharField(max_length=30, null=True, blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    avaliador = models.CharField(max_length=100, null=True, blank=True)
    data_assinatura_avaliador = models.DateField(null=True, blank=True)
    verificador_interno = models.CharField(max_length=100, null=True, blank=True)
    data_assinatura_verificador = models.DateField(null=True, blank=True)
    data_assinatura_estudante = models.DateField(null=True, blank=True)

    @property
    def inicias_nome(self):
        palavras = self.nome.split(" ")
        inicias = [palavra[0].upper() for palavra in palavras]
        return "".join(inicias)
    
    def __str__(self):
        return f'{self.inicias_nome} - {self.turma.nome}'

class ResultadoAprendizagem(models.Model):
    nome = models.CharField(max_length=255)
    numero = models.PositiveSmallIntegerField()
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        # Save ResultadoAprendizagem
        super().save(*args, **kwargs)
        
        # Criar Avalicao Automaticamente para o RDA a ser salvo
        if is_new:
            Avaliacao.objects.create(
                numero = self.numero,
                nome = f"Sumativa {self.numero}",
                modulo = self.modulo,
                resultado_aprendizagem = self
            )



class Avaliacao(models.Model):
    numero = models.PositiveSmallIntegerField()
    nome = models.CharField(max_length=100)
    data_avaliacao = models.DateField(null=True, blank=True)
    data_reavaliacao1 = models.DateField(null=True, blank=True)
    data_reavaliacao2 = models.DateField(null=True, blank=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    resultado_aprendizagem = models.ForeignKey(ResultadoAprendizagem, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            estudantes = Estudante.objects.filter(turma=self.modulo.turma.pk)
            for estudante in estudantes:
                Resultado.objects.create(
                    estudante = estudante,
                    avaliacao = self
                )
    

    def __str__(self):
        return f"{self.nome} | {self.modulo}"


class Resultado(models.Model):
    admitido = "A"
    naoAdmitido = "NA"
    NaoFez = "WD"
    nenhumResultado = ""

    OPECOES_RESULTADOS = (
        (admitido, "Admitido(A)"),
        (naoAdmitido, "Nao Admitido(NA)"),
        (NaoFez, "Nao Fez Avaliacao(WD)"),
        (nenhumResultado, "Nenhum Resultado")
    )
    resultado_avaliacao = models.CharField(max_length=10, choices=OPECOES_RESULTADOS, null=True, blank=True)
    resultado_reavaliacao1 = models.CharField(max_length=10, choices=OPECOES_RESULTADOS, null=True, blank=True)
    resultado_reavaliacao2 = models.CharField(max_length=10, choices=OPECOES_RESULTADOS, null=True, blank=True)
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE)

    @property
    def resultado_final(self):
        lista_alvali_e_reaval = (self.resultado_avaliacao, self.resultado_reavaliacao1, self.resultado_reavaliacao2)
        if(self.admitido in lista_alvali_e_reaval):
            return self.admitido
        if(self.naoAdmitido in lista_alvali_e_reaval):
            return self.naoAdmitido
        if(self.naoAdmitido in lista_alvali_e_reaval):
            return self.naoAdmitido
        
        return self.nenhumResultado
    

    def save(self, *args, **kwargs):
        if self.resultado_avaliacao == self.admitido:
            self.resultado_reavaliacao1 = self.nenhumResultado
            self.resultado_reavaliacao2 = self.nenhumResultado
        
        if self.resultado_reavaliacao1 == self.admitido:
            self.resultado_reavaliacao2 = self.nenhumResultado
            
        super().save(*args, **kwargs)
