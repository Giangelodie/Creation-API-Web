from lxml import etree as ET
from bottle import *
import re
import json
from collections import OrderedDict
import os
from pathlib import *

#Le code ci-dessous mis en commentaire permet de tronquer le fichier xml "dblp.xml" en des fichiers de taille plus réduite afin de faciliter le parsage du fichier.

'''
publications = ['</article>', '</inproceedings>', '</proceedings>','</book>', '</incollection>', '</phdthesis>','</mastersthesis>']
publications2 = ['<article', '<inproceedings', '<proceedings','<book', '<incollection', '<phdthesis','<mastersthesis']
end=['</dblp>']
entete=['<?xml version="1.0" encoding="ISO-8859-1"?>\n', '<!DOCTYPE dblp SYSTEM "dblp.dtd">\n', '<dblp>\n']

path1=Path("dblp.xml")

def word_in(line, publi):
    for p in publi :
    	for l in range (len(line)-len(p)+1) :
    		if(line[l:l+len(p)]==p):
    			return [True, len(p)]
    return [False, 0]


with open(path1, "r") as file:
	fin=False
	num=0
	numerofichier=str(num)
	lignesuiv=''
	while(fin==False):
		fichier="fichier"+numerofichier
		path=Path(fichier+".xml")
		with open(path,"a") as fichier1:
			cpt=0
			fichier1.write('<?xml version="1.0" encoding="ISO-8859-1"?>' + '\n')
			fichier1.write('<!DOCTYPE dblp SYSTEM "dblp.dtd">' + '\n')
			fichier1.write('<dblp>' + '\n')
			if (lignesuiv != ''):
				fichier1.write(lignesuiv)
			while(cpt<1000000):
				line=file.readline()
				print(line)
				if line not in entete:
					word0=word_in(line, end)
					if (line=='</dblp>'):
						fichier1.write(line)
						fin=True	
						break
					if (word0[0]==True):
						fichier1.write(line[:len(line)-word0[1]])
						fichier1.write('\n</dblp>')
						fin=True
						break
					word=word_in(line, publications)
					word2=word_in(line, publications2)
					if(word[0]==True):
						cpt+=1
					if (cpt==500000):
						if (word2[0]==True):
							fichier1.write(line[0:word[1]])
							fichier1.write('\n</dblp>')
							lignesuiv=line[word[1]:]
						else :
							fichier1.write(line)
							fichier1.write('</dblp>')
							break
						
					else :
						lignesuiv=''
						fichier1.write(line)

			num+=1
			numerofichier=str(num)
	
	cpt1=0
	with open(path,"r") as fichier2:
		while(True):
			line=fichier2.readline()
			cpt1+=1
			if line== '</dblp>':
				break
	print(cpt1, str(path))
	if cpt1==4:
		try:
			os.remove(path)
		except OSError as e:
			print(e)
		else:
			print("File is deleted successfully")
'''

local_input = "dblp_2020_2020.xml"
p = ET.XMLParser(recover=True)
tree = ET.parse(local_input, parser=p)
root = tree.getroot()
print(f"XML File loaded and parsed, root is {root.tag}")


@route('/publications/<id>')
def identifiant(id):
	#L'id est le titre (champs title) de la publication. La fonction renvoie une chaîne de caractères contenant chaque champs qui composent la publication.
	#La fonction renvoie une erreur de type 404 lorsqu'aucune publication ayant le titre "id" n'est trouvée.
	cpt=0
	s=''
	for title in root.iter('title'):
		if(title.text==id):
			child=root[cpt]
			for i in range (len(child)):
				s+=str(child[i].tag) + " : " + str(child[i].text) + "<br/>"				
			return s
		cpt+=1
	abort(404, "Not found: '/publications/"+id+"'")
	return 0
#http://localhost:8080/publications/Pragmatism%20and%20Care%20in%20Engineering%20Ethics.
#http://localhost:8080/publications/How to Weigh Values in Value Sensitive Design: A Best Worst Method Approach for the Case of Smart Metering.
#http://localhost:8080/publications/

def id_publi(id):
	#La fonction prend en paramètre "id" qui est le titre (champs title) d'une publication et renvoie une chaîne de caractères contenant chaque champs qui composent la publication.
	cpt=0
	s=''
	for title in root.iter('title'):
		if(title.text==id):
			child=root[cpt]
			s+='<article>'
			for i in range (len(child)):
				s+=str(child[i].tag) + " : " + str(child[i].text) + "<br/>"
			s+='------------------------------------------------------------'+ "<br/>"
			s+='</article>'	
			return s
		cpt+=1
		
		
