#coding=utf-8
from flask import Flask, render_template, request, session, redirect, url_for,  jsonify
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '123456789'

# 建立與 MySQL 的連接
database = mysql.connector.connect(
  host = "127.0.0.1",
  user = "root",
  password = "e",
  database = "BookStore_DB" # 替換成你的資料庫名稱
)

UPLOAD_FOLDER = './static/uploads'  # 選擇一個適合您的路徑
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允許的檔案類型

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')

        cursor = database.cursor()
        query = "SELECT Account, Password FROM Member WHERE Account = %s"
        cursor.execute(query, (account,))
        user = cursor.fetchone()
        
        
        if user and user[1] == password:
            session['logged_in'] = True
            session['username'] = account
            return redirect(url_for('index'))
        else:
            return render_template('login.html') # 如果使用者名稱或密碼不正確，則畫面不動
    else:
        return render_template('login.html') # 如果是 GET 請求，則渲染登入頁面

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        account = request.form.get('account')
        password = request.form.get('password')
        email = request.form.get('email')
        birthdate = request.form.get('birthdate')

        cursor = database.cursor()
        query = "INSERT INTO Member (Name, Birth, Account, Password, Email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, birthdate, account, password, email))
        database.commit()

        return redirect(url_for('login')) # 如果註冊成功，將用戶重定向到登入頁面
    else:
        return render_template('register.html') # 如果是 GET 請求，則渲染註冊頁面

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        cursor = database.cursor()
        cursor.execute('SELECT SUM(Quantity) FROM CartItems WHERE UserID = %s', (session['username'],))
        try:
            cart_count = int(cursor.fetchone()[0])
        except:
            cart_count=0
        return render_template('index.html',cart_count=cart_count)
    return render_template('index.html')


@app.route('/bookByCategory')
def bookByCategory():
    category = request.args.get('category', '')#哪個類型的書
    #從上方的導覽列or下方選擇是哪種類型的書
    #SELECT * FROM Book WHERE Cateogory LIKE %s
    query = request.args.get('query', '')
    cursor = database.cursor()
    cursor.execute("SELECT * FROM Book WHERE Category LIKE %s", ('%' + category + '%',))
    
    books = cursor.fetchall()
    # 準備空的書本列表
    books_list = []
    # 處理每一本書
    for book in books:
        # 取得 Author_ID 和 Publisher_ID
        author_id = book[1]
        publisher_id = book[2]

        # 查找作者名
        cursor.execute("SELECT Name FROM Author WHERE ID = %s", (author_id,))
        author_name = cursor.fetchone()[0]

        # 查找出版商名
        cursor.execute("SELECT Name FROM Publisher WHERE ID = %s", (publisher_id,))
        publisher_name = cursor.fetchone()[0]

        # 組裝書本信息
        book_dict = {
            "BookName": book[0],
            "AuthorName": author_name,
            "PublisherName": publisher_name,
            "Description": book[3],
            "Language": book[4],
            "Category": book[5],
            "Price": book[6],
            "Inventory": book[7]
        }
        # 添加到書本列表
        books_list.append(book_dict)
        print(books_list[0])

    if 'logged_in' in session and session['logged_in']:
        cursor = database.cursor()
        cursor.execute('SELECT SUM(Quantity) FROM CartItems WHERE UserID = %s', (session['username'],))
        try:
            cart_count = int(cursor.fetchone()[0])
        except:
            cart_count = 0
    else:
        cart_count = 0
    address = category + '.html'
    print(address)
    return render_template(address, books = books_list, cart_count = cart_count)


@app.route('/search')
def search():
    category = request.args.get('category', '')#哪個類型的書
    #從上方的導覽列or下方選擇是哪種類型的書
    #SELECT * FROM Book WHERE Cateogory LIKE %s
    query = request.args.get('query', '')
    cursor = database.cursor()
    cursor.execute("SELECT * FROM Book WHERE Category LIKE %s", ('%' + category + '%',))
    
    books = cursor.fetchall()
    # 準備空的書本列表
    books_list = []
    # 處理每一本書
    for book in books:
        # 取得 Author_ID 和 Publisher_ID
        author_id = book[1]
        publisher_id = book[2]

        # 查找作者名
        cursor.execute("SELECT Name FROM Author WHERE ID = %s", (author_id,))
        author_name = cursor.fetchone()[0]

        # 查找出版商名
        cursor.execute("SELECT Name FROM Publisher WHERE ID = %s", (publisher_id,))
        publisher_name = cursor.fetchone()[0]

        # 組裝書本信息
        book_dict = {
            "BookName": book[0],
            "AuthorName": author_name,
            "PublisherName": publisher_name,
            "Description": book[3],
            "Language": book[4],
            "Category": book[5],
            "Price": book[6],
            "Inventory": book[7]
        }
        # 添加到書本列表
        books_list.append(book_dict)
        print(books_list[0])

    if 'logged_in' in session and session['logged_in']:
        cursor = database.cursor()
        cursor.execute('SELECT SUM(Quantity) FROM CartItems WHERE UserID = %s', (session['username'],))
        try:
            cart_count = int(cursor.fetchone()[0])
        except:
            cart_count = 0
    else:
        cart_count = 0
    return render_template('search.html', query=query, books=books_list,cart_count=cart_count)

