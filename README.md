# gera_orm_django

Este projeto foi feito para otmização e abstração do uso da linguagem python no servidor django a partir do modelo de dados.

Dessa forma conseguimos criar o ORM para o framework django através de uma imagem do modelo de dados do sistema, como exemplificado a baixo.

<h1>Instalação:</h1>

- Abra o terminal: 
<br>    pip install virtualenv
- Crie o ambiente virtual: 
<br>    virtualenv nome_da_pasta
- Entre na pasta da virtualenv: 
<br>    cd ./nome_da_pasta
- Crie a pasta do projeto:
<br>    mkdir pasta_projeto
- Entre na pasta do projeto:
<br>    cd ./pasta_projeto
- clone o projeto:
<br>    git clone https://github.com/romulorizo/gera_orm_django.git

<h1>Uso do programa</h1>

Para rodar o programa, deve ser feito um desenho do modelo de dados e colocar ele na pasta principal do projeto:

![alt text](modelo_dados.png)
    modelo_dados.png

Em seguida, compilar o arquivo criar_modelos.py , para criar o código do ORM:
![alt text](./img/img_models.png)
    models.py

