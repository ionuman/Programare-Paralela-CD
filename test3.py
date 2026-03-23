#pip3 install mpi4py
import mpi4py
from mpi4py import MPI
 
comm = MPI.COMM_WORLD
#comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
#returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
#numarul total de procese care ruleaza
 
n = 10000
dim_baza = n // size
rest = n % size

#calculam intervalul pentru fiecare proces
inceput = rank * dim_baza + min(rank, rest) + 1
sfarsit = inceput + dim_baza - 1

if rank < rest:
    sfarsit += 1
    
if inceput <= sfarsit:
    suma_locala = (inceput + sfarsit) * (sfarsit - inceput + 1) // 2
else:
    suma_locala = 0
    
suma_totala = comm.reduce(suma_locala, op=MPI.SUM, root=0)
if rank == 0:
    suma_corecta = n * (n + 1) // 2
    print(f"n = {n}")
    print(f"SUMA MPI = {suma_totala}")
    print(f"SUMA CORECTA = {suma_corecta}")
    print(f"Corectitudine: {suma_totala == suma_corecta}")
    