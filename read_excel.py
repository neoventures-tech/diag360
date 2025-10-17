
import pandas as pd

def read_excel_sheets():
    excel_path = 'forms/management/commands/Avaliação de maturidade de inovação (2).xlsx'
    try:
        xls = pd.ExcelFile(excel_path)
        
        df_sales = pd.read_excel(xls, 'Gatilhos de venda')
        print('sales_triggers = {')
        for index, row in df_sales.iterrows():
            level_str = str(row['Nível de Maturidade']).split(':')[0]
            level = int(level_str)
            print(f'    {level}: {{')
            print(f'        "PE": """{row["Pequena Empresa (PE)"]}""",')
            print(f'        "PME": """{row["Pequena-Média Empresa (PME)"]}""",')
            print(f'        "ME": """{row["Média Empresa (ME)"]}""",')
            print(f'        "GE": """{row["Grande Empresa (GE)"]}""",')
            print(f'        "GGE": """{row["Muito Grande Empresa (MGE)"]}""",')
            print('    },')
        print('}')

        df_maintenance = pd.read_excel(xls, 'Manutenção do nível de inovação')
        print('\nmaintenance_actions = {')
        for index, row in df_maintenance.iterrows():
            level_str = str(row['Nível de Maturidade']).split(':')[0]
            level = int(level_str)
            print(f'    {level}: {{')
            print(f'        "PE": """{row["Pequena Empresa (PE)"]}""",')
            print(f'        "PME": """{row["Pequena-Média Empresa (PME)"]}""",')
            print(f'        "ME": """{row["Média Empresa (ME)"]}""",')
            print(f'        "GE": """{row["Grande Empresa (GE)"]}""",')
            print(f'        "GGE": """{row["Muito Grande Empresa (MGE)"]}""",')
            print('    },')
        print('}')

    except FileNotFoundError:
        print(f'Error: Excel file not found at {excel_path}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    read_excel_sheets()