@route('/publications/')
def lim():
	#La fonction renvoie par défaut les 100 premières publications sous la forme d'une chaîne de caractères contenant chaque champs qui composent chaque publication. 
    #Elle accepte les paramètres d'url : limit (la fonction renverra alors les "limit" premières publications), start et count (la fonction affichera "count" publications à partir de la "start"-ième publication), order (permet de trier la liste par rapport à un champs précisé).
	limit=request.query.limit
	start=request.query.start
	count=request.query.count
	order=request.query.order
	cpt=0
	if (limit==""):
		limit=100
	if (start==""):
		start=0
	if (count!="") and (int (count) <=100):
		limit=count
	s=''
	publications=[]
	dico_pour_ranger={}
	if order!="":
		for i in range(int(start),int(start)+int(limit)):
			child=root[i]
			for j in range (len(child)):
				if(child[j].tag=='title'):
					titre=child[j].text
					for k in range (len(child)):
						if(child[k].tag==order):
							dico_pour_ranger[titre]=child[k].text
	else :
		for i in range(int(start),int(start)+int(limit)):
			s+='<article>'
			child=root[i]
			for j in range (len(child)):
				s+=str(child[j].tag) + " : " + str(child[j].text) + "<br/>"
			s+='------------------------------------------------------------'+ "<br/>"
			s+='</article>'
	if(len(dico_pour_ranger)!=0):
		dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[1]))
		for keys in dico_range:
			publications.append(keys)
		for p in publications:
			s+=id_publi(p)
	return s

#http://localhost:8080/publications/?order=title
#http://localhost:8080/publications/?order=journal

@route('/authors/<name>')
def info_auth(name):
	#La fonction prend en paramètre le nom d'un auteur et renvoie une chaîne de caractères contenant le nombre de publication dont il est co-auteur (ainsi que la liste de ces publications) et le nombre de ses co-auteurs (ainsi que leur nom). 
    #Elle renvoie une erreur de type 404 lorsqu'on ne trouve aucune publication ni co-auteurs associés à l'auteur (car cela signifie que l'auteur n'existe pas).
	publications=[]
	co_authors=[]
	s=''
	for child in root:
		for i in range(len(child)):
			if child[i].tag=="author":
				if child[i].text==name:
					for j in range(len(child)):
						if child[j].tag=="author":
							if (child[j].text!=name) and (child[j].text not in co_authors):
								co_authors.append(child[j].text)
						if child[j].tag=="title":
							if child[j].text not in publications:
								publications.append(child[j].text)
	if(len(publications)==0 & len(co_authors)==0):
        	abort(404, "Not found: '/authors/"+name+"'")
        	return 0
	s+="Nom de l'auteur : " + str(name) + "<br/><br/>"
	s+="Nombre de publications : " + str(len(publications)) + "<br/><br/>"
	for i in range(len(publications)):
		s+= str(publications[i])+"<br/>"

	s+= "<br/>"+"Nombre de co-auteurs : " + str(len(co_authors)) + "<br/><br/>"
	for i in range(len(co_authors)):
		s+= co_authors[i]+ "<br/>"				
	return s

#http://localhost:8080/authors/Indira%20Nair
#http://localhost:8080/authors/Louise%20A.%20Dennis
#http://localhost:8080/authors/
#http://localhost:8080/authors/mj

