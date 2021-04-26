from modules.database import db
from modules.post import Post
from modules.creator import Creator
from modules.render import Render_post
from modules.userlogin import UserLogin


class Creator():

    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password