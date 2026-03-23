#pip3 install mpi4py
import mpi4py
import random
from mpi4py import MPI
 
def aruncare_cu_zarul(times = 1):
    times = range(times)
    result = [] 
    for _ in times:
        result.append(random.randint(1,6))
    return result
    
comm = MPI.COMM_WORLD
#comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
#returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
#numarul total de procese care ruleaza
 
match rank:
    case 0:
        proces_0_arunca = aruncare_cu_zarul() 
        suma_proces = sum(proces_0_arunca)    
        print(f"Procesul {rank} a aruncat zarul si a obtinut: {proces_0_arunca}")
        print(f"Suma aruncarilor procesului {rank} este: {suma_proces}")
    case 1:
        proces_1_arunca = aruncare_cu_zarul(2)
        print(f"Procesul {rank} a aruncat zarul de 2 ori si a obtinut: {proces_1_arunca}")
        suma_proces = sum(proces_1_arunca)
        print(f"Suma aruncarilor procesului {rank} este: {suma_proces}")
    case 2:
        proces_2_arunca = aruncare_cu_zarul(3)
        print(f"Procesul {rank} a aruncat zarul de 3 ori si a obtinut: {proces_2_arunca}")
        suma_proces = sum(proces_2_arunca)
        print(f"Suma aruncarilor procesului {rank} este: {suma_proces}")
    case _:
        suma_proces = 0
        print(f"Zarul nu a fost aruncat de procesul {rank}")

suma_totala = comm.gather(suma_proces, root=3)
if rank == 3:
    print(f"Suma tuturor aruncarilor cu zarul este: {sum(suma_totala)}")