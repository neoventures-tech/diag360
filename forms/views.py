from django import forms as django_forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from formtools.wizard.views import SessionWizardView
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .ai_assistants import Inova360AIAssistant
from .models import InnovationEvaluation, Question, Choice, EvaluationAnswer, COMPANY_SIZE


class CompanyInfoForm(django_forms.Form):
    """Formulário para coletar informações da empresa"""
    company_name = django_forms.CharField(
        label='Nome da Empresa',
        max_length=255,
        required=True,
        widget=django_forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome da empresa'
        })
    )
    contact_email = django_forms.EmailField(
        label='Email de Contato',
        required=True,
        widget=django_forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seuemail@empresa.com'
        })
    )
    phone = django_forms.CharField(
        label='Telefone',
        max_length=20,
        required=True,
        widget=django_forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(00) 00000-0000'
        })
    )
    captcha = ReCaptchaField(
        label='Verificação de Segurança',
        widget=ReCaptchaV2Checkbox(attrs={
            'data-theme': 'light',
        }),
        error_messages={
            'required': 'Por favor, complete a verificação de segurança.',
            'captcha_invalid': 'Erro na verificação. Por favor, tente novamente.',
            'captcha_error': 'Erro na verificação de segurança. Recarregue a página e tente novamente.',
        }
    )

    # Flag para indicar se o captcha já foi validado (será setado pelo wizard)
    _captcha_already_validated = False

    def clean_captcha(self):
        """
        Validação customizada do captcha para evitar erro timeout-or-duplicate.
        Se o captcha já foi validado anteriormente (flag setada pelo wizard),
        retorna um valor válido sem validar novamente.
        """
        # Se o captcha já foi validado anteriormente, pular validação
        if self._captcha_already_validated:
            print("DEBUG [clean_captcha]: Captcha já validado anteriormente - pulando validação")
            return 'ALREADY_VALIDATED'

        # Caso contrário, validação normal (feita pelo ReCaptchaField)
        captcha_value = self.cleaned_data.get('captcha')
        return captcha_value


