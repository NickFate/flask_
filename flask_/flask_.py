
from flask import Flask, render_template, url_for

from config import setting




class Post():

    def __init__(self, id, creator_id, *tags):
        self.id = id
        self.creator_id = creator_id
        self.tags = tags


post = [Post(i, "Fate") for i in range(5)]

# human.csv
# data.csv
#
#
#
# person {
# name
# date
# email
# password
# id
# }

data = open("static/data/data.csv")
for i in 


app = Flask(__name__)

@app.route('/main')
def main_page():
    return render_template("main_page.html", title=setting["site-name"], posts=range(1, 3))


@app.route('/index/<int:page>')
def index(page):
    print(post[page * 2:(page + 1) * 2])
    return render_template("main_page.html", title=setting["site-name"], posts=post[page * 10:(page + 1) * 10], next_page=page + 1)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
