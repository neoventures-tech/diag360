from django.core.management.base import BaseCommand
from forms.models import InnovationEvaluation, AxisScore, EvaluationAnswer


class Command(BaseCommand):
    help = 'Popula os AxisScores para avaliações existentes que ainda não têm'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populando AxisScores para avaliações existentes...'))
        self.stdout.write('=' * 80)

        evaluations = InnovationEvaluation.objects.all()

        if not evaluations.exists():
            self.stdout.write(self.style.WARNING('Nenhuma avaliação encontrada!'))
            return

        processed = 0
        skipped = 0
        errors = 0

        for evaluation in evaluations:
            # Verificar se já tem AxisScores
            existing_scores = AxisScore.objects.filter(evaluation=evaluation).count()

            if existing_scores > 0:
                self.stdout.write(
                    self.style.WARNING(f'⏭  Avaliação {evaluation.id} já possui {existing_scores} AxisScores - pulando')
                )
                skipped += 1
                continue

            try:
                # Coletar respostas
                answers = {}
                for answer in evaluation.answers.all():
                    answers[answer.question.order] = answer.choice.value

                # Criar AxisScores
                axis_scores = AxisScore.create_axis_scores_for_evaluation(evaluation, answers)

                self.stdout.write(
                    self.style.SUCCESS(f'✓ Avaliação {evaluation.id}: {axis_scores.count()} AxisScores criados')
                )

                # Mostrar detalhes
                for axis_score in axis_scores:
                    self.stdout.write(
                        f'  {axis_score.axis.name}: {axis_score.score_obtained:.2f}/{axis_score.max_score_possible:.2f} ({axis_score.percentage:.1f}%)'
                    )

                processed += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Erro ao processar avaliação {evaluation.id}: {str(e)}')
                )
                errors += 1

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Processadas: {processed}'))
        self.stdout.write(self.style.WARNING(f'⏭  Puladas: {skipped}'))

        if errors > 0:
            self.stdout.write(self.style.ERROR(f'✗ Erros: {errors}'))
