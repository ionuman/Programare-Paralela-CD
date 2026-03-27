import time
import string
import random

def genereaza_cuvinte(n):
    lista_cuvinte = []

    for _ in range(n):
        lungime = random.randint(3, 5)
        cuvant = ''.join(random.choices(string.ascii_lowercase, k=lungime))
        lista_cuvinte.append(cuvant)

    palindroame_initiale = ["ana", "maram", "asa"]

    lista_cuvinte.extend(palindroame_initiale)

    return lista_cuvinte

def este_palindrom(text):
    return text == text[::-1]

def numar_vocale(text):
    vocale = "aeiou"
    return sum(1 for litera in text if litera in vocale)

def run_program(n):
    dictionar = genereaza_cuvinte(n)

    palindroame = []
    total = 0
    vocale = 0

    for text in dictionar:
        if este_palindrom(text):
            palindroame.append(text)
            total += 1

        vocale += numar_vocale(text)
    
    print(f"Dictionar initial: {dictionar}")
    print(f"Palindroame gasite: {palindroame}")
    print(f"Total palindroame: {total}")
    print(f"Total vocale: {vocale}")
          
run_program(100)        

    









