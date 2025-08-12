from flask import Flask, request

#Flask class instance
app = Flask(__usersDb__)

#route to add user
@app.route('/add_user', methods = ['POST'])
def add_user():
    # Get username and email from email from incoming request 
    new_usernames = request.json.get ('username')
    me_email = request.json.get('email')

    #Connect to  database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    #use a parameterized query to prevent    
    cursor.execute('INSERT INTO users (username, email)') VALUES (?,?)', (new_username, new_email))
                
    conn.commit()
    conn.close()

    return f"User {new_username} added successfully"
