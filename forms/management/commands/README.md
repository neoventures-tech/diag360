# Comandos de Gerenciamento - Ordem de Execução

Este diretório contém comandos de gerenciamento Django para popular e configurar o sistema de avaliação de maturidade de inovação.

## Ordem de Execução (Instalação Nova)

Execute os comandos na seguinte ordem para configurar o sistema do zero:

### 1. Popular Níveis de Maturidade
```bash
python manage.py 1-populate_maturity_levels
```
**Função**: Cria os 5 níveis de maturidade com suas faixas de pontuação, focos e descrições.

### 2. Popular Eixos de Avaliação
```bash
python manage.py 2-populate_axis
```
**Função**: Cria os 6 eixos de avaliação ISO 56002 (Liderança, Estratégia, Governança, Recursos, Processos, Resultados).

### 3. Popular Questões
```bash
python manage.py 3-populate_questions
```
**Função**: Cria as 12 questões com suas opções de resposta e associa cada uma ao seu eixo correspondente.

**⚠️ Nota**: Este comando deleta questões existentes. Se já existirem avaliações no sistema, use o comando `3-update_questions_axis` em vez deste.

### 3. Atualizar Questões Existentes (Alternativa)
```bash
python manage.py 3-update_questions_axis
```
**Função**: Atualiza as questões existentes associando-as aos eixos de avaliação, sem deletar dados.

**Quando usar**: Use este comando quando já existirem questões e avaliações no banco de dados.

### 4. Calcular Pontuações Máximas dos Eixos
```bash
python manage.py 4-calculate_axis_max_scores
```
**Função**: Calcula e armazena a pontuação máxima de cada eixo por porte de empresa (PE, PME, ME, GE, GGE).

**⚠️ Importante**: Execute este comando sempre que:
- Adicionar ou remover questões
- Alterar os pesos das questões em `QUESTION_WEIGHTS`
- Alterar a associação de questões aos eixos

### 5. Popular Pontuações por Eixo (Avaliações Existentes)
```bash
python manage.py 5-populate_axis_scores_for_existing
```
**Função**: Popula os AxisScores para avaliações existentes que ainda não possuem pontuações por eixo.

**Quando usar**:
- Após adicionar o modelo AxisScore
- Para avaliações antigas que não têm pontuações por eixo

### 6. Recalcular Benchmarks dos Eixos
```bash
python manage.py 6-recalculate_axis_benchmarks
```
**Função**: Recalcula os benchmarks (melhor percentual histórico) de todos os AxisScores.

**Quando usar**:
- Após popular AxisScores para múltiplas avaliações
- Periodicamente para atualizar os benchmarks históricos
- Quando novos recordes são atingidos

## Execução Completa (Instalação Nova)

Para executar todos os comandos em sequência:

```bash
python manage.py 1-populate_maturity_levels && \
python manage.py 2-populate_axis && \
python manage.py 3-populate_questions && \
python manage.py 4-calculate_axis_max_scores
```

**Nota**: Após as primeiras avaliações serem feitas, execute:
```bash
python manage.py 6-recalculate_axis_benchmarks
```

## Atualização (Sistema Existente)

Para atualizar um sistema que já possui dados:

```bash
python manage.py 2-populate_axis && \
python manage.py 3-update_questions_axis && \
python manage.py 4-calculate_axis_max_scores && \
python manage.py 5-populate_axis_scores_for_existing && \
python manage.py 6-recalculate_axis_benchmarks
```

## Observações

- A questão 1 (pergunta direcionadora) **não possui eixo** pois serve apenas para identificar o porte da empresa
- As questões 2-12 são distribuídas pelos 6 eixos de avaliação
- Os pesos das questões variam conforme o porte da empresa
- A soma dos pesos deve totalizar 100 pontos para cada porte (exceto PE que atualmente soma 90)
