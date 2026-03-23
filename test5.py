#pip3 install mpi4py
import mpi4py
import random
import time
import string
from mpi4py import MPI


comm = MPI.COMM_WORLD
#comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
#returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
#numarul total de procese care ruleaza


if rank != 0:
    print(f"Echipa de Mesteri numarul {rank}")
    time_start = time.time()
    #Simulam o munca care dureaza intre 5 si 30 secunde
    time.sleep(random.randint(5,30))
    time_end = time.time()
    elapsed_time = time_end - time_start
    comm.send(elapsed_time, 0)
else:
    print("SEF DE DEPARTAMENT")
    time = 0
    for i in range(size):
        if i == rank:
            continue
        time += comm.recv(source=i)
    print(f"Ziua de munca s-a incheiat, au fost folosite {time} secunde")



#mpiexec -np 5 python "calea_catre_fisierul.py"