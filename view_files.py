from fetcher import *
# # Получение всех статей
# articles = get_all_articles()
# for article in articles:
#     print(f"ID: {article.id}, Title: {article.title}, Link: {article.link}")

# # Получение статьи по ID
# article = get_article_by_id(1)
# if article:
#     print(f"ID: {article.id}, Title: {article.title}, Link: {article.link}")
#
# Получение всех людей
# people = get_all_people()
# for person in people:
#     print(f"ID: {person.id}, Name: {person.name}")

# Получение количества статей по руководителю
# supervisor_name = "Быковский С.В."
# articles_count = count_articles_by_supervisor(supervisor_name)
# print(f"Supervisor: {supervisor_name}, Articles count: {articles_count}")

# # Получение человека по ID
# person = get_person_by_id(1)
# if person:
#     print(f"ID: {person.id}, Name: {person.name}")
#
# # Получение статей по автору
# author_name = "Иванов И.И."
# articles_by_author = get_articles_by_author(author_name)
# for article in articles_by_author:
#     print(f"ID: {article.id}, Title: {article.title}, Link: {article.link}")

# # Получение статей по научному руководителю
# supervisor_name = "Буковский П.П."
# articles_by_supervisor = get_articles_by_supervisor(supervisor_name)
# for article in articles_by_supervisor:
#     print(f"ID: {article.id}, Title: {article.title}, Link: {article.link}")

# Вывести руководителей из списка в порядке убывания количества статей
# known_supervisors = ["Быковский С.В.",
#                      "Алиев Т.И.",
#                      "Цопа Е.А.",
#                      "Кореньков Ю.Д.",
#                      "Исаев И.В.",
#                      "Клименков С.В.",
#                      "Бессмертный И.А.",
#                      "Перл И.А.",
#                      "Афанасьев Д.Б.",
#                      "Логинов И.П.",
#                      "Лаздин А.В.",
#                      "Балакшин П.В."]
# supervisors = []
# for supervisor in known_supervisors:
#     articles_count = count_articles_by_supervisor(supervisor)
#     supervisors.append((supervisor, articles_count))
# supervisors.sort(key=lambda x: x[1], reverse=True)
# print("Supervisors by articles count:")
# # display as pandas table
# import pandas as pd
# from IPython.display import display
# df = pd.DataFrame(supervisors, columns=['Supervisor', 'Articles count'])
# display(df)

import pandas as pd
from IPython.display import display
from db import get_session, Article, People
supervisor_name = "Быковский С.В."
session = get_session()
supervisor = session.query(People).filter(People.name == supervisor_name).first()
if supervisor:
    articles = supervisor.supervised_articles
else:
    articles = []
articles_list = [[article.id, article.title, article.link, article.congress, article.direction, article.section] for article in articles]
df = pd.DataFrame(articles_list, columns=['ID', 'Title', 'Link', 'Congress', 'Direction', 'Section'])
dff = df[['Congress', 'Direction', 'Section', 'Title']]
display(dff)
session.close()

