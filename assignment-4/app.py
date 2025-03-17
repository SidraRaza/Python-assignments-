import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Custom CSS for Improved Styling
st.markdown(
    """
    <style>
        .stApp {
            color: #333333 !important;
        }
        h1, h2, h3 {
            color: white !important;
            text-align: center; 
            font-weight: bold; 
        }
        .css-1d391kg {
            background-color: #2c3e50 !important; 
        }
        .css-1d391kg span {
            color: white !important;
        }
        .book-card {
            background: white;
            width: 230px; 
            border-radius: 12px; 
            padding: 20px; 
            box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.15); 
            text-align: center;
            margin-bottom: 15px; 
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }
        .book-card:hover {
            transform: scale(1.05);
            box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.2);
        }
        .book-card h3 {
            margin: 0;
            color: #222222;
            font-weight: bold;
            font-size: 20px;
        }
        .book-card p {
            margin: 5px 0;
            color: #444444;
            font-size: 16px;
        }
        .book-card .year {
            font-weight: bold;
            color: #ff4b4b;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Supabase Credentials
SUPABASE_URL = "https://qxevhqzymxmtnbpyukuj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF4ZXZocXp5bXhtdG5icHl1a3VqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIxNDg5NjMsImV4cCI6MjA1NzcyNDk2M30.6GXhnXzvhoavQ7uagt63xVSiQ__zzC22pbB482QaDKo"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📚 Personal Library Manager")

def get_books():
    try:
        response = supabase.table("books").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching books: {e}")
        return []

def add_book(title, author, genre, year):
    if not title or not author or not genre or not year:
        st.error("All fields are required!")
        return

    # Check if genre already exists
    # existing_genre = supabase.table("books").select("genre").eq("genre", genre).execute()

    # if existing_genre.data:
    #     st.error(f"❌ Genre '{genre}' already exists. Please choose another genre.")
    #     return

    # Insert the new book
    supabase.table("books").insert({
        "title": title, "author": author, "genre": genre, "year": year
    }).execute()
    
    st.success(f"✅ '{title}' added successfully!")
    st.rerun()


def delete_book(book_id):
    supabase.table("books").delete().eq("id", book_id).execute()
    st.warning(f"❌ Book with ID {book_id} deleted!")
    st.rerun()

def update_book(book_id, title, author, genre, year):
    if not title or not author or not genre or not year:
        st.error("All fields are required!")
        return
    supabase.table("books").update({
        "title": title, "author": author, "genre": genre, "year": year
    }).eq("id", book_id).execute()
    st.success(f"✅ '{title}' updated successfully!")
    st.rerun()

menu = st.sidebar.selectbox("Menu", ["📖 View Books", "➕ Add Book", "✏️ Update Book", "🗑️ Delete Book"])

if menu == "📖 View Books":
    st.markdown('<h3>📚 Library Collection</h3>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search by Title, Author, or Genre").lower()
    books = get_books()
    if search_query:
        books = [book for book in books if search_query in book['title'].lower() or 
                 search_query in book['author'].lower() or search_query in book['genre'].lower()]
    if books:
        cols = st.columns(3)
        for index, book in enumerate(books):
            with cols[index % 3]:
                st.markdown(
                    f"""
                    <div class="book-card">
                        <h4>{book.get('title', 'Unknown')}</h4>
                        <p><strong>Author:</strong> {book.get('author', 'Unknown')}</p>
                        <p><strong>Genre:</strong> {book.get('genre', 'Unknown')}</p>
                        <p class="year"><strong>Year:</strong> {str(book.get('year', 'N/A'))}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No books found. Try adding some!")

elif menu == "➕ Add Book":
    st.subheader("➕ Add New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Year", min_value=1000, max_value=2025, step=1)
    if st.button("Add Book"):
        add_book(title, author, genre, year)

elif menu == "✏️ Update Book":
    st.subheader("✏️ Update Book Details")
    books = get_books()
    book_options = {book["title"]: book["id"] for book in books}
    if book_options:
        selected_title = st.selectbox("Select Book", list(book_options.keys()))
        selected_id = book_options[selected_title]
        book = next((b for b in books if b["id"] == selected_id), None)
        if book:
            title = st.text_input("Title", book["title"])
            author = st.text_input("Author", book["author"])
            genre = st.text_input("Genre", book["genre"])
            year = st.number_input("Year", min_value=1000, max_value=2025, step=1, value=book["year"])
            if st.button("Update Book"):
                update_book(selected_id, title, author, genre, year)
    else:
        st.warning("No books available to update.")

elif menu == "🗑️ Delete Book":
    st.subheader("🗑️ Delete Book")
    books = get_books()
    book_options = {book["title"]: book["id"] for book in books}
    if book_options:
        selected_title = st.selectbox("Select Book", list(book_options.keys()))
        selected_id = book_options[selected_title]
        st.warning(f"Are you sure you want to delete '{selected_title}'?")
        if st.button("Yes, Delete"):
            delete_book(selected_id)
    else:
        st.warning("No books available to delete.")
