from PIL import Image
import pytesseract
import os
import json

pacote_json = 'pacote_teste.json'

def gera_json(p_json):
    try: os.listdir('./resultado')
    except : os.mkdir('./resultado')

    dirs = os.listdir('./imagens_tabelas/')
    arq_json = open(f'./resultado/{p_json}','w')
    dicionario_ordem_tratamento = {}
    lista_index_ordem = []

    for img in dirs:
        texto = pytesseract.image_to_string( Image.open(f'./imagens_tabelas/{img}') )
        texto = texto.split('\n')
        texto = [ t for t in texto if t!='' and t!=' ' and t!='\x0c' ]
        # print(texto)
        count = len([ x for x in texto if ('FK]' in x) or ('Fk]' in x) ])
        try:
            if dicionario_ordem_tratamento[str(count)] :
                lista = dicionario_ordem_tratamento[str(count)]
                lista.append(texto)
        except :
            dicionario_ordem_tratamento[str(count)] = [texto]
        if not(count in lista_index_ordem):
            lista_index_ordem.append(count)
            lista_index_ordem.sort()


    dicionario_modelo={}

    def muda_tipo(tipo):
        if tipo == 'INTEGER':
            return 'integer'
        if tipo == 'FLOAT':
            return 'float'
        elif tipo == 'VARCHAR':
            return 'text'
        elif tipo == 'TIMESTAMP' or 'DATE':
            return 'date'
        return tipo


    for i in lista_index_ordem:
        # print(dicionario_ordem_tratamento[str(i)])
        for item in dicionario_ordem_tratamento[str(i)]:
            colunas = []
            primary_keys =[]
            self = ''
            for col in item[1:]:
                dados = col.split(':')
                if len(dados)<2 : dados = col.split('.')

                if dados[0][-3:] == '_id': nome = dados[0][:-3]
                else: nome = dados[0]

                if '[self]' in dados[1] : self = nome

                if ('[PK]' in dados[1]) or ('[PFK]' in dados[1]) : primary_keys.append(nome)

                if ('[FK]' in dados[1]) or ('[PFK]' in dados[1]): tipo = 'foreignKey'
                else: tipo = muda_tipo(dados[1].split(' ')[1])

                if not( 'NOT NULL' in dados[1] ): 
                    adicionar = { 
                        "name" : nome, "type" : tipo,
                        "widgets" : { "null" : True }
                    }
                elif nome == 'data_criacao':
                    adicionar = { 
                        "name" : nome, "type" : tipo,
                        "widgets" : { "auto_now_add" : True }
                    }
                elif nome == 'data_atualizacao':
                    adicionar = { 
                        "name" : nome, "type" : tipo,
                        "widgets" : { "auto_now" : True }
                    }
                else:
                    adicionar = { "name" : nome, "type" : tipo }

                colunas.append(adicionar)

            dicionario_modelo[item[0]] = { 
                "columms" : colunas, "primary_key" : { "name" : primary_keys }, "self" : self
            }
            
    json_object = json.dumps(dicionario_modelo,indent=4) 
    print('JSON de dados criado.')
    # print(json_object)

    arq_json.write(json_object)
    arq_json.close()

if __name__ == "__main__":
    gera_json(pacote_json)