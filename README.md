# API - Realtors

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Básico** 

A ideia do site é facilitar a vida o corretor de imóveis

Nós sabemos que o dia dia de um corretor não é fácil. Muitas vezes  entre uma visita e outra, ele não tem tempo de organizar os imóveis que tem na sua carteira, são informações que muitas vezes se perdem.Imagine as fotos que ele poderia mostrar para os clientes, se perderem, ou poir,  não saber de qual imóvel ou comodo é a imagem.

Por isso foi criado este site, onde ele pode organizar de forma lógica todos imóves de sua carteira.Começando pela a imobiliária do imóvel, passando pelo cadastro de cada comôdo individualmente e finalmente o cadastro das fotos por cada comôdo.

Desta forma, ele consegue visualizar de forma simples, direta e organizada os imóveis.

Aqui temos as instruções para instalar e executar o Back-end do projeto

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5050
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5050 --reload
```

Abra o [http://localhost:5050/#/](http://localhost:5050/#/) no navegador para verificar o status da API em execução.

