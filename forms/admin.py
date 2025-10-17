from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from forms.models import (
    MaturityLevel,
    PriorityAction,
    InnovationEvaluation,
    EvaluationAxis,
    AxisScore,
    Question,
    Choice,
    EvaluationAnswer
)


class PriorityActionInline(admin.TabularInline):
    model = PriorityAction
    extra = 0
    fields = ['company_size', 'action']
    ordering = ['company_size']


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    fields = ['value', 'text', 'order']
    ordering = ['order']


@admin.register(MaturityLevel)
class MaturityLevelAdmin(admin.ModelAdmin):
    list_display = ['level_number', 'name', 'min_score', 'max_score', 'focus']
    list_filter = ['level_number']
    search_fields = ['name', 'focus', 'description']
    ordering = ['level_number']
    inlines = [PriorityActionInline]
    fieldsets = (
        ('Informações do Nível', {
            'fields': ('level_number', 'name', 'min_score', 'max_score')
        }),
        ('Detalhes', {
            'fields': ('focus', 'description')
        }),
    )


@admin.register(PriorityAction)
class PriorityActionAdmin(admin.ModelAdmin):
    list_display = ['maturity_level', 'company_size', 'action_preview']
    list_filter = ['maturity_level', 'company_size']
    search_fields = ['action']
    ordering = ['maturity_level__level_number', 'company_size']

    def action_preview(self, obj):
        return obj.action[:100] + '...' if len(obj.action) > 100 else obj.action
    action_preview.short_description = 'Ação Prioritária'


