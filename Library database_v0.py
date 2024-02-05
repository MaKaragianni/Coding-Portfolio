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

    def register_user(self):
        name = input("What's your name? ")
        last_name = input("What's your last name? ")
        phone_number = input(int("What's your phone number? "))
        address = input("Please provide your address: ")
        email = input("Please provide your email address: ")

        self.cursor.execute('INSERT INTO Users (name, last_name, phone_number, address, email) VALUES (?, ?, ?, ?, ?)', (name, last_name, phone_number, address, email))
        self.conn.commit()
        return self.cursor.lastrowid

    def display_books(self):
        self.cursor.execute('SELECT id, title FROM Books')
        books = self.cursor.fetchall()
        for idx, book in enumerate(books, start=1):
            print(f"{idx}. {book[1]}")
        return books

    def borrow_book(self, user_id):
        books = self.display_books()
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

    def return_book(self, user_id):
        books = self.display_books()
        try:
            book_number = int(input("Enter the number of the book you are returning: ")) - 1
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return
        
        if 0 <= book_number < len(books):
            book_id = books[book_number][0]
            self.cursor.execute('''SELECT id, return_date FROM BorrowedBooks WHERE user_id = ? AND book_id = ? AND returned = 'N' ''', (user_id, book_id))
            borrowed_book = self.cursor.fetchone()

            if borrowed_book:
                borrowed_book_id, return_date = borrowed_book
                return_date = datetime.strptime(return_date, '%Y-%m-%d')
                current_date = datetime.now()
                late_days = (current_date - return_date).days
                late_fee = max(0, late_days * 1)  # Assuming $1 per day late fee
                self.cursor.execute('UPDATE BorrowedBooks SET returned = \'Y\' WHERE id = ?', (borrowed_book_id,))
                self.conn.commit()
                print(f"Book returned. Late fee: ${late_fee}")
            else:
                print("No such borrowed book found or it has already been returned.")
        else:
            print("Invalid book number. Please try again.")

if __name__ == "__main__":
    lib_system = EnhancedLibrarySystem()

    # User registration
    user_id = lib_system.register_user()
    print(f"Registered successfully. Your user ID is {user_id}.")

    # Ask the user if they want to borrow or return a book
    choice = input("Do you want to borrow or return a book? (borrow/return): ").lower()
    if choice == 'borrow':
        lib_system.borrow_book(user_id)
    elif choice == 'return':
        lib_system.return_book(user_id)
    else:
        print("Invalid choice. Please enter 'borrow' or 'return'.")
