from django.core.management.base import BaseCommand
from forms.models import EvaluationAxis


class Command(BaseCommand):
    help = 'Calcula e atualiza as pontuações máximas de cada eixo de avaliação por porte de empresa'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Calculando pontuações máximas para cada eixo...'))
        self.stdout.write('=' * 80)

        axes = EvaluationAxis.objects.all()

        if not axes.exists():
            self.stdout.write(self.style.WARNING('Nenhum eixo de avaliação encontrado!'))
            return

        for axis in axes:
            max_scores = axis.update_max_scores()

            self.stdout.write(f'\n📊 {axis.name} ({axis.code})')
            self.stdout.write('-' * 80)

            for size_code, score in max_scores.items():
                self.stdout.write(f'  {size_code:4s}: {score:6.2f} pontos')

            self.stdout.write(self.style.SUCCESS(f'✓ Eixo atualizado'))

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS(f'\n✓ {axes.count()} eixos atualizados com sucesso!'))

        # Verificar se a soma dos máximos dá 100 para cada porte
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write('VERIFICAÇÃO: Soma total de pontuações máximas por porte')
        self.stdout.write('=' * 80)

        totals = {
            'PE': 0.0,
            'PME': 0.0,
            'ME': 0.0,
            'GE': 0.0,
            'GGE': 0.0,
        }

        for axis in axes:
            for size_code in totals.keys():
                totals[size_code] += axis.max_score_by_size.get(size_code, 0)

        for size_code, total in totals.items():
            status = '✓' if abs(total - 100.0) < 0.1 else '⚠'
            self.stdout.write(f'{status} {size_code:4s}: {total:6.2f} / 100.00')
