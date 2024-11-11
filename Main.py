import tkinter as tk
from tkinter import messagebox

# Fő ablak létrehozása
root = tk.Tk()
root.title("Amőba játék")
root.withdraw()  # A fő ablakot kezdetben elrejtjük

# Változók a játékosok nevének tárolására
player1_name = ""
player2_name = ""
current_player = ""
winner = None
board = [""] * 9
buttons = []  # Gombok listája a játéktáblához

# Játék kezdése előtt nevek bekérése
def get_player_names():
    global player1_name, player2_name, current_player
    player1_name = player1_entry.get()
    player2_name = player2_entry.get()
    current_player = player1_name  # Az első játékos kezd

    # Névbekérő ablak bezárása és fő játék indítása
    name_window.destroy()
    center_window(root, 300, 330)  # A játék ablak középre helyezése és fix méret beállítása
    root.deiconify()  # Fő ablak megjelenítése
    create_game_board()

# Függvény a gombok létrehozásához és index átadásához
def create_button_command(index):
    return lambda: make_move(index)

# Játék táblának és gomboknak a létrehozása
def create_game_board():
    status_label.config(text=f"{current_player} következik!")
    for i in range(9):
        button = tk.Button(root, text="", font="Helvetica 20 bold", width=5, height=2, command=create_button_command(i))
        button.grid(row=i // 3, column=i % 3)
        buttons.append(button)

# Lépés végrehajtása
def make_move(i):
    global current_player, winner

    if board[i] == "" and not winner:
        if current_player == player1_name:
            board[i] = "X"
            buttons[i].config(text="X", fg="red")
        else:
            board[i] = "O"
            buttons[i].config(text="O", fg="blue")

        # Győzelem vagy döntetlen ellenőrzése
        if check_winner():
            winner = current_player
            save_result()
            show_end_game_message(f"{current_player} nyert!")
        elif "" not in board:
            winner = "Döntetlen"
            save_result()
            show_end_game_message("Döntetlen!")
        else:
            # Játékos váltás
            current_player = player1_name if current_player == player2_name else player2_name
            status_label.config(text=f"{current_player} következik!")

# Győzelem ellenőrzése
def check_winner():
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Sorok
                      (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Oszlopok
                      (0, 4, 8), (2, 4, 6)]  # Átlók

    for (x, y, z) in win_conditions:
        if board[x] == board[y] == board[z] and board[x] != "":
            return True
    return False

# Eredmény mentése fájlba
def save_result():
    with open("amoba_eredmenyek.txt", "a", encoding="utf-8") as file:
        if winner == "Döntetlen":
            file.write(f"{player1_name} vs {player2_name} - Döntetlen\n")
        else:
            file.write(f"{player1_name} vs {player2_name} - {winner} nyert\n")

# Játék újraindítása
def reset_game():
    global board, winner, current_player
    board = [""] * 9
    winner = None
    current_player = player1_name
    for button in buttons:
        button.config(text="")
    status_label.config(text=f"{current_player} következik!")

# Játék vége üzenet és választási lehetőségek
def show_end_game_message(message):
    response = messagebox.askquestion("Játék vége", f"{message}\nSzeretnétek új játékot kezdeni?")
    if response == "yes":
        reset_game()  # Új játék indítása
    else:
        root.quit()  # Kilépés a játékból

# Ablak középre igazítása
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)  # Ablak átméretezésének letiltása

# Névbekérő ablak létrehozása és középre helyezése
name_window = tk.Toplevel(root)
name_window.title("Játékosok Neve")
name_window.configure(bg="white")
center_window(name_window, 300, 200)

# Címsor
title_label = tk.Label(name_window, text="Amőba", font="Helvetica 16 bold", bg="white", fg="black")
title_label.pack(pady=10)

# Beviteli mezők a nevekhez
tk.Label(name_window, text="Első játékos neve:", bg="white", fg="black").pack()
player1_entry = tk.Entry(name_window)
player1_entry.pack()

tk.Label(name_window, text="Második játékos neve:", bg="white", fg="black").pack()
player2_entry = tk.Entry(name_window)
player2_entry.pack()

tk.Button(name_window, text="Kezdés", command=get_player_names).pack(pady=10)

# Fő játék státusz kijelzője
status_label = tk.Label(root, text="", font="Helvetica 14")
status_label.grid(row=3, column=0, columnspan=3)

# Fő ablak indítása
root.mainloop()
