import mysql.connector

# Create a new MySQL connection
database = mysql.connector.connect(
  host = "127.0.0.1",
  user = "yueh",
  password = "oslab"
)

# Create a new cursor
cursor = database.cursor()

# Use the new database
cursor.execute("USE BookStore_DB")

# Create tables
tables = [
sql_commands = [
    """
    INSERT INTO Author (Name)
    VALUES 
    ('J.K. Rowling'),
    ('George R.R. Martin'),
    ('J.R.R. Tolkien');
    """,
    
    """
    INSERT INTO Publisher (Name)
    VALUES 
    ('Bloomsbury Publishing'),
    ('Bantam Books'),
    ('HarperCollins');
    """,
    
    """
    INSERT INTO Book (BookName, Author_ID, Publisher_ID, Description, Language, Category, Price, Inventory)
    VALUES 
    ('Harry Potter', 1, 1, 'Description of the book', 'english', 'fantastic', 19.99, 10),
    ('Game of Thrones', 2, 2, 'Description of the book', 'english', 'fantastic', 24.99, 8),
    ('The Lord of the Rings', 3, 3, 'Description of the book', 'english', 'fantastic', 29.99, 5);
    """,
    
    """
    INSERT INTO Member (Account, Password, Name, Birth, Email)
    VALUES 
    ('user1', 'password1', 'John Doe', '1980-01-01', 'johndoe@example.com'),
    ('user2', 'password2', 'Jane Doe', '1985-02-02', 'janedoe@example.com');
    """,
    
    """
    INSERT INTO CartItems (UserID, Title, Quantity)
    VALUES 
    ('user1', 'Harry Potter', 1),
    ('user2', 'The Lord of the Rings', 2);
    """,
    
    """
    INSERT INTO Orders (UserID, OrderDate, Recipient, Address)
    VALUES 
    ('user1', '2023-01-12', 'John Doe', '123 Main St, City, Country'),
    ('user2', '2023-02-23', 'Jane Doe', '456 Maple Ave, City, Country');
    """,
    
    """
    INSERT INTO OrderItems (OrderID, Title, Quantity, Price)
    VALUES 
    (1, 'Harry Potter', 1, 19.99),
    (2, 'The Lord of the Rings', 2, 29.99);
    """
]
]
i=0
for table in tables:
    cursor.execute(table)
    database.commit()