@app.before_request
def before_request():
    if 'logged_in' in session and session['logged_in']:
        session['cart_total'] = sum(session.get('cart', {}).values())
    else:
        session['cart_total'] = 0

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json(force = True)
    book_name = data.get('book_name')
    quantity = data.get('quantity')
    cursor = database.cursor()

    sql = """
    INSERT INTO CartItems (UserID, Title, Quantity)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE Quantity = Quantity + VALUES(Quantity)
    """

    cursor.execute(sql, (session['username'], book_name, quantity))
    database.commit()

    cursor.execute('SELECT SUM(Quantity) FROM CartItems WHERE UserID = %s', (session['username'],))
    total_items = cursor.fetchone()
    
    return jsonify({'total_items': total_items})


@app.route('/manage')
def manage():
    return render_template('manage.html')

@app.route('/renew')
def renew():
    return render_template('renew.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        title = request.form.get('title')
        description = request.form.get('description')
        language = request.form.get('language')
        category = request.form.get('category')
        author_name = request.form.get('author')
        publisher_name = request.form.get('publisher')
        price = request.form.get('price')
        amount = request.form.get('amount')
        
        cursor = database.cursor()

        # 對於作者和出版商，先嘗試查詢
        cursor.execute('SELECT id FROM Author WHERE Name = %s', (author_name,))
        result = cursor.fetchone()
        if result:
            # 如果找到了結果，取得ID
            author_id = result[0]
        else:
            # 如果沒有找到結果，插入新的記錄並取得新插入記錄的ID
            cursor.execute('INSERT INTO Author (Name) VALUES (%s)', (author_name,))
            database.commit()
            cursor.execute('SELECT LAST_INSERT_ID()')
            author_id = cursor.fetchone()[0]

        cursor.execute('SELECT id FROM Publisher WHERE Name = %s', (publisher_name,))
        result = cursor.fetchone()
        if result:
            publisher_id = result[0]
        else:
            cursor.execute('INSERT INTO Publisher (Name) VALUES (%s)', (publisher_name,))
            database.commit()
            cursor.execute('SELECT LAST_INSERT_ID()')
            publisher_id = cursor.fetchone()[0]

        # 假設您的Book表有相應的欄位
        query = "INSERT INTO Book (BookName, Description, Language, Category, Author_ID, Publisher_ID, Price,Inventory) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        cursor.execute(query, (title, description, language, category, author_id, publisher_id, price,amount))
        database.commit()

        photo = request.files['file']
        
        # 檔案存在且格式允許，進行儲存
        if photo and allowed_file(photo.filename):
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], title+'.jpg'))


        return redirect(url_for('manage')) 
    else:
        return render_template('upload.html')
    
@app.route('/show_cart')
def show_cart():
    # 取出購物車中所有的商品
    cursor = database.cursor()
    if (session['username']):
        cursor.execute('SELECT * FROM CartItems WHERE UserID = %s', (session['username'],))
    total_items = cursor.fetchall()

    cart_items=[]

    for item in total_items:

        cursor.execute('SELECT Price FROM Book WHERE BookName = %s', (item[1],))
        price = int(cursor.fetchone()[0])

        cart_dict = {
            "name": item[1],
            "quantity": item[2],
            "price": price,
        }

        cart_items.append(cart_dict)


    # 計算總價
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    total_quantity = sum(item['quantity'] for item in cart_items)

    # 將購物車中的商品和總價傳遞給模板
    return render_template('cart.html', cart_items=cart_items, total_price=total_price,cart_count=total_quantity)
   
