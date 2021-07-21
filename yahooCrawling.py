from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
import pymysql
import urllib.request
import urllib.parse

def keyword_handler(event, context):

    engine=create_engine('mysql+pymysql://') # put mysql+pymysql here.
    Base = declarative_base()
    engine.connect()

    class Key_Word(Base):
        __tablename__ = 'key_word'

        id = Column(Integer, Sequence('word_id_seq'), primary_key=True)
        rank=Column(String(10))
        word = Column(String(30))

        def __init__(self, rank, word):
            self.rank = rank
            self.word = word

        def __repr__(self):
            id=""
            if self.id is not None:
                id = str(self.id)
            else:
                id = "None"

            return "<Key_Word('%s','%s','%s')>" %(id, self.rank, self.word)

    Base.metadata.create_all(engine)

    url = "https://us.yahoo.com/"
    html = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html,"html.parser")
    list_ranks = soup.findAll('span', {'class':'D(ib) W(1.3em) Ta(e) C(#000)'})
    list_words = soup.findAll('span', {'class':'C($searchBlue):h Fw(b) Mstart(2px)'})
    print(list_ranks)
    print(list_words)
    word=[]

    for i in range(len(list_ranks)):
        new_keyword_data = Key_Word(list_ranks[i].text, list_words[i].text)
        word.append(new_keyword_data)
    print(word)

    Session = sessionmaker(bind=engine)
    session = Session()
    for i in range(len(list_ranks)):
        session.add(word[i])

    session.commit()

    temp = session.query(Key_Word).all()
    for item in temp:
        session.delete(item)
