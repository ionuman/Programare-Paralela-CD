#===============================================================================
# Nume project: Sistem Distribuit pentru Analiza Textelor
# Creat de: [Chivari Andrei] si [Manea Ionut]
# Data: [23.03.2026]
# Proiect prezentare - Procesare distribuita a unui dictionar de cuvinte
# Scop: Demonstram utilizarea operatiilor MPI (Scatter, Gather, Reduce si Barrier)
# pentru a distribui, procesa si agrega date intr-un mod eficient.
#===================================================================================

from mpi4py import MPI
import random
import time
import string

# --- INITIALIZARE MPI ---
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Functie ajutatoare pentru generarea de cuvinte random si pentru a cauta palindroame
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

def este_palindrom(text):
    return text == text[::-1]

def numara_vocale(text):
    vocale = "aeiou"
    return sum(1 for litera in text if litera in vocale)

# --- PASUL 1: MASTERUL PREGATESTE DATELE ---
pachete_cuvinte = None
if rank == 0:
    print("--- INCEPERE PROCESARE DISTRIBUITA ---")
    # Generam un numar de cuvinte in functie de numarul de procese
    numar_total_cuvinte = size * 10 
    dictionar_complet = genereaza_cuvinte(numar_total_cuvinte)
    
    # Impartim lista mare in sub-liste pentru fiecare proces (inspirat din test4.py)
    pachete_cuvinte = [dictionar_complet[i::size] for i in range(size)]
    print(f"Master (Rank 0): Am generat {len(dictionar_complet)} cuvinte si le-am impartit in {size} pachete.\n")

# --- PASUL 2: DISTRIBUIREA DATELOR (SCATTER) ---
# Fiecare proces primeste pachetul sau de cuvinte
cuvinte_locale = comm.scatter(pachete_cuvinte, root=0)

# --- PASUL 3: PROCESAREA LOCALA (WORKERS) ---
palindroame_gasite = []
total_vocale_local = 0

for cuvant in cuvinte_locale:
    # Simulam ca procesarea fiecarui cuvant este o operatie grea, adaugand o intarziere aleatoare.
    time.sleep(random.uniform(0.05, 0.15))
    
    # Numaram vocalele
    total_vocale_local += numara_vocale(cuvant)
    
    # Cautam palindroame
    if este_palindrom(cuvant):
        palindroame_gasite.append(cuvant)

print(f"Procesul {rank} a analizat {len(cuvinte_locale)} cuvinte, a gasit {total_vocale_local} vocale si palindroamele: {palindroame_gasite}", flush=True)

# --- PASUL 4: AGREGAREA DATELOR (REDUCE & GATHER) ---
suma_totala_vocale = comm.reduce(total_vocale_local, op=MPI.SUM, root=0)

# gathered_palindroame va fi o lista de liste pe rank 0
gathered_palindroame = comm.gather(palindroame_gasite, root=0)

# --- PASUL 5: SINCRONIZARE (BARRIER) ---
comm.Barrier()

# --- PASUL 6: MASTERUL AFISEAZA REZULTATUL FINAL ---
if rank == 0:
    time.sleep(0.5)  # Asteptam jumatate de secunda ca toate print-urile intarziate sa ajunga pe ecran
    # Aplatizam lista de liste (extragem cuvintele din listele individuale)
    toate_palindroamele = []
    for lista in gathered_palindroame:
        toate_palindroamele.extend(lista)
        
    print("\n--- REZULTATE FINALE ALE ANALIZEI ---", flush=True)
    print(f"Numarul total de vocale procesate in sistem: {suma_totala_vocale}")
    print(f"Numarul total de palindroame gasite: {len(toate_palindroamele)}")
    print(f"Palindroamele sunt: {toate_palindroamele}")
    print("-------------------------------------")

# Pentru rulare: mpiexec -np 5 python proiect_analiza.py