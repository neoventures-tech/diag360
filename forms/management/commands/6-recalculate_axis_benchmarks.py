from django.core.management.base import BaseCommand
from forms.models import AxisScore, EvaluationAxis
from django.db.models import Max


class Command(BaseCommand):
    help = 'Recalcula os benchmarks (melhor percentual histórico) de todos os AxisScores'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Recalculando benchmarks para todos os AxisScores...'))
        self.stdout.write('=' * 80)

        # Para cada eixo, calcular o benchmark
        axes = EvaluationAxis.objects.all()

        for axis in axes:
            # Buscar o melhor percentual deste eixo
            best_percentage = AxisScore.objects.filter(axis=axis).aggregate(
                Max('percentage')
            )['percentage__max']

            if best_percentage is None:
                self.stdout.write(
                    self.style.WARNING(f'⚠ {axis.name}: Nenhum score encontrado')
                )
                continue

            # Atualizar todos os AxisScores deste eixo
            updated_count = AxisScore.objects.filter(axis=axis).update(benchmark=best_percentage)

            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ {axis.name}: {updated_count} registros atualizados (benchmark: {best_percentage:.1f}%)'
                )
            )

        self.stdout.write('\n' + '=' * 80)

        # Mostrar resumo por eixo
        self.stdout.write('\nBenchmarks por eixo:')
        self.stdout.write('=' * 80)

        for axis in axes:
            scores = AxisScore.objects.filter(axis=axis)
            if scores.exists():
                best = scores.aggregate(Max('percentage'))['percentage__max']
                avg = sum([s.percentage for s in scores]) / scores.count()

                self.stdout.write(
                    f'{axis.name:15s}: Melhor = {best:6.1f}% | Média = {avg:6.1f}% | Total registros = {scores.count()}'
                )

        self.stdout.write('=' * 80)
        self.stdout.write(self.style.SUCCESS('\n✓ Benchmarks recalculados com sucesso!'))
