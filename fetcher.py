from db import get_session, Article, People

def get_all_articles():
    session = get_session()
    articles = session.query(Article).all()
    session.close()
    return articles

def get_article_by_id(article_id):
    session = get_session()
    article = session.query(Article).filter(Article.id == article_id).first()
    session.close()
    return article

def get_all_people():
    session = get_session()
    people = session.query(People).all()
    session.close()
    return people

def get_person_by_id(person_id):
    session = get_session()
    person = session.query(People).filter(People.id == person_id).first()
    session.close()
    return person

def get_articles_by_author(author_name):
    session = get_session()
    author = session.query(People).filter(People.name == author_name).first()
    if author:
        articles = author.articles
    else:
        articles = []
    session.close()
    return articles

def get_articles_by_supervisor(supervisor_name):
    session = get_session()
    supervisor = session.query(People).filter(People.name == supervisor_name).first()
    if supervisor:
        articles = supervisor.supervised_articles
    else:
        articles = []
    session.close()
    return articles

# count articles by author name
def count_articles_by_author(author_name):
    session = get_session()
    author = session.query(People).filter(People.name == author_name).first()
    if author:
        articles = author.articles
    else:
        articles = []
    session.close()
    return len(articles)

# count articles by supervisor name
def count_articles_by_supervisor(supervisor_name):
    session = get_session()
    supervisor = session.query(People).filter(People.name == supervisor_name).first()
    if supervisor:
        articles = supervisor.supervised_articles
    else:
        articles = []
    session.close()
    return len(articles)