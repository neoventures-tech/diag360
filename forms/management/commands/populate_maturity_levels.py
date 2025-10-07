from django.core.management.base import BaseCommand
from forms.models import MaturityLevel, PriorityAction
MATURITY_LEVELS = {
    1: {
        "faixa": (0, 20),
        "nivel": "Nível 1: Inicial / Caótico",
        "foco": "Consciência e Patrocínio Executivo.",
        "descricao": "A empresa está começando sua jornada de inovação. Falta estrutura formal, processos e comprometimento consistente da liderança.",
        "acoes_prioritarias": {
            "PE": "Definir o Dono da Inovação (CEO ou Líder) e garantir tempo alocado para ideias (5% do tempo).",
            "PME": "Garantir Patrocínio e alocar um orçamento mínimo para as primeiras iniciativas.",
            "ME": "Obter buy-in formal da liderança e treinar 1-2 líderes em metodologias básicas de inovação.",
            "GE": "Alocar um sponsor executivo e definir a área responsável (ex: P&D/Estratégia) para iniciar o mapeamento.",
            "GGE": "Garantir o Fundo Dedicado (capital de risco) e alinhar a visão de inovação com o C-Level para superar a inércia.",
        }
    },
    2: {
        "faixa": (21, 40),
        "nivel": "Nível 2: Emergente / Reativo",
        "foco": "Formalização e Processos Básicos.",
        "descricao": "A empresa possui alguma consciência sobre inovação, mas ainda é reativa. Processos básicos estão sendo implementados.",
        "acoes_prioritarias": {
            "PE": "Criar o primeiro funil de ideias focado em Melhoria de Processos (Incremental) para gerar eficiência imediata.",
            "PME": "Formalizar um Comitê de Governança da Inovação e desenhar um funil básico de ideias/melhorias.",
            "ME": "Implementar um Funil de Inovação e estabelecer 3 KPIs básicos de input e throughput (taxa de conversão).",
            "GE": "Formalizar o Comitê de Governança e mapear as competências necessárias para a inovação (upskilling).",
            "GGE": "Estruturar o radar de tendências (Q6) e monitoramento de sinais externos para alimentar o funil estrategicamente.",
        }
    },
    3: {
        "faixa": (41, 60),
        "nivel": "Nível 3: Gerenciado / Funcional",
        "foco": "Integração Estratégica e Mensuração.",
        "descricao": "A inovação está integrada à estratégia da empresa. Há processos formais, métricas definidas e resultados mensuráveis.",
        "acoes_prioritarias": {
            "PE": "Integrar as Metas de inovação (ex: savings) aos objetivos anuais da empresa e criar o primeiro dashboard de ROI.",
            "PME": "Focar no Alinhamento Estratégico (Q2): garantir que o funil trabalhe os maiores desafios da empresa para escalar resultados.",
            "ME": "Formalizar o Funil Radical (Novos Negócios) e separá-lo da Inovação Incremental para evitar conflitos de foco e métricas.",
            "GE": "Garantir que a estrutura dedicada (Q3) tenha autoridade para tomar decisões de portfólio e para encerrar projetos sem resultados.",
            "GGE": "Integrar a área de Inovação com as áreas de Negócio (ex: secondment de colaboradores) e usar o ROI para justificar investimentos anuais.",
        }
    },
    4: {
        "faixa": (61, 80),
        "nivel": "Nível 4: Otimizado / Integrado",
        "foco": "Excelência Operacional e Inovação Contínua.",
        "descricao": "A inovação é parte da cultura organizacional. Processos otimizados, inovação aberta e gestão de portfólio bem estabelecida.",
        "acoes_prioritarias": {
            "PE": "Otimizar o Funil Incremental para melhorar a taxa de conversão (ideia > resultado) e usar o aprendizado para revisar o orçamento (orçamento otimizado).",
            "PME": "Estruturar um programa de Embaixadores da Inovação para disseminar a cultura e envolver colaboradores de todas as áreas (Q5).",
            "ME": "Estruturar um processo de Inovação Aberta simples (ex: parceria com 1 ou 2 startups) para testar tecnologias externas.",
            "GE": "Implementar a gestão de Portfólio (balanceamento de risco/retorno) e fortalecer o Programa de Inovação Aberta.",
            "GGE": "Aprimorar a Legitimidade Externa (Q11): focar na reputação, parcerias com universidades e uso de benchmarking global.",
        }
    },
    5: {
        "faixa": (81, 100),
        "nivel": "Nível 5: Disruptivo / Referência",
        "foco": "Vantagem Competitiva e Expansão de Fronteiras.",
        "descricao": "A empresa é referência em inovação no mercado. Capacidade de criar e escalar inovações disruptivas, influenciando o setor.",
        "acoes_prioritarias": {
            "PE": "Fazer uma revisão estratégica para definir se é hora de escalar (tornar-se PME) ou criar um novo core de negócio (inovação radical).",
            "PME": "Estruturar um veículo de Corporate Venture simples (internal incubator) para desdobrar a inovação radical de forma semi-autônoma.",
            "ME": "Criar um programa de Corporate Venture Capital (CVC) com foco em startups adjacentes para aquisição de novas tecnologias e mercados.",
            "GE": "Fortalecer a área de Inovação como uma parceira estratégica da alta liderança e influenciar o roadmap do setor em nível nacional.",
            "GGE": "Explorar Novas Fronteiras de Mercado, atuar como referência global em gestão de inovação e garantir que o processo seja à prova de burocracia.",
        }
    },
}

class Command(BaseCommand):
    help = 'Popula os níveis de maturidade e ações prioritárias no banco de dados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Removendo níveis de maturidade e ações prioritárias existentes...'))
        MaturityLevel.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Criando níveis de maturidade...'))

        for level_num, level_data in MATURITY_LEVELS.items():
            min_score, max_score = level_data['faixa']

            # Cria o nível de maturidade
            maturity_level = MaturityLevel.objects.create(
                level_number=level_num,
                min_score=min_score,
                max_score=max_score,
                name=level_data['nivel'],
                focus=level_data['foco'],
                description=level_data['descricao']
            )

            self.stdout.write(
                self.style.SUCCESS(f'✓ Criado nível {level_num}: {level_data["nivel"]} ({min_score}-{max_score} pontos)')
            )

            # Cria as ações prioritárias para cada porte de empresa
            for company_size, action in level_data['acoes_prioritarias'].items():
                PriorityAction.objects.create(
                    maturity_level=maturity_level,
                    company_size=company_size,
                    action=action
                )
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Criada ação para {company_size}')
                )

        total_levels = MaturityLevel.objects.count()
        total_actions = PriorityAction.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Concluído! {total_levels} níveis de maturidade e {total_actions} ações prioritárias criadas.'
            )
        )