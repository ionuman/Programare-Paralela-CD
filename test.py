#pip3 install mpi4py
import mpi4py
from mpi4py import MPI
 
comm = MPI.COMM_WORLD
#comunicarea globala intre toate procesele MPI
rank = comm.Get_rank()
#returneaza rang-ul procesului curent (ID unic pentru fiecare proc. MPI, incepand de la 0!)
size = comm.Get_size()
#numarul total de procese care ruleaza
 
#Broadcast
# if rank == 0 :
#     data = {'key1':[7,12.22,2+9j],
#             'key2':('abc','def')
#            }
# else:
#     data = None
 
# data = comm.bcast(data,root=0)
#print(f"{data} pe {rank}")
 
#Send & Receive
# if rank == 0:
#     data = {'msg':'Salut de la procesul 0'}
#     comm.send(data, dest=1)
# elif rank == 1:
#     data = comm.recv(source = 0)
#     print("Procesul 1 a primit date: ",data)
 
 
#Scatter
# if rank == 0 :
#     data = list([0,1,2,3,4,5])
# else:
#     data = None
# #Fiecare proces primeste cate un element    
# received_data = comm.scatter(data,root=0)
# print(f"Procesul {rank} a primit: {received_data}")
 
#Gather
#Fiecare proces trimite o valoare catre procesul root, proces care colecteaza datele intr-o lista
# send_data = rank # Fiecare proces trimite propriul rank
# gathered_data = comm.gather(send_data, root = 0)
 
# if rank== 0:
#     print("Datele au fost colectate ", gathered_data)
 
 
#Reduce
#Aplica o operatie asupra datelor de la toate procesele si trimite rezultatul unui singur proces
# This code snippet is using MPI (Message Passing Interface) in Python to perform a reduction
# operation. Here's a breakdown of what it does:
send_data = rank
reduced_data = comm.reduce(send_data,op=MPI.SUM, root=0)
if rank == 0 :
    print("Suma rank-urilor este:", reduced_data)
 
 
 
#mpiexec -np 5 python "calea_catre_fisierul.py"