from sqlalchemy import create_engine, MetaData, Table, Column, String

engine = create_engine("sqlite:///memes.db", echo=True)
