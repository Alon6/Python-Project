from flask import Flask, request
import json

# Initialize server and data structures

books = []
authors = dict()
id_title_map = dict()
title_author_map = dict()
app = Flask(__name__)
# Function gets new books in json format and updates the structures accordingly
@app.route('/addBooks', methods=['POST'])
def addBooks():
    books_json = request.get_json()
    for book in books_json['newBooks']:
        id = len(books) + 1
        books.append((id, book['bookTitle'], book['AuthorName']))
        if book['AuthorName'] not in authors:
            authors[book['AuthorName']] = set()
        authors[book['AuthorName']].add(id)
        print("adding " + str(id) + " to " + book['AuthorName'])
        id_title_map[id] = book['bookTitle']
        title_author_map[book['bookTitle']] = book['AuthorName']
    return "success"


@app.route('/searchBookByAuthor')
# Function gets an author name and returns all of his book's names
def searchBookByAuthor():
    name = request.args.get('author')
    book_titles = []
    if name in authors:
        for id in authors[name]:
            print(id)
            book_titles.append(id_title_map[id])
    else:
        return "error invalid input"
    return book_titles


# Function gets a book name and returns the name of its author
@app.route('/searchAuthorByBook')
def searchAuthorByBook():
    title = request.args.get('title')
    if title in title_author_map:
        return title_author_map[title]
    return "error invalid input"


# Function returns library representation in json format
@app.route('/library')
def getLibrary():
    library = dict()
    library['library'] = dict()
    for author in authors:
        book_list = []
        for id in authors[author]:
            book_dict = dict()
            book_dict["bookID"] = id
            book_dict["bookTitle"] = id_title_map[id]
            book_list.append(book_dict)
        library['library'][author] = book_list
    return json.dumps(library)
if __name__ == "__main__":
    app.run()