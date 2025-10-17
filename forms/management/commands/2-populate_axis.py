from django.core.management.base import BaseCommand
from forms.models import EvaluationAxis


class Command(BaseCommand):
    help = 'Popula os eixos de avaliação ISO 56002 no banco de dados'

    def handle(self, *args, **options):
        axes_data = [
            {
                'name': 'Liderança',
                'code': 'LEADERSHIP',
                'order': 1,
                'description': 'Avalia o comprometimento da alta liderança com a inovação'
            },
            {
                'name': 'Estratégia',
                'code': 'STRATEGY',
                'order': 2,
                'description': 'Verifica o alinhamento das iniciativas de inovação com a estratégia corporativa'
            },
            {
                'name': 'Governança',
                'code': 'GOVERNANCE',
                'order': 3,
                'description': 'Avalia a estrutura organizacional dedicada à gestão da inovação'
            },
            {
                'name': 'Recursos',
                'code': 'RESOURCES',
                'order': 4,
                'description': 'Avalia a disponibilidade de recursos financeiros e humanos para inovação'
            },
            {
                'name': 'Processos',
                'code': 'PROCESSES',
                'order': 5,
                'description': 'Avalia os processos de inovação, incluindo monitoramento de tendências e funis de inovação'
            },
            {
                'name': 'Resultados',
                'code': 'RESULTS',
                'order': 6,
                'description': 'Avalia os resultados e impactos da inovação na organização'
            },
        ]

        self.stdout.write(self.style.SUCCESS('Criando/atualizando eixos de avaliação...'))

        created_count = 0
        updated_count = 0

        for axis_data in axes_data:
            axis, created = EvaluationAxis.objects.update_or_create(
                code=axis_data['code'],
                defaults={
                    'name': axis_data['name'],
                    'order': axis_data['order'],
                    'description': axis_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Criado eixo {axis.order}: {axis.name} ({axis.code})'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Atualizado eixo {axis.order}: {axis.name} ({axis.code})'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal: {created_count} eixos criados, {updated_count} atualizados!'))
