'''
Program: Models_
Author: Maya Name
Creation Date: 01/02/2025
Revision Date: 
Description: Data structure models for microblog app

Revisions:


'''

import sqlalchemy as sa
import sqlalchemy.orm as so
from .extensions import db
from datetime import datetime, timezone
from typing import Optional

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), 
                                                index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), 
                                             index=True,
                                             unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return f'<User: {self.username}>'


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(256))
    timestamp: so.Mapped[datetime] = so.mapped_column(
                index=True, 
                default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post: {self.body}>'