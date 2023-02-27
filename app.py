
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Set up the database connection
conn = sqlite3.connect('shoes.db', check_same_thread=False)
c = conn.cursor()

# Create a new database table for storing shoe details
c.execute('''CREATE TABLE IF NOT EXISTS shoes
             (name TEXT, image_url TEXT, price REAL)''')














if __name__ == '__main__':
    app.run()
