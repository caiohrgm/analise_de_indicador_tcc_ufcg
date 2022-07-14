from sqlite3 import DateFromTicks
import pandas as pd

global companies_set 

def prepare_datasets(csv_path):
    path = r"D:\Documentos_D\UFCG\2021.2e\TCC\Project\analise_de_indicador_tcc_ufcg\data\raw\indicadores_raw.csv"
    base_df = pd.read_csv(path, sep =",")
    
    df = base_df[['Indicador','Dim1_Membro_Mome','Dim2_Membro_Mome','Dim3_Membro_Mome','VLR_Ocorrencia','Tipo_Registro','Data_Ocorrencia']]
    df = df[df['Tipo_Registro'] == "Apurado"] 
    df = df.drop(['Tipo_Registro','Indicador'],axis=1) 
    df.columns = ['Empresa','Canal_Distribuicao','Mercado','Volume_Venda','Data']

    df = df.fillna("Indefinido")

    df = df[((df.Empresa != "Indefinido") & (df.Canal_Distribuicao == "Indefinido") & (df.Mercado == "Indefinido"))
        |((df.Empresa != "Indefinido") & (df.Canal_Distribuicao != "Indefinido") & (df.Mercado == "Indefinido"))
        |((df.Empresa != "Indefinido") & (df.Canal_Distribuicao != "Indefinido") & (df.Mercado != "Indefinido"))]

    df = df[(df.Volume_Venda != "Indefinido")].reset_index()

    new_index = []
    for i in range(len(df)):
        new_index.append(i+1)
    df = df.set_index(pd.Index(new_index))
    del df['index']

    df['Mercado'] = df['Mercado'].replace(['Am.Norte', 'Ásia' , 'Europa' ,'Am.Latina', 'Japão' , 'Brasil'],
                                          [   'AN'   , 'AS'   ,   'EU'   ,    'AL'   ,  'JP'   ,   'BRL'])

    df['Empresa'] = df['Empresa'].replace(['BC' , 'BR', 'BI', 'BT'], 
                                          ['E1' , 'E2', 'E3', 'E4'])

    df['Canal_Distribuicao'] = df['Canal_Distribuicao'].replace(['ME' , 'EE', 'MI'],
                                                                ['C1' , 'C2', 'C3' ])

    empresas = df.Empresa.unique()
    canais = df.Canal_Distribuicao.unique()
    mercados = df.Mercado.unique()


    mercados = df.Mercado.unique()

    print("Informações básicas do conjunto de indicadores:")
    print("Empresas: ", empresas)
    print("Canais: ", canais)
    print("Mercado: ", mercados)
    print("\nObs: Os canais e mercados que são 'NaN' serão desconsiderados.")

    group_by_empresa = df.groupby(['Empresa'])
 
    companies_set = [] 
    for company_name in empresas:
        temp_df = group_by_empresa.get_group(company_name)
        companies_set.append((company_name, temp_df))
    
    return companies_set