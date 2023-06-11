#coding=utf-8

import mysql.connector

# Create a new MySQL connection
database = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  password = "e"
)

# Create a new cursor
cursor = database.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS BookStore_DB CHARACTER SET utf8 COLLATE utf8_general_ci;")


# Use the new database
cursor.execute("USE BookStore_DB")

# Create tables
tables = [
    """
    CREATE TABLE Author (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE Publisher (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE Book (
        BookName VARCHAR(255) PRIMARY KEY,
        Author_ID INT,
        Publisher_ID INT,
        Description TEXT,
        Language VARCHAR(255),
        Category VARCHAR(255),
        Price DECIMAL(10,2),
        Inventory INT,
        FOREIGN KEY (Author_ID) REFERENCES Author(ID),
        FOREIGN KEY (Publisher_ID) REFERENCES Publisher(ID)
    )
    """,
    """
    CREATE TABLE Member (
        Account VARCHAR(255) PRIMARY KEY,
        Password VARCHAR(255),
        Name VARCHAR(255),
        Birth DATE,
        Email VARCHAR(255)
    )
    """,
    """
    CREATE TABLE CartItems (
    UserID varchar(255) NOT NULL,
    Title varchar(255) NOT NULL,
    Quantity int NOT NULL,
    PRIMARY KEY (UserID, Title),
    FOREIGN KEY (UserID) REFERENCES Member(Account),
    FOREIGN KEY (Title) REFERENCES Book(BookName)
    )
    """,
    """
    CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID varchar(255) NOT NULL,
    OrderDate date NOT NULL,
    Recipient varchar(255) NOT NULL,
    Address varchar(255) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Member(Account)
    )
    """,
    """
    CREATE TABLE OrderItems (
    OrderID INT NOT NULL,
    Title varchar(255) NOT NULL,
    Quantity int NOT NULL,
    Price decimal(8,2) NOT NULL,
    PRIMARY KEY (OrderID, Title),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (Title) REFERENCES Book(BookName)
    )
    """,
    """
    INSERT INTO Member (Name, Birth, Account, Password, Email)
    VALUES ('admin', '1980-01-01', 'admin', 'admin', 'oslab20230606@hotmail.com');
    """
]
i=0
for table in tables:
    cursor.execute(table)
database.commit()

cursor.execute('INSERT INTO Author (Name) VALUES (%s)', ("J.K. Rowling",))
database.commit()
cursor.execute('INSERT INTO Publisher (Name) VALUES (%s)', ("皇冠文化出版社",))


database.commit()


book_list = [
    ("Harry Potter and the Philosopher's Stone", "在哈利波特的十一歲生日時，他從一封信中發現了自己的魔法血統。他來到了霍格華茲魔法學校，並開始了關於魔法石的神秘冒險。","chinese", "fiction", 1, 1, 300.00, 100),
    ("Harry Potter and the Chamber of Secrets", "在哈利、榮恩和妙麗的探索下，霍格華茲學校的密室之謎逐漸揭示。他們必須用智慧和勇氣拯救學校免於古老威脅的侵害。","chinese", "fiction", 1, 1, 300.00, 100),
    ("Harry Potter and the Prisoner of Azkaban", "隨著小天狼星從阿茲卡班監獄的逃脫，霍格華茲學校的危險降臨。哈利必須深入自己的過去，並鼓起勇氣去面對等待他的黑暗真相。","chinese", "fiction", 1, 1, 300.00, 100),
    ("Harry Potter and the Goblet of Fire", "今年在霍格華茲，三所魔法學校的學生們將在充滿危險的三強爭霸賽中競爭。但當哈利的名字意外地從火盃中冒出，一個新的驚險篇章即將展開。","chinese", "fiction", 1, 1, 300.00, 100),
    ("Harry Potter and the Order of the Phoenix", "隨著魔法世界陷入混亂，哈利必須面對自己命運的真相。一個祕密組織，一場預言的夢，以及一所被圍攻的學校，賭注從未如此之高。","chinese", "fiction", 1, 1, 300.00, 100),
    ("Harry Potter and the Half-Blood Prince", "隨著佛地魔的力量增長，哈利揭示了屬於混血王子的神秘魔藥書中的黑暗秘密。同時，鄧布利多也在為哈利準備即將來臨的最後戰鬥。","chinese", "fiction", 1, 1, 300.00, 100),
    ("Harry Potter and the Deathly Hallows", "終章開始。哈利、羅恩和妙麗踏上危險的任務，去尋找並摧毀佛地魔永生的秘密。他們必須面對無數的挑戰，賭注從未如此之高。","chinese", "fiction", 1, 1, 300.00, 100)]


for book in book_list:
    query = "INSERT INTO Book (BookName, Description, Language, Category, Author_ID, Publisher_ID, Price,Inventory) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
    cursor.execute(query, book)
    database.commit()


cart_list = [
    ("admin", "Harry Potter and the Philosopher's Stone", 1),
    ("admin", "Harry Potter and the Chamber of Secrets", 1),
    ("admin", "Harry Potter and the Prisoner of Azkaban", 1),
    ("admin", "Harry Potter and the Goblet of Fire", 1),
    ("admin", "Harry Potter and the Order of the Phoenix", 1),
    ("admin", "Harry Potter and the Half-Blood Prince", 1),
    ("admin", "Harry Potter and the Deathly Hallows", 1)
]

for cart_item in cart_list:
    query = "INSERT INTO CartItems (UserID, Title, Quantity) VALUES (%s, %s, %s)"
    cursor.execute(query, cart_item)
    database.commit()


