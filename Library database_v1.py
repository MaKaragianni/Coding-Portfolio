import sqlite3
from datetime import datetime, timedelta

class EnhancedLibrarySystem:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')  # In-memory database for demonstration
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        self.cursor.execute('''CREATE TABLE Users (id INTEGER PRIMARY KEY, name TEXT, last_name TEXT, phone_number TEXT, address TEXT, email TEXT)''')
        self.cursor.execute('''CREATE TABLE Books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT)''')
        self.cursor.execute('''CREATE TABLE BorrowedBooks (id INTEGER PRIMARY KEY, user_id INTEGER, book_id INTEGER, borrow_date TEXT, return_date TEXT, returned TEXT, FOREIGN KEY (user_id) REFERENCES Users (id), FOREIGN KEY (book_id) REFERENCES Books (id))''')

    def welcome_message(self):
        print("Hello, welcome to our library. Would you like to borrow or return a book?")
        user_id = self.get_or_register_user()
        choice = input("Type 'borrow' to borrow a book or 'return' to return a book: ").lower()
        if choice == 'borrow':
            self.process_borrow(user_id)
        elif choice == 'return':
            self.process_return(user_id)
        else:
            print("Invalid choice. Please type 'borrow' or 'return'.")

    def get_or_register_user(self):
        name = input("What's your name? ")
        last_name = input("What's your last name? ")
        # Check if the user already exists
        self.cursor.execute('SELECT id FROM Users WHERE name = ? AND last_name = ?', (name, last_name))
        user = self.cursor.fetchone()
        if user:
            print("You are already registered.")
            return user[0] # Return existing user ID
        else:
            # Continue with the registration process if the user is new
            phone_number = input("What's your phone number? ")
            address = input("Please provide your address: ")
            email = input("Please provide your email address: ")
            self.cursor.execute('INSERT INTO Users (name, last_name, phone_number, address, email) VALUES (?, ?, ?, ?, ?)', (name, last_name, phone_number, address, email))
            self.conn.commit()
        return self.cursor.lastrowid # Return new user ID
    
    def process_borrow(self, user_id):
        print("Available book to borrow: ")
        books = self.display_books() # Display available books
        try:
            book_number = int(input("Enter the number of the book you want to borrow: ")) - 1
            borrow_days = int(input("Enter the number of days you want to borrow the book for: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        if 0 <= book_number < len(books):
            book_id = books[book_number][0]
            borrow_date = datetime.now()
            return_date = borrow_date + timedelta(days=borrow_days)
            self.cursor.execute('INSERT INTO BorrowedBooks (user_id, book_id, borrow_date, return_date, returned) VALUES (?, ?, ?, ?, ?)', (user_id, book_id, borrow_date.strftime('%Y-%m-%d'), return_date.strftime('%Y-%m-%d'), 'N'))
            self.conn.commit()
            print(f"You have borrowed '{books[book_number][1]}' for {borrow_days} days.")
        else:
            print("Invalid book number. Please try again.")

    def process_return(self, user_id):
        # Prompt for user's name and last name
        name = input("What's your first name? ")
        last_name = input("What's your last name? ")
        self.return_book(name, last_name)

    def return_book(self, name, last_name):
        # Find user_id based on name and last name
        self.cursor.execute('SELECT id FROM Users WHERE name = ? AND last_name = ?', (name, last_name))
        user_info = self.cursor.fetchone()
        # if the user is found
        if user_info:
            user_id = user_info[0]
            # Continue with book return
        books = self.display_books()
        book_number = int(input("Enter the number of the book you are returning: ")) - 1
        if 0 <= book_number < len(books):
            book_id = books[book_number][0]
            self.cursor.execute('''SELECT id, return_date FROM BorrowedBooks WHERE user_id = ? AND book_id = ? AND returned = 'N' ''', (user_id, book_id))
            borrowed_book = self.cursor.fetchone()
            if borrowed_book:
                borrowed_book_id, return_date = borrowed_book
                current_date = datetime.now()
                return_date = datetime.strptime(return_date, '%Y-%m-%d')
                late_days = (current_date - return_date).days
                if late_days > 0:
                    late_fee = max(0, late_days * 1)  # Assuming $1 per day late fee
                    self.cursor.execute('UPDATE BorrowedBooks SET returned = \'Y\' WHERE id = ?', (borrowed_book_id,))
                    self.conn.commit()
                    print(f"Book returned. Late fee: ${late_fee}")
                else:
                    print("No such borrowed book found or it has already been returned.")
            else:
                print("Invalid book number. Please try again.")
        else:
            print("User not found. Please ensure your name and last name are entered correctly.")

    def display_books(self):
        self.cursor.execute('SELECT id, title FROM Books WHERE id NOT IN (SELECT book_id FROM BorrowedBooks WHERE returned = "N")')
        books = self.cursor.fetchall()
        for index, book in enumerate(books, start=1):
            print(f"{index}. {book[1]}")
        return books
    
    def display_borrowed_books(self, user_id):
        self.cursor.execute('SELECT id, book_id FROM BorrowedBooks WHERE user_id = ? AND returned = "N"', (user_id))
        borrowed_books = self.cursor.fetchall()
        for index, book in enumerate(borrowed_books, start=1):
            self.cursor.execute('SELECT title FROM Books WHERE id = ?', (book[1],))
            book_title = self.cursor.fetchone()[0]
            print(f"{index}. {book_title}")
        return borrowed_books

if __name__ == "__main__":
    lib_system = EnhancedLibrarySystem()
    lib_system.welcome_message()

    sample_books = [
        ("Pride and Prejudice", "Jane Austen", "1111111111"),
        ("1984", "George Orwell", "2222222222"),
        ("To Kill a Mockingbird", "Harper Lee", "3333333333"),
        ("The Great Gatsby", "F. Scott Fitzgerald", "4444444444"),
        ("One Hundred Years of Solitude", "Gabriel García Márquez", "5555555555"),
        ("In Search of Lost Time", "Marcel Proust", "6666666666"),
        ("Moby-Dick", "Herman Melville", "7777777777"),
        ("War and Peace", "Leo Tolstoy", "8888888888"),
        ("Hamlet", "William Shakespeare", "9999999999"),
        ("The Catcher in the Rye", "J.D. Salinger", "0000000000")
        ]
    self.cursor.executemany('INSERT INTO Books (title, author, isbn) VALUES (?, ?, ?)', sample_books)
    self.conn.commit()

    # User registration
    user_id = lib_system.process_borrow()
    print(f"Registered successfully. Your user ID is {user_id}.")
