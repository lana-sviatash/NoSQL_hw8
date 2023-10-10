import json

from models import Author, Quote
# from connect import db


if __name__ == '__main__':
    with open("authors.json", "r", encoding="utf-8") as authors_file:
        authors_data = json.load(authors_file)

    with open("quotes.json", "r", encoding="utf-8") as quotes_file:
        quotes_data = json.load(quotes_file)

    for author_data in authors_data:
        author = Author(**author_data)
        # db.authors.insert_one(author_data)
        author.save()

    for quote_data in quotes_data:
        author_fullname = quote_data['author']
        author = Author.objects(fullname=author_fullname).first()

        del quote_data['author']

        quote = Quote(**quote_data, author=author)
        # db.quotes.insert_one(quote_data)
        quote.save()