@route('/authors/<name>/publications')
def publi(name):
	#La fonction prend en paramètre le nom d'un auteur (name) et renvoie par défaut les 100 premières publications d'un auteur sous la forme d'une chaîne de caractères. 
    #Elle accepte les paramètres d'url : start et count (la fonction affichera "count" publications à partir de la "start"-ième publication), order (permet de trier la liste par rapport à un champs précisé). 
    #Elle renvoie une erreur de type 404 lorsqu'on ne trouve aucune publication associé à l'auteur (car cela signifie que l'auteur n'existe pas) ou alors si le paramètre start dépasse le nombre de publications.
	limit=100
	start=request.query.start
	count=request.query.count
	order=request.query.order
	if (start==""):
		start=0
	if (count!="") and (int (count) <=100):
		limit=int(count)
	if (order==""):
		order=0
	s=""
	cpt=0
	publications=[]
	dico_pour_ranger = {}
	if (order == 0):
		for child in root:
			for i in range (len(child)):
				if child[i].tag=="author":
					if child[i].text==name:
						for j in range(len(child)):
							if child[j].tag=="title":
								if child[j].text not in publications:
									publications.append(child[j].text)
	else :
		for child in root:
			for i in range (len(child)):
				if child[i].tag=="author":
					if child[i].text==name:
						for j in range(len(child)):
							if child[j].tag == order:
								for l in range(len(child)):
									if (child[l].tag=="title"): 
										if child[j].text not in dico_pour_ranger:
											dico_pour_ranger[child[j].text] = child[l].text
	if(len(dico_pour_ranger)!=0):
		dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[0]))
		for keys in dico_range :
			publications.append(dico_range[keys])
	if(len(publications)==0 or len(publications)<=int(start)):
		abort(404, "Not found: '/authors/"+name+"/publications'")
		return 0 
	s="Publications de l'auteur " + str(name) + " :<br/><br/>"
	for k in range(int(start),len(publications)):
		if(cpt<int(limit)):
			s+= publications[k]+ "<br/>"
			cpt+=1
	return s

#http://localhost:8080/authors/Louise%20A.%20Dennis/publications?start=1&count=1
#http://localhost:8080/authors/Indira%20Nair/publications
#http://localhost:8080/authors/Louise%20A.%20Dennis/publications?limit=2

@route('/authors/<name>/coauthors')
def co_auth(name):
    #La fonction prend en paramètre le nom d'un auteur (name) et renvoie par défaut les 100 premiers co-auteurs d'un auteur sous la forme d'une chaîne de caractères. 
    #Elle accepte les paramètres d'url : start et count (la fonction affichera "count" co-auteurs à partir du "start"-ième co-auteur), order (permet de trier la liste par rapport à un champs précisé). 
    #Elle renvoie une chaîne de caractères qui indique une erreur lorsqu'on ne trouve aucun co-auteur associé à l'auteur et une erreur de type 404 si le paramètre start dépasse le nombre de co-auteurs.
    limit=100
    start=request.query.start
    count=request.query.count
    order=request.query.order
    if (start==""):
        start=0
    if (count!="") and (int (count) <=100):
        limit=int(count)
    if (order==""):
        order=0
    s=""
    cpt=0
    co_authors=[]
    dico_pour_ranger = {}
    if (order == 0):
        for child in root:
            for i in range (len(child)):
                if child[i].tag=="author":
                    if child[i].text==name:
                        for j in range(len(child)):
                            if child[j].tag=="author":
                                if (child[j].text!=name) and (child[j].text not in co_authors):
                                    co_authors.append(child[j].text)
    else :
        for child in root:
            for i in range (len(child)):
                if child[i].tag=="author":
                    if child[i].text==name:
                        for j in range(len(child)):
                            if (child[j].tag=="author"):
                                if (child[j].text!=name and child[j].text not in dico_pour_ranger):
                                    for l in range(len(child)):
                                        if child[l].tag == order:
                                            if order == "author" :
                                                if (child[l].text==child[j].text):
                                                    dico_pour_ranger[child[j].text] = child[j].text
                                            else :
                                                dico_pour_ranger[child[j].text] = child[l].text
    if(len(dico_pour_ranger)!=0):
        dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[1]))
        for keys in dico_range :
            co_authors.append(keys)
    if len(co_authors)==0:
        return "Pas de co auteurs"

    if (int(start)>=len(co_authors)):
        abort(404, "Not found: '/authors/"+name+"/coauthors'")
        return 0
    s="Co-auteurs de l'auteur " + str(name) + " :<br/><br/>"
    for i in range(int(start),len(co_authors)):
        if(cpt<limit):
            s+= co_authors[i] + "<br/>"
            cpt+=1
    return s

#http://localhost:8080/authors/Indira%20Nair/coauthors

#http://localhost:8080/authors/Inconnu/coauthors

#cas où l'auteur n'a pas de co auteur

#http://localhost:8080/authors/Alexander%20Guda/coauthors

#http://localhost:8080/authors/Alexander%20Guda/coauthors?start=2

#­http://localhost:8080/authors/Alexander%20Guda/coauthors?count=3
#­http://localhost:8080/authors/Alexander%20Guda/coauthors?count=3&start=5

