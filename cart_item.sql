-- Insert data into Book table
INSERT INTO Book (BookName, Author_ID, Publisher_ID, Description, Language, Category, Price, Inventory) VALUES
    ('Book 1', 1, 1, 'Description 1', 'English', 'Fiction', 19.99, 10),
    ('Book 2', 2, 2, 'Description 2', 'English', 'Non-Fiction', 29.99, 5),
    ('Book 3', 3, 3, 'Description 3', 'Spanish', 'Fiction', 24.99, 8);

-- Insert data into Member table
INSERT INTO Member (Account, Password, Name, Birth, Email) VALUES
    ('user1', 'password1', 'John Doe', '1990-01-01', 'john@example.com'),
    ('user2', 'password2', 'Jane Smith', '1995-02-15', 'jane@example.com'),
    ('user3', 'password3', 'Mike Johnson', '1988-09-20', 'mike@example.com');

-- Insert data into CartItems table
INSERT INTO CartItems (UserID, Title, Quantity) VALUES
    ('user1', 'Book 1', 2),
    ('user1', 'Book 2', 1),
    ('user2', 'Book 2', 3),
    ('user3', 'Book 3', 1);

