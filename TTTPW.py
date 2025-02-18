import tkinter as tk  # Importing Tkinter for GUI
import json  # Importing JSON to store passwords persistently
import os  # Importing os to check for file existence

# File to store passwords
PASSWORD_FILE = "passwords.json"

# Secret admin password to access the password manager
SECRET_PASSWORD = "chipmunk"

# Load stored passwords from the file if it exists; otherwise, use default passwords
if os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, "r") as file:
        passwords = json.load(file)  # Load stored passwords
else:
    passwords = {
        "Netflix": "notpassword1",
        "Bank": "CSULA465",
        "Email": "fjejnnjfe2323",
        "CSULA": "P@ssw0rd",
        "CSUN": "CSUNisgreat"
    }

# Save passwords to file
def save_passwords():
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)  # Store passwords in a JSON file

# Function to check admin password
def check_password():
    if entry.get() == SECRET_PASSWORD:  # If the entered password matches, open the password manager
        open_password_manager()

# Open password manager GUI
def open_password_manager():
    new_window = tk.Toplevel(root)  # Create a new window
    new_window.geometry('400x450')  # Set window size
    new_window.title("Password Manager")  # Set window title

    tk.Label(new_window, text="Stored Passwords:", font=("Arial", 12)).pack(pady=5)

    # Loop through stored passwords and create UI elements for each
    for service, password in passwords.items():
        frame = tk.Frame(new_window)
        frame.pack(fill='x', padx=10, pady=2)

        # Label displaying the service name
        tk.Label(frame, text=f"{service}:", width=12, anchor='w').pack(side='left')

        # Entry widget to display the password (masked by default)
        pw_entry = tk.Entry(frame, show="*", width=20)
        pw_entry.insert(0, password)  # Insert the stored password
        pw_entry.pack(side='left')

        # Function to toggle password visibility
        def toggle_password(entry=pw_entry):
            if entry.cget("show") == "*":  # If password is masked, show it
                entry.config(show="")
            else:
                entry.config(show="*")  # Otherwise, mask it again

        # Button to show/hide the password
        tk.Button(frame, text="Show", command=toggle_password).pack(side='left')

        # Function to update and save a password
        def update_password(entry=pw_entry, service=service):
            passwords[service] = entry.get()  # Update the dictionary
            save_passwords()  # Save changes to the file
            tk.Label(new_window, text=f"{service} updated!", fg='green').pack()  # Confirmation message

        # Button to save updated password
        tk.Button(frame, text="Save", command=update_password).pack(side='left')

    # Section to edit PW
    tk.Label(new_window, text="Edit Passwords≠:").pack(pady=5)

    new_service_entry = tk.Entry(new_window, width=15)  # Entry for the new service name
    new_service_entry.pack()

    new_password_entry = tk.Entry(new_window, width=20, show="*")  # Entry for the new password (masked)
    new_password_entry.pack()

    # Function to add a new password to the dictionary and save it
    def add_password():
        service = new_service_entry.get()
        password = new_password_entry.get()
        if service and password:  # Ensure both fields are filled
            passwords[service] = password  # Add new password to the dictionary
            save_passwords()  # Save changes to the file
            tk.Label(new_window, text=f"{service} added!", fg='green').pack()  # Confirmation message
    
    def delete_password():
        if service in passwords:  # Ensure both fields are filled
            del passwords[service]  # Remove password from dictionary # delete password from manager
            save_passwords()  # Save changes to the file
            tk.Label(new_window, text=f"{service} deleted!", fg='green').pack()  # Confirmation message

    # Button to add a new password
    tk.Button(new_window, text="Add Password", command=add_password).pack(pady=5)
    tk.Button(new_window, text="Delete Password", command=delete_password).pack(pady=5)


# ========== TIC TAC TOE GAME ==========
def callback(r, c):
    global player, winner, moves
    
    if states[r][c] == 0 and not winner:
        b[r][c].config(text=player, fg='black', bg='white')
        states[r][c] = player
        player = 'O' if player == 'X' else 'X'
        moves += 1
    
    check_for_winner()

def check_for_winner():
    global winner
    
    for i in range(3):
        if states[i][0] == states[i][1] == states[i][2] != 0:
            highlight_winner([(i, 0), (i, 1), (i, 2)])
            return
        if states[0][i] == states[1][i] == states[2][i] != 0:
            highlight_winner([(0, i), (1, i), (2, i)])
            return
    
    if states[0][0] == states[1][1] == states[2][2] != 0:
        highlight_winner([(0, 0), (1, 1), (2, 2)])
        return
    if states[2][0] == states[1][1] == states[0][2] != 0:
        highlight_winner([(2, 0), (1, 1), (0, 2)])
        return
    
    if moves == 9 and not winner:
        congrats_label.config(text="It's a tie!", fg="red")
        play_again_button.grid(row=6, column=1, columnspan=1)

def highlight_winner(coords):
    global winner
    for r, c in coords:
        b[r][c].config(bg='grey')
    winner = True
    congrats_label.config(text="Congratulations!", fg="green")
    play_again_button.grid(row=6, column=1, columnspan=1)

def play_again():
    global states, player, winner, moves
    for i in range(3):
        for j in range(3):
            states[i][j] = 0
            b[i][j].config(text='', bg='lightgrey')
    player = 'X'
    winner = False
    moves = 0
    congrats_label.config(text="")
    play_again_button.grid_forget()

# ========== MAIN GUI ==========
root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg='black')

b = [[None] * 3 for _ in range(3)]
states = [[0] * 3 for _ in range(3)]
player = 'X'
winner = False
moves = 0

for i in range(3):
    for j in range(3):
        b[i][j] = tk.Button(root, font=('Arial', 20), width=5, height=2, bg='lightgrey', command=lambda r=i, c=j: callback(r, c))
        b[i][j].grid(row=i, column=j, padx=5, pady=5)

congrats_label = tk.Label(root, text="", font=("Arial", 12), bg='black', fg='white')
congrats_label.grid(row=4, column=0, columnspan=3)

# Entry field for the admin password (masked)
entry = tk.Entry(root, show="*")
entry.grid(row=5, column=0, columnspan=3)

# Button to check if the entered password is correct
check_entry_button = tk.Button(root, text="Play Again", command=check_password, bg= "black")
check_entry_button.grid(row=6, column=0, columnspan=3)

# Play again button for Tic Tac Toe
play_again_button = tk.Button(root, text="Play Again", command=play_again)


# Run the application
root.mainloop()
