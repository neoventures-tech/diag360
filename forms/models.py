import uuid
from django.db import models

COMPANY_SIZE_CHOICES = [
    ('PE', 'Pequena Empresa (até R$ 4,8 milhões/ano)'),
    ('PME', 'Pequena Média Empresa (R$ 4,8 a R$ 10 milhões/ano)'),
    ('ME', 'Média Empresa (R$ 10 a R$ 100 milhões/ano)'),
    ('GE', 'Grande Empresa (R$ 100 a R$ 300 milhões/ano)'),
    ('GGE', 'Muito Grande Empresa (acima de R$ 300 milhões/ano)'),
]

COMPANY_SIZE = {
    1: 'PE',   # Pequena Empresa (até R$ 4,8 milhões/ano)
    2: 'PME',  # Pequena Média Empresa (R$ 4,8 a R$ 10 milhões/ano)
    3: 'ME',   # Média Empresa (R$ 10 a R$ 100 milhões/ano)
    4: 'GE',   # Grande Empresa (R$ 100 a R$ 300 milhões/ano)
    5: 'GGE',  # Muito Grande Empresa (acima de R$ 300 milhões/ano)
}

QUESTION_WEIGHTS = {
    # Pergunta 2 - Liderança
    2: {
        'PE': 10.0,
        'PME': 9.0,
        'ME': 8.0,
        'GE': 7.0,
        'GGE': 6.0,
    },
    # Pergunta 3 - Estratégia
    3: {
        'PE': 8.0,
        'PME': 10.0,
        'ME': 11.0,
        'GE': 9.0,
        'GGE': 8.0,
    },
    # Pergunta 4 - Suporte & Governança
    4: {
        'PE': 6.0,
        'PME': 7.0,
        'ME': 8.0,
        'GE': 10.0,
        'GGE': 12.0,
    },
    # Pergunta 5 - Recursos (Financeiros)
    5: {
        'PE': 7.0,
        'PME': 8.0,
        'ME': 9.0,
        'GE': 9.0,
        'GGE': 8.0,
    },
    # Pergunta 6 - Recursos (Humanos)
    6: {
        'PE': 10.0,
        'PME': 9.0,
        'ME': 8.0,
        'GE': 7.0,
        'GGE': 6.0,
    },
    # Pergunta 7 - Insights & Oportunidades
    7: {
        'PE': 8.0,
        'PME': 9.0,
        'ME': 9.0,
        'GE': 10.0,
        'GGE': 12.0,
    },
    # Pergunta 8 - Processos (Incremental)
    8: {
        'PE': 14.0,
        'PME': 12.0,
        'ME': 9.0,
        'GE': 7.0,
        'GGE': 5.0,
    },
    # Pergunta 9 - Processos (Radical)
    9: {
        'PE': 5.0,
        'PME': 6.0,
        'ME': 8.0,
        'GE': 9.0,
        'GGE': 10.0,
    },
    # Pergunta 10 - Resultados (Mensuração)
    10: {
        'PE': 6.0,
        'PME': 10.0,
        'ME': 9.0,
        'GE': 8.0,
        'GGE': 7.0,
    },
    # Pergunta 11 - Resultados (Impacto)
    11: {
        'PE': 8.0,
        'PME': 9.0,
        'ME': 9.0,
        'GE': 9.0,
        'GGE': 9.0,
    },
    # Pergunta 12 - Resultados (Relevância)
    12: {
        'PE': 8.0,
        'PME': 11.0,
        'ME': 12.0,
        'GE': 15.0,
        'GGE': 17.0,
    },
}



class MaturityLevel(models.Model):
    level_number = models.IntegerField(unique=True, help_text="Número do nível (1-5)")
    min_score = models.IntegerField(help_text="Pontuação mínima")
    max_score = models.IntegerField(help_text="Pontuação máxima")
    name = models.CharField(max_length=100, help_text="Nome do nível (ex: Nível 1: Inicial / Caótico)")
    focus = models.CharField(max_length=200, help_text="Foco principal do nível")
    description = models.TextField(help_text="Descrição do nível de maturidade")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['level_number']
        verbose_name = "Nível de Maturidade"
        verbose_name_plural = "Níveis de Maturidade"

    def __str__(self):
        return f"{self.name} ({self.min_score}-{self.max_score} pontos)"

    @staticmethod
    def calculate_maturity_level(total_score):
        if total_score is None:
            return None

        level = MaturityLevel.objects.filter(
            min_score__lte=total_score,
            max_score__gte=total_score
        ).first()

        if level:
            return {
                "numero": level.level_number,
                "nivel": level.name,
                "foco": level.focus,
                "descricao": level.description,
                "faixa": (level.min_score, level.max_score),
            }


