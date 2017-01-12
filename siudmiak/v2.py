import sqlite3
import re
import urllib.request


URL1 = "http://pogoda.interia.pl/"

def doRequest (url):
    # funkcja pomocnicza, łaczy się z zadanym adresem URL i zwraca zawartość
    return urllib.request.urlopen(url).read().decode()

def wybierz():
	#
    print (doRequest(URL1))

def main():
    wybierz();


if __name__ == '__main__':
        main()