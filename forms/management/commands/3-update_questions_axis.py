from django.core.management.base import BaseCommand
from forms.models import Question, EvaluationAxis


class Command(BaseCommand):
    help = 'Atualiza as questões existentes associando-as aos eixos de avaliação'

    def handle(self, *args, **options):
        # Mapping de cada questão ao seu eixo de avaliação (baseado no xlsx)
        # Questão 1 (Pergunta direcionadora) não tem eixo
        question_axis_mapping = {
            2: 'LEADERSHIP',        # Liderança
            3: 'STRATEGY',          # Estratégia
            4: 'GOVERNANCE',        # Governança
            5: 'RESOURCES',         # Recursos
            6: 'RESOURCES',         # Recursos
            7: 'PROCESSES',         # Processos
            8: 'PROCESSES',         # Processos
            9: 'PROCESSES',         # Processos
            10: 'RESULTS',          # Resultados
            11: 'RESULTS',          # Resultados
            12: 'RESULTS',          # Resultados
        }

        self.stdout.write(self.style.SUCCESS('Atualizando questões com eixos de avaliação...'))

        # Remover eixo da questão 1 (pergunta direcionadora)
        try:
            question_1 = Question.objects.get(order=1)
            question_1.axis = None
            question_1.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Questão 1 (pergunta direcionadora) configurada sem eixo')
            )
        except Question.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('⚠ Questão 1 não encontrada')
            )

        updated_count = 0
        not_found_count = 0

        for question_order, axis_code in question_axis_mapping.items():
            try:
                question = Question.objects.get(order=question_order)

                try:
                    axis = EvaluationAxis.objects.get(code=axis_code)
                    question.axis = axis
                    question.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Questão {question.order} associada ao eixo: {axis.name}')
                    )
                except EvaluationAxis.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Eixo {axis_code} não encontrado para questão {question_order}')
                    )
                    not_found_count += 1

            except Question.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Questão {question_order} não encontrada no banco de dados')
                )
                not_found_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ {updated_count} questões atualizadas com sucesso!')
        )
        if not_found_count > 0:
            self.stdout.write(
                self.style.WARNING(f'⚠ {not_found_count} questões ou eixos não encontrados')
            )
