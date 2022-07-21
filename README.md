# Challenge Cross Comerce

## Sobre o objetivo do projeto
Se enquadra num processo ETL (extract, transform and load). Queremos pegar uma base bruta de uma API e suas muitas páginas, tratar seus dados(colocando-os em ordem crescente) e por fim carregando os dados por meio de um API rest.

Exemplo de uma página não tratada:
![image](https://user-images.githubusercontent.com/48094120/151010841-ce41d266-4d0e-4f9d-8c14-20c64d362741.png)

Já os resultados postados ficam organizados:

Primeira página:
![image](https://user-images.githubusercontent.com/48094120/151011232-d6f44ee9-83dd-4309-a15d-63bd283c739b.png)

Última página:
![image](https://user-images.githubusercontent.com/48094120/151011378-a7e30d77-494b-48a8-8c5f-583fda4ff7d2.png)

## Sobre a organização do Json tratado

Optou-se por paginar o conteúdo devido ao grande número de informações existente.
1. Para as páginas com conteúdo:
	``` 
	json= {
                
                'numbers': array,
                'page': current_page,
                'nextPage': current_page+1 if i<number_pages else None,
                'totalPages': number_pages,
                'perPage': 100
            }
	```

1. Caso já não tenha mais conteúdo na página pedida:

	```
	json={
	
            'numbers':[],
            'nextPage': None,
            'totalPages': number_pages
        }
	```
	Temos um array vazio em numbers, nextPage: None.
	Dessa forma, conseguimos verificar algum eventual erro.

## O que foi usado no projeto?
Linguagem: Python
Libraries utilizadas: flask, json, time, requests, concurrent.futures

Optou-se por criar um método para busca individual de páginas e por usar concurrent.futures(ThreadPoolExecutor) para acelerar o processo de busca, pois há trabalho sendo feito simultaneamente.

Para não ter problemas muito recorrentes com limit by peer, criou-se uma sessão.

Para se ter uma noção do processo, no console é printado o número de interações que se passaram.


## Sobre arquivos
1. timeout.py:
	Métodos para lidar com problemas de TimeOut 

1. api.py:
	Aqui temos os métodos demandados no desafio:
	
		`get_page(page) #Nos retorna a página $page da API, retornando um request http://challenge.dienekes.com.br/api/numbers`
		
		`extract() #Extrai os dados de todas as páginas, retornando uma lista de números`
		
		`transform() #Organiza os números em ordem crescente [Utilizou-se aqui o método MergeSort]`
		
		`load() #Posta os dados por métodos rest api`
		

1. app.py:
	Invoca-se o método load e posta-se os dados de forma organizada por páginas


## Sobre testes

Nos métodos extract e load pode-se inserir o limite de centenas que queremos extrair, exemplor `extract(1)` vai extrair apenas 100 páginas. Analogo para load.

## Estrutura de rotas

`route "/": Principal e com um link de referência para visualização dos números`

`route /numbers/{page} os números, com cada página tendo 100 números`


## Sobre a execução
Para executar, nosso "playground" de teste é o script app.py
