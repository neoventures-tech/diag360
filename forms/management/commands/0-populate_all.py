from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Executa todos os comandos de população do banco de dados na ordem correta'

    def handle(self, *args, **options):
        commands = [
            ('1-populate_maturity_levels', 'Níveis de Maturidade, Ações Prioritárias, Gatilhos de Venda e Manutenção'),
            ('2-populate_axis', 'Eixos de Avaliação'),
            ('3-populate_questions', 'Questões e Opções'),
            ('4-calculate_axis_max_scores', 'Pontuações Máximas dos Eixos'),
            ('5-populate_axis_scores_for_existing', 'Scores de Eixos para Avaliações Existentes'),
            ('6-recalculate_axis_benchmarks', 'Benchmarks dos Eixos'),
        ]

        self.stdout.write(
            self.style.SUCCESS('\n' + '=' * 80)
        )
        self.stdout.write(
            self.style.SUCCESS('🚀 EXECUTANDO TODOS OS COMANDOS DE POPULAÇÃO')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 80 + '\n')
        )

        for idx, (command_name, description) in enumerate(commands, 1):
            self.stdout.write(
                self.style.WARNING(f'\n[{idx}/{len(commands)}] Executando: {command_name}')
            )
            self.stdout.write(
                self.style.WARNING(f'     Descrição: {description}')
            )
            self.stdout.write(
                self.style.WARNING('-' * 80)
            )

            try:
                call_command(command_name)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {command_name} concluído com sucesso!\n')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao executar {command_name}: {str(e)}\n')
                )
                self.stdout.write(
                    self.style.ERROR('Abortando execução...\n')
                )
                return

        self.stdout.write(
            self.style.SUCCESS('\n' + '=' * 80)
        )
        self.stdout.write(
            self.style.SUCCESS('✅ TODOS OS COMANDOS FORAM EXECUTADOS COM SUCESSO!')
        )
        self.stdout.write(
            self.style.SUCCESS('=' * 80 + '\n')
        )