class AssessmentWizard(SessionWizardView):

    def post(self, *args, **kwargs):
        """
        Sobrescreve post para marcar captcha como validado na primeira tentativa bem-sucedida.
        """
        # Obtém o formulário atual
        wizard_goto_step = self.request.POST.get('wizard_goto_step', None)

        # Se não está navegando para outro step, é uma submissão normal
        if not wizard_goto_step:
            current_step = self.steps.current

            # Se estamos no step company_info, verificar se captcha já foi validado
            if current_step == 'company_info':
                # Marcar na sessão que estamos tentando validar o captcha
                captcha_validated_key = f'{self.prefix}_captcha_validated'

                # Se o captcha já foi validado anteriormente, skipar nova validação
                if self.request.session.get(captcha_validated_key):
                    # Remove o campo captcha dos dados POST para evitar revalidação
                    post_data = self.request.POST.copy()
                    if f'{current_step}-captcha' in post_data:
                        # Marcar como já validado
                        post_data[f'{current_step}-captcha'] = 'ALREADY_VALIDATED'
                    self.request.POST = post_data

        response = super().post(*args, **kwargs)

        return response

    def get_form(self, step=None, data=None, files=None):
        """
        Sobrescreve get_form para substituir o campo captcha quando já foi validado.
        Isso evita o erro 'timeout-or-duplicate' do reCAPTCHA.
        """
        form = super().get_form(step, data, files)

        # Se é o step company_info e o formulário tem captcha
        if step == 'company_info' and hasattr(form, 'fields') and 'captcha' in form.fields:
            # Verificar se captcha já foi validado
            captcha_validated_key = f'{self.prefix}_captcha_validated'
            captcha_already_validated = self.request.session.get(captcha_validated_key, False)

            print(f"DEBUG [get_form]: Step={step}, Captcha validado anteriormente={captcha_already_validated}")

            if captcha_already_validated:
                # SUBSTITUIR o ReCaptchaField por um CharField oculto
                # Isso evita que o ReCaptchaField tente validar o token novamente
                form.fields['captcha'] = django_forms.CharField(
                    required=False,
                    widget=django_forms.HiddenInput(),
                    initial='ALREADY_VALIDATED'
                )
                form._captcha_already_validated = True
                print("DEBUG [get_form]: Campo captcha substituído por HiddenInput - validação pulada")

        return form

    def get_form_step_data(self, form):
        """
        Remove dados do captcha ao armazenar dados do formulário na sessão.
        Isso garante que um novo captcha seja sempre solicitado.
        """
        data = super().get_form_step_data(form)
        # NÃO remover captcha aqui - será removido em process_step após validação
        return data

    def process_step(self, form):
        """
        Processa o step atual. Remove captcha dos dados armazenados após validação.
        """
        current_step = self.steps.current

        # Se é company_info e o form é válido, marcar captcha como validado ANTES do super()
        if current_step == 'company_info' and form.is_valid():
            # Verificar se captcha está no cleaned_data do form
            if 'captcha' in form.cleaned_data:
                # Marcar na sessão que o captcha foi validado com sucesso
                captcha_validated_key = f'{self.prefix}_captcha_validated'
                self.request.session[captcha_validated_key] = True
                self.request.session.modified = True
                print(f"DEBUG [process_step]: ✓ Captcha validado com sucesso! Marcado na sessão.")

        # Validação padrão do wizard
        validated_data = super().process_step(form)

        print(f"DEBUG [process_step]: Step={current_step}, Form válido={form.is_valid()}")
        print(f"DEBUG [process_step]: Session captcha_validated={self.request.session.get(f'{self.prefix}_captcha_validated', False)}")

        return validated_data

    def render(self, form=None, **kwargs):
        """
        Renderiza o formulário. Logs de debug para troubleshooting.
        """
        if form and not form.is_valid() and 'captcha' in form.errors:
            print(f"DEBUG [render]: Erro no captcha detectado: {form.errors['captcha']}")

        return super().render(form, **kwargs)

    @classmethod
    def get_initkwargs(cls, *args, **kwargs):
        # Gera formulários dinamicamente do banco de dados
        try:
            questions = Question.objects.filter(is_active=True).order_by('order')
        except Exception:
            questions = []

        form_list = []

        for question in questions:
            choices = [(choice.value, choice.text) for choice in question.choices.all().order_by('order')]

            # Cria classe de formulário dinamicamente
            form_class = type(
                f'DynamicQuestion{question.order}Form',
                (django_forms.Form,),
                {
                    question.field_name: django_forms.ChoiceField(
                        label=question.label,
                        choices=choices,
                        widget=django_forms.RadioSelect
                    )
                }
            )

            step_name = f"q{question.order}"
            form_list.append((step_name, form_class))

        # Adiciona formulário de informações da empresa como última etapa
        if form_list:
            form_list.append(('company_info', CompanyInfoForm))

        if not form_list:
            placeholder_form = type(
                'PlaceholderForm',
                (django_forms.Form,),
                {
                    'placeholder': django_forms.CharField(
                        label='Nenhuma pergunta disponível',
                        required=False
                    )
                }
            )
            form_list.append(('placeholder', placeholder_form))

        kwargs['form_list'] = form_list
        kwargs = super().get_initkwargs(*args, **kwargs)
        return kwargs

    def get_template_names(self):
        return ["forms/question.html"]

    def done(self, form_list, **kwargs):
        """Processa as respostas quando o wizard é completado"""
        # Limpar flag de captcha validado da sessão
        captcha_validated_key = f'{self.prefix}_captcha_validated'
        if captcha_validated_key in self.request.session:
            del self.request.session[captcha_validated_key]
            self.request.session.modified = True

        answers_display = []
        answers_dict = {}  # Para cálculo de pontuação

        # Busca todas as perguntas ativas ordenadas
        questions = Question.objects.filter(is_active=True).order_by('order')

        # Separa o formulário de contato dos formulários de perguntas
        form_list = list(form_list)
        company_info_form = form_list[-1]  # Último formulário é o de informações da empresa
        question_forms = form_list[:-1]  # Todos os outros são perguntas

        # Coleta as respostas de cada formulário
        for question, form in zip(questions, question_forms):
            field_name = list(form.fields.keys())[0]
            choice_value = int(form.cleaned_data[field_name])
            question_label = form.fields[field_name].label

            choices = dict(form.fields[field_name].choices)
            answer_text = choices.get(choice_value, "Resposta desconhecida")

            answers_display.append({
                "pergunta": question_label,
                "resposta": answer_text,
                "ponto": choice_value,
            })

            # Armazena resposta para cálculo de pontuação
            answers_dict[question.order] = choice_value

        # Debug: mostra as respostas coletadas
        print("DEBUG - answers_dict:", answers_dict)

        # Calcula pontuação ponderada
        total_score = EvaluationAnswer.calculate_weighted_score(answers_dict)
        company_size_level = answers_dict.get(1)
        company_size_code = COMPANY_SIZE.get(company_size_level)

        # Gera relatório completo de maturidade
        report = InnovationEvaluation.generate_full_report(total_score, company_size_code)

        # Pega os dados do formulário de informações da empresa
        company_data = company_info_form.cleaned_data

        # Busca o objeto MaturityLevel baseado no level_number do report
        from .models import MaturityLevel
        maturity_level_obj = None
        if 'level_number' in report:
            maturity_level_obj = MaturityLevel.objects.filter(
                level_number=report['level_number']
            ).first()

        # Salva a avaliação no banco de dados
        evaluation = InnovationEvaluation.objects.create(
            company_name=company_data['company_name'],
            contact_email=company_data['contact_email'],
            phone=company_data['phone'],
            total_score=total_score,
            company_size=company_size_code,
            maturity_level_fk=maturity_level_obj,  # Adiciona o FK
            focus=report['level_focus'],
            description=report['level_description'],
            priority_action_fk=report['priority_action_obj'],
            sales_trigger=report['sales_trigger_obj'],
            maintenance_action=report['maintenance_action_obj'],
        )

        # Salva cada resposta individualmente
        for question, form in zip(questions, question_forms):
            field_name = list(form.fields.keys())[0]
            choice_value = int(form.cleaned_data[field_name])

            # Busca a choice correspondente
            choice = Choice.objects.get(question=question, value=choice_value)

            # Cria a resposta
            EvaluationAnswer.objects.create(
                evaluation=evaluation,
                question=question,
                choice=choice
            )

        # Cria as pontuações por eixo
        from .models import AxisScore
        AxisScore.create_axis_scores_for_evaluation(evaluation, answers_dict)

        # Calcula e salva as estatísticas de ranking
        evaluation.update_ranking_stats()

        # Gera análise da IA com os dados do relatório
        import json
        assistant = Inova360AIAssistant()

        # Formata o relatório como JSON para a IA
        report_json = json.dumps(report, ensure_ascii=False, indent=2)
        ai_output = assistant.run(report_json)

        evaluation.ai_analysis = ai_output
        evaluation.save()

        # Redireciona para a página de resultado usando o UUID
        return redirect('evaluation_result', evaluation_id=evaluation.id)


