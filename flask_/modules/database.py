
from modules.post import Post
from modules.creator import Creator
from modules.render import Render_post
from modules.userlogin import UserLogin

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