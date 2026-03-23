import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

# Functia care ruleaza motorul MPI in fundal
def ruleaza_mpi_in_fundal():
    # Dezactivam butonul cat timp ruleaza pentry a preveni dublarea procesului.
    buton_start.config(state=tk.DISABLED, text="Se proceseaza...")
    consola.insert(tk.END, ">>> Initializare MPI cu 5 procese...\n")
    
    try:
        # Aici apelam efectiv comanda din terminal!
        rezultat = subprocess.run(
            ["mpiexec", "-np", "5", "python", "proiect_analiza.py"],
            capture_output=True, # Capturam ce ar fi scris in terminal
            text=True,           # Sa fie text, nu ca byti
            check=True
        )
        
        # Daca a rulat cu succes, afisam rezultatul in fereastra.
        consola.insert(tk.END, rezultat.stdout)
        
    except subprocess.CalledProcessError as e:
        # Daca a aparut o eroare in codul MPI
        consola.insert(tk.END, f"\n[EROARE MPI]:\n{e.stderr}\n")
    except FileNotFoundError:
        # Daca mpiexec nu e instalat sau gasit
        consola.insert(tk.END, "\n[EROARE]: Nu s-a gasit comanda 'mpiexec'. Verifica setarile sistemului.\n")

    consola.insert(tk.END, "\n>>> Analiza a fost finalizata cu succes.\n")
    consola.insert(tk.END, "-" * 60 + "\n\n")
    consola.see(tk.END) # Scroll automat la ultimul mesaj
    
    # Reactivam butonul
    buton_start.config(state=tk.NORMAL, text="Porneste Analiza Distribuita")

# Pentru a nu bloca interfata cat timp ruleaza MPI, o pornim pe un "thread" separat
def porneste_analiza():
    thread_analiza = threading.Thread(target=ruleaza_mpi_in_fundal)
    thread_analiza.start()

# ==========================================
# CONSTRUIREA INTERFETEI GRAFICE (GUI)
# ==========================================

fereastra = tk.Tk()
fereastra.title("Sistem Distribuit - Analiza Textelor")
fereastra.geometry("750x550")
fereastra.configure(bg="#f0f0f0")

# Titlu
titlu = tk.Label(fereastra, text="Analizator Distribuite cu MPI", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
titlu.pack(pady=15)

# Instructiuni
descriere = tk.Label(fereastra, text="Apasati butonul de mai jos pentru a lansa procesarea distribuita pe 5 noduri.", font=("Helvetica", 10), bg="#f0f0f0")
descriere.pack(pady=5)

# Butonul de start
buton_start = tk.Button(fereastra, text="Porneste Analiza Distribuita", font=("Helvetica", 12, "bold"), 
                        bg="#4CAF50", fg="white", width=30, height=2, command=porneste_analiza)
buton_start.pack(pady=15)

# O casuta de text care va juca rolul consolei/terminalului
frame_consola = tk.LabelFrame(fereastra, text=" Rezultatele Procesarii (Log Terminal) ", font=("Helvetica", 10, "bold"), bg="#f0f0f0")
frame_consola.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

consola = scrolledtext.ScrolledText(frame_consola, wrap=tk.WORD, font=("Consolas", 10), bg="black", fg="#00FF00")
consola.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Pornim aplicatia
fereastra.mainloop()