class HomeWizard(TemplateView):
    template_name = 'forms/home.html'


def get_assessment_wizard_view(request):
    return AssessmentWizard.as_view()(request)


def evaluation_result(request, evaluation_id):
    """Exibe o resultado da avaliação pelo UUID"""
    import json
    import re
    from django.utils.safestring import mark_safe
    from .models import MaturityLevel

    evaluation = get_object_or_404(InnovationEvaluation, id=evaluation_id)

    # Processar e dividir a análise de IA em 3 seções
    ai_section_1 = ""  # Sua pontuação indica que
    ai_section_2 = ""  # Ganhos com a implementação
    ai_section_3 = ""  # Alertas para manutenção

    def markdown_to_html(text):
        """Converte markdown simples em HTML"""
        if not text:
            return ""

        # Converter **negrito**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

        # Converter listas com -
        lines = text.split('\n')
        in_list = False
        result_lines = []

        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result_lines.append('<ul>')
                    in_list = True
                item_text = line.strip()[2:]
                result_lines.append(f'<li>{item_text}</li>')
            else:
                if in_list:
                    result_lines.append('</ul>')
                    in_list = False
                result_lines.append(line)

        if in_list:
            result_lines.append('</ul>')

        text = '\n'.join(result_lines)

        # Converter quebras de linha duplas em parágrafos
        paragraphs = text.split('\n\n')
        formatted_paragraphs = []

        for p in paragraphs:
            p = p.strip()
            if p:
                if not (p.startswith('<ul>') or p.startswith('</ul>')):
                    p = f'<p>{p}</p>'
                formatted_paragraphs.append(p)

        return '\n'.join(formatted_paragraphs)

    if evaluation.ai_analysis:
        # Dividir a análise em seções usando os títulos ### como delimitadores
        # O regex retorna: ['', 'TÍTULO 1', 'conteúdo 1', 'TÍTULO 2', 'conteúdo 2', ...]
        sections = re.split(r'### \d+\.\s*(.+?)(?=\n)', evaluation.ai_analysis)

        # Processar pares de (título, conteúdo)
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                title = sections[i].strip().upper()
                content = sections[i + 1].strip()

                # Identificar e processar cada seção
                if 'SUA PONTUAÇÃO INDICA' in title or 'PONTUAÇÃO INDICA' in title:
                    ai_section_1 = mark_safe(markdown_to_html(content))
                elif 'GANHOS COM A IMPLEMENTAÇÃO' in title or 'GANHOS' in title:
                    ai_section_2 = mark_safe(markdown_to_html(content))
                elif 'ALERTAS PARA MANUTENÇÃO' in title or 'ALERTAS' in title:
                    ai_section_3 = mark_safe(markdown_to_html(content))

    # Buscar todos os níveis de maturidade do banco de dados
    maturity_levels = MaturityLevel.objects.all().order_by('level_number')

    # Preparar dados dos níveis para o JavaScript
    levels_data = []
    for level in maturity_levels:
        levels_data.append({
            'name': level.name,
            'min': level.min_score,
            'max': level.max_score,
            'level_number': level.level_number
        })

    # Encontrar o nível atual baseado na pontuação
    current_level = None
    level_colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981']
    for idx, level in enumerate(maturity_levels):
        if evaluation.total_score >= level.min_score and evaluation.total_score <= level.max_score:
            current_level = {
                'name': level.name,
                'color': level_colors[idx] if idx < len(level_colors) else '#FF6B35'
            }
            break

    # Monta o dicionário de estatísticas de ranking a partir dos dados salvos
    ranking_stats = {
        'position': evaluation.ranking_position,
        'total': evaluation.ranking_total,
        'percentile': evaluation.ranking_percentile,
        'better_than_percentage': evaluation.ranking_better_than_percentage,
        'average_score': evaluation.ranking_average_score,
        'top_score': evaluation.ranking_top_score,
        'is_only_one': evaluation.ranking_total == 1
    }

    # Buscar AxisScores para o radar de maturidade
    axis_scores = evaluation.axis_scores.all().order_by('axis__order')

    # Preparar dados para o gráfico radar
    radar_labels = []
    radar_obtained = []
    radar_benchmarks = []
    radar_percentages = []

    # Preparar dados para os cards
    axis_cards_data = []

    for axis_score in axis_scores:
        radar_labels.append(axis_score.axis.name)
        radar_obtained.append(float(axis_score.score_obtained))
        radar_benchmarks.append(float(axis_score.max_score_possible))
        radar_percentages.append(float(axis_score.percentage))

        axis_cards_data.append({
            'name': axis_score.axis.name,
            'score': axis_score.score_obtained,
            'benchmark': axis_score.benchmark,
            'percentage': axis_score.percentage
        })

    return render(request, "forms/evaluation_result.html", {
        "evaluation": evaluation,
        "ai_section_1": ai_section_1,
        "ai_section_2": ai_section_2,
        "ai_section_3": ai_section_3,
        "maturity_levels_json": json.dumps(levels_data),
        "ranking_stats": ranking_stats,
        "current_level": current_level,
        "axis_scores": axis_scores,
        "radar_labels": json.dumps(radar_labels),
        "radar_obtained": json.dumps(radar_obtained),
        "radar_benchmarks": json.dumps(radar_benchmarks),
        "radar_percentages": json.dumps(radar_percentages),
        "axis_cards_data": axis_cards_data,
    })