#­http://localhost:8080/authors/Alexander%20Guda/coauthors?order=author
#­http://localhost:8080/authors/Alexander%20Guda/coauthors?order=author&count=2
#­http://localhost:8080/authors/Alexander%20Guda/coauthors?order=title

def word_in(line, word):
	#La fonction prend en paramètre une chaîne de caractères et un mot.
    #Elle renvoie un booléen à True si la chaîne de caractères "line" contient le mot "word", False sinon.
	line=line.lower()
	word=word.lower()
	for l in range (len(line)-len(word)+1) :
		if(line[l:l+len(word)]==word):
			return True
	return False

@route('/search/authors/<searchString>')
def search_aut(searchString):
	#La fonction prend en paramètre une chaîne de caractères et renvoie par défaut les 100 premiers auteurs dont le nom contient "searchString" sous la forme d'une chaîne de caractères. 
    #Elle accepte les paramètres d'url : start et count (la fonction affichera "count" auteurs à partir du "start"-ième auteur), order (permet de trier la liste par rapport à un champs précisé). 
    #Elle renvoie une chaîne de caractères qui indique une erreur lorsqu'on ne trouve aucun auteur contenant la chaîne de caractères et une erreur de type 404 si le paramètre start dépasse le nombre d'auteurs.
	limit=100
	start=request.query.start
	count=request.query.count
	order=request.query.order
	if (start==""):
		start=0
	if (count!="") and (int (count) <=100):
		limit=int(count)
	if (order==""):
		order=0
	s=""
	cpt=0
	authors=[]
	dico_pour_ranger = {}
	if (order == 0):
		for child in root:
			for i in range (len(child)):
				if child[i].tag=="author":
					if (word_in(str(child[i].text), str(searchString))) and (child[i].text not in authors):
						authors.append(child[i].text)
	else :
		for child in root:
			for i in range (len(child)):
				if child[i].tag=="author":
					if (word_in(str(child[i].text), str(searchString)) and child[i].text not in dico_pour_ranger):
						for j in range(len(child)):
							if child[j].tag == order:
								if order == "author" :
									if (child[j].text==child[i].text):
										dico_pour_ranger[child[i].text] = child[i].text
								else :
									dico_pour_ranger[child[i].text] = child[j].text
	if(len(dico_pour_ranger)!=0):
		dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[1]))
		for keys in dico_range:
			authors.append(keys)
	if len(authors)==0 :
		return "Aucun auteur trouvé"
	if(len(authors)<=int(start)):
		abort(404, "Not found: '/authors/"+searchString+"'")
		return 0 
	s="Auteurs contenant la chaîne de caractères : " + str(searchString) + "<br/><br/>"
	for k in range(int(start),len(authors)):
		if(cpt<int(limit)):
			s+="<author>"
			s+= authors[k] + "<br/>"
			s+="</author>"
			cpt+=1
	return s
		
#http://localhost:8080/search/authors/alex
#http://localhost:8080/search/authors/alex?start=2&count=2
#http://localhost:8080/search/authors/Pauline
#http://localhost:8080/search/authors/Pauline?order=author


