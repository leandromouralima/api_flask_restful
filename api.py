import pandas as pd
import matplotlib.pyplot as plt
import json2table
import json
from flask import Flask
from flask_restful import Resource, Api

df_paises = pd.read_csv("WHRData2021.csv")

app = Flask(__name__)
api = Api(app)

class Paises(Resource):
    def get(self):
        jsonfile = df_paises['Country name'].to_json()
        jsondict = json.loads(jsonfile)
        return jsondict

class Pais(Resource):
    def get(self, pais_id):
        pais_procurado = df_paises['Country name'] == pais_id
        df_pais = df_paises[pais_procurado]
        pais_escolhido = json.loads(df_pais.to_json())
        
        fig = df_pais["Median age"].plot(kind="bar")
        #plt.show()
        
        return fig 
        
#        return pais_escolhido
#        return df_pais.to_json()

api.add_resource(Paises, '/')
api.add_resource(Pais, '/pais/<string:pais_id>')

if __name__ == '__main__':
    app.run(debug=True)
