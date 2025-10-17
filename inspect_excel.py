import pandas as pd

excel_path = 'forms/management/commands/Avaliação de maturidade de inovação (2).xlsx'

try:
    xls = pd.ExcelFile(excel_path)

    print("=== ABA: Gatilhos de venda ===")
    df_sales = pd.read_excel(xls, 'Gatilhos de venda')
    print("Colunas:", df_sales.columns.tolist())
    print("\nPrimeiras linhas:")
    print(df_sales.head())

    print("\n\n=== ABA: Manutenção do nível de inovação ===")
    df_maintenance = pd.read_excel(xls, 'Manutenção do nível de inovação')
    print("Colunas:", df_maintenance.columns.tolist())
    print("\nPrimeiras linhas:")
    print(df_maintenance.head())

except Exception as e:
    print(f'Erro: {e}')
    import traceback
    traceback.print_exc()
