import flask
from flask import Flask, render_template, request, redirect, url_for, abort, session
from sqlalchemy import create_engine, text
from random import randint

app = Flask(__name__)
conn_str = 'mysql://root:Cookiebear1@localhost/180final'
engine = create_engine(conn_str, echo = True)
conn = engine.connect()
app.secret_key = 'secret key'

# USER PANEL
# Home page
@app.route('/')
def homepage():
    return render_template('base.html')

# Login & logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = conn.execute(text("SELECT * FROM users WHERE username = :username AND password = :password"), request.form)
        user_data = account.fetchone()
        if not account:
            toBeR = conn.execute(text("Select username from  where username = :username "), {'username': user_data[0]})
            toBeUse = toBeR.fetchone()
            if username == toBeUse[0] and password == toBeUse[6]:
                session['loggedin'] = True
                session['Username'] = toBeUse[0]
                session["Name"] = f"{toBeUse[1]} {toBeUse[2]}"
                session["WaitingForApproval"] = True
                return redirect(url_for('wait'))
        elif account:
            if username == user_data[0] == "Admin":
                session['loggedin'] = True
                session['Username'] = "Admin"
                return redirect(url_for('admin_home'))
            elif username == user_data[0] and password == user_data[6]:
                session['loggedin'] = True
                session['Username'] = user_data[0]
                session["Name"] = f"{user_data[1]} {user_data[2]}"
                msg = 'Login success!'
                return redirect(url_for('index'))
            else:
                msg = 'Wrong username or password'



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('homepage'))

@app.route('/accounts_page')
def accounts_page():
    if 'username' in session:
        return render_template('accounts_page.html')
    else:
        return redirect(url_for('login'))


@app.route('/create_acc', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first = request.form.get('first')
        last = request.form.get('last')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        conn.execute(text(
            'INSERT INTO account (first, last, username, password, email) VALUES (:first, :last, :username, :password, :email)'),
                     {'first': first, 'last': last, 'username': username, 'password': password , 'email': email})
        conn.commit()
        return render_template("create_acc.html")
    else:
        return render_template('create_acc.html')

@app.route('/')
def home():
    return "Welcome to the homepage"

# @app.route('/my_account', methods=['GET'])
# def my_account():
#     user = session.get('user')
#     if user is None:
#         return redirect(url_for('login'))

#     account_info = conn.execute(text("SELECT * FROM accounts WHERE accountID = :accountID LIMIT 1"), {'user_id': user[0], 'accountID':  }).fetchone()
#     return render_template('my_account.html', info_type=account_info)

# @app.route('/my_account', methods=['GET', 'POST'])
# def my_account():
#     if request.method == 'GET':
#         all_accounts = conn.execute(text("SELECT * FROM accounts")).fetchone()
#         return render_template('my_account.html', info_type = all_accounts)
#     elif request.method == 'POST':
#         x = request.form['type']
#         account_info = conn.execute(text("SELECT * FROM accounts WHERE  = :type LIMIT 1"), {'type': x}).fetchone()
#         return render_template('my_account.html', info_type=account_info)
    
    
# @app.route('/deposit_money', methods=['GET', 'POST'])
# def send_money():
#     if request.method == "POST":
#         amounted = float(request.form['amount'])
#         account_num = int(request.form['accountNum'])
#         conn.execute(text(f'UPDATE accounts SET balance = balance + {amounted} where bank_number = {account_num}'),  {"amounted": amounted, "account_num": account_num} )
#         conn.commit()
#         return redirect("/deposit_money")
#     else:
#         return render_template("deposit_money.html")

# @app.route('/transfer', methods=['GET', 'POST'])
# def transfer_money():
#     if request.method == 'POST':
#         amount = float(request.form['amount'])
#         sender_bank_number = request.form['sender_bank_number']
#         receiver_bank_number = request.form['receiver_bank_number']
#         conn.execute(text("UPDATE accounts SET balance = balance - :amount WHERE bank_number = :bank_number"), {'amount': amount, 'bank_number': sender_bank_number})
#         conn.execute(text("UPDATE accounts SET balance = balance + :amount WHERE bank_number = :bank_number"), {'amount': amount, 'bank_number': receiver_bank_number})
#         conn.commit()
#         return render_template("transfer.html", message="Transfer successful")
#     else:
#         return render_template("transfer.html", message="Transfer failed! Make sure account numbers are correct.")
    
# # ADMIN PANEL
# # View pending accounts
# @app.route('/admin_dashboard', methods=['GET', 'POST'])
# def if_admin():
#     accounts = conn.execute(text('select * from pending_accounts')).all()
#     return render_template('admin_dashboard', account_info=accounts)


# @app.route('/accounts_page', methods=['GET', 'POST'])
# def account():
#     if request.method == 'GET':
#         all_accounts = conn.execute(text("SELECT * FROM accounts")).fetchall()
#         return render_template('accounts_page.html', info_type = all_accounts)
#     elif request.method == 'POST':
#         x = request.form['type']
#         account_info = conn.execute(text("SELECT * FROM accounts WHERE  = :type"), {'type': x}).fetchall()
#         return render_template('accounts_page.html', info_type=account_info)
    
# # Accept pending accounts
# @app.route('/accept', methods = ['GET', 'POST'])
# def accept():
#     if request.method == 'POST':
#         x = request.form['accept']
#         params = {"approval":'true', 'type' : x}
#         conn.execute(text(f"UPDATE accounts SET approved=:approval where accountID =  {x} ;"), params)
#         conn.commit()
#         bank_number = randint(0, 1000000000)
#         conn.execute(text("UPDATE accounts SET bank_number = :bank_number WHERE accountID = :account_id;"), {"bank_number": bank_number, "account_id": x})
#         conn.commit()
#         return redirect('/accounts_page')


if __name__ == '__main__':
    app.run(debug=True)