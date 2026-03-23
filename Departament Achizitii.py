#pip3 install mpi4py
import random
import time
import string
import mpi4py
from mpi4py import MPI
import random

#departament achizitii


def genereaza_oferta(cantitate_ceruta: int) -> dict:
    cantitate_oferta = random.randint(max(0, cantitate_ceruta -50), cantitate_ceruta + 50)
    pret_unitar = round(random.uniform(1, 5), 2)
    return {
        'cantitate': cantitate_oferta,
        'pret_unitar': pret_unitar
    }

def cheie_pret_unitar(oferta:dict) -> float:
    return oferta['pret_unitar']    

comm = MPI.COMM_WORLD
#comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
#returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
#numarul total de procese care ruleaza

if rank == 0:
    cantitate_ceruta = 100
    oferta = genereaza_oferta(cantitate_ceruta)
    rank_angajati = list(range(1, size))
    for r in rank_angajati:
        comm.send(cantitate_ceruta, dest=r)
    #primim ofertele
    oferte = []
    for r in rank_angajati:
        oferta = comm.recv(source=r)
        oferte.append(oferta)
        #oferte.append((r, oferta))

    #sortam dupa pret
    oferte.sort(key=cheie_pret_unitar)
    cost_total = 0.0
    ramas_de_cumparat = cantitate_ceruta

    print("OFERTE PRIMITE  |    OFERTE ORDONATE DUPA PRET")
    for i, oferta in enumerate(oferte, start=1):
        print(f"Oferta {i}: cantitatea = {oferta['cantitate']}, pret_unitar = {oferta['pret_unitar']}")

    print ("DECIZIE DE CUMPARARE")
    for oferta in oferte:
        if ramas_de_cumparat == 0:
            break
        iau = min(ramas_de_cumparat, oferta['cantitate'])
        cost_total += iau * oferta['pret_unitar']
        ramas_de_cumparat -= iau
        print(f"IAU {iau} buc la {oferta['pret_unitar']} RON/buc ->  Mai raman de cumparat {ramas_de_cumparat}")    
    if ramas_de_cumparat > 0:
        print(f"Nu s-a putut acoperi toata cererea. Lipsesc {ramas_de_cumparat} caiete.")
    else:
        print(f"Costul total este  = {cost_total} RON")
else:
    cantitate_ceruta = comm.recv(source=0)
    oferta = genereaza_oferta(cantitate_ceruta)
    print(f"Angajatul {rank} trimit oferta: {oferta['cantitate']} bucati cu pretul = {oferta['pret_unitar']} RON/buc")
    comm.send(oferta, dest=0)
    
    
#mpiexec -np 5 python "calea_catre_fisierul.py"