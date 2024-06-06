import re
from db import get_session, Article, People
from utils import abbreviate_name, pretify_name
import logging
logger = logging.getLogger(__name__)

def find_authors(text):
    pattern = re.compile(r'^\b\w+[- ]?\w+\s*\w\.\s*(?:\w\.)?')
    clean_pattern = re.compile(r'^\.?,?')
    authors = []
    match = pattern.search(text)

    while match:
        authors.append(match.group())
        text = text[match.end():]
        text = re.sub(clean_pattern, '', text.strip())
        match = pattern.search(text.strip())

    if not authors:
        print(f"Author not found in text: {text}")
    return authors, text

def find_supervisors(text):
    text = re.sub(r'\(науч\. рук\.', '', text.strip()).strip()
    pattern = re.compile(r'^\b\w+[- ]?\w+\s*\w\.\s*(?:\w\.)?')
    clean_pattern = re.compile(r'^\.?,?')
    supervisors = []
    match = pattern.search(text.strip())
    while match:
        supervisors.append(match.group())
        text = text[match.end():].strip()
        text = re.sub(clean_pattern, '', text.strip())
        match = pattern.search(text.strip())
    if not supervisors:
        logger.debug(f"Supervisor not found in text: {text}")
    return supervisors, text

def process_data(links, info):
    session = get_session()
    congress = re.findall(r'^\w+', info[0][0].text)[0].strip().lower()
    direction = info[1][0].text.strip().lower()
    section = info[2][0].text.strip().lower()

    for href, text in links:
        text = text.strip()
        logger.info(f"Processing article {text}")
        supervisors_text = re.findall(r'\(науч\. рук\..*?\)', text)
        if not supervisors_text:
            logger.debug(f"Supervisor not found in text: {text}")
            continue
        supervisors_text = re.sub(r'\(науч\. рук\.|\)', '', supervisors_text[0])
        supervisors = supervisors_text.split(',')
        supervisors = [supervisor.strip() for supervisor in supervisors]
        text = re.sub(r'\(науч\. рук\..*?\)', '', text)
        title_text = re.findall(r'[^.]*.?$', text)
        if not title_text:
            logger.error(f"Title not found in text: {text}")
            continue
        text = re.sub(r'[^.]*.?$', '', text)
        authors = text.split(',')
        try:
            authors = [pretify_name(author) for author in authors]
        except Exception as e:
            logger.error(f"This text to hard for me: {text}")
            continue
        if not authors:
            logger.error(f"Author not found in text: {text}")
            continue
        for author in authors:
            if 'науч.' in author:
                print(f"Something went wrong: \n authors: {authors}\n text: {text}\n")
        authors = [author.strip() for author in authors]
        title = title_text[0].strip().lower()
        existing_article = session.query(Article).filter(Article.link == href).first()
        if existing_article:
            new_article = existing_article
        else:
            new_article = Article(title=title, link=href, congress=congress, direction=direction, section=section)
            session.add(new_article)
            session.commit()  # Commit here to get the article ID

        for author in authors:
            author_obj = session.query(People).filter(People.name == author).first()
            if not author_obj:
                author_obj = People(name=author)
                session.add(author_obj)
            if author_obj not in new_article.authors:
                new_article.authors.append(author_obj)

        for supervisor in supervisors:
            supervisor_obj = session.query(People).filter(People.name == supervisor).first()
            if not supervisor_obj:
                supervisor_obj = People(name=supervisor)
                session.add(supervisor_obj)
            if supervisor_obj not in new_article.supervisors:
                new_article.supervisors.append(supervisor_obj)

        session.commit()

    session.close()

def process_winners(winners, conf_num):
    session = get_session()
    for winner in winners:
        winner_abr = abbreviate_name(winner.strip())
        person = session.query(People).filter(People.name == winner_abr).first()
        if person:
            flag = False
            for article in person.articles:
                if article.congress == conf_num:
                    flag = True
                    article.isWin = 1
            if not flag:
                print(f"Winner {winner} article not found in the database")
        else:
            # split the name into parts and merge last name and first name
            # winner_abr = winner_abr.split()
            winner_abr = abbreviate_name(' '.join(winner.split()[0:2]))
            person = session.query(People).filter(People.name == winner_abr).first()
            if person:
                flag = False
                for article in person.articles:
                    if article.congress == conf_num:
                        flag = True
                        article.isWin = 1
                if not flag:
                    print(f"Winner {winner} article not found in the database")
            else:
                print(f"Winner {winner} not found in the database")
        session.commit()
    session.close()