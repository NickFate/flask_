
from config import setting



from flask import Flask, render_template, url_for, request, redirect
from flask_login import LoginManager, login_user, login_required, current_user


class Post():

    def __init__(self, id, creator_id, tags, text):
        self.id = id
        self.creator_id = creator_id
        self.tags = tags
        self.text = text

        
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


class Render_post():

    def __init__(self, image, creator, creator_id, tags, text):
        self.image = image
        self.creator = creator
        self.creator_id = creator_id
        self.tags = tags
        self.text = text

class Creator():

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password



class db():

    def __init__(self, creator_data, post_data):
        creator = open(creator_data).readlines()
        self.creators_data = [Creator(i[0], i[1], i[2]) 
                              for i in list(map(lambda x: x.strip().split(";"),
                                               creator))]
        data = open(post_data).readlines()
        self.posts_data = [Post(i[0], i[1], i[2], i[3])
                          for i in list(map(lambda x: x.strip().split(";"), 
                                            data))]

    def update_posts(self, post_data):
        data = open(post_data).readlines()
        self.posts_data = [Post(i[0], i[1], i[2], i[3])
                          for i in list(map(lambda x: x.strip().split(";"), 
                                            data))]

    def update_creators(self, creator_data):
        creator = open(creator_data).readlines()
        self.creators_data = [Creator(i[0], i[1], i[2]) 
                              for i in list(map(lambda x: x.strip().split(";"),
                                               creator))]

    def creator_id(self, username):
        for user in self.creators_data:
            if user.name == username:
                return user.id
        return False


def is_image(file):
    if file.split(".")[-1].lower() in ["png", "jpg"]:
        return True
    return False


def hash_password(password):
    return password


def check_password_hash(password, id):
    if hash_password(password) == db.creators_data[id].password:
        return "True"
    return False


posts_file = "static/data/data.csv"
creators_file = "static/data/creators.csv"
db = db(creators_file, posts_file)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

# Работа с Авторизициями
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    # print("load_user")
    return UserLogin().from_db(user_id, db.creators_data)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = db.creator_id(request.form['username'])
        password = request.form['password']
        if user:
            if check_password_hash(password, int(user)):
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                return redirect(url_for('index', page=0))
            else:
                return render_template("login.html", title="Авторизация", message="Не верный пароль")
        else:
            return render_template("login.html", title="Авторизация", message="Не существующий пользователь")
 
 
    return render_template("login.html", title="Авторизация", message="")


@app.route('/main')
@login_required
def main_page():
    return render_template("main_page.html", title=setting["site-name"], posts=range(1, 3), page=0)


@app.route('/index/<int:page>')
def index(page):
    if current_user.is_authenticated:
        user = str(current_user.id)
    render = [Render_post(i.id, db.creators_data[int(i.creator_id)].name, int(i.creator_id), ", ".join(i.tags.split("#")), i.text)
             for i in db.posts_data[page * 10:(page + 1) * 10]]
    return render_template("main_page.html", title=setting["site-name"], posts=render, page=page)


@app.route('/post/<int:id>')
def post_page(id):
    _post = db.posts_data[id]
    print(_post.tags[0].split("#"))
    render = Render_post(_post.id,
                        db.creators_data[int(_post.creator_id)].name, int(_post.creator_id), ", ".join(_post.tags[0].split("#")), _post.text)
    return render_template("post.html", title=setting["site-name"], post=render)


@app.route('/new_post', methods=["POST", "GET"])
def load_post():
    if not current_user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        
        post_id = len(db.posts_data)
        creator_id = current_user.id
        image = request.files["file"]
        tags = request.form["tags"] or ""
        text = request.form["text"] or ""
        if is_image(image.filename):
            image.save(f"static/data/img/{post_id}.png")
            f = open(posts_file, "a")
            f.write(f"\n{post_id};{creator_id};{tags};{text}")
            f.close()
            db.update_posts(posts_file)
            return redirect(url_for('index', page=0))


    return render_template("new_post.html")


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":
        user = db.creator_id(request.form['name'])
        password = request.form['password']
        s_password = request.form['s_password']
        if user:
           return render_template("register.html", title="Регистрация", message="Пользователь существует")
        else:
           user = request.form['name']
           if password != s_password:
               return render_template("register.html", title="Регистрация", message="Пароли не совпадают")
           else:
               id = len(db.creators_data)
               f = open(creators_file, "a")
               f.write(f"\n{id};{user};{password}")
               f.close()
               db.update_creators(creators_file)
               img = request.files["ava"]
               if img:
                   image.save(f"static/data/avatar/{id}.png")
               return redirect(url_for('index', page=0))
 
 
    return render_template("register.html", title="Регистрация", message="")

@app.route("/id/<int:id>")
def creator_page(id):
    return render_template("p_creator.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
