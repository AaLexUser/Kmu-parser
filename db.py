from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///links.db')
Base = declarative_base()

article_author_association = Table(
    'article_author_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('author_id', Integer, ForeignKey('people.id'))
)

article_supervisor_association = Table(
    'article_supervisor_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('supervisor_id', Integer, ForeignKey('people.id'))
)


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    articles = relationship(
        "Article",
        secondary=article_author_association,
        back_populates="authors"
    )
    supervised_articles = relationship(
        "Article",
        secondary=article_supervisor_association,
        back_populates="supervisors"
    )


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)
    congress = Column(String)
    direction = Column(String)
    section = Column(String)
    isWin = Column(Integer, default=0)
    authors = relationship(
        "People",
        secondary=article_author_association,
        back_populates="articles"
    )
    supervisors = relationship(
        "People",
        secondary=article_supervisor_association,
        back_populates="supervised_articles"
    )


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