@route('/search/publications/<searchString>')
def search_title(searchString):
    #La fonction prend en paramètre une chaîne de caractères et renvoie par défaut les 100 premières publications dont le titre contient "searchString" sous la forme d'une chaîne de caractères. 
    #Elle accepte les paramètres d'url : start et count (la fonction affichera "count" publications à partir de la "start"-ième publication), order (permet de trier la liste par rapport à un champs précisé). 
    #Elle renvoie une chaîne de caractères qui indique une erreur lorsqu'on ne trouve aucune publication contenant la chaîne de caractères et une erreur de type 404 si le paramètre start dépasse le nombre de publications.
    limit=100
    start=request.query.start
    count=request.query.count
    order=request.query.order
    if (start==""):
        start=0
    if (count!="") and (int (count) <=100):
        limit=int(count)
    if (order==""):
        order=0
    s=""
    cpt=0
    filtre="{"+ request.query.filter + "}"
    dic2 = ""
    quote = False
    
    for d in filtre:
        if d.isalnum():
            if not quote:
                dic2 += '"'
                quote = True
        else :
            if quote:
                dic2 += '"'
                quote = False
        dic2 += d

    dictionary=json.loads(dic2)
    publications=[]
    dico_pour_ranger = {}
    
    if len(dictionary)==0:
        if (order == 0):
            for child in root:
                for i in range (len(child)):
                    if child[i].tag=="title":
                        if (word_in(str(child[i].text), str(searchString)) and child[i].text not in publications):
                            publications.append(child[i].text)
                            print(child[i].text)
        else :
            for child in root:
                for i in range (len(child)):
                    if child[i].tag=="title":
                        if (word_in(str(child[i].text), str(searchString)) and child[i].text not in dico_pour_ranger):
                            for j in range(len(child)):
                                if child[j].tag == order:
                                    if order == "title" :
                                        if (child[j].text==child[i].text):
                                            dico_pour_ranger[child[i].text] = child[i].text
                                    else :
                                        dico_pour_ranger[child[i].text] = child[j].text   
    else :
        if (order == 0):
            for child in root:
                for i in range (len(child)):
                    if child[i].tag=="title":
                        if (word_in(str(child[i].text), str(searchString))==True):
                            cpt=0
                            for key in dictionary.keys():
                                for k in range (len(child)):
                                    if child[k].tag==key:
                                        if (word_in(str(child[k].text), dictionary[key])==True):
                                            cpt+=1
                            if (cpt==len(dictionary)) and (child[i].text not in publications):
                                publications.append(child[i].text)
        else :
            for child in root:
                for i in range (len(child)):
                    if child[i].tag=="title":
                        if (word_in(str(child[i].text), str(searchString))==True):
                            cpt=0
                            for key in dictionary.keys():
                                for k in range (len(child)):
                                    if child[k].tag==key:
                                        if (word_in(str(child[k].text), dictionary[key])==True):
                                            cpt+=1
                            if (cpt==len(dictionary)) and (child[i].text not in dico_pour_ranger):
                                for j in range(len(child)):
                                    if child[j].tag == order:
                                        if order == "title" :
                                            if (child[j].text==child[i].text):
                                                dico_pour_ranger[child[i].text] = child[i].text
                                        else :
                                            dico_pour_ranger[child[i].text] = child[j].text
    
            
    if(len(dico_pour_ranger)!=0):
        dico_range = OrderedDict(sorted(dico_pour_ranger.items(), key=lambda t: t[1]))
        for keys in dico_range:
            publications.append(keys)
    
    if (len(publications)==0):
        return "Aucune publication trouvée"

    if (int(start)>=len(publications)):
        abort(404, "Not found: '/publications/"+searchString+"'")
        return 0
    
    s="Publications contenant la chaîne de caractères : " + str(searchString) + "<br/><br/>"
    for i in range (int(start), len(publications)):
        if(cpt<int(limit)):
            cpt+=1
            s+= "<publication>"
            s+= publications[i] + "<br/>"
            s+= "</publication>"
    return s

#http://localhost:8080/search/publications/moral
#http://localhost:8080/search/publications/morali

#http://localhost:8080//search/publications/smsmsms

#http://localhost:8080/search/publications/moral?count=10

#http://localhost:8080/search/publications/moral?count=3
#http://localhost:8080/search/publications/moral?count=3&start=100

#http://localhost:8080/search/publications/morali
#http://localhost:8080/search/publications/morali?order=author
#http://localhost:8080/search/publications/morali&order=title
#http://localhost:8080/search/publications/morali?filter=year:20&order=title

#http://localhost:8080/search/publications/moral
#http://localhost:8080/search/publications/moral?filter=number:2,year:20
#http://localhost:8080/search/publications/moral?filter=number:2,year:20&count=3



def minimal(dic):
	#La fonction prend en paramètre un dictionnaire et renvoie la plus petite valeur du dictionnaire et le chemin associé à cette valeur
	mini_v=float("inf")
	mini_k=''
	for cle, valeur in dic.items():
		if valeur[0]<mini_v:
			mini_v=valeur[0]
			mini_k=cle
	if (mini_v==float("inf")):
		return (mini_v, '')
	else:
		return (mini_v,dic[mini_k][1])
	
