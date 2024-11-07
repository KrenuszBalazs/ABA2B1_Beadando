import tkinter as tk
from tkinter import messagebox

# Fő ablak létrehozása
root = tk.Tk()
root.title("Amőba játék")

# Változók a játékosok nevének tárolására
player1_name = ""
player2_name = ""
current_player = ""
winner = None
board = [""] * 9


# Játék kezdése előtt nevek bekérése
def get_player_names():
    global player1_name, player2_name, current_player
    player1_name = player1_entry.get()
    player2_name = player2_entry.get()
    current_player = player1_name  # Az első játékos kezd

    # Ablak bezárása és fő játék indítása
    name_window.destroy()
    create_game_board()


# Játék táblának és gomboknak a létrehozása
def create_game_board():
    status_label.config(text=f"{current_player} következik!")
    for i in range(9):
        button = tk.Button(root, text="", font="Helvetica 20 bold", width=5, height=2, command=lambda i=i: make_move(i))
        button.grid(row=i // 3, column=i % 3)
        buttons.append(button)


# Lépés végrehajtása
def make_move(i):
    global current_player, winner

    if board[i] == "" and not winner:
        board[i] = "X" if current_player == player1_name else "O"
        buttons[i].config(text=board[i])

        # Győzelem vagy döntetlen ellenőrzése
        if check_winner():
            winner = current_player
            save_result()
            messagebox.showinfo("Játék vége", f"{current_player} nyert!")
            reset_game()
        elif "" not in board:
            winner = "Döntetlen"
            save_result()
            messagebox.showinfo("Játék vége", "Döntetlen!")
            reset_game()
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
    with open("amoba_eredmenyek.txt", "a") as file:
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


# Játékablak és beviteli mezők a nevekhez
name_window = tk.Toplevel(root)
name_window.title("Játékosok Neve")
name_window.geometry("300x150")

tk.Label(name_window, text="Első játékos neve:").pack()
player1_entry = tk.Entry(name_window)
player1_entry.pack()

tk.Label(name_window, text="Második játékos neve:").pack()
player2_entry = tk.Entry(name_window)
player2_entry.pack()

tk.Button(name_window, text="Kezdés", command=get_player_names).pack()

# Fő játék státusz kijelzője
status_label = tk.Label(root, text="", font="Helvetica 14")
status_label.grid(row=3, column=0, columnspan=3)

# Gombok listája a játéktáblához
buttons = []

# Fő ablak indítása
root.mainloop()
