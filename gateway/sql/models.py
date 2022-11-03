from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last_name", String, nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String, nullable=False)
    author_id = Column("author_id", Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
