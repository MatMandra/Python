# dołaczanie bibliotek
import sqlite3
import re
import urllib.request

##--------------------------------------------------------------------------##
URL1 = "http://www.ptable.com/?lang=pl"

def doRequest (url):
    # funkcja pomocnicza, łaczy się z zadanym adresem URL i zwraca zawartość
    return urllib.request.urlopen(url).read().decode()
##--------------------------------------------------------------------------##
def create_BD():
    #Funkca tworzy bazę danych i odpowiednią tabelkę z krotkami 
    baza_pierwiastkow = sqlite3.connect('Kolos1.db')

    print ("Opened database successfully")
    print ("********************************************")
    print ("")
	# Tabela jest z tworzona jeśli nie istnieje
    baza_pierwiastkow.executescript('''
                   
           CREATE TABLE IF NOT EXISTS TABELKA
           (ID INTEGER PRIMARY KEY     ASC,
           nazwa                VARCHAR     NOT NULL,
		   symbol               VARCHAR     NOT NULL,
           liczba_atomowa       VARCHAR     NOT NULL,
           masa_atomowa         VARCHAR     NOT NULL,
           wartosciowosc       VARCHAR     NOT NULL)''')

    print ("Table created successfully")
    print ("********************************************")
    print ("")

    baza_pierwiastkow.close() 
##--------------------------------------------------------------------------##
def wpisuje(wzor):
    #wybranie potrzebnych danych z pobranej zawartości strony www
    baza_pierwiastkow = sqlite3.connect('Kolos1.db')
    nazwa=re.sub(r'<strong an="\d+".+<em>',"",wzor[0])
    nazwa=re.sub(r'</em>.+',"",nazwa)
    print(nazwa)
    symbol=re.sub(r'<strong an="\d+".+<acronym>',"",wzor[0])
    symbol=re.sub(r'</acronym>.+',"",symbol)
    print(symbol)
    liczba_atomowa = re.sub(r'<strong an="\d+".',"",wzor[0])
    liczba_atomowa = re.sub(r'</strong>.+',"",liczba_atomowa)
    print(liczba_atomowa)
    masa_atomowa = re.sub(r'<strong an="\d+".+<i>',"",wzor[0])
    masa_atomowa = re.sub(r'</i>.+',"",masa_atomowa)
    print(masa_atomowa)
    wartosciowosc = re.sub(r'<strong an="\d+".+<small>',"",wzor[0])
    wartosciowosc = re.sub(r'</small>',"", wartosciowosc)
    wartosciowosc = re.sub(r'<br>',", ",wartosciowosc)
    print(wartosciowosc)
    print("")
    print("Operation done successfully")
    print("")
	#wprowadzenie danych do bazy danych
    baza_pierwiastkow.execute('INSERT INTO TABELKA VALUES(NULL, ?, ?, ?, ?, ?);', (nazwa, symbol, liczba_atomowa, masa_atomowa, wartosciowosc)) 
    baza_pierwiastkow.commit()
    baza_pierwiastkow.close() 
##--------------------------------------------------------------------------##
def pobieram1() :
    # funkcja wyszukuje podany pierwiastek i czyta dane (Po nazwie pierwiastka)
    
    zrodlo_strony = doRequest(URL1) 
    print("Podaj nazwę pierwiastka")
    zmienna = input("Pierwiastek :")  		
    
    pattern = re.compile(r'<strong an="\d+".+'+zmienna+r'.+</small>')
    p = pattern.findall(zrodlo_strony)
    
    wpisuje(p);
##----------------------------------####
def pobieram2() :
    # funkcja wyszukuje podany pierwiastek i czyta dane (Po Liczbie atomowej)
    
    zrodlo_strony = doRequest(URL1) 
    print("Podaj liczbę atomową pierwiastka")
    zmienna = input("Liczba :")  
    
    pattern = re.compile(r'<strong an="\d+">'+zmienna+r'.+</small>')
    p = pattern.findall(zrodlo_strony)
    
    wpisuje(p);
##---------------------------------------------------------------------------##
def wypisz_dane ():
    # Funkcja SELECT. Wybór z bazy 
    baza_pierwiastkow = sqlite3.connect('Kolos1.db')

    #print ("Opened database successfully")

    cursor = baza_pierwiastkow.execute("SELECT nazwa, symbol, liczba_atomowa, masa_atomowa, wartosciowosc  from TABELKA ")
    print ("********************************************")   
    print("Wypisuję dane z tabelki")
    print ("")
    for row in cursor:
       print ("nazwa = ", row[0])
       print ("symbol = ", row[1])
       print ("liczba_atomowa = ", row[2])
       print ("masa_atomowa = ", row[3])
       print ("wartosciowosc = ", row[4], "\n")

    print ("Operation done successfully")
    print ("********************************************")
    print ("")

    baza_pierwiastkow.close()	
##---------------------------------------------------------------------------##	
def create_BD2():
    #Funkca dla DB Opcja 2. Usuwa tabele i tworzy  na nowo. Na życzenie Usera
    baza_pierwiastkow = sqlite3.connect('Kolos1.db')

    print ("Opened database successfully")
    print ("********************************************")
    print ("")
	# Tabela jest usuwana i tworzona.
    baza_pierwiastkow.executescript('''
           DROP TABLE IF EXISTS TABELKA;                   
           CREATE TABLE IF NOT EXISTS TABELKA
           (ID INTEGER PRIMARY KEY     ASC,
           nazwa                VARCHAR     NOT NULL,
		   symbol               VARCHAR     NOT NULL,
           liczba_atomowa       VARCHAR     NOT NULL,
           masa_atomowa         VARCHAR     NOT NULL,
           wartosciowosc       VARCHAR     NOT NULL)''')

    print ("Table created successfully")
    print ("********************************************")
    print ("")

    baza_pierwiastkow.close() 
##---------------------------------------------------------------------------##	
def main():
    create_BD();
    while True :   #Pętla programu głównego, Będzie powtarzać zapytanie o sposób i wypisywać wypełnioną tabelkę
        print("Co chcesz zrobić ?:  !!!! Nazwę podaj zaczynając Wielką literą, reszta małą. !!!!")
        print ("")
        print("""        1 ---- Wyszukać po nazwie danych o pierwiastku i wprowadzić go do Bazy Danych? wpisz ----- 1
        2 ---- Wyszukać po Liczbie atomowej danych o pierwiastku i wprowadzić go do Bazy Danych? wpisz ----- 2
        3 ---- Wypisać aktualną zawartość Bazy danych wpisz ---- 3
        4 ---- Usuń i utwurz na nowo Tabelę bez danych ---- 4
        
        0 ---- Zakończ Program wpisz ----- 0
        
        ********************************************
        """)
        wybierz = int(input("Opcja : "))
        if wybierz == 1 :
            pobieram1();
        if wybierz == 2 :
            pobieram2();
        if wybierz == 3 :
            wypisz_dane();
        if wybierz == 4 :
            create_BD2();
        if wybierz == 0:
            break
		


if __name__ == '__main__':
        main()