class PriorityAction(models.Model):
    maturity_level = models.ForeignKey(
        MaturityLevel,
        on_delete=models.CASCADE,
        related_name='priority_actions',
        help_text="Nível de maturidade relacionado"
    )
    company_size = models.CharField(
        max_length=10,
        choices=COMPANY_SIZE_CHOICES,
        help_text="Porte da empresa"
    )
    action = models.TextField(help_text="Ação prioritária recomendada")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['maturity_level', 'company_size']
        unique_together = [['maturity_level', 'company_size']]
        verbose_name = "Ação Prioritária"
        verbose_name_plural = "Ações Prioritárias"

    def __str__(self):
        return f"{self.maturity_level.name} - {self.company_size}: {self.action[:50]}..."

    @staticmethod
    def get_priority_action(total_score, company_size):
        if total_score is None or company_size is None:
            return "Não foi possível determinar a ação prioritária."

        # Busca no banco de dados primeiro
        level = MaturityLevel.objects.filter(
            min_score__lte=total_score,
            max_score__gte=total_score
        ).first()

        if level:
            priority = PriorityAction.objects.filter(
                maturity_level=level,
                company_size=company_size
            ).first()

            if priority:
                return priority.action

        return "Não foi possível determinar a ação prioritária."


class EvaluationAxis(models.Model):
    """Eixo de avaliação ISO 56002"""
    name = models.CharField(max_length=100, unique=True, help_text="Nome do eixo (ex: Liderança, Estratégia)")
    code = models.CharField(max_length=50, unique=True, help_text="Código único do eixo (ex: LEADERSHIP)")
    order = models.IntegerField(unique=True, help_text="Ordem de exibição")
    description = models.TextField(blank=True, help_text="Descrição do eixo de avaliação")
    max_score_by_size = models.JSONField(
        default=dict,
        blank=True,
        help_text="Pontuação máxima por porte de empresa (ex: {'PE': 10.0, 'PME': 9.0, ...})"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Eixo de Avaliação"
        verbose_name_plural = "Eixos de Avaliação"

    def __str__(self):
        return self.name

    def calculate_max_scores(self):
        """
        Calcula a pontuação máxima possível para cada porte de empresa neste eixo.
        Pontuação máxima = soma dos pesos de todas as questões do eixo (já que o máximo choice é 5, e (5/5) * peso = peso)
        """
        max_scores = {
            'PE': 0.0,
            'PME': 0.0,
            'ME': 0.0,
            'GE': 0.0,
            'GGE': 0.0,
        }

        # Para cada questão deste eixo
        for question in self.questions.all():
            question_number = question.order

            # Pular se a questão não tem peso definido
            if question_number not in QUESTION_WEIGHTS:
                continue

            # Adicionar o peso de cada porte ao total
            for size_code in max_scores.keys():
                weight = QUESTION_WEIGHTS[question_number].get(size_code, 0)
                max_scores[size_code] += weight

        return max_scores

    def update_max_scores(self):
        """Calcula e salva as pontuações máximas no campo max_score_by_size"""
        self.max_score_by_size = self.calculate_max_scores()
        self.save()
        return self.max_score_by_size


class Question(models.Model):
    order = models.IntegerField(unique=True, help_text="Ordem da pergunta (1, 2, 3...)")
    label = models.TextField(help_text="Texto da pergunta")
    field_name = models.CharField(max_length=50, unique=True, help_text="Nome do campo (ex: question1)")
    axis = models.ForeignKey(
        EvaluationAxis,
        on_delete=models.PROTECT,
        related_name='questions',
        null=True,
        blank=True,
        help_text="Eixo de avaliação ISO 56002"
    )
    is_active = models.BooleanField(default=True, help_text="Pergunta ativa no formulário")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return f"Pergunta {self.order}: {self.label[:50]}..."


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    value = models.IntegerField(help_text="Valor da opção (1-5)")
    text = models.TextField(help_text="Texto da opção de resposta")
    order = models.IntegerField(help_text="Ordem de exibição")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['question', 'order']
        unique_together = [['question', 'value'], ['question', 'order']]
        verbose_name = "Opção de Resposta"
        verbose_name_plural = "Opções de Resposta"

    def __str__(self):
        return f"{self.question.field_name} - Opção {self.value}: {self.text[:50]}..."



class InnovationEvaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255, blank=True, null=True, help_text="Nome da empresa")
    contact_email = models.EmailField(blank=True, null=True, help_text="Email de contato")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Telefone de contato")
    sector = models.CharField(max_length=100, blank=True, null=True, help_text="Setor de atuação")
    company_size = models.CharField(
        max_length=10,
        choices=COMPANY_SIZE_CHOICES,
        blank=True,
        null=True,
        help_text="Porte da empresa"
    )

    total_score = models.FloatField(default=0, help_text="Pontuação total calculada")
    score_by_dimension = models.JSONField(default=dict, blank=True, help_text="Pontuação por dimensão")

    maturity_level = models.CharField(
        max_length=100,
        blank=True,
        help_text="Nível de maturidade (Ex: Nível 1: Inicial / Caótico)"
    )
    maturity_level_fk = models.ForeignKey(
        MaturityLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations',
        help_text="Nível de maturidade da avaliação (novo campo)"
    )
    focus = models.CharField(
        max_length=200,
        blank=True,
        help_text="Foco principal do nível"
    )
    description = models.TextField(
        blank=True,
        help_text="Descrição do nível de maturidade"
    )
    priority_action = models.TextField(
        blank=True,
        help_text="Ação prioritária recomendada"
    )
    ai_analysis = models.TextField(
        blank=True,
        help_text="Análise gerada pela IA (Considerações Finais)"
    )

    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source_ip = models.GenericIPAddressField(blank=True, null=True, help_text="IP de origem da avaliação")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Avaliação de Inovação"
        verbose_name_plural = "Avaliações de Inovação"

    def __str__(self):
        company = self.company_name or "Sem nome"
        return f"{company} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"

    def get_ranking_stats(self):
        """
        Calcula estatísticas de ranking comparando com outras avaliações do mesmo porte.
        Retorna:
        - position: posição no ranking (1 = melhor)
        - total: total de avaliações do mesmo porte
        - percentile: percentil da pontuação
        - better_than_percentage: % de empresas que essa avaliação superou
        - average_score: pontuação média do porte
        - top_score: maior pontuação do porte
        """
        if not self.company_size:
            return None

        # Buscar todas as avaliações do mesmo porte
        same_size_evaluations = InnovationEvaluation.objects.filter(
            company_size=self.company_size
        ).exclude(
            id=self.id  # Excluir a própria avaliação
        ).order_by('-total_score')

        total_count = same_size_evaluations.count()

        if total_count == 0:
            return {
                'position': 1,
                'total': 1,
                'percentile': 100,
                'better_than_percentage': 100,
                'average_score': self.total_score,
                'top_score': self.total_score,
                'is_only_one': True
            }

        # Contar quantas avaliações têm pontuação maior
        better_count = same_size_evaluations.filter(total_score__gt=self.total_score).count()
        position = better_count + 1

        # Calcular percentil (quanto maior, melhor)
        percentile = ((total_count - position + 1) / total_count) * 100

        # Percentual de empresas que essa avaliação superou
        worse_count = same_size_evaluations.filter(total_score__lt=self.total_score).count()
        better_than_percentage = (worse_count / total_count) * 100

        # Estatísticas agregadas
        from django.db.models import Avg, Max
        stats = same_size_evaluations.aggregate(
            avg_score=Avg('total_score'),
            max_score=Max('total_score')
        )

        # Considerar a própria avaliação no top_score
        top_score = max(stats['max_score'] or 0, self.total_score)

        return {
            'position': position,
            'total': total_count + 1,  # +1 para incluir a própria avaliação
            'percentile': round(percentile, 1),
            'better_than_percentage': round(better_than_percentage, 1),
            'average_score': round(stats['avg_score'] or self.total_score, 2),
            'top_score': round(top_score, 2),
            'is_only_one': False
        }

    @staticmethod
    def generate_full_report(total_score, company_size):
        level_info = MaturityLevel.calculate_maturity_level(total_score)
        priority_action = PriorityAction.get_priority_action(total_score, company_size)

        if level_info is None:
            return {
                "erro": "Não foi possível calcular o nível de maturidade.",
                "pontuacao_total": total_score,
                "porte_empresa": company_size,
            }

        print("\n" + "=" * 80)
        print("🏆 RELATÓRIO DE MATURIDADE DE INOVAÇÃO")
        print("=" * 80)
        print(f"📊 Pontuação Total: {total_score:.2f} / 100")
        print(f"🏢 Porte da Empresa: {company_size}")
        print(f"📈 {level_info['nivel']} ({level_info['faixa'][0]}-{level_info['faixa'][1]} pontos)")
        print(f"🎯 Foco Principal: {level_info['foco']}")
        print(f"📝 Descrição: {level_info['descricao']}")
        print("=" * 80)
        print(f"✨ PRÓXIMA AÇÃO PRIORITÁRIA:")
        print(f"   {priority_action}")
        print("=" * 80 + "\n")

        full_report = {
            "total_score": total_score,
            "company_size": company_size,
            "level_number": level_info["numero"],
            "level_name": level_info["nivel"],
            "level_focus": level_info["foco"],
            "level_description": level_info["descricao"],
            "level_range": level_info["faixa"],
            "priority_action": priority_action,
        }

        return full_report


