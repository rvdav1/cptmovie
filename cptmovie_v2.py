#!/usr/bin/env python3
# coding: utf-8

import webbrowser
import urllib.parse
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import threading

IMDB = "https://www.imdb.com"
ALLMOVIE = "https://www.allmovie.com"
THEMOVIEDB = "https://www.themoviedb.org"
LETTERBOXD = "https://letterboxd.com"
ICHECKMOVIES = "https://www.icheckmovies.com"
ROTTENTOMATOES = "https://www.rottentomatoes.com"
HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

isThRunning = True

def getUrls(s):
    if s.strip() == '':
        s = 'Nothing'
    searchString = urllib.parse.quote(s.upper())
    reLi = []
    reLi.append("{basePage}{searchReg}{searchText}{searchPost}"
                .format(basePage=IMDB,
                        searchReg='/find?q=',
                        searchText=searchString,
                        searchPost='&s=tt&ttype=ft&ref_=fn_ft/'))
    reLi.append("{basePage}{searchReg}{searchText}{searchPost}"
                .format(basePage=ALLMOVIE,
                        searchReg='/search/movies/',
                        searchText=searchString,
                        searchPost='/'))
    reLi.append("{basePage}{searchReg}{searchText}{searchPost}"
                .format(basePage=THEMOVIEDB,
                        searchReg='/search/movie?query=',
                        searchText=searchString,
                        searchPost='/'))
    reLi.append("{basePage}{searchReg}{searchText}{searchPost}"
                .format(basePage=LETTERBOXD,
                        searchReg='/search/films/',
                        searchText=searchString,
                        searchPost='/'))
    reLi.append("{basePage}{searchReg}{searchText}{searchPost}"
                .format(basePage=ICHECKMOVIES,
                        searchReg='/search/movies/?query=',
                        searchText=searchString,
                        searchPost='/'))
    reLi.append("{basePage}{searchReg}{searchText}{searchPost}"
                .format(basePage=ROTTENTOMATOES,
                        searchReg='/search/?search=',
                        searchText=searchString,
                        searchPost='/'))
    return reLi

def getImdb(s):
    r = requests.get(s, headers=HDR)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        return (IMDB + soup.find('a', href=re.compile('/title//*'))['href'])
    except:
        return s

def getAllmovie(s):
    r = requests.get(s, headers=HDR)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        return (ALLMOVIE + soup.find('a', href=re.compile('/movie//*'))['href'])
    except:
        return s

def getThemoviedb(s):
    r = requests.get(s, headers=HDR)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        return (THEMOVIEDB + soup.find('a', { 'class' : 'result' },
                                   href=re.compile('/movie//*'))['href'])
    except:
        return s
    
def getLetterboxd(s):
    r = requests.get(s, headers=HDR)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        return (LETTERBOXD + soup.find('div',
            { 'data-film-link' : re.compile('/*')})['data-film-link'])
    except:
        return s

def getIcheck(s):
    r = requests.get(s, headers=HDR)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        return (ICHECKMOVIES + soup.find('a', href=re.compile('/search/result*'))['href'])
    except:
        return s

def getRotten(s):
    r = requests.get(s, headers=HDR)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        temp = str(soup.find('div', id='search-results-root').parent.find('script'))
        return (ROTTENTOMATOES + temp[temp.find('"url":"/m/')+7:
                                temp[temp.find('"url":"/m/')+8:
                                ].find('"') +
                                temp.find('"url":"/m/')+8])
    except:
        return s
    
def openImdb(s):
    webbrowser.open(getImdb(s))
    
def openAllmovie(s):
    webbrowser.open(getAllmovie(s))
    
def openThemoviedb(s):
    webbrowser.open(getThemoviedb(s))
        
def openLetterboxd(s):
    webbrowser.open(getLetterboxd(s))
        
def openIcheck(s):
    webbrowser.open(getIcheck(s))
     
def openRotten(s):
    webbrowser.open(getRotten(s))
    
def opener(urls):
    threading.Thread(target=openImdb, args={urls[0]}).start()
    threading.Thread(target=openAllmovie, args={urls[1]}).start()
    threading.Thread(target=openThemoviedb, args={urls[2]}).start()
    threading.Thread(target=openLetterboxd, args={urls[3]}).start()
    threading.Thread(target=openIcheck, args={urls[4]}).start()
    threading.Thread(target=openRotten, args={urls[5]}).start()
    global isThRunning
    isThRunning = False
    
def loading():
    sys.stdout.write('Loading')
    while isThRunning:
        time.sleep(1)
        sys.stdout.write('.')
        sys.stdout.flush()
    sys.stdout.write('\nScript finished running.')

def main():
    s = input('Movie title: ')
    urls = getUrls(s)
    t1 = threading.Thread(target=opener, args=([urls]))
    t2 = threading.Thread(target=loading)
    t1.start()
    t2.start()

if __name__ == "__main__":
    main()