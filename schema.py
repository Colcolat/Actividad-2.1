import typing

import strawberry

from database import Base, SessionLocal, engine
from models import PeliculaModel


@strawberry.type
class Director:
    nombre: str


@strawberry.type
class Pelicula:
    titulo: str
    director: Director
    anio: int
    disponible: bool


def row_to_pelicula(row):
    return Pelicula(
        titulo=row.titulo,
        director=Director(nombre=row.director),
        anio=row.anio,
        disponible=row.disponible,
    )


def preparar_datos():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(PeliculaModel).count() == 0:
            db.add_all(
                [
                    PeliculaModel(
                        titulo="Cinema Paradiso",
                        director="Giuseppe Tornatore",
                        anio=1988,
                        disponible=True,
                    ),
                    PeliculaModel(
                        titulo="Spirited Away",
                        director="Hayao Miyazaki",
                        anio=2001,
                        disponible=True,
                    ),
                    PeliculaModel(
                        titulo="The Godfather",
                        director="Francis Ford Coppola",
                        anio=1972,
                        disponible=False,
                    ),
                ]
            )
            db.commit()
    finally:
        db.close()


preparar_datos()


def get_peliculas():
    db = SessionLocal()
    try:
        rows = db.query(PeliculaModel).order_by(PeliculaModel.id).all()
        return [row_to_pelicula(row) for row in rows]
    finally:
        db.close()


@strawberry.type
class Query:
    peliculas: typing.List[Pelicula] = strawberry.field(resolver=get_peliculas)

    @strawberry.field
    def pelicula(self, titulo: str) -> typing.Optional[Pelicula]:
        db = SessionLocal()
        try:
            row = (
                db.query(PeliculaModel)
                .filter(PeliculaModel.titulo == titulo)
                .first()
            )
            if row is None:
                return None
            return row_to_pelicula(row)
        finally:
            db.close()

    @strawberry.field
    def peliculas_disponibles(self) -> typing.List[Pelicula]:
        db = SessionLocal()
        try:
            rows = (
                db.query(PeliculaModel)
                .filter(PeliculaModel.disponible == True)  # noqa: E712
                .order_by(PeliculaModel.id)
                .all()
            )
            return [row_to_pelicula(row) for row in rows]
        finally:
            db.close()


@strawberry.input
class AgregarPeliculaInput:
    titulo: str
    director: str
    anio: int
    disponible: bool


@strawberry.type
class Mutation:
    @strawberry.mutation
    def agregar_pelicula(self, pelicula: AgregarPeliculaInput) -> Pelicula:
        db = SessionLocal()
        try:
            row = PeliculaModel(
                titulo=pelicula.titulo,
                director=pelicula.director,
                anio=pelicula.anio,
                disponible=pelicula.disponible,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            return row_to_pelicula(row)
        finally:
            db.close()


schema = strawberry.Schema(query=Query, mutation=Mutation)
