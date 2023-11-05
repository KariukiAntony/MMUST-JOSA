from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
          id = db.Column(db.Integer, primary_key = True, index=True)
          first_name = db.Column(db.String(20), nullable=False)
          last_name = db.Column(db.String(20), nullable=False)
          email = db.Column(db.String(30), unique=True)
          password = db.Column(db.String(30), nullable=False)
          date_created = db.Column(db.DateTime, default=datetime.now())
          news = db.relationship("News", backref="user", passive_deletes=True)
          blogs = db.relationship("Business", backref="user", passive_deletes=True)
          blogs = db.relationship("Sports", backref="user", passive_deletes=True)
          blogs = db.relationship("Entertainment", backref="user", passive_deletes=True)


          def user_dict(self):
               
               return {
                    'id': self.id,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'email': self.email,
                    'date_created': self.date_created,
                    }


class News(db.Model):
        id = db.Column(db.Integer, primary_key=True, index=True)
        title = db.Column(db.String(50), nullable=False)
        slug = db.Column(db.String(100), nullable=False)
        image_id = db.Column(db.String(100), nullable=False, unique=True)
        body = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now())
        published_on = db.Column(db.DateTime, default = datetime.now(), onupdate=datetime.now())
        author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
        
class Business(db.Model):
        id = db.Column(db.Integer, primary_key=True, index=True)
        title = db.Column(db.String(100), nullable=False)
        slug = db.Column(db.String(100), nullable=False)
        image_id = db.Column(db.String(100), nullable=False, unique=True)
        body = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now())
        published_on = db.Column(db.DateTime, default = datetime.now(), onupdate=datetime.now())
        author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


class Sports(db.Model):
        id = db.Column(db.Integer, primary_key=True, index=True)
        title = db.Column(db.String(100), nullable=False)
        slug = db.Column(db.String(100), nullable=False)
        image_id = db.Column(db.String(100), nullable=False, unique=True)
        body = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now())
        published_on = db.Column(db.DateTime, default = datetime.now(), onupdate=datetime.now())
        author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

     
class Entertainment(db.Model):
        id = db.Column(db.Integer, primary_key=True, index=True)
        title = db.Column(db.String(100), nullable=False)
        slug = db.Column(db.String(100), nullable=False)
        image_id = db.Column(db.String(100), nullable=False, unique=True)
        body = db.Column(db.Text, nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now())
        published_on = db.Column(db.DateTime, default = datetime.now(), onupdate=datetime.now())
        author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


