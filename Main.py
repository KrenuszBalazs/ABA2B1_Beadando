import tkinter as tk
from tkinter import messagebox

class KBP_Jatek:
    def __init__(self, ablak):
        # Játék változók kezdeti beállítása
        self.ablak = ablak
        self.ablak.withdraw()  # Fő ablak elrejtése, amíg a nevek megadása nem történik meg
        self.jatekos1_nev = ""
        self.jatekos2_nev = ""
        self.aktualis_jatekos = ""
        self.nyertes = None
        self.tabla = [""] * 9
        self.gombok = []  # Gombok listája a játéktáblához

        # Fő játék státusz kijelző
        self.statusz_label = tk.Label(self.ablak, text="", font="Helvetica 14")
        self.statusz_label.grid(row=3, column=0, columnspan=3)

        # Kezdő névbekérő ablak létrehozása
        self.kbp_nevbekero_ablak()

    # Névbekérő ablak létrehozása
    def kbp_nevbekero_ablak(self):
        # Névbekérő ablak középre helyezése és dizájn
        self.nev_ablak = tk.Toplevel(self.ablak)
        self.nev_ablak.title("Játékosok Neve")
        self.nev_ablak.configure(bg="white")
        self.kbp_ablak_kozepre(self.nev_ablak, 300, 200)

        # Címsor beállítása
        tk.Label(self.nev_ablak, text="Amőba", font="Helvetica 16 bold", bg="white", fg="black").pack(pady=10)

        # Játékos 1 nevének bekérése
        tk.Label(self.nev_ablak, text="Első játékos neve:", bg="white", fg="black").pack()
        self.jatekos1_mezo = tk.Entry(self.nev_ablak)
        self.jatekos1_mezo.pack()

        # Játékos 2 nevének bekérése
        tk.Label(self.nev_ablak, text="Második játékos neve:", bg="white", fg="black").pack()
        self.jatekos2_mezo = tk.Entry(self.nev_ablak)
        self.jatekos2_mezo.pack()

        # Kezdés gomb
        tk.Button(self.nev_ablak, text="Kezdés", command=self.kbp_nev_ellenorzes).pack(pady=10)

    # Játékos nevének bekérése és a játéktábla létrehozása
    def kbp_nev_ellenorzes(self):
        self.jatekos1_nev = self.jatekos1_mezo.get()
        self.jatekos2_nev = self.jatekos2_mezo.get()

        # Ellenőrzés, hogy a nevek nem üresek-e
        if not self.jatekos1_nev or not self.jatekos2_nev:
            messagebox.showwarning("Figyelem", "Kérlek, add meg mindkét játékos nevét!")
            return

        self.aktualis_jatekos = self.jatekos1_nev

        # Névbekérő ablak bezárása és a fő ablak megjelenítése
        self.nev_ablak.destroy()
        self.ablak.deiconify()  # Fő ablak megjelenítése
        self.kbp_ablak_kozepre(self.ablak, 300, 330)
        self.kbp_jatek_tabla()

    # Játéktábla és gombok létrehozása
    def kbp_jatek_tabla(self):
        self.statusz_label.config(text=f"{self.aktualis_jatekos} következik!")
        for i in range(9):
            gomb = tk.Button(self.ablak, text="", font="Helvetica 20 bold", width=5, height=2,
                             command=self.kbp_gomb_parancs(i))
            gomb.grid(row=i // 3, column=i % 3)
            self.gombok.append(gomb)

    # Gomb parancsának beállítása
    def kbp_gomb_parancs(self, index):
        return lambda: self.kbp_lepes(index)

    # Lépés végrehajtása
    def kbp_lepes(self, i):
        if self.tabla[i] == "" and not self.nyertes:
            if self.aktualis_jatekos == self.jatekos1_nev:
                self.tabla[i] = "X"
                self.gombok[i].config(text="X", fg="red")  # X piros
            else:
                self.tabla[i] = "O"
                self.gombok[i].config(text="O", fg="blue")  # O kék

            # Győzelem vagy döntetlen ellenőrzése
            if self.kbp_gyoztes_ellenorzes():
                self.nyertes = self.aktualis_jatekos
                self.kbp_eredmeny_mentes()
                self.kbp_jatek_vege(f"{self.aktualis_jatekos} nyert!")
            elif "" not in self.tabla:
                self.nyertes = "Döntetlen"
                self.kbp_eredmeny_mentes()
                self.kbp_jatek_vege("Döntetlen!")
            else:
                # Játékos váltás
                self.aktualis_jatekos = self.jatekos1_nev if self.aktualis_jatekos == self.jatekos2_nev else self.jatekos2_nev
                self.statusz_label.config(text=f"{self.aktualis_jatekos} következik!")

    # Győzelem ellenőrzése
    def kbp_gyoztes_ellenorzes(self):
        nyero_kombinaciok = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Sorok
                             (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Oszlopok
                             (0, 4, 8), (2, 4, 6)]  # Átlók

        for (x, y, z) in nyero_kombinaciok:
            if self.tabla[x] == self.tabla[y] == self.tabla[z] and self.tabla[x] != "":
                return True
        return False

    # Eredmény mentése fájlba
    def kbp_eredmeny_mentes(self):
        with open("amoba_eredmenyek.txt", "a", encoding="utf-8") as file:
            if self.nyertes == "Döntetlen":
                file.write(f"{self.jatekos1_nev} vs {self.jatekos2_nev} - Döntetlen\n")
            else:
                file.write(f"{self.jatekos1_nev} vs {self.jatekos2_nev} - {self.nyertes} nyert\n")

    # Játék vége üzenet és új játék lehetőség
    def kbp_jatek_vege(self, uzenet):
        valasz = messagebox.askquestion("Játék vége", f"{uzenet}\nSzeretnétek új játékot kezdeni?")
        if valasz == "yes":
            self.kbp_jatek_ujrainditas()
        else:
            self.ablak.quit()

    # Játék újraindítása
    def kbp_jatek_ujrainditas(self):
        self.tabla = [""] * 9
        self.nyertes = None
        self.aktualis_jatekos = self.jatekos1_nev
        for gomb in self.gombok:
            gomb.config(text="")
        self.statusz_label.config(text=f"{self.aktualis_jatekos} következik!")

    # Ablak középre helyezése és méret beállítása
    def kbp_ablak_kozepre(self, ablak, szelesseg, magassag):
        kepernyo_szelesseg = ablak.winfo_screenwidth()
        kepernyo_magassag = ablak.winfo_screenheight()
        x = (kepernyo_szelesseg // 2) - (szelesseg // 2)
        y = (kepernyo_magassag // 2) - (magassag // 2)
        ablak.geometry(f"{szelesseg}x{magassag}+{x}+{y}")
        ablak.resizable(False, False)

# Fő ablak létrehozása
fo_ablak = tk.Tk()
fo_ablak.title("Amőba játék")

# Játék inicializálása
KBP_Jatek(fo_ablak)

# Fő ablak futtatása
fo_ablak.mainloop()
