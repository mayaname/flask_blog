'''
Program: Models_
Author: Maya Name
Creation Date: 01/02/2025
Revision Date: 01/03/2025
Description: Data structure models for microblog app

Revisions:
01/03/2025 Update User class for login functionality

'''

import sqlalchemy as sa
import sqlalchemy.orm as so
from .extensions import db
from datetime import datetime, timezone
from flask_login import UserMixin
from hashlib import md5
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50))
    lastname: so.Mapped[Optional[str]] = so.mapped_column(sa.String(50), 
                                                index=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), 
                                                index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), 
                                             index=True,
                                             unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))

    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User: {self.username}>'
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.Text)
    timestamp: so.Mapped[datetime] = so.mapped_column(
                index=True, 
                default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post: {self.body}>'