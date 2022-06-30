import pandas as pd

global companies_set 

def prepare_datasets(csv_path):
    path = csv_path
    base_df = pd.read_csv(path, sep =",")
    
    df = base_df[['Indicador','Dim1_Membro_Mome','Dim2_Membro_Mome','Dim3_Membro_Mome','VLR_Ocorrencia','Tipo_Registro','Data_Ocorrencia']]
    df = df[df['Tipo_Registro'] == "Apurado"] 
    df = df.drop(['Tipo_Registro','Indicador'],axis=1) 
    df.columns = ['Empresa','Canal_Distribuicao','Mercado','Volume_Venda','Data']

    df = df.fillna("NaN")
    df.head(5)

    df = df[((df.Empresa != "NaN") & (df.Canal_Distribuicao == "NaN") & (df.Mercado == "NaN"))
        |((df.Empresa != "NaN") & (df.Canal_Distribuicao != "NaN") & (df.Mercado == "NaN"))
        |((df.Empresa != "NaN") & (df.Canal_Distribuicao != "NaN") & (df.Mercado != "NaN"))]

    df = df[(df.Volume_Venda != "NaN")].reset_index()

    new_index = []
    for i in range(len(df)):
        new_index.append(i+1)
    df = df.set_index(pd.Index(new_index))
    del df['index']

    empresas = df.Empresa.unique()
    canais = df.Canal_Distribuicao.unique()
    mercados = df.Mercado.unique()

    df['Mercado'] = df['Mercado'].replace(['Am.Norte','Ásia','Europa','Am.Latina','Japão','Brasil'],
                                          [   'R1'   , 'R2' ,  'R3'  ,    'R4'   ,  'R5' ,  'R6'  ])
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
    
    for tpl in companies_set:
        group = tpl[1].groupby(['Canal_Distribuicao','Mercado']).size()
        group = group.to_frame(name = 'Qtd')
        display(group)


    return companies_set