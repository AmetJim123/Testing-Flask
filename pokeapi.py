import os
from dotenv import load_dotenv
import requests


load_dotenv()


#----------------------------------- Code ----------------------------------------
#Obteniendo la url de la api


class Pokeapi:

    api_url = os.environ("url_api")

    def __init__(self):
        self.data = []


    def consult(self):
        print("1)Ver por página\n2)Dato en específico:\n")
        consult = int(input("->:"))
        if consult == 1:
            complement=self.pagination()
        elif consult == 2:
            print('Recuerde:\nElegir un ID o nombre para:\n-Berry\n-Pokedex(Solo región)\n-Move\n-Pokemon\n2)ID evolution-chain\n')
            complement=self.idParameter()
        return complement,consult


    def idParameter(self):
        ID =str(input('->:')).lower()
        return ID


    def pagination(self):
        print("Ingresar paginación o usar la paginación por defecto?\n1)Ingresar Paginación\n2)Por defecto")
        election = int(input("->:"))
        if election==1:
            print("Ingrese el límite")
            limit = str(input('->:'))
            print("ingrese la página en la que quiere empezar")
            pag = str(input('->:'))
            paginate = '/?offset='+pag+'&limit='+limit
        elif election == 2:
            paginate = '/?offset=0limit=20'
        return paginate


    def query(self):
        print("Ingrese el endpoint que quiera ver:\n*Berry\n*Evolution-Chain\n*Pokedex\n*Move\n*Pokemon")
        choice=str(input("\n->:")).lower()
        endpoint = choice+"/"
        print(f"endpoint elegido: {endpoint}")
        complement, election = self.consult()
        url = self.api_url + endpoint + complement
        return url, election


    def get_pokemon_data(self, election,  url_pokemon='', ):
        response = requests.get(url_pokemon)
        body = response.json()
        election = election
        if election == 1:
            self.data = {
                'Total:': '',
                'Siguiente:': '',
                'Anterior:': '',
                'Resultados:':''
            }
            self.data['Total:'] = body['count']
            self.data['Siguiente:'] = body['next']
            self.data['Anterior:'] = body['previous']
            self.data['Resultados:'] = body['results']
        elif election ==2:
            if 'berry' in url_pokemon:
                self.data = {
                    'ID:': '',
                    'Nombre:': '',
                    'Tiempo de crecimiento:': '',
                    'Cantidad de la cosecha:': '',
                    'Poder entregado:': '',
                    'Tamaño:': '',
                    'Suavidad:': '',
                    'Sequedad del suelo:': '',
                    'Firmeza:': '',
                    'Sabores:': '',
                    'Objeto:': '',
                    'Regalo natural a tipo:':''
                }
                self.data['ID:'] = body['id']
                self.data['Nombre:'] = body['name']
                self.data['Tiempo de crecimiento:'] = body['growth_time']
                self.data['Cantidad de la cosecha:'] = body['max_harvest']
                self.data['Poder entregado:'] = body['natural_gift_power']
                self.data['Tamaño:'] = body['size']
                self.data['Suavidad:'] = body['smoothness']
                self.data['Sequedad del suelo:'] = body['soil_dryness']
                self.data['Firmeza:'] = body['firmness']['name']
                self.data['Sabores:'] = body['flavors']
                self.data['Objeto:'] = body['item']['name']
                self.data['Regalo natural a tipo:'] = body['natural_gift_type']

            elif 'evolution-chain' in url_pokemon:
                self.data = {
                    'ID:': '',
                    'Cadena evolutiva:': [],
                }
                self.data['ID:'] = body['id']
                self.data['Cadena evolutiva:'] = body['chain']

            elif 'pokedex' in url_pokemon:
                self.data={
                    'ID:': '',
                    'Nombre de región:': '',
                    'Tipo de pokedex:': '',
                    'Pokemon:': [],
                    'Versión:':[]
                }
                self.data['ID:'] = body['id']
                self.data['Nombre de región:'] = body['name']
                for pokedex in body['descriptions']:
                    if pokedex['language']['name']=='en':
                        self.data['Tipo de pokedex:']=pokedex['description']
                for pokemon in body['pokemon_entries']:
                    number = str(pokemon['entry_number'])
                    name = str(pokemon['pokemon_species']['name'])
                    self.data['Pokemon:'].append(number+')'+name)
                for version in body['version_groups']:
                    self.data['Versión:'].append(version['name'])

            elif 'move' in url_pokemon:
                self.data={
                    'ID:':'',
                    'Nombre:':'',
                    'Precisión:':'',
                    'Puntos de uso:':'',
                    'Prioridad:':'',
                    'Potencia:':'',
                    'Tipo:':[],  
                    'Aprendido por:':[],
                }
                self.data['ID:'] = body['id']
                for name in body['names']:
                    if name['language']['name']=='es':
                        self.data['Nombre:'] = name['name']
                self.data['Precisión:'] = body['accuracy']
                self.data['Puntos de uso:'] = body['pp']
                self.data['Prioridad:'] = body['priority']
                self.data['Potencia:'] = body['power']
                self.data['Tipo:'] = body['type']['name']
                for learnedBy in body['learned_by_pokemon']:
                    self.data['Aprendido por:'].append(learnedBy[0]['name'])
            
            elif 'pokemon' in url_pokemon:
                self.data={
                    'ID:':'',
                    'Nombre:':'',
                    'Experiencia base:':'',
                    'Altura:':'',
                    'Orden:':'',
                    'Peso:':'',
                    'Habilidades':[],
                    'Tipo:':[],
                }
                self.data['ID:'] = body['id']
                self.data['Nombre:'] = body['name']
                self.data['Experiencia base:'] = body['base_experience']
                self.data['Altura:'] = body['height']
                self.data['Orden:'] = body['order']
                self.data['Peso:'] = body['weight']
                for abilities in body['abilities']:
                    self.data['Habilidades:'].append(abilities['ability']['name'])  
                for types in body['types']:
                    self.data['Tipo:'].append(types['type']['name'])
        return self.data


    def outClass(self):
        return False


prueba = Pokeapi()
s = True
while s == True:
    url, election = prueba.query()
    data = prueba.get_pokemon_data(election,url)
    print(data)
    print(f"\nToda la información fue extraída de {url}, para más información ingrese ahí")
    print("\n\nSalir?\n-Sí\n-No")
    out = str(input('->:')).lower()
    if out == 'no':
        s=True
    else:
        s = prueba.outClass()
