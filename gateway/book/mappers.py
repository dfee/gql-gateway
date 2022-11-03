from gateway.sql import models

from .dtos import BookDto, CreateBookDto


def book_model_to_dto(model: models.Book) -> BookDto:
    return BookDto(id=model.id, title=model.title, author_id=model.author_id)


def create_book_dto_to_model(dto: CreateBookDto) -> models.Book:
    return models.Book(id=dto.id, title=dto.title, author_id=dto.author_id)


def get_book_author_id(book: BookDto) -> int:
    return book.author_id