# delete the whole cart item
@app.route('/delete_cart_item', methods=['POST'])
def delete_cart_item():
    cursor = database.cursor()
    item_name = request.form.get('item_name')
    
    cursor.execute('DELETE FROM CartItems WHERE UserID = %s AND Title = %s', (session['username'], item_name))
    database.commit()
    
    return 'Cart item deleted successfully'


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    # 取得ajax請求中的資料
    item_name = request.form.get('item_name')
    quantity = int(request.form.get('quantity'))

    cursor = database.cursor()

    if quantity == 0:
        # 如果數量為0，從購物車中移除該商品
        cursor.execute('DELETE FROM CartItems WHERE UserID = %s AND Title = %s', (session['username'], item_name))
    else:
        # 更新購物車中商品的數量
        cursor.execute('UPDATE CartItems SET Quantity = %s WHERE UserID = %s AND Title = %s', (quantity, session['username'], item_name))
    
    database.commit()

    # 取得新的購物車資料
    cursor.execute('SELECT * FROM CartItems WHERE UserID = %s', (session['username'],))
    total_items = cursor.fetchall()
    print(total_items)

    cart_items = []

    for item in total_items:
        cursor.execute('SELECT Price FROM Book WHERE BookName = %s', (item[1],))
        price = int(cursor.fetchone()[0])

        cart_dict = {
            "name": item[1],
            "quantity": item[2],
            "price": price,
        }

        cart_items.append(cart_dict)

    # 計算新的總價和總數量
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    total_quantity = sum(item['quantity'] for item in cart_items)

    return jsonify({'success': True, 'total_price': total_price, 'total_quantity': total_quantity, 'cart_items': cart_items, 'quantity': quantity})

@app.route('/order_process', methods=['POST'])
def order_process():
    recipient = request.form.get('recipient')
    address = request.form.get('address')
    
    print(recipient)
    print(address)
    order_date = datetime.now()

    cursor = database.cursor()

    query = "INSERT INTO Orders (UserID, OrderDate, Recipient, Address) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (session['username'], order_date, recipient, address))
    database.commit()

    cursor.execute("SELECT MAX(OrderID) FROM Orders")
    order_id = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM CartItems WHERE UserID = %s",(session['username'],))
    results = cursor.fetchall()

    for result in results:
        cursor.execute("SELECT Price From Book WHERE BookName = %s",(result[1],))
        price=int(cursor.fetchone()[0])

        query = "INSERT INTO OrderItems (OrderID, Title, Quantity, Price) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (order_id, result[1], result[2], price))
        database.commit()

    cursor.execute('DELETE FROM CartItems WHERE UserID = %s',(session['username'],))
    database.commit()

    # 在這裡進行後續的訂單處理

    # return jsonify({'status': 'success', 'message': '訂單已收到'})
    return render_template('index.html')

  
@app.route('/member',methods=['GET'])
def member():
#    return render_template('tables-data.html')
    return render_template('member.html')

@app.route('/get_orders', methods=['POST'])
def get_orders():
    data = request.get_json()
    selected_option = data['selectedOption']
    cursor = database.cursor()

    orders = []

    if selected_option == "option1":
        query = f"""
        SELECT OrderID
        FROM Orders
        WHERE DATE(OrderDate) = CURDATE() AND UserID = %s
        """
        cursor.execute(query, (session['username'],))
        result = cursor.fetchall()

        for row in result:
            orders.append(row[0])
    else:
        query = f"""
        SELECT OrderID
        FROM Orders
        WHERE UserID = %s
        """
        cursor.execute(query, (session['username'],))
        result = cursor.fetchall()

        for row in result:
            orders.append(row[0])
    
    return jsonify({'orders': orders})

@app.route('/get_order_items',methods=['POST'])
def get_order_items():
    data = request.get_json()
    cursor = database.cursor()

    query = f"""
        SELECT Title,Quantity,Price
        FROM OrderItems
        WHERE OrderID = %s
        """
    cursor.execute(query, (data['orderID'],))
    result = cursor.fetchall()
    
    order_items=[]
    for item in result:
        order_items.append((item[0],item[1],item[2]))

    return jsonify({'order_items':order_items})

@app.route('/api/getImages', methods=['POST'])
def get_images():
    category = request.json['category']
    cursor = database.cursor()
    if category != 'all':
        query = f"""SELECT BookName, SUM(Quantity) AS TotalQuantity FROM Book 
                    JOIN OrderItems ON Book.BookName = OrderItems.Title 
                    WHERE  Category = %s 
                    GROUP BY  BookName 
                    ORDER BY  TotalQuantity DESC
                    LIMIT 5;"""
        cursor.execute(query, (category,))
    else:
        query = f"""SELECT BookName, SUM(Quantity) AS TotalQuantity FROM Book 
                    JOIN OrderItems ON Book.BookName = OrderItems.Title 
                    GROUP BY  BookName 
                    ORDER BY  TotalQuantity DESC
                    LIMIT 5;"""
        cursor.execute(query)
    result = cursor.fetchall()
    images = []
    for item in result:
        images.append(item[0])
        if len(images)==5:
            break
    return jsonify(images)





if __name__ == "__main__":
    app.run(debug=True, port=9874)
