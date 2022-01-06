import json
from detecta_quadrados_com_borda import detecta_quadrados_com_borda 
from gera_json import gera_json 

def includeTypeField(tip):
    if tip == 'integer':
        return f"IntegerField( "
    elif tip == 'text':
        return f"TextField( "
    elif tip == 'float':
        return f"FloatField( "
    elif tip == 'date':
        return f"DateTimeField( "
    elif tip == 'binary':
        return f"BinaryField( "

def includeForeignKeyField(col,related_name):
    fk_text = f"ForeignKey( {col.title()}, on_delete=models.PROTECT, related_name='"
    related_name = related_name[0].lower()+related_name[1:]
    fk_text += f"{related_name}_{col}', db_column='{col}_id'"
    return fk_text

def includeWidgets(widgets):
    count = 0
    textW = ''
    for a in widgets:
        if count == 0:
            textW += f"{a}={widgets[a]}"
            count+=1
        else:
            textW += f", {a}={widgets[a]}"
    return textW 

def montaClasse(numClass,tab):
    nomeClass = numClass.replace('_',' ').title().replace(' ','')
    textClass = f'\nclass {nomeClass}(models.Model):\n'
    textMeta = f'{tab}class Meta:\n{tab}{tab}db_table = "{numClass}"\n'
    ids = obj[numClass]['primary_key']['name']
    if len(ids)>1:
        textMeta += f'{tab}{tab}unique_together = {[tuple(ids)]}\n'
    columms = obj[numClass]['columms']
    for x in columms:
        textClass += f"{tab}{x['name']} = models."
        if x['type'] != 'foreignKey':
            textClass += includeTypeField(x['type'])
        else:
            textClass += includeForeignKeyField(x['name'],nomeClass)
        if len(ids)==1:
            if x['name'] in ids:
                textClass += includeWidgets({ "primary_key" : True })
        try:
            if textClass[-1] != ' ':
                textClass += f', '+includeWidgets(x['widgets'])
            else:
                textClass += includeWidgets(x['widgets'])
        except :
            pass
        textClass +=' )\n'
    self = obj[numClass]['self']
    textStr = f'{tab}def __str__(self):\n{tab}{tab}return self.{self}\n'
    return textClass+textMeta+textStr

def salvar(text,nome_model):
    arquivo = open(f"./resultado/{nome_model}", "w")
    arquivo.write(text)
    print('models.py criado.')
    arquivo.close()

def leArquivo(arq):
    arquivoJSON = open(arq, "r")
    textdjson = arquivoJSON.read()
    arquivoJSON.close()
    global obj
    obj = json.loads(textdjson)
    classes = list(obj.keys())
    return classes


if __name__ == "__main__":
    nome_arq = 'modelo_dados.png'
    pacote_json = 'pacote.json'
    nome_model = 'models.py'

    detecta_quadrados_com_borda(nome_arq)

    gera_json(pacote_json)

    classes = leArquivo(f"./resultado/{pacote_json}")
    text = f'from django.db import models\n'
    for numClass in classes: text += montaClasse(numClass,4*' ')

    salvar(text,nome_model)