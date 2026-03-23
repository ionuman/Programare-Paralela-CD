from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
# comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
# returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
# numarul total de procese care ruleaza

# Verificam daca sunt exact 6 procese
if size != 6:
    if rank == 0:
        print("Eroare: Ruleaza programul cu exact 6 procese!")
    exit()

# Seed dinamic pentru a avea castigatori diferiti la fiecare rulare
random.seed(time.time() + rank)

preturi = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55]
licitatie_incheiata = False

for pret in preturi:
    
    if rank == 0:
        time.sleep(1)
        
    pret_curent = comm.bcast(pret, root=0)
    
    decizie = False
    if rank != 0:
        if pret_curent == 100:
            decizie = False
        else:
            decizie = random.random() < 0.15 
    
    decizii_totale = comm.allgather(decizie)
    
    if rank == 0:
        print(f"Producatorul a strigat pretul: {pret_curent}")
        
        for i in range(1, size):
            if decizii_totale[i] == True:
                time.sleep(0.5) 
                print(f"*** Licitatia s-a incheiat! Televiziunea {i} a acceptat pretul de {pret_curent}. ***\n")
                break 
                
    if True in decizii_totale[1:]:
        licitatie_incheiata = True
        break 

# Bariera de sincronizare inainte de final
comm.Barrier()

if rank == 0 and not licitatie_incheiata:
    print("*** Esec! Nicio televiziune nu a cumparat drepturile. ***")