@admin.register(EvaluationAxis)
class EvaluationAxisAdmin(admin.ModelAdmin):
    list_display = ['order', 'name', 'code', 'questions_count', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['order']
    fieldsets = (
        ('Informações do Eixo', {
            'fields': ('name', 'code', 'order')
        }),
        ('Descrição', {
            'fields': ('description',)
        }),
    )

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Nº de Questões'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'field_name', 'axis_name', 'label_preview', 'is_active', 'updated_at']
    list_filter = ['is_active', 'axis', 'created_at']
    search_fields = ['label', 'field_name']
    ordering = ['order']
    inlines = [ChoiceInline]
    fieldsets = (
        ('Informações da Questão', {
            'fields': ('order', 'field_name', 'axis', 'is_active')
        }),
        ('Texto da Pergunta', {
            'fields': ('label',)
        }),
    )

    def label_preview(self, obj):
        return obj.label[:80] + '...' if len(obj.label) > 80 else obj.label
    label_preview.short_description = 'Pergunta'

    def axis_name(self, obj):
        return obj.axis.name if obj.axis else '-'
    axis_name.short_description = 'Eixo'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'value', 'text_preview', 'order']
    list_filter = ['question']
    search_fields = ['text']
    ordering = ['question__order', 'order']

    def text_preview(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    text_preview.short_description = 'Texto da Opção'


class AxisScoreInline(admin.TabularInline):
    model = AxisScore
    extra = 0
    fields = ['axis', 'score_obtained', 'max_score_possible', 'percentage', 'benchmark']
    readonly_fields = ['axis', 'score_obtained', 'max_score_possible', 'percentage', 'benchmark']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class EvaluationAnswerInline(admin.TabularInline):
    model = EvaluationAnswer
    extra = 0
    fields = ['question', 'choice', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(AxisScore)
class AxisScoreAdmin(admin.ModelAdmin):
    list_display = [
        'evaluation_id_short',
        'company_name',
        'company_size',
        'axis',
        'score_obtained',
        'max_score_possible',
        'percentage_display',
        'benchmark_display',
        'created_at'
    ]
    list_filter = ['axis', 'evaluation__company_size', 'created_at']
    search_fields = ['evaluation__company_name', 'evaluation__contact_email', 'axis__name']
    readonly_fields = ['evaluation', 'axis', 'score_obtained', 'max_score_possible', 'percentage', 'benchmark', 'created_at', 'updated_at']
    ordering = ['-created_at', 'evaluation', 'axis__order']

    fieldsets = (
        ('Avaliação', {
            'fields': ('evaluation', 'axis')
        }),
        ('Pontuações', {
            'fields': ('score_obtained', 'max_score_possible', 'percentage', 'benchmark')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def evaluation_id_short(self, obj):
        """Exibe versão curta do UUID da avaliação"""
        return str(obj.evaluation.id)[:8]
    evaluation_id_short.short_description = 'ID Aval.'

    def company_name(self, obj):
        """Exibe nome da empresa"""
        return obj.evaluation.company_name or '-'
    company_name.short_description = 'Empresa'

    def company_size(self, obj):
        """Exibe porte da empresa"""
        return obj.evaluation.company_size or '-'
    company_size.short_description = 'Porte'

    def percentage_display(self, obj):
        """Exibe percentual formatado"""
        return f"{obj.percentage:.1f}%"
    percentage_display.short_description = 'Percentual'
    percentage_display.admin_order_field = 'percentage'

    def benchmark_display(self, obj):
        """Exibe benchmark formatado"""
        return f"{obj.benchmark:.1f}%"
    benchmark_display.short_description = 'Benchmark'
    benchmark_display.admin_order_field = 'benchmark'

    def has_add_permission(self, request):
        return False


@admin.register(EvaluationAnswer)
class EvaluationAnswerAdmin(admin.ModelAdmin):
    list_display = ['evaluation', 'question', 'choice', 'created_at']
    list_filter = ['question', 'created_at']
    search_fields = ['evaluation__company_name', 'evaluation__contact_email']
    readonly_fields = ['evaluation', 'question', 'choice', 'created_at']

    def has_add_permission(self, request):
        return False


@admin.register(InnovationEvaluation)
class InnovationEvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'company_name',
        'company_size',
        'total_score',
        'maturity_level_short',
        'created_at',
        'view_result_button'
    ]
    list_filter = ['company_size', 'created_at', 'sector', 'maturity_level']
    search_fields = ['company_name', 'contact_email', 'maturity_level__name']
    readonly_fields = [
        'total_score',
        'maturity_level',
        'maturity_focus',
        'maturity_description',
        'priority_action',
        'ai_analysis',
        'created_at',
        'updated_at',
        'source_ip'
    ]
    inlines = [AxisScoreInline, EvaluationAnswerInline]
    fieldsets = (
        ('Dados da Empresa', {
            'fields': ('company_name', 'contact_email', 'phone', 'sector', 'company_size')
        }),
        ('Pontuação e Nível de Maturidade', {
            'fields': ('total_score', 'maturity_level', 'maturity_focus', 'maturity_description')
        }),
        ('Ação Prioritária', {
            'fields': ('priority_action',)
        }),
        ('Análise da IA', {
            'fields': ('ai_analysis',)
        }),
        ('Detalhes Adicionais', {
            'fields': ('score_by_dimension',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at', 'source_ip'),
            'classes': ('collapse',)
        }),
    )

    def maturity_level_short(self, obj):
        """Exibe versão curta do nível de maturidade"""
        if obj.maturity_level_fk:
            # Extrai apenas "Nível X" do texto completo
            name = obj.maturity_level_fk.name
            return name.split(':')[0] if ':' in name else name
        return '-'
    maturity_level_short.short_description = 'Nível'

    def maturity_focus(self, obj):
        """Exibe o foco do nível de maturidade"""
        return obj.maturity_level_fk.focus if obj.maturity_level_fk else '-'
    maturity_focus.short_description = 'Foco'

    def maturity_description(self, obj):
        """Exibe a descrição do nível de maturidade"""
        return obj.maturity_level_fk.description if obj.maturity_level_fk else '-'
    maturity_description.short_description = 'Descrição'

    def view_result_button(self, obj):
        """Botão para visualizar o resultado da avaliação"""
        url = reverse('evaluation_result', kwargs={'evaluation_id': obj.id})
        return format_html(
            '<a class="button" href="{}" target="_blank" style="padding: 5px 10px; background-color: #FF6B35; color: white; text-decoration: none; border-radius: 4px; display: inline-block;">'
            '<i class="fas fa-external-link-alt"></i> Ver Resultado'
            '</a>',
            url
        )
    view_result_button.short_description = 'Ações'
    view_result_button.allow_tags = True