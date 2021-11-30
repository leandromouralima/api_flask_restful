# api_flask_restful
Exercício para criar uma API 

## Instruções:

O banco de dados utilizado foi obtido do Kaggle: https://www.kaggle.com/johnharshith/world-happiness-report-2021-worldwide-mortality

Rodar o arquivo api.py (python api.py)

O endereço "http://127.0.0.1:5000/" retorna as opções para realizar o filtro dos dados. 

É possivel filtrar os dados de acorgo com categorias de população em 2020:
 - '0-5'      Até 5 milhões,
 - '5-11'     Entre 5 e 11 milhões,
 - '11-34'    Entre 11 e 34 milhões,
 - '34+'      Maior que 34 milhões,
 - 'completo' Nesse caso é exibita a base de dados completa

Para realizar o filtro é necessário utilizar o caminho: "http://127.0.0.1:5000/populacao/0-5" por exemplo para filtrar países com até 5 milhões. 

A API irá retornar um json com os dados filtrados e também irá persistir o .csv, .json e uma figura .png.

