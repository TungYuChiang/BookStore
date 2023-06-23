import mysql.connector

# Create a new MySQL connection
database = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  password = "IM880319"
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
#i=0
#for table in tables:
    #scursor.execute(table)
#database.commit()

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
    
    
insert_query=[
"""
INSERT INTO Author (Name)
VALUES ('Robert C. Martin'),  
       ('Erich Gamma'),       
       ('Michael Sipser'),    
       ('James F. Kurose'),   
       ('Thomas H. Cormen'), 
       ('Stuart Russell');    
""",
"""
INSERT INTO Publisher (Name)
VALUES ('Prentice Hall'),    
       ('Addison-Wesley'),   
       ('Cengage Learning'), 
       ('Pearson'),          
       ('The MIT Press'),    
       ('Pearson');          
""",
"""
INSERT INTO Book (BookName, Author_ID, Publisher_ID, Description, Language, Category, Price, Inventory)
VALUES 
('Clean Code: A Handbook of Agile Software Craftsmanship', 2, 2, 'Emphasizes the importance of writing clean code and provides guidelines for developers on how to write elegant and easily understandable code.', 'english', 'textbook', 900, 50),
('Design Patterns: Elements of Reusable Object-Oriented Software', 3, 3, 'Introduces 23 common design patterns to help developers understand how to achieve reusability and flexibility in object-oriented software design.', 'english', 'textbook', 950, 55),
('Introduction to the Theory of Computation', 4, 4, 'Provides a deep introduction to the theory of computation, including automata, formal languages, Turing machines, as well as complexity theory and NP-completeness.', 'english', 'textbook', 1000, 60),
('Computer Networking: A Top-Down Approach', 5, 5, 'Provides a comprehensive perspective to understand the core concepts of computer networking, from the application layer to the physical layer.', 'english', 'textbook', 1050, 65),
('Introduction to Algorithms', 6, 6, 'Thoroughly introduces major algorithms and data structures, and provides actual Python code implementations.', 'english', 'textbook', 1100, 70),
('Artificial Intelligence: A Modern Approach', 7, 5, 'A classic work in the field of artificial intelligence, covering comprehensive content from basic theory to latest developments, including search, game theory, machine learning, etc.', 'english', 'textbook', 1150, 75);
""",
"""
INSERT INTO Author (Name)
VALUES 
('Edward Felsenthal'),
('Susan Goldberg'),
('Zanny Minton Beddoes'),
('Randall Lane'),
('David Remnick'),
('Anna Wintour'),
('Laura Helmuth'),
('Gideon Lichfield');
""",
"""
INSERT INTO Publisher (Name)
VALUES 
('TIME USA, LLC'),
('National Geographic Partners'),
('The Economist Group'),
('Forbes Media LLC'),
('Condé Nast'),
('Springer Nature');
""",
"""
INSERT INTO Book (BookName, Author_ID, Publisher_ID, Description, Language, Category, Price, Inventory)
VALUES 
('TIME', 8, 7, 'An American weekly news magazine and news website', 'english', 'magazine', 300, 200),
('National Geographic', 9, 8, 'A monthly magazine known for its detailed reports and stunning photography', 'english', 'magazine', 350, 250),
('The Economist', 10, 9, 'An international weekly newspaper that focuses on current affairs, international business, politics, technology, and culture', 'english', 'magazine', 400, 300),
('Forbes', 11, 10, 'A business magazine known for its lists and rankings', 'english', 'magazine', 450, 350),
('The New Yorker', 12, 11, 'An American magazine featuring journalism, commentary, criticism, essays, fiction, satire, cartoons, and poetry', 'english', 'magazine', 500, 400),
('Vogue', 13, 11, 'A fashion and lifestyle magazine', 'english', 'magazine', 300, 200),
('Scientific American', 14, 12, 'A popular science magazine that features articles by scientists who write about their fields for the general public', 'english', 'magazine', 350, 250),
('Wired', 15, 11, 'A magazine that focuses on how emerging technologies affect culture, the economy, and politics', 'english', 'magazine', 400, 300);
""",
"""
INSERT INTO Author (Name)
VALUES 
('Jane Austen'),
('Emily Brontë'),
('William Shakespeare'),
('F. Scott Fitzgerald'),
('曹雪芹'),
('張愛玲'),
('張恨水'),
('桐華');
""",
"""
INSERT INTO Publisher (Name)
VALUES 
('Penguin Books'),
('Oxford University Press'),
('Scribner'),
('人民文學出版社'),
('花城出版社'),
('中國友誼出版公司'),
('長江文藝出版社');
""",
"""
INSERT INTO Book (BookName, Author_ID, Publisher_ID, Description, Language, Category, Price, Inventory)
VALUES 
('Pride and Prejudice', 16, 13, 'A romantic novel by Jane Austen about manners and marriage in early 19th-century England', 'english', 'romance', 300, 300),
('Wuthering Heights', 17, 13, 'A novel by Emily Brontë that explores love and revenge on the Yorkshire moors', 'english', 'romance', 350, 300),
('Romeo and Juliet', 18, 14, 'A tragic play by William Shakespeare about two young star-crossed lovers', 'english', 'romance', 400, 300),
('The Great Gatsby', 19, 15, 'A novel by F. Scott Fitzgerald that critiques the American dream in the Jazz Age', 'english', 'romance', 450, 300),
('紅樓夢', 20, 16, '曹雪芹的經典小說，描述了賈府中的愛情與失落', 'chinese', 'romance', 500, 300),
('紅玫瑰與白玫瑰', 21, 17, '張愛玲的中篇小說，描述了一名女子與兩兄弟之間的愛情三角關係', 'chinese', 'romance', 350, 300),
('鴛鴦蝴蝶', 22, 18, '張恨水的小說，講述了20世紀初北京的愛情與犧牲', 'chinese', 'romance', 400, 300),
('步步驚心', 23, 19, '桐華的小說，描述了一段發生在清朝的穿越時空的愛情故事', 'chinese', 'romance', 450, 300);
""",
"""
INSERT INTO Author (Name)
VALUES 
('井上井恵介'),
('岸本齋史'),
('冨樫義博'),
('久保帯人'),
('尾田榮一郎');
""","""
INSERT INTO Publisher (Name)
VALUES 
('集英社');
""",
"""
INSERT INTO Book (BookName, Author_ID, Publisher_ID, Description, Language, Category, Price, Inventory)
VALUES 
('灌籃高手', 24, 20, '一部描繪了籃球競技與青春成長的漫畫', 'chinese', 'comic', 300, 150),
('火影忍者', 25, 20, '描述了忍者世界的冒險與成長的漫畫', 'chinese', 'comic', 300, 150),
('通靈王', 26, 20, '描述了冒險與對抗惡魔的漫畫', 'chinese', 'comic', 300, 150),
('死神', 27, 20, '描述了死神世界的冒險與戰鬥的漫畫', 'chinese', 'comic', 300, 150),
('海賊王', 28, 20, '描述了冒險海洋尋找寶藏的歷程的漫畫', 'chinese', 'comic', 300, 150);
"""
]

for table in insert_query:
    cursor.execute(table)
    database.commit()
