from gateway.client.author import AuthorDto, CreateAuthorDto
from gateway.sql import models


def author_model_to_dto(model: models.Author) -> AuthorDto:
    return AuthorDto(
        id=model.id, first_name=model.first_name, last_name=model.last_name
    )


def create_author_dto_to_model(dto: CreateAuthorDto) -> models.Author:
    return models.Author(id=dto.id, first_name=dto.first_name, last_name=dto.last_name)
