from django.core.management.base import BaseCommand
from forms.models import (
    InnovationEvaluation,
    EvaluationAnswer,
    AxisScore,
    Question,
    Choice,
    EvaluationAxis,
    MaturityLevel,
    PriorityAction,
    SalesTrigger,
    InnovationLevelMaintenance
)


class Command(BaseCommand):
    help = 'Limpa todo o banco de dados mantendo apenas os usuários'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Confirma a limpeza sem pedir confirmação interativa',
        )

    def handle(self, *args, **options):
        # Contagem antes da limpeza
        counts = {
            'evaluations': InnovationEvaluation.objects.count(),
            'answers': EvaluationAnswer.objects.count(),
            'axis_scores': AxisScore.objects.count(),
            'questions': Question.objects.count(),
            'choices': Choice.objects.count(),
            'axes': EvaluationAxis.objects.count(),
            'maturity_levels': MaturityLevel.objects.count(),
            'priority_actions': PriorityAction.objects.count(),
            'sales_triggers': SalesTrigger.objects.count(),
            'maintenance_actions': InnovationLevelMaintenance.objects.count(),
        }

        self.stdout.write(
            self.style.WARNING('\n' + '=' * 80)
        )
        self.stdout.write(
            self.style.WARNING('⚠️  ATENÇÃO: LIMPEZA DO BANCO DE DADOS')
        )
        self.stdout.write(
            self.style.WARNING('=' * 80)
        )
        self.stdout.write('\nOs seguintes dados serão PERMANENTEMENTE deletados:\n')

        for model_name, count in counts.items():
            if count > 0:
                self.stdout.write(f'  • {model_name}: {count} registros')

        self.stdout.write(
            self.style.SUCCESS('\n✓ Os usuários e suas senhas serão MANTIDOS\n')
        )

        # Confirmação
        if not options['yes']:
            self.stdout.write(
                self.style.WARNING('Digite "LIMPAR" (em maiúsculas) para confirmar a operação:')
            )
            confirmation = input('> ')

            if confirmation != 'LIMPAR':
                self.stdout.write(
                    self.style.ERROR('\n❌ Operação cancelada pelo usuário.\n')
                )
                return

        self.stdout.write(
            self.style.WARNING('\n' + '=' * 80)
        )
        self.stdout.write(
            self.style.WARNING('🗑️  INICIANDO LIMPEZA DO BANCO DE DADOS...')
        )
        self.stdout.write(
            self.style.WARNING('=' * 80 + '\n')
        )

        # Ordem de deleção respeitando as foreign keys
        deletions = [
            ('Respostas de Avaliações', EvaluationAnswer),
            ('Scores por Eixo', AxisScore),
            ('Avaliações de Inovação', InnovationEvaluation),
            ('Opções de Resposta', Choice),
            ('Questões', Question),
            ('Ações Prioritárias', PriorityAction),
            ('Gatilhos de Venda', SalesTrigger),
            ('Ações de Manutenção', InnovationLevelMaintenance),
            ('Níveis de Maturidade', MaturityLevel),
            ('Eixos de Avaliação', EvaluationAxis),
        ]

        for model_name, model_class in deletions:
            count = model_class.objects.count()
            if count > 0:
                model_class.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {model_name}: {count} registros deletados')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⏭  {model_name}: nenhum registro para deletar')
                )

        self.stdout.write(
            self.style.SUCCESS('\n' + '=' * 80)
        )
        self.stdout.write(
            self.style.SUCCESS('✅ LIMPEZA CONCLUÍDA COM SUCESSO!')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 80)
        )
        self.stdout.write(
            self.style.SUCCESS('\n💡 Dica: Execute "python manage.py 0-populate_all" para repopular o banco\n')
        )
