
from config import setting

from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, login_user, login_required, current_user


class db():

    def __init__(self, creator_data, post_data):
        creator = open(creator_data).readlines()
        self.creators_data = [Creator(i[0], i[1], i[2], i[3]) 
                              for i in list(map(lambda x: x.strip().split(";"),
                                               creator))]
        data = open(post_data).readlines()
        self.posts_data = [Post(i[0], i[1], i[2])
                          for i in list(map(lambda x: x.strip().split(";"), 
                                            data))]

    def update_posts(self, posts):
        self.posts_data = posts

    def update_creators(self, creators):
        self.creators_data = creators

    def creator_id(self, username):
        for user in self.creators_data:
            if user.name == username:
                return user.id


class Post():

    def __init__(self, id, creator_id, *tags):
        self.id = id
        self.creator_id = creator_id
        self.tags = tags


class Creator():

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name


class Render_post():

    def __init__(self, image, creator, tags):
        self.image = image
        self.creator = creator
        self.tags = tags

db = db("static/data/creators.csv", "static/data/data.csv")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

# Работа с Авторизициями
login_manager = LoginManager(app)




class UserLogin():

    def from_db(self, user_id, creators_db):
        self.__user = creators_db[int(user_id)]
        self.id = user_id
        return self
 
    def create(self, user):
        self.id = user
        self.__user = user
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    # print("load_user")
    return UserLogin().from_db(user_id, db.creators_data)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = db.creator_id(request.form['username'])
        userlogin = UserLogin().create(user)
        login_user(userlogin)
        return redirect(url_for('index', page=0))
 
        flash("Неверная пара логин/пароль", "error")
 
    return render_template("login.html", title="Авторизация")




# @login_required


@app.route('/main')
@login_required
def main_page():
    return render_template("main_page.html", title=setting["site-name"], posts=range(1, 3), page=0)



@app.route('/index/<int:page>')
def index(page):
    if current_user.is_authenticated:
        user = str(current_user.id)
        print(user)
    render = [Render_post(i.id, db.creators_data[int(i.creator_id)].name, i.tags) for i in db.posts_data[page * 10:(page + 1) * 10]]
    return render_template("main_page.html", title=setting["site-name"], posts=render, page=page)


@app.route('/post/<int:id>')
def post_page(id):
    _post = db.posts_data[id]
    render = Render_post(_post.id, db.creators_data[int(_post.creator_id)].name, _post.tags)
    return render_template("post.html", title=setting["site-name"], post=render)


@app.route('/new_post')
def load_post():
    if current_user.is_authenticated:
        pass
    else:
        return redirect("login")
    return render_template("new_post.html")




#@app.route('/login', methods=['post', 'get'])
#def login_page():
#    if request.method == "POST":

#        print(request.form.get("username"))
#        pass
#    return render_template("login.html", title="Авторицазия")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
