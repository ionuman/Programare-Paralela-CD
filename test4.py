#pip3 install mpi4py
import mpi4py
import random
import time
import string
from mpi4py import MPI
 
def genereaza_dictionar(n):
    lista_cuvinte = []
    for _ in range(n):
        lungime = random.randint(2, 3)
        cuvant = ''.join(random.choices(string.ascii_lowercase, k=lungime))
        lista_cuvinte.append(cuvant)
    return lista_cuvinte
 
def este_palindrom(text):
    return text == text[::-1]
    #abc - > text[::-1] => returneaza "c"
 
comm = MPI.COMM_WORLD
#comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
#returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
#numarul total de procese care ruleaza

pachete_cuvinte = None
if rank == 0:
    dictionar_complet = genereaza_dictionar(100)
    pachete_cuvinte = [dictionar_complet[i::size] for i in range(size)]


cuvinte_locale = comm.scatter(pachete_cuvinte, root=0)

for cuvant in cuvinte_locale:
    rezultat = este_palindrom(cuvant)
    status = "este palindrom" if rezultat else "NU este palindrom"
    print(f"Procesul {rank} a verificat cuvantul '{cuvant}' si a obtinut rezultatul: {status}")

comm.Barrier()  # Asiguram sincronizarea tuturor proceselor inainte de a termina

if rank == 0:
    print("Toate procesele au terminat verificarea cuvintelor.")

#mpiexec -np 5 python "calea_catre_fisierul.py"