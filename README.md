# Diag360

Plataforma Django para avaliação de maturidade em inovação baseada na norma ISO 56002.

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
# Criar conf/.env com DEBUG, ENVIRONMENT, OPENAI_API_KEY

# Configurar banco de dados
python manage.py migrate
python manage.py populate_maturity_levels
python manage.py populate_questions

# Executar servidor
python manage.py runserver
```

## Funcionalidades

- Questionário dinâmico multi-etapas
- Pontuação ponderada por porte da empresa
- Classificação em 5 níveis de maturidade
- Análise inteligente com GPT-4o-mini
- Ranking comparativo entre empresas similares
- Recomendações de ações prioritárias


## Comandos Principais

```bash
python manage.py runserver              # Iniciar servidor
python manage.py makemigrations         # Criar migrações
python manage.py migrate                # Aplicar migrações
python manage.py createsuperuser        # Criar admin
python manage.py collectstatic          # Coletar arquivos estáticos
```

## Deploy

```bash
fab init --server=prod deploy
```

## URLs

- `/` - Página inicial
- `/avaliacao/` - Questionário
- `/resultado/<uuid>/` - Resultados
- `/admin/` - Administração
