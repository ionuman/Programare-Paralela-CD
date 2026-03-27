import string
import random

# ---> TEST concepte din functia genereaza_cuvinte(n) <---
#   Functia choices din random.choices extrage cu repetitie, un element poate fi ales de mai multe ori
#   string.ascii_lowercase este un sir constant din Python care contine tot alfabetul cu litere mici
#   '' din ''.join este separatorul care va lipi literele intr-un cuvant. Fara join am primi o lista de litere precum ['a', 'b', 'c']

litera = ''.join(random.choices(string.ascii_lowercase, k=3))
lungime = random.randint(3, 5)

#   extend aplatizeaza lista. Despacheteaza lista primita si adauga fiecare element in parte la finalul listei - vom avea o singura lista lunga
#   append ia obiectul primit (in cazul nostru o lista) si o adauga ca un bloc la finalul listei - vom avea o lista in lista
#   OUTPUT: ['ana', 'are', 'pepene', 'mango', ['mere', 'pere']] 
lista = ["ana", "are"]
lista.extend(["pepene", "mango"])
lista.append(["mere", "pere"])

print(litera)
print(lungime)
print(lista)

# ---> TEST concepte din functia este_palindrom(text) <---
#   nume[::-1] - inversarea unui sir de caractere. Intoarce stringul inversat. Daca nume este egal cu nume[::-1], atunci nume este un palindrom
#   slicing (start:stop:step) - start este indexul de la care incepe extragerea, stop este indexul la care se opreste extragerea (nu este inclus), step este pasul cu care se extrage (daca este negativ, se extrage de la final spre inceput)
nume = "ionut"
rezultat = True if nume==nume[::-1] else False

def verfica_palindrom(text):
    return text == text[::-1]

oras = "brasov"
print(oras[1:3:])

print(nume[::-1])
print(verfica_palindrom("ana"))


# ---> TEST concepte din functia numara_vocale(text) <---
#   Structura (1 for litera in text if litera in vocale) se numeste generator expression
#   Expresia emite valoarea 1 pentru fiecare litera care trece de filtru, iar functia sum aduna toate valoarile
def numara_vocale(text):
    vocale = "aeiou"
    total = 0
    for litera in text:
        if litera in vocale:
            total+=1
    return total

def numara_vocale_generator(text):
    vocale = "aeiou"
    return sum(1 for litera in text if litera in vocale)


# ---> TEST genereaza_cuvinte() <---
def genereaza_cuvinte(n):
    lista_cuvinte = []
    for _ in range(n):
        lungime = random.randint(3, 5)
        cuvant = ''.join(random.choices(string.ascii_lowercase, k=lungime))
        lista_cuvinte.append(cuvant)
        
    # Adaugam manual cateva palindroame pentru a fi siguri ca gasim ceva
    lista_cuvinte.extend(["ana", "cojoc", "capac", "radar", "minim", "rotor", "civic",])
    random.shuffle(lista_cuvinte)
    return lista_cuvinte

dictionar = genereaza_cuvinte(2)

print(numara_vocale("aeiou"))
print(numara_vocale_generator("ionut"))
print(dictionar)