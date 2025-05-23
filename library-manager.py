import json
import os
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="📚 Personal Library", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
<style>
/* App background gradient: pink theme */
.stApp {
    background: linear-gradient(to right, #8e2de2, #c06c84);
}

/* Sidebar container */
section[data-testid="stSidebar"] {
    background-color: #ffe6f0 !important;
    animation: slideIn 1.5s ease-out;
    color: #4b004b;
}

/* Slide-in animation */
@keyframes slideIn {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(0); }
}

/* Option menu container box with pink gradient */
section[data-testid="stSidebar"] ul {
    background: linear-gradient(135deg, #9d50bb, #6e48aa);
    border-radius: 16px;
    padding: 0.5rem;
    box-shadow: 0 4px 16px rgba(110, 72, 170, 0.4);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Menu items */
.nav-link {
    color: #f8e1ff !important;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    transition: all 0.3s ease;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Hover effect */
.nav-link:hover {
    background: rgba(248, 225, 255, 0.15);
    transform: translateX(6px);
    box-shadow: 0 0 10px rgba(248, 225, 255, 0.3);
}

/* Selected item — pink gradient */
div[data-testid="stSidebar"] ul > li > a.nav-link.active {
    background: linear-gradient(to right, #7b2ff7, #f107a3) !important;
    color: #fff !important;
    font-weight: bold;
    transform: scale(1.05);
    border-radius: 12px;
    box-shadow: 0 0 12px rgba(241, 7, 163, 0.6);
    transition: all 0.3s ease;
}

/* Icon styles */
.nav-link i {
    transition: transform 0.6s ease, color 0.3s ease;
    display: inline-block;
    font-size: 1.2em;
    color: #f8e1ff !important;
}

/* Hover icon */
.nav-link:hover i {
    transform: rotate(10deg) scale(1.1);
    color: #fff !important;
}

/* Spin animation for selected icon */
div[data-testid="stSidebar"] ul > li > a.nav-link.active i {
    animation: spin 1.5s linear infinite;
    color: #fff !important;
}

/* Spin keyframes */
@keyframes spin {
    0% { transform: rotate(0deg);}
    100% { transform: rotate(360deg);}
}

/* Mobile tweaks: smaller padding and font */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] ul {
        padding: 0.3rem;
    }
    .nav-link {
        padding: 0.4rem 0.8rem;
        font-size: 0.9rem;
    }
    .nav-link i {
        font-size: 1em;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- Book Manager Class ----------
class BookManager:
    def __init__(self, filepath='books_data.json'):
        self.filepath = filepath
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_books(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.books, f, indent=4)

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def delete_book(self, title):
        self.books = [b for b in self.books if b['title'].lower() != title.lower()]
        self.save_books()

    def update_book(self, old_title, new_data):
        for book in self.books:
            if book['title'].lower() == old_title.lower():
                book.update(new_data)
        self.save_books()

    def find_books(self, query):
        return [b for b in self.books if query.lower() in b['title'].lower() or query.lower() in b['author'].lower()]

    def get_progress(self):
        total = len(self.books)
        read = sum(1 for b in self.books if b['read'])
        return total, read, (read / total * 100 if total else 0)

    def export_books(self):
        return json.dumps(self.books, indent=4)

    def import_books(self, uploaded_file):
        try:
            books = json.load(uploaded_file)
            if isinstance(books, list):
                self.books.extend(books)
                self.save_books()
                return True
            return False
        except:
            return False


# ---------- App Logic ----------
manager = BookManager()

with st.sidebar:
    selected = option_menu("💘 Library Manager", [
        "Add Book", "View Books", "Search", "Reading Progress", "Update Book", "Delete Book", "Export", "Import"
    ], icons=["plus", "book", "search", "bar-chart", "pencil", "trash", "cloud-download", "cloud-upload"], default_index=0)

st.title("📚 Personal Library Manager")

if selected == "Add Book":
    st.header("➕ Add New Book")
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Read")
        submit = st.form_submit_button("Add Book")
        if submit:
            if title.strip() and author.strip():
                manager.add_book({"title": title, "author": author, "year": year, "genre": genre, "read": read})
                st.success("Book added!")
            else:
                st.error("Title and Author are required.")

elif selected == "View Books":
    st.header("📚 Book Collection")
    if not manager.books:
        st.info("No books in collection.")
    else:
        for book in manager.books:
            st.markdown(f"""
            <div class='book-card' style="
                background: linear-gradient(135deg, #9d50bb, #6e48aa);
                padding: 1em;
                margin-bottom: 12px;
                border-radius: 12px;
                color: #fff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                transition: transform 0.3s ease;
            ">
                <h4>{book['title']}</h4>
                <p><b>Author:</b> {book['author']} | <b>Year:</b> {book['year']} | <b>Genre:</b> {book['genre']}</p>
                <p>Status: {'✅ Read' if book['read'] else '📖 Unread'}</p>
            </div>
            """, unsafe_allow_html=True)

elif selected == "Search":
    st.header("🔍 Search Books")
    query = st.text_input("Enter title or author")
    if query:
        results = manager.find_books(query)
        if results:
            for book in results:
                st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No books found.")

elif selected == "Reading Progress":
    st.header("📈 Reading Progress")
    total, read, percent = manager.get_progress()
    st.metric("Total Books", total)
    st.metric("Books Read", read)
    st.progress(percent / 100)

elif selected == "Update Book":
    st.header("✏️ Update Book")
    titles = [b['title'] for b in manager.books]
    if titles:
        selected_title = st.selectbox("Select a book to update", titles)
        book = next((b for b in manager.books if b['title'] == selected_title), None)
        if book:
            title = st.text_input("Title", value=book['title'])
            author = st.text_input("Author", value=book['author'])
            year = st.text_input("Year", value=book['year'])
            genre = st.text_input("Genre", value=book['genre'])
            read = st.checkbox("Read", value=book['read'])
            if st.button("Update"):
                manager.update_book(selected_title, {"title": title, "author": author, "year": year, "genre": genre, "read": read})
                st.success("Book updated!")
    else:
        st.info("No books to update.")

elif selected == "Delete Book":
    st.header("❌ Delete Book")
    titles = [b['title'] for b in manager.books]
    if titles:
        book_to_delete = st.selectbox("Select book to delete", titles)
        if st.button("Delete"):
            manager.delete_book(book_to_delete)
            st.success(f"Deleted: {book_to_delete}")
    else:
        st.info("No books to delete.")

elif selected == "Export":
    st.header("📄 Export Book List")
    exported_data = manager.export_books()
    st.download_button("Download JSON", data=exported_data, file_name="exported_books.json", mime="application/json")

elif selected == "Import":
    st.header("📅 Import Book List")
    uploaded = st.file_uploader("Upload a JSON file", type="json")
    if uploaded and manager.import_books(uploaded):
        st.success("Books imported successfully!")
    elif uploaded:
        st.error("Invalid file format.")
