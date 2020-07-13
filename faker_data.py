import hashlib
import random

from blog import db
from blog.models import *

alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']


def make_words():
    n = random.randint(2, 8)
    return "".join(random.sample(alphabet_list, n))


def make_title():
    n = random.randint(2, 7)
    title_list = (make_words() for i in range(n))
    return " ".join(title_list)


def make_content():
    n = random.randint(50, 300)
    content_list = (make_words() for i in range(n))
    return " ".join(content_list)


def make_data():
    print("making data...")
    user = User(username="admin", password=hashlib.md5("admin123456".encode('utf-8')).hexdigest(), nickname="admin")
    tag_names = [make_words() for _ in range(3)]
    category_names = [make_words() for _ in range(3)]
    while db.query(Tag).filter(Tag.name.in_(tag_names)).count() or db.query(Category).filter(
            Category.name.in_(category_names)).count():
        tag_names = [make_words() for _ in range(3)]
        category_names = [make_words() for _ in range(3)]

    tags = [Tag(name=i) for i in tag_names]
    categories = [Category(name=i) for i in category_names]

    db.add_all([user] + tags + categories)
    db.flush()

    posts = [Post(title=make_title(), content=make_content(), author_id=user.id, del_flag=False) for i in range(100)]
    for i in posts:
        n = random.randint(1, 3)
        i.tags = random.sample(tags, n)
        i.category = random.choice(categories)
    db.add_all(posts)
    db.commit()
    print("finish.")
