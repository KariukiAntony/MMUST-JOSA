from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate()


class User(UserMixin, db.Model):
          id = db.Column(db.Integer, primary_key = True, index=True)
          first_name = db.Column(db.String(20), nullable=False)
          last_name = db.Column(db.String(20), nullable=False)
          email = db.Column(db.String(30), unique=True)
          password = db.Column(db.String(30), nullable=False)
          date_created = db.Column(db.DateTime, default=datetime.now())
          blogs = db.relationship("Blogs", backref="user", passive_deletes=True)


          def user_dict(self):
               
               return {
                    'id': self.id,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'email': self.email,
                    'date_created': self.date_created.isoformat(),
                    }


class Blogs(db.Model):
        id = db.Column(db.Integer, primary_key=True, index=True)
        title = db.Column(db.String(30), nullable=False)
        category = db.Column(db.String(100), nullable=True)
        content = db.Column(db.String(500), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.now())
        updated_at = db.Column(db.DateTime, default = datetime.now(), onupdate=datetime.now())
        owner_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

        def blogs_dict(self):
          return {
                    'id': self.id,
                    'title': self.title,
                    'content': self.content,
                    'category': self.category,
                    'date_created': self.date_created.isoformat(),
                    'updatedAt': self.updated_at.isoformat()
          }