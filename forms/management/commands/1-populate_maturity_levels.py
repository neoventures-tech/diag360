from django.core.management.base import BaseCommand
from forms.models import MaturityLevel, PriorityAction, SalesTrigger, InnovationLevelMaintenance

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
        },
        "gatilhos_venda": {
            "PE": "Você precisa de clareza estratégica para convencer a liderança. Contrate a Mentoria Neoventures para estruturar a visão do CEO e criar o plano de ação básico que garante os primeiros recursos",
            "PME": "O capital não pode ser desperdiçado. Garanta que seu plano de inovação tenha objetivos e métricas claras antes de alocar o orçamento. Contrate a Mentoria Neoventures para desenhar um plano de ROI e alinhar o board com a estratégia de inovação.",
            "ME": "É urgente formalizar a prioridade. Defina os membros do futuro Comitê para centralizar o patrocínio da alta gestão. Contrate a Mentoria Neoventures para criar a estrutura de governança e treinar a liderança no papel de sponsor da inovação.",
            "GE": "Seu principal gap é o comprometimento financeiro. É necessário separar o fundo de risco da operação e definir focos estratégicos para projetos.Use a Mentoria Neoventures para criar a estrutura de financiamento e definir os primeiros desafios estratégicos do portfólio.",
            "GGE": "Você está perdendo a visão de futuro. É vital estabelecer uma política formal de Inovação Aberta e mapear o ecossistema.Use a plataforma SOLV para iniciar o mapeamento de desafios e problemáticas e receber os primeiros insights externos.",
        },
        "manutencao": {
            "PE": "Monitorar ativamente o tempo dedicado à inovação e garantir que o CEO reforce a prioridade a cada trimestre. Procure uma Mentoria para realizar revisões trimestrais da visão e plano de ação básico.",
            "PME": "Tornar o orçamento dedicado um item fixo e não negociável do planejamento anual. Treinar novos líderes no pitch de inovação.",
            "ME": "Realizar reuniões obrigatórias do Comitê de Inovação para reforçar o buy-in e evitar cortes no funding dedicado.",
            "GE": "Usar os desafios estratégicos como input obrigatório no roadmap de inovação, garantindo que o tema não se torne obsoleto.",
            "GGE": "Comunicar o impacto estratégico dos projetos de inovação para toda a organização, evitando que a inovação seja vista como \"modismo\".",
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
        },
        "gatilhos_venda": {
            "PE": "Chegou a hora de transformar ideias em ganhos de eficiência. Crie seu primeiro funil simples focado em Melhoria Contínua  Contrate a Mentoria Neoventures para desenhar o funil Lean, garantindo que o processo seja ágil e alinhado com o seu segmento.",
            "PME": "Sua iniciativa precisa de ordem e profissionalismo. Formalize a Governança e defina os 3 KPIs que provarão o valor da inovação. Contrate a Mentoria Neoventures para garantir que seus processos sejam otimizados e que os indicadores não sejam aleatórios, mas sim estratégicos.",
            "ME": "Não perca ideias por falta de método. Implemente um Funil de Inovação para captação, avaliação e priorização de todas as ideias. Gatilho de Venda: Use a plataforma SOLV para lançar o funil de ideias de forma gamificada e simplificada, garantindo o engajamento imediato dos colaboradores.",
            "GE": "Seu maior risco é a inércia. Você precisa de um Radar de Tendências (Q6) para alimentar o funil com inteligência de mercado. Use a plataforma SOLV para mapear desafios, gerenciar o funil de captação interna e hospedar o repositório de tendências.",
            "GGE": "Para gerenciar sua complexidade, é vital ter um sistema. Estruture o Radar de Tendências global e o processo de Captação de Startups (Q6). Implemente a plataforma SOLV para gerenciar o scanning e automatizar o processo de avaliação, priorização e acompanhamento das iniciativas externas.",
        },
        "manutencao": {
            "PE": " Auditar o Funil de Melhoria a cada seis meses para garantir que o processo seja seguido e desburocratizado. Use uma plataforma para ter os dados consolidados",
            "PME": "Realizar uma auditoria anual dos KPIs para assegurar que os indicadores sejam relevantes e que o Comitê de Governança mantenha sua autoridade.",
            "ME": "Manter o treinamento em metodologias como um item constante do RH, garantindo que o conhecimento não se perca com a rotatividade.",
            "GE": "Manter e atualizar o Radar de Tendências (Q6) como um evento anual obrigatório que informa a alocação de recursos. Gatilho: Usar a plataforma SOLV para manter o repositório de insights atualizado.",
            "GGE": "Institucionalizar o processo de scouting de tendências e startups, garantindo a atualização tecnológica constante do board. Utilize uma plataforma de inovação para gerar um banco de Startups",
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
        },
        "gatilhos_venda": {
            "PE": "Sua inovação precisa ser um motor financeiro. Integre os resultados da inovação (ex: savings) aos objetivos anuais da empresa. Gatilho de Venda: Uma plataforma de inovação como o SOLV para auxiliar na integração Estratégica e no acompanhamento das iniciativas com de ROI simples.",
            "PME": "Você precisa escalar o sucesso. Garanta que o funil trabalhe apenas nos desafios de maior impacto e com o alinhamento estratégico da liderança. Conheça a Plataforma SOLV para otimizar e acompanhar seus processos, garantindo que as ações no funil gerem o resultado esperado.",
            "ME": "Não misture alhos com bugalhos. Formalize o Funil Radical (Novos Negócios) e separe-o do Incremental. Use a plataforma SOLV para gerenciar os dois funis em ambientes separados, com indicadores de portfólio adequados a cada tipo de risco.",
            "GE": "Seu principal gap é a execução radical. Inicie um programa-piloto de Inovação Aberta para aprender a lidar com startups e tecnologias externas. Use a plataforma SOLV para lançar os primeiros desafios externos (Captação de Startups) e gerenciar o acompanhamento das POCs.",
            "GGE": "Sua estrutura está em risco de silo. É crucial integrar a área de Inovação com as áreas de Negócio, por meio de Comitês e secondments de talentos. Use a Mentoria Neoventures para fazer o alinhamento interdepartamental e treinar líderes na gestão de portfólio dual.",
        },
        "manutencao": {
            "PE": "Usar os resultados de ROI  para justificar e aumentar o orçamento de inovação no ciclo seguinte. Procure uma Mentoria Neoventures para auxiliar na elaboração do relatório de impacto financeiro.",
            "PME": "Realizar workshops de alinhamento trimestrais com a liderança para garantir que o funil continue estratégico e não vire um mero pipeline operacional.",
            "ME": "Instituir uma revisão de portfólio formal (mensal/trimestral) com base em indicadores de sucesso e fracasso para matar ou escalar projetos rapidamente. Usar a plataforma SOLV para monitorar os indicadores de portfólio e a saúde dos projetos.",
            "GE": "Realizar encontros formais (roadshows) para a área de inovação com outras diretorias, garantindo integração e buy-in contínuos. Gatilho: Mentoria Neoventures para desenvolver o Plano de Comunicação e Engajamento interno.",
            "GGE": "Revisar anualmente o modelo de funding de portfólio para garantir que a alocação de recursos ainda equilibre eficiência (core) e disrupção (radical).",
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
        },
        "gatilhos_venda": {
            "PE": "Seus processos são bons, mas precisam de excelência. Otimize a Taxa de Conversão do funil incremental e use os resultados para revisar o orçamento. Conheça a ferramenta SOLV para garantir auditoria e melhoria contínua dos seus processos de inovação, com foco na eficiência.",
            "PME": "Sua inovação precisa ser uma cultura. Estruture o programa de Embaixadores/Agentes da Inovação para disseminar o engajamento. Use a plataforma SOLV para lançar o programa de intraempreendedorismo gamificado, incentivando e premiando os Agentes da Inovação.",
            "ME": "Está na hora de escalar o risco. Estruture um processo de Inovação Aberta simples (parceria com startups) para acelerar a busca por soluções externas. Use a plataforma SOLV para gerenciar as parcerias e o pipeline de startups, garantindo o acompanhamento dos projetos externos.",
            "GE": "O principal gap é o reconhecimento. Fortaleça o Programa de Inovação Aberta e a Legitimidade Externa Use a plataforma SOLV para escalar os desafios e integrar todas as iniciativas (internas/externas) em um único portfólio comparável.",
            "GGE": "Seu desafio é a agilidade. Você precisa de um sistema que suporte a complexidade.Contrate a Mentoria Neoventures para fazer a auditoria de processos e garantir que sua gestão de inovação seja otimizada e não burocrática.",
        },
        "manutencao": {
            "PE": "Tornar o programa de Agentes da Inovação (ou Embaixadores) um processo de desenvolvimento de liderança contínuo, não apenas uma iniciativa de ideias.",
            "PME": "Institucionalizar a comunidade de Inovação Aberta, garantindo o fluxo constante de parcerias e a captação de novas tecnologias. Usar a plataforma SOLV para gerenciar o pipeline de parcerias e o relacionamento com o ecossistema.",
            "ME": "Fazer um benchmarking anual de melhores práticas de Inovação Aberta para garantir que a empresa mantenha a vantagem competitiva. Mentoria Neoventures para realizar o benchmarking e auditoria do processo de parceira.",
            "GE": "Auditar o sistema de mensuração para garantir que os KPIs continuem impulsionando a disrupção e não apenas a eficiência (evitar \"KPIs de conforto\"). Utilizar plataforma de inovação como o SOLV para medir o impacto cultural da inovação.",
            "GGE": "Garantir que o orçamento dual seja mantido e que a área de inovação influencie as decisões de M&A e o roadmap de longo prazo da empresa.",
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
        },
        "gatilhos_venda": {
            "PE": "Seu próximo passo é a expansão. Revise a estratégia para definir se é hora de escalar o porte ou criar uma nova linha de receita (Inovação Radical).Contrate a Mentoria Neoventures para validar o modelo de negócio da nova linha de receita e auxiliar na tomada de decisão estratégica.",
            "PME": "Crie um veículo de Corporate Venture (internal incubator) Dentro de uma plataforma de inovação como o SOLV para desdobrar a inovação radical com autonomia. Contrate a Mentoria Neoventures para estruturar o modelo de venture interna e garantir que o processo esteja alinhado com o mercado.",
            "ME": "Estruture um programa de CVC (Corporate Venture Capital) para aquisição estratégica de startups e tecnologias. Gatilho de Venda: Use a plataforma SOLV como ferramenta de scouting e relacionamento contínuo com as startups investidas.",
            "GE": "Seu principal desafio é manter a agilidade. Use a plataforma SOLV para integrar todas as formas de inovação (interna, externa, CVC) em um único sistema de inteligência de portfólio.",
            "GGE": "Você é o benchmark! O foco é garantir que a estrutura seja ágil e à prova de burocracia, mantendo a liderança global. Contrate a Mentoria Neoventures para realizar auditorias e benchmarking de processo com as empresas mais inovadoras do mundo, garantindo a melhoria contínua.",
        },
        "manutencao": {
            "PE": "Realizar uma Revisão Estratégica (Deep Dive) a cada 2 anos, usando dados de tendências globais para evitar o conformismo e buscar o próximo desafio. Gatilho: Mentoria Neoventures para facilitar a revisão estratégica e deep dives em novos mercados.",
            "PME": "Proteger e nutrir o veículo de Corporate Venture, garantindo que ele mantenha a autonomia e o foco na disrupção, longe da burocracia do core.",
            "ME": "Manter o programa de CVC totalmente ativo, com monitoramento rigoroso de performance e alinhamento constante com as unidades de negócio. Usar a plataforma SOLV para gerenciar o portfólio de startups e medir o impacto no pipeline interno.",
            "GE": "Focar na legitimidade externa , utilizando a inovação como branding e fator de atração de talentos/investimentos. ",
            "GGE": "Realizar auditorias de agilidade (interna e externa) para garantir que o processo não tenha sido burocratizado pelo sucesso, mantendo-se líder global.  Contratar a Mentoria Neoventures para auditoria e benchmarking de processos, buscando a excelência evolutiva.",
        }
    },
}

