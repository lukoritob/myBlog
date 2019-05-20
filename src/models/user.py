import datetime
import uuid

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password): # check whether a user's email matches the password they sent us #
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password # check the password
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            # user doesn't exists, so we have to create it
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email # only happens when the user logs in
            return True
        else:
            # user exists
            return False

    @staticmethod
    def login(user_email):
        # login has already been called when the session contains an email the user is logged in
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def new_blog(self, title, description):
        # author, title, description, author_id,
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        # title, content, date=datetime.datetime.utcnow()
        blog = Blog.from_mongo(blog_id) # return us a specific blog with an id from the database
        blog.new_post(title=title,
                      content=content,
                      date=date)

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def json(self):
        return {
            "email": self.email,
            "id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())