class AxisScore(models.Model):
    """Pontuação por eixo de avaliação"""
    evaluation = models.ForeignKey(
        'InnovationEvaluation',
        on_delete=models.CASCADE,
        related_name='axis_scores',
        help_text="Avaliação relacionada"
    )
    axis = models.ForeignKey(
        EvaluationAxis,
        on_delete=models.PROTECT,
        related_name='scores',
        help_text="Eixo de avaliação"
    )
    score_obtained = models.FloatField(
        default=0,
        help_text="Pontuação obtida neste eixo"
    )
    max_score_possible = models.FloatField(
        default=0,
        help_text="Pontuação máxima possível para este eixo (baseada no porte da empresa)"
    )
    percentage = models.FloatField(
        default=0,
        help_text="Percentual de atingimento (score_obtained / max_score_possible * 100)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['axis__order']
        unique_together = [['evaluation', 'axis']]
        verbose_name = "Pontuação por Eixo"
        verbose_name_plural = "Pontuações por Eixo"

    def __str__(self):
        return f"{self.evaluation.id} - {self.axis.name}: {self.percentage:.1f}%"

    def calculate_percentage(self):
        """Calcula e atualiza o percentual de atingimento"""
        if self.max_score_possible > 0:
            self.percentage = (self.score_obtained / self.max_score_possible) * 100
        else:
            self.percentage = 0
        return self.percentage

    def save(self, *args, **kwargs):
        """Calcula o percentual antes de salvar"""
        self.calculate_percentage()
        super().save(*args, **kwargs)

    @staticmethod
    def calculate_axis_scores(evaluation, answers):
        """
        Calcula as pontuações por eixo para uma avaliação.

        Args:
            evaluation: Instância de InnovationEvaluation
            answers: Dict com respostas {question_number: choice_value}

        Returns:
            List de dicionários com os scores por eixo
        """
        if not evaluation.company_size:
            return []

        company_level = answers.get(1)
        if not company_level:
            return []

        company_size_code = COMPANY_SIZE.get(company_level)
        if not company_size_code:
            return []

        axis_scores = []

        # Para cada eixo de avaliação
        for axis in EvaluationAxis.objects.all():
            score_obtained = 0.0
            max_score = axis.max_score_by_size.get(company_size_code, 0)

            # Somar pontuação de todas as questões deste eixo
            for question in axis.questions.all():
                question_number = question.order
                selected_level = answers.get(question_number, 0)

                if selected_level > 0 and question_number in QUESTION_WEIGHTS:
                    weight = QUESTION_WEIGHTS[question_number].get(company_size_code, 0)
                    # Fórmula: (nivel_escolhido / 5) × Peso
                    score_obtained += (selected_level / 5.0) * weight

            # Calcular percentual
            percentage = (score_obtained / max_score * 100) if max_score > 0 else 0

            axis_scores.append({
                'axis': axis,
                'score_obtained': round(score_obtained, 2),
                'max_score_possible': round(max_score, 2),
                'percentage': round(percentage, 2)
            })

        return axis_scores

    @staticmethod
    def create_axis_scores_for_evaluation(evaluation, answers):
        """
        Cria os registros de AxisScore para uma avaliação.

        Args:
            evaluation: Instância de InnovationEvaluation
            answers: Dict com respostas {question_number: choice_value}
        """
        # Deletar scores anteriores se existirem
        AxisScore.objects.filter(evaluation=evaluation).delete()

        # Calcular e criar novos scores
        axis_scores_data = AxisScore.calculate_axis_scores(evaluation, answers)

        for score_data in axis_scores_data:
            AxisScore.objects.create(
                evaluation=evaluation,
                axis=score_data['axis'],
                score_obtained=score_data['score_obtained'],
                max_score_possible=score_data['max_score_possible']
            )

        return AxisScore.objects.filter(evaluation=evaluation)


class EvaluationAnswer(models.Model):
    evaluation = models.ForeignKey(
        InnovationEvaluation,
        on_delete=models.CASCADE,
        related_name='answers',
        help_text="Avaliação relacionada"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        help_text="Pergunta respondida"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.PROTECT,
        help_text="Opção escolhida"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['evaluation', 'question__order']
        unique_together = [['evaluation', 'question']]
        verbose_name = "Resposta da Avaliação"
        verbose_name_plural = "Respostas das Avaliações"

    def __str__(self):
        return f"{self.evaluation.id} - Pergunta {self.question.order}: {self.choice.value}"

    @staticmethod
    def calculate_weighted_score(answers):
        """
        Calcula a pontuação ponderada com base nas respostas.

        Fórmula: Total Ponderado da Linha = (Nível Escolhido / 5) × Peso do Seu Porte
        """
        company_level = answers.get(1)

        if company_level is None:
            print("❌ ERRO: Sem resposta para pergunta 1")
            return None

        level = COMPANY_SIZE.get(company_level)
        if not level:
            print(f"❌ ERRO: Porte inválido para nivel {company_level}")
            return None

        print("\n" + "=" * 70)
        print(f"📊 CÁLCULO DE PONTUAÇÃO PONDERADA")
        print("=" * 70)
        print(f"🏢 Porte da Empresa (Pergunta 1): {level} (nível {company_level})")
        print(f"📐 Fórmula: (Nível Escolhido / 5) × Peso do Porte")
        print("=" * 70)

        total_weighted = 0.0

        # Desconsiderar a primeira pergunta
        for question_number in range(2, 13):
            selected_level = answers.get(question_number, 0)
            if selected_level == 0:
                print(f"⏭️  Pergunta {question_number}: Não respondida (pulando)")
                continue

            weight = QUESTION_WEIGHTS[question_number][level]

            # Fórmula: (nivel_escolhido / 5) × Peso
            total_weighted_line = (selected_level / 5.0) * weight
            total_weighted += total_weighted_line

            print(
                f"✓ Pergunta {question_number:2d}: ({selected_level} / 5) × {weight:5.1f} = {total_weighted_line:6.2f}")

        print("=" * 70)
        print(f"🎯 PONTUAÇÃO TOTAL: {round(total_weighted, 2)}")
        print("=" * 70 + "\n")

        return round(total_weighted, 2)

    @staticmethod
    def get_question_weight(question_number, company_level):
        """
        Retorna o peso de uma pergunta específica para um porte de empresa.
        """
        if question_number not in QUESTION_WEIGHTS:
            return None

        if company_level is None:
            return None

        level = COMPANY_SIZE.get(company_level)
        if not level:
            return None

        return QUESTION_WEIGHTS[question_number].get(level)

