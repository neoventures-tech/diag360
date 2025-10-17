from django.core.management.base import BaseCommand
from forms.models import Question, Choice, EvaluationAxis


class Command(BaseCommand):
    help = 'Popula as questões e opções no banco de dados a partir do forms.py'

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

        questions_data = [
            {
                'order': 1,
                'field_name': 'question1',
                'label': 'Qual é o Porte e Escala da sua organização em termos de faturamento e complexidade operacional?',
                'choices': [
                    (1, "A empresa está em fase pré-operacional ou de ideação e ainda não gera faturamento significativo."),
                    (2, "O faturamento é de até R$ 4,8 milhões/ano. Foco total na sobrevivência e na eficiência básica (micro/pequena)."),
                    (3, "O faturamento está na faixa de R$ 4,8 milhões a R$ 10 milhões/ano. A empresa busca formalização e precisa estruturar os primeiros processos."),
                    (4, "O faturamento está na faixa de R$ 10 milhões a R$ 100 milhões/ano. A empresa possui estrutura departamental e está em fase de escalabilidade regional."),
                    (5, "Muito grande empresa - O faturamento está acima de R$ 100 milhões ao ano. A empresa já é consolidada e gerencia um portfólio complexo de produtos/serviços."),
                ]
            },
            {
                'order': 2,
                'field_name': 'question2',
                'label': 'A alta liderança está comprometida com a inovação, comunica sua visão e prioriza iniciativas?',
                'choices': [
                    (1, "O CEO menciona inovação de vez em quando em discursos, mas não há ações ou tempo dedicados."),
                    (2, "A liderança patrocina projetos-piloto isolados, mas o comprometimento oscila com os resultados trimestrais."),
                    (3, "A liderança participa ativamente do Comitê de Inovação, comunica formalmente a visão e aloca orçamento."),
                    (4, "A liderança incorpora a inovação na estratégia anual, usando métricas no seu próprio bônus."),
                    (5, "O CEO e executivos atuam como Embaixadores da Inovação, liderando a busca por insights e revisando a estratégia."),
                ]
            },
            {
                'order': 3,
                'field_name': 'question3',
                'label': 'As iniciativas de inovação estão alinhadas à estratégia e contribuem para os resultados?',
                'choices': [
                    (1, "O alinhamento é intuitivo, mas não há metas formais ou mensuração de como a inovação apoia a estratégia."),
                    (2, "Há metas de alto nível para inovação (ex: novo mercado), mas elas não são desdobradas nem monitoradas de forma consistente."),
                    (3, "A inovação é direcionada por metas de alto nível e monitorada em relatórios gerenciais trimestrais."),
                    (4, "O alinhamento é bicondicional: inovação é uma prioridade estratégica, e as metas são revisadas mutuamente com a estratégia corporativa."),
                    (5, "A estratégia do negócio é revisada anualmente com base nas oportunidades geradas pela inovação, sendo o driver central de crescimento."),
                ]
            },
            {
                'order': 4,
                'field_name': 'question4',
                'label': 'A empresa possui uma área funcional, equipe ou comitê formalmente estabelecido e dedicado a gerir as iniciativas?',
                'choices': [
                    (1, "Existe uma pessoa (ou grupo) responsável pela inovação, mas o papel é secundário e não formalizado em organograma."),
                    (2, "Existe um Comitê de Inovação com reuniões irregulares, mas sem poder de decisão ou orçamento próprio."),
                    (3, "Existe um Comitê de Inovação com reuniões mensais e uma equipe dedicada (ou PMO) com escopo e orçamento definidos."),
                    (4, "A governança é ágil, atuando como investidor de portfólio, integrando times multidisciplinares de forma fluida para cada projeto."),
                    (5, "A estrutura de inovação é uma central de serviço para o negócio, capacitando as unidades operacionais a inovar de forma autônoma (estrutura descentralizada)."),
                ]
            },
            {
                'order': 5,
                'field_name': 'question5',
                'label': 'Existe um orçamento centralizado e suficiente para as iniciativas de inovação, bem como recursos distribuídos?',
                'choices': [
                    (1, "Há um valor, mas é insuficiente e consumido por custos operacionais, não sobrando capital para novos projetos."),
                    (2, "Há um orçamento dedicado, mas não há critérios para investimento e o funding é competitivo com a operação."),
                    (3, "Há um orçamento dedicado com critérios claros para investimento e um processo formal de follow-up financeiro."),
                    (4, "O orçamento é dual (exploração/manutenção), com funding assegurado e autonomia delegada às áreas para iniciativas menores."),
                    (5, "O funding é visto como capital de risco estratégico, com modelos de investimento adaptados ao nível de incerteza do projeto (ex: venture capital interno)."),
                ]
            },
            {
                'order': 6,
                'field_name': 'question6',
                'label': 'A organização disponibiliza recursos humanos suficientes para inovação (tempo, competências), além da equipe dedicada?',
                'choices': [
                    (1, "O colaborador precisa pedir permissão para dedicar tempo à inovação, o que é raramente concedido."),
                    (2, "Há treinamentos em metodologias (Design Thinking, Agilidade) e o tempo para inovação é incentivado, mas não formalizado."),
                    (3, "Os colaboradores têm tempo alocado (ex: 10% do tempo) para projetos de inovação, e a inovação é um item de avaliação de desempenho."),
                    (4, "Há um programa estruturado de gestão de talentos de inovação, com rotatividade planejada para disseminar conhecimento."),
                    (5, "A empresa atrai ativamente talentos pela sua reputação em inovação, e a capacidade de inovar é um diferencial competitivo no RH."),
                ]
            },
            {
                'order': 7,
                'field_name': 'question7',
                'label': 'A empresa realiza monitoramento de tendências para orientar as decisões de inovação?',
                'choices': [
                    (1, "O monitoramento é feito de forma manual e esporádica por indivíduos-chave; não há repositório ou compartilhamento."),
                    (2, "A empresa realiza pesquisas anuais de tendências, mas o conhecimento não é usado formalmente para iniciar projetos."),
                    (3, "A empresa possui um repositório formal de tendências, e a liderança o utiliza como input obrigatório no início de novos projetos."),
                    (4, "O monitoramento é contínuo e sistemático (ferramentas de scanning), e influencia diretamente a revisão do portfólio e a estratégia de M&A."),
                    (5, "A empresa possui redes de inovação aberta (parcerias com startups/universidades) que geram insights constantes, atuando como um radar global."),
                ]
            },
            {
                'order': 8,
                'field_name': 'question8',
                'label': 'Existe um funil de inovação formal, eficiente e eficaz para a melhoria de produtos e serviços existentes, que funciona de forma comprovada?',
                'choices': [
                    (1, "Existe uma caixa de sugestões, mas o feedback é inconsistente e o sucesso dos projetos é acidental."),
                    (2, "Há um funil com etapas, mas ele é lento e burocrático, ou a taxa de conversão de ideias em resultados é muito baixa."),
                    (3, "Há um funil de ideias para melhoria (ex: sugestões de funcionários), com critérios de priorização e follow-up de resultados."),
                    (4, "O funil incremental é totalmente automatizado e integrado ao ciclo de vida do produto (PDCA), gerando savings e ganhos de eficiência mensuráveis."),
                    (5, "O processo de melhoria é autogerenciado pelos times operacionais e funde-se com a cultura Lean, gerando otimização contínua de classe mundial."),
                ]
            },
            {
                'order': 9,
                'field_name': 'question9',
                'label': 'Existe um funil de inovação formal para a criação de novos produtos, serviços ou processos com etapas definidas?',
                'choices': [
                    (1, "Os projetos radicais seguem a metodologia de projetos de rotina (Waterfall), que é inadequada para a incerteza da inovação."),
                    (2, "Existe um processo (Stage-Gate ou Agile), mas ele é parcialmente aplicado e os critérios de avanço/morte dos projetos não são claros."),
                    (3, "Existe um processo de Stage-Gate ou metodologia ágil (Lean Startup) com critérios claros para avançar (ou matar) as inovações radicais."),
                    (4, "Os processos de inovação incremental e radical são claramente diferenciados e gerenciados como um portfólio com riscos e retornos balanceados."),
                    (5, "A organização possui múltiplos \"motores de crescimento\" (ex: Corporate Ventures) que financiam e escalam inovações radicais com sucesso."),
                ]
            },
            {
                'order': 10,
                'field_name': 'question10',
                'label': 'A organização possui indicadores claros para medir o desempenho e os monitora continuamente para provocar a melhoria?',
                'choices': [
                    (1, "Existem alguns indicadores de output (ex: número de ideias), mas o monitoramento é inconsistente (anual ou trimestral)."),
                    (2, "Há um painel (dashboard) de KPIs de inovação (ex: throughput do funil) revisado mensalmente, mas sem impacto nas decisões."),
                    (3, "Os KPIs são ligados aos objetivos da área de inovação, e o monitoramento gera relatórios que são usados para justificar o orçamento."),
                    (4, "Os KPIs são ligados aos bônus da liderança, e o monitoramento gera ações de melhoria no próprio processo de inovação (double-loop learning)."),
                    (5, "A área utiliza análise preditiva e benchmarking constante, com os indicadores de inovação antecipando resultados operacionais e de mercado."),
                ]
            },
            {
                'order': 11,
                'field_name': 'question11',
                'label': 'No último ano, a empresa obteve receita relevante oriunda de novos produtos ou serviços lançados ao mercado?',
                'choices': [
                    (1, "Houve receita, mas ela não cobre o custo dos projetos de inovação. É uma exceção, não uma regra."),
                    (2, "A empresa possui uma meta interna de receita de novos produtos, mas raramente a atinge ou o valor é pouco expressivo."),
                    (3, "A empresa possui uma meta anual de receita de novos produtos (ex: 5% da receita) e a atinge consistentemente."),
                    (4, "A receita de inovações radicais é a principal fonte de crescimento da empresa nos últimos 3 anos, ultrapassando os concorrentes."),
                    (5, "O Novo Valor gerado é monitorado por métricas de margem e rentabilidade, provando que a inovação é o motor de lucro da empresa."),
                ]
            },
            {
                'order': 12,
                'field_name': 'question12',
                'label': 'A área de inovação (ou a função) possui relevância e legitimidade interna e externa?',
                'choices': [
                    (1, "A área é tolerada, mas raramente consultada e tem dificuldade em obter buy-in de outras áreas operacionais."),
                    (2, "A área é consultada para novos projetos e possui reconhecimento interno por ter entregue resultados pequenos, mas consistentes."),
                    (3, "A área de inovação tem poder de influência e colabora formalmente com outras áreas (Marketing, TI, Operações) no planejamento."),
                    (4, "A área é referência de mercado em inovação e tem poder de veto sobre projetos que não estejam alinhados à visão de futuro da empresa."),
                    (5, "A área de inovação é vista como parceira estratégica da alta liderança, sendo um fator-chave na retenção de talentos e na atração de negócios."),
                ]
            },
        ]

        self.stdout.write(self.style.SUCCESS('Atualizando questões e opções...'))
        for q_data in questions_data:
            # Buscar o eixo de avaliação para esta questão
            axis_code = question_axis_mapping.get(q_data['order'])
            axis = None
            if axis_code:
                try:
                    axis = EvaluationAxis.objects.get(code=axis_code)
                except EvaluationAxis.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Eixo {axis_code} não encontrado para questão {q_data["order"]}')
                    )

            # Cria ou atualiza a questão
            question, created = Question.objects.update_or_create(
                order=q_data['order'],
                defaults={
                    'field_name': q_data['field_name'],
                    'label': q_data['label'],
                    'axis': axis,
                    'is_active': True
                }
            )

            # Cria ou atualiza as opções de resposta
            for idx, (value, text) in enumerate(q_data['choices'], start=1):
                _, choice_created = Choice.objects.update_or_create(
                    question=question,
                    value=value,
                    defaults={
                        'text': text,
                        'order': idx
                    }
                )

            action_verb = 'Criada' if created else 'Atualizada'
            axis_info = f' (Eixo: {axis.name})' if axis else ''
            self.stdout.write(self.style.SUCCESS(f'✓ {action_verb} questão {question.order}: {question.field_name}{axis_info}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Concluído! Total no banco: {Question.objects.count()} questões.'))
