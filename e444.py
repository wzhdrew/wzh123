from sqlalchemy import create_engine, Column, String, ForeignKey, Date, Enum
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
import enum
import os

os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'


Base = declarative_base()
engine = create_engine('sqlite:///library.db')

class BookStatus(enum.Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"

class Book(Base):
    __tablename__ = 'books'
    
    BookID = Column(String, primary_key=True)
    Title = Column(String)
    Author = Column(String)
    ISBN = Column(String)
    Status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE)
    reservations = relationship("Reservation", back_populates="book")

class User(Base):
    __tablename__ = 'users'
    
    UserID = Column(String, primary_key=True)
    Name = Column(String)
    Email = Column(String)
    reservations = relationship("Reservation", back_populates="user")

class Reservation(Base):
    __tablename__ = 'reservations'
    
    ReservationID = Column(String, primary_key=True)
    BookID = Column(String, ForeignKey('books.BookID'))
    UserID = Column(String, ForeignKey('users.UserID'))
    ReservationDate = Column(Date, default=datetime.date.today)
    book = relationship("Book", back_populates="reservations")
    user = relationship("User", back_populates="reservations")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def prompt(message: str) -> str:
    return input(message + ": ")

def execute_with_session(func):
    def wrapper(*args, **kwargs):
        with Session() as session:
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                print(f"Error: {e}")
    return wrapper

@execute_with_session
def add_book(session):
    book = Book(
        BookID=prompt("Please enter BookID"),
        Title=prompt("Please enter the title"),
        Author=prompt("Please enter author"),
        ISBN=prompt("Please enter ISBN"),
        Status=prompt("Please enter the status (available or reserved)")
    )
    session.add(book)

@execute_with_session
def find_book_by_id(session):
    book_id = prompt("Please enter BookID")
    book = session.query(Book).filter_by(BookID=book_id).first()
    if book:
        print(vars(book))
    else:
        print("Book not found!")

@execute_with_session
def find_all_books(session):
    for book in session.query(Book).all():
        print(vars(book))

@execute_with_session
def update_book(session):
    book_id = prompt("Please enter BookID")
    book = session.query(Book).filter_by(BookID=book_id).first()
    if not book:
        print("Book not found!")
        return

    updates = {
        'Title': prompt("Please enter a new title or leave it blank"),
        'Author': prompt("Please enter a new author or leave blank"),
        'ISBN': prompt("Please enter a new ISBN or leave it blank"),
        'Status': prompt("Please enter a new status or leave it blank (available or reserved)")
    }

    for key, value in updates.items():
        if value:
            setattr(book, key, value)

@execute_with_session
def delete_book(session):
    book_id = prompt("Please enter BookID")
    book = session.query(Book).filter_by(BookID=book_id).first()
    if book:
        session.delete(book)
    else:
        print("Book not found!")

def main():
    ACTIONS = {
        '1': add_book,
        '2': find_book_by_id,
        '3': find_all_books,
        '4': update_book,
        '5': delete_book
    }

    while True:
        choice = input('''
        Please select an action:
        1. Add new book
        2. Find book details based on BookID
        3. Find all books
        4. Update the book details
        5. Delete book
        6. Quit
        ''')
        
        if choice == '6':
            break

        action = ACTIONS.get(choice)
        if action:
            action()

if __name__ == "__main__":
    main()
