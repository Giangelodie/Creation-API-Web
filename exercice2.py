from requests import *
from json import *
import unittest

def error(url, research):
    s = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN"><html><head><title>Error: 404 Not Found</title><style type="text/css">html {background-color: #eee; font-family: sans-serif;}body {background-color: #fff; border: 1px solid #ddd;padding: 15px; margin: 15px;}pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}</style></head><body<h1>Error: 404 Not Found</h1><p>Sorry, the requested URL <tt>&#039;'
    s+=url
    s+= ';</tt>caused an error:</p><pre>Not found: &#039;'
    s+=research
    s+= '&#039;</pre></body></html>'
    return s

class TestAPIMethods(unittest.TestCase):
    server_ip = "127.0.0.1"
    server_port = 8080
    def test_1_publication_id(self): #test bon fonctionnement
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/How to Weigh Values in Value Sensitive Design: A Best Worst Method Approach for the Case of Smart Metering.")
        data = r1.text
        l = "author : Geerten van de Kaa<br/>author : Jafar Rezaei 0001<br/>author : Behnam Taebi<br/>author : Ibo van de Poel<br/>author : Abhilash Kizhakenath<br/>title : How to Weigh Values in Value Sensitive Design: A Best Worst Method Approach for the Case of Smart Metering.<br/>pages : 475-494<br/>year : 2020<br/>volume : 26<br/>journal : Sci. Eng. Ethics<br/>number : 1<br/>ee : https://doi.org/10.1007/s11948-019-00105-3<br/>ee : https://www.wikidata.org/entity/Q92959988<br/>url : db/journals/see/see26.html#KaaRTPK20<br/>"
        self.assertEqual(data,l)
    
    def test_2_publication_id(self): #test sans nom de publi donc doit rendre 100 publi et pas egal à l
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/")
        data = r1.text
        l = "author : Geerten van de Kaa<br/>author : Jafar Rezaei 0001<br/>author : Behnam Taebi<br/>author : Ibo van de Poel<br/>author : Abhilash Kizhakenath<br/>title : How to Weigh Values in Value Sensitive Design: A Best Worst Method Approach for the Case of Smart Metering.<br/>pages : 475-494<br/>year : 2020<br/>volume : 26<br/>journal : Sci. Eng. Ethics<br/>number : 1<br/>ee : https://doi.org/10.1007/s11948-019-00105-3<br/>ee : https://www.wikidata.org/entity/Q92959988<br/>url : db/journals/see/see26.html#KaaRTPK20<br/>"
        cpt=0
        for l in range (len(data)):
            if(data[l:l+9]=="<article>"):
                cpt+=1
        self.assertEqual(cpt,100)
        self.assertNotEqual(data,l)
        
    def test_1_publication_100(self): #test bon fonctionnement 
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/")
        data = r1.text
        cpt=0
        for l in range (len(data)):
            if(data[l:l+9]=="<article>"):
                cpt+=1
        self.assertEqual(cpt,100)
    
    def test_2_publication(self): #test avec un nombre de publi à afficher
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/?limit=12")
        data = r1.text
        cpt=0
        for l in range (len(data)):
            if(data[l:l+9]=="<article>"):
                cpt+=1
        self.assertEqual(cpt,12)
        
    def test_3_publication(self): #test qu'on affiche bien à partir de 100 deux publi
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/?start=100&count=2")
        data = r1.text
        l = '<article>author : Cristina Voinea<br/>author : Constantin Vica<br/>author : Emilian Mihailov<br/>author : Julian Savulescu<br/>title : The Internet as Cognitive Enhancement.<br/>pages : 2345-2362<br/>year : 2020<br/>volume : 26<br/>journal : Sci. Eng. Ethics<br/>number : 4<br/>ee : https://doi.org/10.1007/s11948-020-00210-8<br/>ee : https://www.wikidata.org/entity/Q91614977<br/>url : db/journals/see/see26.html#VoineaVMS20<br/>------------------------------------------------------------<br/></article><article>author : Lisa Sigl<br/>author : Ulrike Felt<br/>author : Maximilian Fochler<br/>title : "I am Primarily Paid for Publishing...": The Narrative Framing of Societal Responsibilities in Academic Life Science Research.<br/>pages : 1569-1593<br/>year : 2020<br/>volume : 26<br/>journal : Sci. Eng. Ethics<br/>number : 3<br/>ee : https://doi.org/10.1007/s11948-020-00191-8<br/>ee : https://www.wikidata.org/entity/Q89669967<br/>url : db/journals/see/see26.html#SiglFF20<br/>------------------------------------------------------------<br/></article>'
        cpt=0
        for m in range (len(data)):
            if(data[m:m+9]=="<article>"):
                cpt+=1
        self.assertEqual(cpt,2)
        self.assertEqual(data,l)
    
    def test_4_publication(self): #test qu'on affiche bien à partir de 200, 100 publi et non 200
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/?start=200")
        data = r1.text
        cpt=0
        for m in range (len(data)):
            if(data[m:m+9]=="<article>"):
                cpt+=1
        self.assertEqual(cpt,100)
        self.assertNotEqual(cpt,200)
    
    def test_5_publication(self): #test qu'on affiche bien 100 publi et non 300 car pas utilisation de limit
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/?count=300")
        data = r1.text
        cpt=0
        for m in range (len(data)):
            if(data[m:m+9]=="<article>"):
                cpt+=1
        self.assertEqual(cpt,100)
        self.assertNotEqual(cpt,300)
        
    def test_6_publication(self): #test le bon fonctionnement de order en fonction du titre
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/?count=4")
        data1 = r1.text
        r2 = get(f"http://{self.server_ip}:{self.server_port}/publications/?count=4&order=title")
        data2 = r2.text
        self.assertNotEqual(data1,data2) #pour cet exemple != mais peut pour d'autres possible ==
       
    def test_1_authors(self): #test pour verifier que qd on dmd un auteur on affiche pas que le nom, mais bien le reste
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis")
        data = r1.text
        l = "Nom de l'auteur : Louise A. Dennis<br/><br/>Nombre de publications : 3<br/><br/>Computational Goals, Values and Decision-Making.<br/>Adaptable and Verifiable BDI Reasoning.<br/>Verifiable Self-Aware Agent-Based Autonomous Systems.<br/><br/>Nombre de co-auteurs : 4<br/><br/>Peter Stringer<br/>Rafael C. Cardoso<br/>Xiaowei Huang 0001<br/>Michael Fisher 0001<br/>"
        self.assertEqual(data,l)
        self.assertNotEqual(data,"Louise A. Dennis")
    
    def test_2_authors(self): #renvoie une erreur si l'auteur n'existe pas
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/mj")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)
    
    def test_3_authors(self): #renvoie une erreur si on met pas d'auteur ou de suite
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)
                  
    def test_1_authors_publications(self): #test bon fonctionnement
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Indira%20Nair/publications")
        data = r1.text
        l = "Publications de l'auteur Indira Nair :<br/><br/>Pragmatism and Care in Engineering Ethics.<br/>"
        self.assertEqual(data,l)
    
    def test_2_authors_publications(self): #test d'un inconnu qui doit afficher erreur
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Inconnu/publications")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)
    
    def test_3_authors_publications(self): #test start
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis/publications")
        data1 = r1.text
        l = "Publications de l'auteur Louise A. Dennis :<br/><br/>Computational Goals, Values and Decision-Making.<br/>Adaptable and Verifiable BDI Reasoning.<br/>Verifiable Self-Aware Agent-Based Autonomous Systems.<br/>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis/publications?start=1")
        data2 = r2.text
        m = "Publications de l'auteur Louise A. Dennis :<br/><br/>Adaptable and Verifiable BDI Reasoning.<br/>Verifiable Self-Aware Agent-Based Autonomous Systems.<br/>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
        
    def test_4_authors_publications(self): #test count
    
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis/publications")
        data1 = r1.text
        l = "Publications de l'auteur Louise A. Dennis :<br/><br/>Computational Goals, Values and Decision-Making.<br/>Adaptable and Verifiable BDI Reasoning.<br/>Verifiable Self-Aware Agent-Based Autonomous Systems.<br/>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis/publications?count=1")
        data2 = r2.text
        m = "Publications de l'auteur Louise A. Dennis :<br/><br/>Computational Goals, Values and Decision-Making.<br/>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)

    def test_5_authors_publications(self): #test order=journal
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis/publications")
        data1 = r1.text
        l = "Publications de l'auteur Louise A. Dennis :<br/><br/>Computational Goals, Values and Decision-Making.<br/>Adaptable and Verifiable BDI Reasoning.<br/>Verifiable Self-Aware Agent-Based Autonomous Systems.<br/>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/authors/Louise%20A.%20Dennis/publications?order=journal")
        data2 = r2.text
        m = "Publications de l'auteur Louise A. Dennis :<br/><br/>Verifiable Self-Aware Agent-Based Autonomous Systems.<br/>Computational Goals, Values and Decision-Making.<br/>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
           
    def test_1_coauthors(self): #test bon fonctionnement
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Indira%20Nair/coauthors")
        data = r1.text
        l = "Co-auteurs de l'auteur Indira Nair :<br/><br/>William M. Bulleit<br/>"
        self.assertEqual(data,l)
        self.assertNotEqual(data,"William M. Bulleit")
     
    def test_2_coauthors(self):#test d'un inconnu n'a pas de coauteur
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Inconnu/coauthors")
        data = r1.text
        l = "Pas de co auteurs"
        self.assertEqual(data,l)
            
    #def test_3_coauthors(self): #trouver un auteur sans coauteurs 
     #   r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/.../coauthors")
      #  data = r1.text
       # l = "Pas de co auteurs"
        #self.assertEqual(data,l)

    def test_4_coauthors(self): #test start
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Alexander%20Guda/coauthors")
        data1 = r1.text
        l = "Co-auteurs de l'auteur Alexander Guda :<br/><br/>Andrea Martini<br/>Sergey Guda<br/>G. Smolentsev<br/>Alexander Algasov<br/>Oleg Usoltsev<br/>Mikhail A. Soldatov<br/>Aram Bugaev<br/>Yury Rusalev<br/>C. Lamberti<br/>A. V. Soldatov<br/>Andrey V. Chernov<br/>Maria Butakova<br/>Petr Shevchuk<br/>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/authors/Alexander%20Guda/coauthors?start=2")
        data2 = r2.text
        m = "Co-auteurs de l'auteur Alexander Guda :<br/><br/>G. Smolentsev<br/>Alexander Algasov<br/>Oleg Usoltsev<br/>Mikhail A. Soldatov<br/>Aram Bugaev<br/>Yury Rusalev<br/>C. Lamberti<br/>A. V. Soldatov<br/>Andrey V. Chernov<br/>Maria Butakova<br/>Petr Shevchuk<br/>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
    
    def test_5_coauthors(self): #test count
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Alexander%20Guda/coauthors")
        data1 = r1.text
        l = "Co-auteurs de l'auteur Alexander Guda :<br/><br/>Andrea Martini<br/>Sergey Guda<br/>G. Smolentsev<br/>Alexander Algasov<br/>Oleg Usoltsev<br/>Mikhail A. Soldatov<br/>Aram Bugaev<br/>Yury Rusalev<br/>C. Lamberti<br/>A. V. Soldatov<br/>Andrey V. Chernov<br/>Maria Butakova<br/>Petr Shevchuk<br/>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/authors/Alexander%20Guda/coauthors?count=3")
        data2 = r2.text
        m = "Co-auteurs de l'auteur Alexander Guda :<br/><br/>Andrea Martini<br/>Sergey Guda<br/>G. Smolentsev<br/>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
        
    def test_6_coauthors(self): #test order
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Alexander%20Guda/coauthors")
        data1 = r1.text
        l = "Co-auteurs de l'auteur Alexander Guda :<br/><br/>Andrea Martini<br/>Sergey Guda<br/>G. Smolentsev<br/>Alexander Algasov<br/>Oleg Usoltsev<br/>Mikhail A. Soldatov<br/>Aram Bugaev<br/>Yury Rusalev<br/>C. Lamberti<br/>A. V. Soldatov<br/>Andrey V. Chernov<br/>Maria Butakova<br/>Petr Shevchuk<br/>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/authors/Alexander%20Guda/coauthors?order=author")
        data2 = r2.text
        m = "Co-auteurs de l'auteur Alexander Guda :<br/><br/>A. V. Soldatov<br/>Alexander Algasov<br/>Andrea Martini<br/>Andrey V. Chernov<br/>Aram Bugaev<br/>C. Lamberti<br/>G. Smolentsev<br/>Maria Butakova<br/>Mikhail A. Soldatov<br/>Oleg Usoltsev<br/>Petr Shevchuk<br/>Sergey Guda<br/>Yury Rusalev<br/>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)

    def test_1_search_authors(self): #test bon fonctionnement
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/alex")
        data =r1.text
        cpt=0
        for l in range (len(data)):
            if(data[l:l+8]=="<author>"):
                cpt+=1
        self.assertEqual(cpt,100)
        
    def test_2_search_authors(self): #test bon fonctionnement, plus visible car =1
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Tsalidis")
        data =r1.text
        l = "Auteurs contenant la chaîne de caractères : Tsalidis<br/><br/><author>Christos Tsalidis<br/></author>"
        cpt=0
        for m in range (len(data)):
            if(data[m:m+8]=="<author>"):
                cpt+=1
        self.assertEqual(cpt,1)
        self.assertEqual(data,l)

    def test_3_search_authors(self): #test pas d'auteur trouvé
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Chistos")
        data = r1.text
        l = "Aucun auteur trouvé"
        self.assertEqual(data,l)

    def test_4_search_authors(self): #test start
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline")
        data1 = r1.text
        l = "Auteurs contenant la chaîne de caractères : Pauline<br/><br/><author>Pauline Trouv<br/></author><author>Pauline Hope Cheong<br/></author><author>Pauline Enguehard<br/></author><author>Pauline Buysse<br/></author><author>Pauline Ezanno<br/></author><author>Pauline Meyer-Heye<br/></author><author>Pauline Ribot<br/></author><author>Pauline Puteaux<br/></author><author>Pauline Kergus<br/></author><author>Pauline M. Hilt<br/></author><author>Pauline Bezivin Frere<br/></author><author>Pauline Swee Choo Goh<br/></author><author>Pauline Bernard<br/></author><author>Pauline Thumser-Henner<br/></author><author>Pauline Martin<br/></author><author>Pauline Ong<br/></author><author>Pauline Kongsuwan<br/></author><author>Pauline Lafitte<br/></author><author>Pauline Bimberg<br/></author><author>Pauline Conde<br/></author><author>Pauline Anthonysamy<br/></author><author>Pauline Chevalier<br/></author><author>Pauline Luc<br/></author><author>Pauline Larrouy-Maestri<br/></author><author>Marie-Pauline Krielke<br/></author><author>Pauline Genter<br/></author><author>Pauline Letortu<br/></author><author>Pauline Butaud<br/></author><author>Pauline Wonnenberg<br/></author><author>Jane Pauline Ramos Ramirez<br/></author><author>Pauline Paki<br/></author><author>Pauline Dreesen<br/></author><author>Pauline Lallemant-Dudek<br/></author><author>Pauline P. S. Woo<br/></author><author>Pauline Berry Burke<br/></author><author>Pauline N. Kawamoto<br/></author><author>Pauline Weritz<br/></author><author>Pauline Lacom<br/></author><author>Pauline Agou<br/></author><author>Pauline Folz<br/></author><author>Pauline Bennet<br/></author><author>Pauline Temme<br/></author><author>Joanna Pauline Rivera<br/></author><author>Pauline Boning Huang<br/></author><author>Pauline Chaste<br/></author><author>Pauline Brunet<br/></author><author>Pauline Haas<br/></author><author>Pauline Trial<br/></author>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline?start=15")
        data2 = r2.text
        m = "Auteurs contenant la chaîne de caractères : Pauline<br/><br/><author>Pauline Ong<br/></author><author>Pauline Kongsuwan<br/></author><author>Pauline Lafitte<br/></author><author>Pauline Bimberg<br/></author><author>Pauline Conde<br/></author><author>Pauline Anthonysamy<br/></author><author>Pauline Chevalier<br/></author><author>Pauline Luc<br/></author><author>Pauline Larrouy-Maestri<br/></author><author>Marie-Pauline Krielke<br/></author><author>Pauline Genter<br/></author><author>Pauline Letortu<br/></author><author>Pauline Butaud<br/></author><author>Pauline Wonnenberg<br/></author><author>Jane Pauline Ramos Ramirez<br/></author><author>Pauline Paki<br/></author><author>Pauline Dreesen<br/></author><author>Pauline Lallemant-Dudek<br/></author><author>Pauline P. S. Woo<br/></author><author>Pauline Berry Burke<br/></author><author>Pauline N. Kawamoto<br/></author><author>Pauline Weritz<br/></author><author>Pauline Lacom<br/></author><author>Pauline Agou<br/></author><author>Pauline Folz<br/></author><author>Pauline Bennet<br/></author><author>Pauline Temme<br/></author><author>Joanna Pauline Rivera<br/></author><author>Pauline Boning Huang<br/></author><author>Pauline Chaste<br/></author><author>Pauline Brunet<br/></author><author>Pauline Haas<br/></author><author>Pauline Trial<br/></author>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
        
    def test_5_search_authors(self): #test count
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline")
        data1 = r1.text
        l = "Auteurs contenant la chaîne de caractères : Pauline<br/><br/><author>Pauline Trouv<br/></author><author>Pauline Hope Cheong<br/></author><author>Pauline Enguehard<br/></author><author>Pauline Buysse<br/></author><author>Pauline Ezanno<br/></author><author>Pauline Meyer-Heye<br/></author><author>Pauline Ribot<br/></author><author>Pauline Puteaux<br/></author><author>Pauline Kergus<br/></author><author>Pauline M. Hilt<br/></author><author>Pauline Bezivin Frere<br/></author><author>Pauline Swee Choo Goh<br/></author><author>Pauline Bernard<br/></author><author>Pauline Thumser-Henner<br/></author><author>Pauline Martin<br/></author><author>Pauline Ong<br/></author><author>Pauline Kongsuwan<br/></author><author>Pauline Lafitte<br/></author><author>Pauline Bimberg<br/></author><author>Pauline Conde<br/></author><author>Pauline Anthonysamy<br/></author><author>Pauline Chevalier<br/></author><author>Pauline Luc<br/></author><author>Pauline Larrouy-Maestri<br/></author><author>Marie-Pauline Krielke<br/></author><author>Pauline Genter<br/></author><author>Pauline Letortu<br/></author><author>Pauline Butaud<br/></author><author>Pauline Wonnenberg<br/></author><author>Jane Pauline Ramos Ramirez<br/></author><author>Pauline Paki<br/></author><author>Pauline Dreesen<br/></author><author>Pauline Lallemant-Dudek<br/></author><author>Pauline P. S. Woo<br/></author><author>Pauline Berry Burke<br/></author><author>Pauline N. Kawamoto<br/></author><author>Pauline Weritz<br/></author><author>Pauline Lacom<br/></author><author>Pauline Agou<br/></author><author>Pauline Folz<br/></author><author>Pauline Bennet<br/></author><author>Pauline Temme<br/></author><author>Joanna Pauline Rivera<br/></author><author>Pauline Boning Huang<br/></author><author>Pauline Chaste<br/></author><author>Pauline Brunet<br/></author><author>Pauline Haas<br/></author><author>Pauline Trial<br/></author>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline?count=2")
        data2 = r2.text
        m = "Auteurs contenant la chaîne de caractères : Pauline<br/><br/><author>Pauline Trouv<br/></author><author>Pauline Hope Cheong<br/></author>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
        
    def test_6_search_authors(self): #test order=author
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline")
        data1 = r1.text
        l = "Auteurs contenant la chaîne de caractères : Pauline<br/><br/><author>Pauline Trouv<br/></author><author>Pauline Hope Cheong<br/></author><author>Pauline Enguehard<br/></author><author>Pauline Buysse<br/></author><author>Pauline Ezanno<br/></author><author>Pauline Meyer-Heye<br/></author><author>Pauline Ribot<br/></author><author>Pauline Puteaux<br/></author><author>Pauline Kergus<br/></author><author>Pauline M. Hilt<br/></author><author>Pauline Bezivin Frere<br/></author><author>Pauline Swee Choo Goh<br/></author><author>Pauline Bernard<br/></author><author>Pauline Thumser-Henner<br/></author><author>Pauline Martin<br/></author><author>Pauline Ong<br/></author><author>Pauline Kongsuwan<br/></author><author>Pauline Lafitte<br/></author><author>Pauline Bimberg<br/></author><author>Pauline Conde<br/></author><author>Pauline Anthonysamy<br/></author><author>Pauline Chevalier<br/></author><author>Pauline Luc<br/></author><author>Pauline Larrouy-Maestri<br/></author><author>Marie-Pauline Krielke<br/></author><author>Pauline Genter<br/></author><author>Pauline Letortu<br/></author><author>Pauline Butaud<br/></author><author>Pauline Wonnenberg<br/></author><author>Jane Pauline Ramos Ramirez<br/></author><author>Pauline Paki<br/></author><author>Pauline Dreesen<br/></author><author>Pauline Lallemant-Dudek<br/></author><author>Pauline P. S. Woo<br/></author><author>Pauline Berry Burke<br/></author><author>Pauline N. Kawamoto<br/></author><author>Pauline Weritz<br/></author><author>Pauline Lacom<br/></author><author>Pauline Agou<br/></author><author>Pauline Folz<br/></author><author>Pauline Bennet<br/></author><author>Pauline Temme<br/></author><author>Joanna Pauline Rivera<br/></author><author>Pauline Boning Huang<br/></author><author>Pauline Chaste<br/></author><author>Pauline Brunet<br/></author><author>Pauline Haas<br/></author><author>Pauline Trial<br/></author>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline?order=author")
        data2 = r2.text
        m = "Auteurs contenant la chaîne de caractères : Pauline<br/><br/><author>Jane Pauline Ramos Ramirez<br/></author><author>Joanna Pauline Rivera<br/></author><author>Marie-Pauline Krielke<br/></author><author>Pauline Agou<br/></author><author>Pauline Anthonysamy<br/></author><author>Pauline Bennet<br/></author><author>Pauline Bernard<br/></author><author>Pauline Berry Burke<br/></author><author>Pauline Bezivin Frere<br/></author><author>Pauline Bimberg<br/></author><author>Pauline Boning Huang<br/></author><author>Pauline Brunet<br/></author><author>Pauline Butaud<br/></author><author>Pauline Buysse<br/></author><author>Pauline Chaste<br/></author><author>Pauline Chevalier<br/></author><author>Pauline Conde<br/></author><author>Pauline Dreesen<br/></author><author>Pauline Enguehard<br/></author><author>Pauline Ezanno<br/></author><author>Pauline Folz<br/></author><author>Pauline Genter<br/></author><author>Pauline Haas<br/></author><author>Pauline Hope Cheong<br/></author><author>Pauline Kergus<br/></author><author>Pauline Kongsuwan<br/></author><author>Pauline Lacom<br/></author><author>Pauline Lafitte<br/></author><author>Pauline Lallemant-Dudek<br/></author><author>Pauline Larrouy-Maestri<br/></author><author>Pauline Letortu<br/></author><author>Pauline Luc<br/></author><author>Pauline M. Hilt<br/></author><author>Pauline Martin<br/></author><author>Pauline Meyer-Heye<br/></author><author>Pauline N. Kawamoto<br/></author><author>Pauline Ong<br/></author><author>Pauline P. S. Woo<br/></author><author>Pauline Paki<br/></author><author>Pauline Puteaux<br/></author><author>Pauline Ribot<br/></author><author>Pauline Swee Choo Goh<br/></author><author>Pauline Temme<br/></author><author>Pauline Thumser-Henner<br/></author><author>Pauline Trial<br/></author><author>Pauline Trouv<br/></author><author>Pauline Weritz<br/></author><author>Pauline Wonnenberg<br/></author>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)
    
    def test_7_search_authors(self): #test erreur
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/Pauline?start=50")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)    
    

    def test_1_search_publications(self): #test bon fonctionnement
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral")
        data = r1.text
        cpt=0
        for l in range (len(data)):
            if(data[l:l+13]=="<publication>"):
                cpt+=1
        self.assertEqual(cpt,100)
   
    def test_2_search_publications(self): #test pas de publi trouvée
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/smsmsms")
        data = r1.text
        l = "Aucune publication trouvée"
        self.assertEqual(data,l)
        
    def test_3_search_publications(self): #test count
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral")
        data1 = r1.text
        cpt1=0
        for l in range (len(data1)):
            if(data1[l:l+13]=="<publication>"):
                cpt1+=1
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral?count=10")
        data2 = r2.text
        cpt2=0
        for l in range (len(data2)):
            if(data2[l:l+13]=="<publication>"):
                cpt2+=1
        self.assertEqual(100,cpt1)
        self.assertEqual(10,cpt2)
        self.assertNotEqual(data2,data1)
        
    def test_4_search_publications(self): #test start
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral?count=3")
        data1 = r1.text
        cpt1=0
        for l in range (len(data1)):
            if(data1[l:l+13]=="<publication>"):
                cpt1+=1
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral?start=100&count=3")
        data2 = r2.text
        cpt2=0
        for l in range (len(data2)):
            if(data2[l:l+13]=="<publication>"):
                cpt2+=1
        self.assertEqual(3,cpt1)
        self.assertEqual(3,cpt2)
        self.assertNotEqual(data2,data1)

    def test_5_search_publications(self): #test order=author
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/morali")
        data1 = r1.text
        l = "Publications contenant la chaîne de caractères : morali<br/><br/><publication>Measuring morality in videogames research.<br/></publication><publication>How religion and morality correlate in age of society 5.0: Statistical analysis of emotional and moral associations with Buddhist religious terms appearing on Japanese blogs.<br/></publication><publication>On the Morality of Artificial Intelligence [Commentary].<br/></publication><publication>Machine Ethics - From Machine Morals to the Machinery of Morality<br/></publication><publication>The Conditions of Artificial General Intelligence: Logic, Autonomy, Resilience, Integrity, Morality, Emotion, Embodiment, and Embeddedness.<br/></publication><publication>Workshop Ethics and Morality in Business Informatics Workshop Ethik und Moral in der Wirtschaftsinformatik (EMoWI 2020).<br/></publication><publication>Integrating Human Acceptable Morality in Autonomous Vehicles.<br/></publication>"
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/morali?order=author")
        data2 = r2.text
        m = "Publications contenant la chaîne de caractères : morali<br/><br/><publication>Integrating Human Acceptable Morality in Autonomous Vehicles.<br/></publication><publication>Machine Ethics - From Machine Morals to the Machinery of Morality<br/></publication><publication>Measuring morality in videogames research.<br/></publication><publication>How religion and morality correlate in age of society 5.0: Statistical analysis of emotional and moral associations with Buddhist religious terms appearing on Japanese blogs.<br/></publication><publication>Workshop Ethics and Morality in Business Informatics Workshop Ethik und Moral in der Wirtschaftsinformatik (EMoWI 2020).<br/></publication><publication>The Conditions of Artificial General Intelligence: Logic, Autonomy, Resilience, Integrity, Morality, Emotion, Embodiment, and Embeddedness.<br/></publication><publication>On the Morality of Artificial Intelligence [Commentary].<br/></publication>"
        self.assertEqual(data1,l)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)

    def test_6_search_publications(self): #test filter=number:2,year:20
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral")
        data1 = r1.text
        cpt=0
        for l in range (len(data1)):
            if(data1[l:l+13]=="<publication>"):
                cpt+=1
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/moral?filter=number:2,year:2")
        data2 = r2.text
        m = "Publications contenant la chaîne de caractères : moral<br/><br/><publication>Fraud and Understanding the Moral Mind: Need for Implementation of Organizational Characteristics into Behavioral Ethics.<br/></publication><publication>Imaginative Value Sensitive Design: Using Moral Imagination Theory to Inform Responsible Technology Design.<br/></publication><publication>Technological Enthusiasm: Morally Commendable or Reprehensible?<br/></publication><publication>Artificial Moral Agents: A Survey of the Current Status.<br/></publication><publication>The ethics of Smart City (EoSC): moral implications of hyperconnectivity, algorithmization and the datafication of urban digital society.<br/></publication><publication>A Normative Approach to Artificial Moral Agency.<br/></publication><publication>Moral Gridworlds: A Theoretical Proposal for Modeling Artificial Moral Cognition.<br/></publication><publication>ArmorAll: Compiler-based Resilience Targeting GPU Applications.<br/></publication><publication>Design, Development, and Usability of a Virtual Environment on Moral, Social, and Emotional Leaning.<br/></publication><publication>Contracting with moral hazard, adverse selection and risk neutrality: when does one size fit all?<br/></publication>"
        self.assertEqual(cpt,100)
        self.assertEqual(data2,m)
        self.assertNotEqual(data2,data1)

    def test_7_search_publications(self): #test erreur
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/morali?start=500")
        data = str(r1)
        l = "<Response [404]>"
        self.assertEqual(data,l)
     
    def test_1_distance(self): #test réponse positive
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Ming Shan/distance/Amos Darko")
        data = r1.text
        l = "La longueur du plus petit chemin ['Ming Shan', 'Albert P. C. Chan'] entre l'auteur Ming Shan et l'auteur Amos Darko est de 2."
        self.assertEqual(data,l)

    def test_2_distance(self): #test réponse négative
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/Ming%20Shan/distance/Peter%20Rasche")
        data = r1.text
        l = "Pas de chemin de l'auteur Ming Shan à l'auteur Peter Rasche."
        self.assertEqual(data,l)        
        
    def test_1_error(self): #test erreur de même format
        r1 = get(f"http://{self.server_ip}:{self.server_port}/authors/")
        data1 = str(r1)
        r2 = get(f"http://{self.server_ip}:{self.server_port}/publications/mj")
        data2 = str(r2)
        self.assertEqual(data1,data2)
        
    def test_2_error(self): #test retour négatif de même format
        r1 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/smsmsms")
        data1 = str(r1)
        r2 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/smsmsms")
        data2 = str(r2)
        r3 = get(f"http://{self.server_ip}:{self.server_port}/authors/Ming%20Shan/distance/Peter%20Rasche")
        data3 = str(r3)
        self.assertEqual(data1,data2)
        self.assertEqual(data1,data3)

if __name__ == '__main__':
    unittest.main()