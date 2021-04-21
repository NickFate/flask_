

data = open("static/data/data.csv", "w")
data.write("")
data.close()
data = open("static/data/data.csv", "a")


class Post():

    def __init__(self, id, creator_id, *tags):
        self.id = id
        self.creator_id = creator_id
        self.tags = tags



post = [Post(i, 0) for i in range(4)]
post.append(Post(4, 0, "a", "b"))
for i in post:
    data.write(f"{i.id};{i.creator_id};{'#'.join(i.tags)}\n")