

from modules.creator import Creator
from modules.render import Render_post
from modules.userlogin import UserLogin


class Post():

    def __init__(self, id, creator_id, tags, text):
        self.id = id
        self.creator_id = creator_id
        self.tags = tags
        self.text = text