class Command(BaseCommand):
    help = 'Popula os níveis de maturidade e ações prioritárias no banco de dados'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Atualizando níveis de maturidade...'))

        for level_num, level_data in MATURITY_LEVELS.items():
            min_score, max_score = level_data['faixa']

            # Cria ou atualiza o nível de maturidade
            maturity_level, created = MaturityLevel.objects.update_or_create(
                level_number=level_num,
                defaults={
                    'min_score': min_score,
                    'max_score': max_score,
                    'name': level_data['nivel'],
                    'focus': level_data['foco'],
                    'description': level_data['descricao']
                }
            )

            action_verb = 'Criado' if created else 'Atualizado'
            self.stdout.write(
                self.style.SUCCESS(f'✓ {action_verb} nível {level_num}: {level_data["nivel"]} ({min_score}-{max_score} pontos)')
            )

            # Cria ou atualiza as ações prioritárias para cada porte de empresa
            for company_size, action in level_data['acoes_prioritarias'].items():
                _, created = PriorityAction.objects.update_or_create(
                    maturity_level=maturity_level,
                    company_size=company_size,
                    defaults={'action': action}
                )
                action_verb = 'Criada' if created else 'Atualizada'
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ {action_verb} ação prioritária para {company_size}')
                )

            # Cria ou atualiza os gatilhos de venda para cada porte de empresa
            for company_size, trigger in level_data['gatilhos_venda'].items():
                _, created = SalesTrigger.objects.update_or_create(
                    maturity_level=maturity_level,
                    company_size=company_size,
                    defaults={'action': trigger}
                )
                action_verb = 'Criado' if created else 'Atualizado'
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ {action_verb} gatilho de venda para {company_size}')
                )

            # Cria ou atualiza as ações de manutenção para cada porte de empresa
            for company_size, maintenance in level_data['manutencao'].items():
                _, created = InnovationLevelMaintenance.objects.update_or_create(
                    maturity_level=maturity_level,
                    company_size=company_size,
                    defaults={'action': maintenance}
                )
                action_verb = 'Criada' if created else 'Atualizada'
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ {action_verb} ação de manutenção para {company_size}')
                )

        total_levels = MaturityLevel.objects.count()
        total_actions = PriorityAction.objects.count()
        total_triggers = SalesTrigger.objects.count()
        total_maintenance = InnovationLevelMaintenance.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Concluído! Total no banco: {total_levels} níveis de maturidade, {total_actions} ações prioritárias, {total_triggers} gatilhos de venda e {total_maintenance} ações de manutenção.'
            )
        )