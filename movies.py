import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database initialization function
def initialize_database():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  director TEXT NOT NULL,
                  year INTEGER NOT NULL,
                  genre TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to add movie
def add_movie():
    title = title_entry.get()
    director = director_entry.get()
    year = year_entry.get()
    genre = genre_entry.get()

    if title and director and year and genre:
        try:
            conn = sqlite3.connect('movies.db')
            c = conn.cursor()
            c.execute("INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)", 
                      (title, director, int(year), genre))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Movie added successfully!")
            clear_fields()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year!")
    else:
        messagebox.showwarning("Input Error", "All fields must be filled!")

# Function to delete movie
def delete_movie():
    movie_id = movie_id_entry.get()
    if movie_id:
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute("DELETE FROM movies WHERE id=?", (movie_id,))
        if c.rowcount == 0:
            messagebox.showwarning("Warning", "No movie found with this ID!")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Movie deleted successfully!")
        conn.close()
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "Please enter a movie ID.")

# Function to search movie
def search_movie():
    title = search_title_entry.get()
    if title:
        conn = sqlite3.connect('movies.db')
        c = conn.cursor()
        c.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + title + '%',))
        movies = c.fetchall()
        conn.close()

        search_results.delete(1.0, tk.END)
        if movies:
            for movie in movies:
                search_results.insert(tk.END, f"ID: {movie[0]}, Title: {movie[1]}, Director: {movie[2]}, Year: {movie[3]}, Genre: {movie[4]}\n")
        else:
            search_results.insert(tk.END, "No movies found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a title to search.")

# Function to edit movie details
def edit_movie():
    movie_id = movie_id_entry.get()
    title = title_entry.get()
    director = director_entry.get()
    year = year_entry.get()
    genre = genre_entry.get()

    if movie_id and title and director and year and genre:
        try:
            conn = sqlite3.connect('movies.db')
            c = conn.cursor()
            c.execute("UPDATE movies SET title=?, director=?, year=?, genre=? WHERE id=?", 
                      (title, director, int(year), genre, movie_id))
            if c.rowcount == 0:
                messagebox.showwarning("Warning", "No movie found with this ID!")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Movie details updated successfully!")
            conn.close()
            clear_fields()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid year!")
    else:
        messagebox.showwarning("Input Error", "All fields must be filled.")

# Function to clear input fields
def clear_fields():
    title_entry.delete(0, tk.END)
    director_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    movie_id_entry.delete(0, tk.END)
    search_title_entry.delete(0, tk.END)

# Setting up Tkinter window
root = tk.Tk()
root.title("Movie Record Management")
root.geometry("600x500")

# Initialize the database
initialize_database()

# Add Movie Section
add_movie_label = tk.Label(root, text="Add Movie", font=('Arial', 12, 'bold'))
add_movie_label.grid(row=0, column=1, pady=10)

title_label = tk.Label(root, text="Title:")
title_label.grid(row=1, column=0, padx=5)
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=1, column=1)

director_label = tk.Label(root, text="Director:")
director_label.grid(row=2, column=0, padx=5)
director_entry = tk.Entry(root, width=40)
director_entry.grid(row=2, column=1)

year_label = tk.Label(root, text="Year:")
year_label.grid(row=3, column=0, padx=5)
year_entry = tk.Entry(root, width=40)
year_entry.grid(row=3, column=1)

genre_label = tk.Label(root, text="Genre:")
genre_label.grid(row=4, column=0, padx=5)
genre_entry = tk.Entry(root, width=40)
genre_entry.grid(row=4, column=1)

add_button = tk.Button(root, text="Add Movie", command=add_movie)
add_button.grid(row=5, column=1, pady=10)

# Delete Movie Section
delete_movie_label = tk.Label(root, text="Delete Movie", font=('Arial', 12, 'bold'))
delete_movie_label.grid(row=6, column=1, pady=10)

movie_id_label = tk.Label(root, text="Movie ID:")
movie_id_label.grid(row=7, column=0, padx=5)
movie_id_entry = tk.Entry(root, width=40)
movie_id_entry.grid(row=7, column=1)

delete_button = tk.Button(root, text="Delete Movie", command=delete_movie)
delete_button.grid(row=8, column=1, pady=10)

# Search Movie Section
search_movie_label = tk.Label(root, text="Search Movie by Title", font=('Arial', 12, 'bold'))
search_movie_label.grid(row=9, column=1, pady=10)

search_title_label = tk.Label(root, text="Movie Title:")
search_title_label.grid(row=10, column=0, padx=5)
search_title_entry = tk.Entry(root, width=40)
search_title_entry.grid(row=10, column=1)

search_button = tk.Button(root, text="Search", command=search_movie)
search_button.grid(row=11, column=1, pady=10)

search_results = tk.Text(root, height=5, width=50)
search_results.grid(row=12, column=0, columnspan=2, padx=10)

# Edit Movie Section
edit_movie_label = tk.Label(root, text="Edit Movie Details", font=('Arial', 12, 'bold'))
edit_movie_label.grid(row=13, column=1, pady=10)

edit_button = tk.Button(root, text="Edit Movie", command=edit_movie)
edit_button.grid(row=14, column=1, pady=10)

root.mainloop()