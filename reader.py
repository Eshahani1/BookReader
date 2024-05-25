import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# Database configuration
DB_HOST = "********************"
DB_USER = "********************"
DB_PASSWORD = "********************"
DB_DATABASE = "********************"


def create_table(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), chapter VARCHAR(50))"
    )


def add_book(name, chapter, cursor):
    cursor.execute("INSERT INTO books (name, chapter) VALUES (%s, %s)", (name, chapter))
    connection.commit()
    update_listbox()


def list_books(cursor):
    cursor.execute("SELECT name, chapter FROM books")
    return cursor.fetchall()


def update_chapter(book_id, new_chapter, cursor):
    cursor.execute(
        "UPDATE books SET chapter = %s WHERE id = %s", (new_chapter, book_id)
    )
    connection.commit()
    update_listbox()


def edit_name(book_id, new_name, cursor):
    cursor.execute("UPDATE books SET name = %s WHERE id = %s", (new_name, book_id))
    connection.commit()
    update_listbox()


def add_book_gui(cursor):
    name = simpledialog.askstring("Input", "Enter the name of the book:")
    if name:
        chapter = simpledialog.askstring("Input", "Enter the chapter you are on:")
        if chapter:
            add_book(name.title(), chapter, cursor)


def update_chapter_gui(cursor):
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Selection error", "No book selected.")
        return

    # Get the selected book's name and chapter
    selected_book = listbox.get(selected_index[0])
    selected_name = selected_book.split(" - ")[0]

    # Find the book ID based on its name
    cursor.execute("SELECT id FROM books WHERE name = %s", (selected_name,))
    result = cursor.fetchone()
    if not result:
        messagebox.showwarning("Error", "Selected book not found in database.")
        return

    book_id = result[0]

    new_chapter = simpledialog.askstring("Input", "Enter the new chapter:")
    if new_chapter:
        update_chapter(book_id, new_chapter, cursor)


def edit_name_gui(cursor):
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("Selection error", "No book selected.")
        return

    # Get the selected book's name and chapter
    selected_book = listbox.get(selected_index[0])
    selected_name = selected_book.split(" - ")[0]

    # Find the book ID based on its name
    cursor.execute("SELECT id FROM books WHERE name = %s", (selected_name,))
    result = cursor.fetchone()
    if not result:
        messagebox.showwarning("Error", "Selected book not found in database.")
        return

    book_id = result[0]

    new_name = simpledialog.askstring("Input", "Enter the new name:")
    if new_name:
        edit_name(book_id, new_name.title(), cursor)


def search_books():
    query = (
        search_entry.get().strip()
    )  # Get the search query and remove leading/trailing whitespace
    if not query:  # If the search query is empty
        update_listbox()  # Show all books
        return

    listbox.delete(0, tk.END)  # Clear the listbox
    for name, chapter in list_books(cursor):
        if query.lower() in name.lower():
            listbox.insert(tk.END, f"{name} - Chapter {chapter}")


def update_listbox():
    listbox.delete(0, tk.END)
    for name, chapter in list_books(cursor):
        listbox.insert(tk.END, f"{name} - Chapter {chapter}")


# Create the main window
root = tk.Tk()
root.title("Book Tracker")
root.geometry("600x400")  # Set initial window size to 600x400 pixels

# Database connection
try:
    connection = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_DATABASE
    )
    cursor = connection.cursor()
    create_table(cursor)
except mysql.connector.Error as error:
    messagebox.showerror("Database Error", f"Error connecting to the database: {error}")
    exit()

# Create a frame for search box
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(
    search_frame, text="Search", font=("Arial", 12), command=search_books
)
search_button.pack(side=tk.LEFT)

# Create a listbox to display the books with a scrollbar
listbox_frame = tk.Frame(root, bg="#f0f0f0")  # Light gray background
listbox_frame.pack(fill=tk.BOTH, expand=True)

listbox = tk.Listbox(
    listbox_frame,
    font=("Arial", 12),
    bg="#ffffff",
    selectbackground="#a6e1ec",
    selectforeground="#000000",
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)

# Create buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_button = tk.Button(
    button_frame,
    text="Add Book",
    font=("Arial", 12),
    command=lambda: add_book_gui(cursor),
)
add_button.pack(side=tk.LEFT, padx=10)

update_button = tk.Button(
    button_frame,
    text="Update Chapter",
    font=("Arial", 12),
    command=lambda: update_chapter_gui(cursor),
)
update_button.pack(side=tk.LEFT, padx=10)

edit_button = tk.Button(
    button_frame,
    text="Edit Name",
    font=("Arial", 12),
    command=lambda: edit_name_gui(cursor),
)
edit_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(
    button_frame, text="Exit", font=("Arial", 12), command=root.quit
)
exit_button.pack(side=tk.LEFT, padx=10)

# Populate the listbox with the current books on startup
update_listbox()

# Run the GUI event loop
root.mainloop()

# Close database connection
cursor.close()
connection.close()
