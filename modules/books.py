# modules/books.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Book
from . import db

books_bp = Blueprint('books', __name__)

@books_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        user_id = session.get('user_id', None)
        new_book = Book(title=title, author=author, description=description, user_id=user_id)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('books.library'))

    return render_template('ab.html')

@books_bp.route('/ab')
def add_book():
    return render_template('ab.html')

@books_bp.route('/library')
def library():
    books = Book.query.all()
    return render_template('library.html', books=books)
