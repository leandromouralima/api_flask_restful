import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json2table
import json
from flask import Flask
from flask_restful import Resource, Api

# Divide a variável qualitativa "População em 2020" em categorias para permitir o filtro 
df = pd.read_csv("https://raw.githubusercontent.com/leandromouralima/api_flask_restful/main/WHRData2021.csv")
b1 = int(np.round(df['Population 2020'].quantile(q=0.25)/1_000_000))
b2 = int(np.round(df['Population 2020'].quantile(q=0.5)/1_000_000))
b3 = int(np.round(df['Population 2020'].quantile(q=0.75)/1_000_000))
bins = [0, b1, b2, b3, np.inf]
nomes = ['0-' + str(b1), str(b1) + '-' + str(b2), str(b2) + '-' + str(b3), str(b3) + '+']
df['Pop2020_cat'] = pd.cut(df['Population 2020']/1_000_000, bins, labels=nomes)

app = Flask(__name__)
api = Api(app)

class Faixas_populacao(Resource):
    def get(self):
        nomes.append('completo')
        chaves = [ str(s) for s in np.arange(0,5,1)]
        jsondict = dict(zip(chaves, nomes))
        
        return jsondict

class Populacao(Resource):
    def get(self, populacao_bin):
        #Se for polulação_bin for 'Completo' não realiza o filtro
        if populacao_bin == 'completo':
                df_populacao = df.copy()
        else:
            populacao_procurada = df['Pop2020_cat'] == populacao_bin
            df_populacao = df[populacao_procurada].copy()
            
        populacao_escolhida = (df_populacao.to_json())
        
        #Agrupa por categorias do índice de Gini e persiste o csv e json
        df_populacao_gini = self.agrupa_gini(df_populacao, populacao_bin)
        
        #Cria e persiste figura do df filtrado
        self.cria_figura(df_populacao_gini, populacao_bin)
        
        return populacao_escolhida
    
    def agrupa_gini(self, df_filtrado, sufixo):
        bins = np.arange(20, 70, 16)
        names = ['20-36', '36-52', '52-68']
        df_filtrado['Gini_categorias'] = pd.cut(df_filtrado['Gini coefficient of income'], bins, labels=names)
        
        df_gini =df_filtrado.groupby(by='Gini_categorias').mean()
        df_gini.to_csv('WHRData2021_agrupado_Gini_' + sufixo + '.csv')
        df_gini.to_json('WHRData2021_agrupado_Gini_' + sufixo + '.json')
        
        return df_filtrado
        
    def cria_figura(sef,df, sufixo):
        sns.lmplot(data=df, x='COVID-19 deaths per 100,000 population in 2020', y='Index of exposure to COVID-19  infections in other countries as of March 31', hue='Gini_categorias', height=6, aspect=1.5)
        plt.xlabel('Mortes por COVID-19 2020 (por 100mil habitantes)')
        plt.ylabel('Índice de exposição à COVID-19 em 31 de março')
        plt.savefig('MortesCovid_vs_IndiceExposicao_' + sufixo + '.png', dpi=100)
        
api.add_resource(Faixas_populacao, '/')
api.add_resource(Populacao, '/populacao/<string:populacao_bin>')

if __name__ == '__main__':
    app.run(debug=True)
