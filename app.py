from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://gamesdt.herokuapp.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query {
	games {
		id	
		title
		portada
		developer
		releaseYear		
		gender {
			name
		}
		platform {
			name
		}
		shop
		diff
	}
}
"""
)
#		{"id" : "1", "name" : "ACTION"},
#       {"id" : "2", "name" : "STRATEGY"},
#        {"id" : "3", "name" : "FPS"},
#        {"id" : "4", "name" : "ADVENTURE"},
#        {"id" : "5", "name" : "HORROR"},
#        {"id" : "6", "name" : "FIGHTING"},
#        {"id" : "7", "name" : "RPG"},
#        {"id" : "8", "name" : "SURVIVAL"},
#        {"id" : "9", "name" : "COOP"},
#        {"id" : "10", "name" : "PARTY"},
## testing selections from the user
choices_g={"ACTION":True,"STRATEGY":True,"FPS":False,
"ADVENTURE":True,"HORROR":True,"FIGHTING":False,
"RPG":False,"SURVIVAL":False,"COOP":False,"PARTY":False}
choices_p={"PC":False,"PLAYSTATION":True,"XBOX":True,"SWITCH":False}
choices_d="FROM SOFTWARE"
choices_diff=7
# Nos da el resultado del query como una lista de diccionarios
result = client.execute(query)
#Como el resultado del query es un diccionario dentro de otro varias veces estas variables lo vuelven mas simple
#se guardan las plataformas de diccionario por diccionario y se reinicia cada ciclo
gameplatform = []
#cada diccionario uno por uno se guarda en esta variable con sus parametros siendo mas sencillos de ingresar
juego = {}
# se guarda cada diccionario de forma sencilla 
listofgames = []
aux=[]
counts=[]
# despues de filtrar las preferencias del usuario aqui se guardan los juego restantes
selection={}
recommendation=[]
f_recommend=["","",""]
for game in result.get('games'):	
	gameplatform.clear()	
	for i in range(len(game.get("platform"))):
		gameplatform.append(game.get("platform")[i].get("name"))
	games = {"id": game.get("id"), "title": game.get("title"),
	"portada":game.get("portada"),"developer":game.get("developer"),
	"releaseYear":game.get("releaseYear"), 
	"gender": game.get("gender").get("name"),"platform":gameplatform[0:] ,"shop":game.get("shop"),"diff":game.get("diff")}
	listofgames.append(games)
for i in range(len(listofgames)):
	juego=listofgames[i]
	#filtra por cada seleccion del usuario
	for x in range(len(choices_g)):
		#cada ciclo if es una de las selecciones dependiendo de que generos quiere el usuario
		if x==0 and choices_g.get("ACTION"):
			if juego.get("gender")=="ACTION":
				aux.append(juego.get('title'))
		if x==1 and choices_g.get("STRATEGY"):
			if juego.get("gender")=="STRATEGY":
				aux.append(juego.get('title'))
		if x==2 and choices_g.get("FPS"):
			if juego.get("gender")=="FPS":
				aux.append(juego.get('title'))
		if x==3 and choices_g.get("ADVENTURE"):
			if juego.get("gender")=="ADVENTURE":
				aux.append(juego.get('title'))
		if x==4 and choices_g.get("HORROR"):
			if juego.get("gender")=="HORROR":
				aux.append(juego.get('title'))
		if x==5 and choices_g.get("FIGHTING"):
			if juego.get("gender")=="FIGHTING":
				aux.append(juego.get('title'))
		if x==6 and choices_g.get("RPG"):
			if juego.get("gender")=="RPG":
				aux.append(juego.get('title'))
		if x==7 and choices_g.get("SURVIVAL"):
			if juego.get("gender")=="SURVIVAL":
				aux.append(juego.get('title'))
		if x==8 and choices_g.get("COOP"):
			if juego.get("gender")=="COOP":
				aux.append(juego.get('title'))
		if x==9 and choices_g.get("PARTY"):
			if juego.get("gender")=="PARTY":
				aux.append(juego.get('title'))
	#ciclo for para validar las plataformas
	for x in range(len(juego.get("platform"))):
		for a in range(len(choices_p)):
			if a==0 and choices_p.get("PC"):
				if juego.get("platform")[x]=="PC":
					aux.append(juego.get('title'))
			if a==1 and choices_p.get("PLAYSTATION"):
				if juego.get("platform")[x]=="PLAYSTATION":
					aux.append(juego.get('title'))
			if a==2 and choices_p.get("XBOX"):
				if juego.get("platform")[x]=="XBOX":
					aux.append(juego.get('title'))
			if a==3 and choices_p.get("SWITCH"):
				if juego.get("platform")[x]=="SWITCH":
					aux.append(juego.get('title'))
	#valida el developer
	if choices_d==juego.get("developer"):
		aux.append(juego.get('title'))
		aux.append(juego.get('title'))
		aux.append(juego.get('title'))
	#valida la dificultad con rango == 3 / diferencia de 1, 2 / diferencia de 2,1.
	if choices_diff==int(juego.get("diff")):
		aux.append(juego.get('title'))
		aux.append(juego.get('title'))
		aux.append(juego.get('title'))
	elif (choices_diff-1)==int(juego.get("diff")) or (choices_diff+1)==int(juego.get("diff")):
		aux.append(juego.get('title'))
		aux.append(juego.get('title'))
	elif (choices_diff-2)==int(juego.get("diff")) or (choices_diff+2)==int(juego.get("diff")):
		aux.append(juego.get('title'))
first=""
second=""
third=""
#se busca la cantidad de veces que cada juego se repite en aux, poniendo su count en un array y su titulo en otro con el mismo index
for i in range(len(aux)):
	if aux[i]!=aux[i-1]:
		selection={"title": aux[i], "count":aux.count(aux[i])}
		recommendation.append(selection.get("title"))
		counts.append(selection.get("count"))
#se organiza de forma descendiente
for i in range(len(counts)):
	for j in range(len(counts)-1):
		if counts[j]<counts[j+1]:
			auxt=recommendation[j]
			auxs=counts[j]
			counts[j]= counts[j+1]
			counts[j+1]=auxs
			recommendation[j]=recommendation[j+1]
			recommendation[j+1]=auxt
#se escojen los primeros 3 titulos
first=recommendation[0]
second=recommendation[1]
third=recommendation[2]
#se buscan los juegos con titulos iguales y se guardan para la recomendacion final
for i in range(len(listofgames)):
	juego=listofgames[i]
	if juego.get("title")==first:
		f_recommend[0]=juego
	elif juego.get("title")==second:
		f_recommend[1]=juego
	elif juego.get("title")==third:
		f_recommend[2]=juego
#recomendaciones que se le muestran al usuario
for i in range(len(f_recommend)):
	print(f_recommend[i])


