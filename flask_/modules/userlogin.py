from modules.database import db
from modules.post import Post
from modules.creator import Creator
from modules.render import Render_post
from modules.userlogin import UserLogin


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

