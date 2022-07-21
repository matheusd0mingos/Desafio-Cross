import requests as r
import flask
import json
import time
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from timeout import TimeoutHTTPAdapter     

class api:
    #Classe api nela temos os métodos para extrair dados de página[get_page], extrair todas as páginas[extract], 
    #organizar vetores[transform] e postar dados organizados[load]
    def __init__(self, url="http://challenge.dienekes.com.br/api/numbers?page=", app = flask.Flask(__name__)) -> None:
        self.url=url
        #app.config["DEBUG"] = True
        self.app=app
        #Configuração da sessão
        self.session=r.Session()
        self.user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        self.session.mount('http://', TimeoutHTTPAdapter(1)) # 1 segundo
        self.session.mount('https://', TimeoutHTTPAdapter(1))
        self.session.headers.update({'User-Agent': self.user_agent})

        

    def get_page(self, page):
        #Método get_page retorna o request da page
        time.sleep(0.001)
        url=self.url+str(page)
        request=self.session.get(url)
        while ('error' in request.json()) or request.status_code!=200:
            time.sleep(0.01)
            request=self.session.get(url)
        return request


    def extract(self, limit=float('inf')):
        lista=[]
        i=1

        while 1:
            print(i)

            lista_url=range(i+100*(i-1), 101*i-1)
            #Aqui faremos uma ThreadPool para acelerar o processo, fazendo em blocos de 100 com 8 trabalhadores
            with ThreadPoolExecutor(max_workers=8) as pool:
                response_list = list(pool.map(self.get_page,lista_url))
            #Vamos colocar cada resposta dessa lista de respostas no vetor lista
            for response in response_list:
                
                resp_dict=eval(str(response.json()))
                numbers=resp_dict.get('numbers')
                if numbers!=[]:
                    lista+=numbers
                else:
                    i=-1    
            if i==-1 or i==limit:
                break
            i+=1
        return lista
        #Retorno lista completa

    def transform(self, lista):
        #Utilizaremos aqui o método MergeSort
        if len(lista) > 1:
            # Termo central
            mid = len(lista)//2
           
            # Divisão em duas listas
            E = lista[:mid]
            D = lista[mid:]

            # Aplicar o método na lista esquerda
            self.transform(E)

            # Aplicar o método na lista direita
            self.transform(D)

            i = j = k = 0

            while i < len(E) and j < len(D):
                if E[i] < D[j]:
                    lista[k] = E[i]
                    i += 1
                else:
                    lista[k] = D[j]
                    j += 1
                k += 1
            while i < len(E):
                lista[k] = E[i]
                i += 1
                k += 1

            while j < len(D):
                lista[k] = D[j]
                j += 1
                k += 1
        return lista

    def load(self, limit=float('inf')):
        numbers=self.extract(limit)

        ordenados=self.transform(numbers)
        chunks = [ordenados[x:x+100] for x in range(0, len(ordenados), 100)]
        per_page=100
        number_pages=ceil(len(ordenados)/per_page)
        dict_list=[]
        i=1
        #Criação das páginas
        for element in chunks:

            json_ordenado= {
                
                'numbers': element,
                'page': i,
                'nextPage': i+1 if i<number_pages else None,
                'totalPages': number_pages,
                'perPage': 100
            }
            i+=1
            dict_list.append(json_ordenado)

        for element in dict_list: element=json.dumps(element)
        #Quando a página for maior que o number_pages
        json_final={
            'numbers':[],
            'nextPage': None,
            'totalPages': number_pages
        }
        json_final=json.dumps(json_final)
        #Criação da rota:
        @self.app.route('/', methods=['GET'])
        def home():
            return '''<h1>Bem-vindo, para conseguir ver todos os números:</h1>
                    <p>Acesse /numbers.</p>
                    <p>Para mudar de páginas /numbers/PAGE</p>

                    <a href="/numbers">Ou veja os números clicando aqui</a>
'''
        
        
        @self.app.route('/numbers/', defaults={'page' : '1'})

        @self.app.route('/numbers/<page>', methods=['GET', 'POST'])
        def api_numbers(page):
            if int(page)<=number_pages:
                return (dict_list[int(page)-1])
            else:
                return (json_final)
        self.app.run()
        

