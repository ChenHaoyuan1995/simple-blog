from sqlalchemy import Table, ForeignKey, Column, String, Integer, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from blog import Base

post_tag = Table('post_tag', Base.metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('post_id', Integer(), ForeignKey('post.id', ondelete="CASCADE")),
                 Column('tag_id', Integer(), ForeignKey('tag.id', ondelete="CASCADE"))
                 )


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship("User", backref="posts")

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", backref="posts")

    tags = relationship('Tag',
                        secondary=post_tag,
                        primaryjoin="post_tag.c.post_id==Post.id",
                        secondaryjoin="post_tag.c.tag_id==Tag.id",
                        back_populates='posts')

    create_time = Column(DateTime(), default=func.now(), server_default=func.now())
    update_time = Column(DateTime(), default=func.now(), onupdate=func.now(), server_default=func.now())
    del_flag = Column(Boolean())


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    posts = relationship('Post',
                         secondary=post_tag,
                         primaryjoin="post_tag.c.tag_id==Tag.id",
                         secondaryjoin="post_tag.c.post_id==Post.id",
                         back_populates='tags')

    def __repr__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __repr__(self):
        return self.name
