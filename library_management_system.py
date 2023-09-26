import sqlite3
import random
class LibraryManagementSystem:

    def __init__(self):
        # Connect to the SQLite database
        self.conn = sqlite3.connect('library_management_system.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_sample_books()

    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        # Create the Books table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                                BookID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Title TEXT,
                                Author TEXT,
                                ISBN TEXT,
                                Status TEXT)''')

        # Create the Users table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                                UserID TEXT PRIMARY KEY,
                                Name TEXT,
                                Email TEXT)''')

        # Create the Reservations table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                                ReservationID TEXT PRIMARY KEY,
                                BookID INTEGER,
                                UserID TEXT,
                                ReservationDate TEXT,
                                FOREIGN KEY (BookID) REFERENCES Books(BookID),
                                FOREIGN KEY (UserID) REFERENCES Users(UserID))''')

        self.conn.commit()

    def insert_sample_books(self):
        """Insert sample books into the Books table."""
        # Generate sample book data for insertion
        n = 50
        titles = ["Book Title {}".format(i) for i in range(n)]
        authors = ["Author {}".format(random.randint(1, 20)) for _ in range(n)]
        isbns = ["9780{}".format(str(i).zfill(7)) for i in range(n)]
        statuses = ["Available" for _ in range(n)]
        sample_books = list(zip(titles, authors, isbns, statuses))

        # Insert into the database
        self.cursor.executemany('''INSERT INTO Books (Title, Author, ISBN, Status)
                                   VALUES (?, ?, ?, ?)''', sample_books)
        self.conn.commit()

    def add_new_book(self, book_details):
        """Add a new book to the database."""
        try:
            self.cursor.execute('''INSERT INTO Books (Title, Author, ISBN, Status)
                                   VALUES (?, ?, ?, ?)''', book_details)
            self.conn.commit()
            return "Book added successfully!"
        except sqlite3.IntegrityError:
            return "A book with the given BookID already exists."

    def find_book_detail(self, book_id):
        """Find a book's detail based on BookID."""
        query = '''SELECT Books.BookID, Title, Author, ISBN, Status, Users.UserID, Name, Email, ReservationDate
                   FROM Books
                   LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                   LEFT JOIN Users ON Reservations.UserID = Users.UserID
                   WHERE Books.BookID = ?'''
        self.cursor.execute(query, (book_id,))
        result = self.cursor.fetchone()
        return result if result else "Book not found."

    def find_reservation_status(self, identifier):
        """Find a book's reservation status based on various identifiers."""
        if identifier.startswith("LB"):  # BookID
            query = '''SELECT Books.BookID, Title, Status, Users.UserID, Name, Email, ReservationDate
                       FROM Books
                       LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                       LEFT JOIN Users ON Reservations.UserID = Users.UserID
                       WHERE Books.BookID = ?'''
            self.cursor.execute(query, (identifier,))
        elif identifier.startswith("LU"):  # UserID
            query = '''SELECT Books.BookID, Title, Status, Users.UserID, Name, Email, ReservationDate
                       FROM Users
                       LEFT JOIN Reservations ON Users.UserID = Reservations.UserID
                       LEFT JOIN Books ON Reservations.BookID = Books.BookID
                       WHERE Users.UserID = ?'''
            self.cursor.execute(query, (identifier,))
        elif identifier.startswith("LR"):  # ReservationID
            query = '''SELECT Books.BookID, Title, Status, Users.UserID, Name, Email, ReservationDate
                       FROM Reservations
                       LEFT JOIN Books ON Reservations.BookID = Books.BookID
                       LEFT JOIN Users ON Reservations.UserID = Users.UserID
                       WHERE Reservations.ReservationID = ?'''
            self.cursor.execute(query, (identifier,))
        else:  # Assume it's a Title
            query = '''SELECT Books.BookID, Title, Status, Users.UserID, Name, Email, ReservationDate
                       FROM Books
                       LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                       LEFT JOIN Users ON Reservations.UserID = Users.UserID
                       WHERE Title = ?'''
            self.cursor.execute(query, (identifier,))
        result = self.cursor.fetchone()
        return result if result else "Book or reservation not found."

    def find_all_books(self):
        """Find all the books in the database."""
        query = '''SELECT Books.BookID, Title, Author, ISBN, Status, Users.UserID, Name, Email, ReservationDate
                   FROM Books
                   LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                   LEFT JOIN Users ON Reservations.UserID = Users.UserID'''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results if results else "No books found."

    def modify_book_details(self, book_id, updated_details):
        """Modify/update book details based on BookID."""
        update_books_query = '''UPDATE Books SET Title=?, Author=?, ISBN=?, Status=?
                                WHERE BookID=?'''
        self.cursor.execute(update_books_query, (*updated_details, book_id))
        if updated_details[3] == "Available":
            delete_reservation_query = '''DELETE FROM Reservations WHERE BookID=?'''
            self.cursor.execute(delete_reservation_query, (book_id,))
        self.conn.commit()
        return f"Book details for {book_id} updated successfully!"

    def delete_book(self, book_id):
        """Delete a book based on its BookID."""
        self.cursor.execute('DELETE FROM Reservations WHERE BookID=?', (book_id,))
        self.cursor.execute('DELETE FROM Books WHERE BookID=?', (book_id,))
        self.conn.commit()
        return f"Book with BookID {book_id} deleted successfully!"

    def display_menu(self):
        """Display the menu options."""
        print("\nLibrary Management System")
        print("1. Add a new book.")
        print("2. Find a book's detail based on BookID.")
        print("3. Find a book's reservation status.")
        print("4. Find all the books in the database.")
        print("5. Modify/update book details.")
        print("6. Delete a book.")
        print("7. Exit.")
        return input("Enter your choice: ")

    def run(self):
        """Main loop for the program."""
        while True:
            choice = self.display_menu()
            if choice == "1":
                title = input("Enter the book title: ")
                author = input("Enter the book author: ")
                isbn = input("Enter the book ISBN: ")
                status = input("Enter the book status (Available/Reserved): ")
                print(self.add_new_book((title, author, isbn, status)))
            elif choice == "2":
                book_id = int(input("Enter the BookID: "))
                print(self.find_book_detail(book_id))
            elif choice == "3":
                identifier = input("Enter the identifier (BookID, UserID, ReservationID or Title): ")
                print(self.find_reservation_status(identifier))
            elif choice == "4":
                books = self.find
                #... continuation
                books = self.find_all_books()
                for book in books:
                    print(book)
            elif choice == "5":
                book_id = int(input("Enter the BookID for the book you want to modify: "))
                title = input("Enter the new book title: ")
                author = input("Enter the new book author: ")
                isbn = input("Enter the new book ISBN: ")
                status = input("Enter the new book status (Available/Reserved): ")
                print(self.modify_book_details(book_id, (title, author, isbn, status)))
            elif choice == "6":
                book_id = int(input("Enter the BookID for the book you want to delete: "))
                print(self.delete_book(book_id))
            elif choice == "7":
                print("Exiting the system. Goodbye!")
                self.conn.close()
                break

# Run the program
if __name__ == "__main__":
    lms = LibraryManagementSystem()
    lms.run()