def distance(name_origin, name_destination, d, l, co_auth, cpt):
	#La fonction prend en paramètre un nom source, un nom destination, 
    #d (un dictionnaire qui va contenir les chemins de la racine jusqu'a chaque nom origin parcouru par récursion), 
    #l (le chemin parcouru de la racine au nom_origin), co_auth (liste des co-auteurs dont faisait parti name_origin), 
    #cpt (longueur du chemin le plus court actuel) et qui renvoie la distance du chemin le plus court ainsi que le chemin associé 
	#si name_origin n'a pas de co-auteurs, on n'a pas trouvé name_destination à partir de ce chemin : on renvoie une distance infinie pour ce chemin
    #si on trouve directement name_destination dans la liste des co-auteurs de name_origin on retourne une distance de 1 et un chemin qui correspond à [name_origin]
    l_copy=l.copy()
    l_copy.append(name_origin)
    co_auth_copy=co_auth.copy()
    co_authors=[]
    #on récupère la liste des co-auteurs de name_origin
    for child in root:
        for i in range (len(child)):
            if child[i].tag=="author":
                if child[i].text==name_origin:
                    for j in range(len(child)):
                        if child[j].tag=="author":
                            if (child[j].text!=name_origin) and (child[j].text not in co_authors) and (child[j].text not in l) and (child[j].text not in co_auth_copy) and (child[j].text not in d.keys()):
                                co_authors.append(child[j].text)
    co_auth_copy=co_authors
    if len(co_authors)==0:
        return [float("inf"),""]
    else :
        if (name_destination in co_authors) and (len(l)==0):
            return [1, l_copy]
        else :
            if name_destination in co_authors :
                if len(l_copy)<cpt:
                    cpt=len(l_copy)
                return [1,l_copy]
            else :
                if(len(l_copy)<cpt):
					#on ne prend pas la peine de parcourir des chemins qui sont plus grand que le chemin plus court actuel
                    if ((len(co_authors)>1) and (name_origin not in d.keys())):
						#si on se retrouve sur un auteur ayant plusieurs co-auteurs, on doit modifier le dictionnaire pour stocker le chemin de la racine jusqu'à l'auteur actuel (name_origin)
						#on créé un dictionnaire dic ayant pour clés chaque co-auteurs de name_origin et la distance qui les sépare de name_destination (distance infinie si on ne lui trouve pas de chemin vers name_destination
                        d[name_origin]=l_copy
                        dic={}
                        for auth in co_authors:
                            dic[auth]=[1,""]
                        for auth in co_authors:
                            res=distance(auth,name_destination, d, d[name_origin], co_auth_copy, cpt)
                            dic[auth][0]+=res[0]
                            dic[auth][1]=res[1]
                        return minimal(dic)
                    else :
						#on créé un dictionnaire dic ayant pour clés chaque co-auteurs de name_origin et la distance qui les sépare de name_destination (distance infinie si on ne lui trouve pas de chemin vers name_destination
                        dic={}
                        for auth in co_authors:
                            dic[auth]=[1,""]
                        for auth in co_authors:
                            res=distance(auth,name_destination, d, l_copy, co_auth_copy, cpt)
                            dic[auth][0]+=res[0]
                            dic[auth][1]=res[1]
                        return minimal(dic)
                else:
					#si le chemin est plus grand que le chemin plus court actuel, on renvoie directement une distance infinie pour ce chemin
                    return [float("inf"),""]

@route('/authors/<name_origin>/distance/<name_destination>')
def dist(name_origin, name_destination):
	#La fonction prend en paramètre un nom d'auteur source (name_origin) et un nom d'auteur destination (name_destination) et va renvoyer une chaîne de caractères indiquant la longueur du plus petit chemin entre name_origin et name_destination et le chemin correspondant, ou une chaîne de caractères indiquant qu'il n'y a pas de chemin si on ne trouve pas de chemin entre name_origin et name_destination.
	distance_mini, chemin_mini=distance(name_origin, name_destination, {}, [], [], float("inf"))
	if distance_mini== float("inf"):
		return "Pas de chemin de l'auteur " + str(name_origin) + " à l'auteur " + str(name_destination) + "."
	else :
		return "La longueur du plus petit chemin " + str(chemin_mini) + " entre l'auteur " + str(name_origin) + " et l'auteur " + str(name_destination)+ " est de " + str(distance_mini) + "."

#http://localhost:8080/authors/Ming%20Shan/distance/Amos%20Darko (résultat : distance = 2)
#http://localhost:8080/authors/Ming%20Shan/distance/Peter%20Rasche (résultat : Pas de chemin)


run(host='localhost', port=8080)


















