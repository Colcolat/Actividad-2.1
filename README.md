# Cineclub en GraphQL y MySQL

Unidad II · Actividad 1 — MySQL y GraphQL con Strawberry.

La cartelera del cineclub se expone con GraphQL (Strawberry) y se guarda en MySQL
(SQLAlchemy + PyMySQL). El esquema no guarda datos: los resolvers leen y escriben en la
tabla `peliculas` de la base `cineclub`.

```
cineclub_Nombre_Apellido/
    database.py   # conexión (engine, SessionLocal, Base)
    models.py     # PeliculaModel -> tabla peliculas
    schema.py     # tipos GraphQL, resolvers, Query y Mutation
```

## 1. Crear la base de datos

```sql
CREATE DATABASE cineclub;
SHOW DATABASES;
```

La tabla `peliculas` la crea la aplicación al arrancar con `Base.metadata.create_all`.

## 2. Entorno e instalación (Windows PowerShell)

```powershell
py -m venv virtualenv
.\virtualenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ajusta usuario y contraseña en `database.py`
(`mysql+pymysql://root:password@localhost:3306/cineclub`) o define la variable de entorno
`DATABASE_URL`.

## 3. Arrancar

```powershell
strawberry dev schema
```

Abre http://localhost:8000/graphql

## 4. Comprobación

```graphql
{
  peliculas {
    titulo
    anio
    disponible
    director { nombre }
  }
}
```

```graphql
{
  pelicula(titulo: "The Godfather") {
    titulo
    director { nombre }
  }
}
```

```graphql
{
  pelicula(titulo: "Amelie") {
    titulo
  }
}
```

```graphql
{
  peliculasDisponibles {
    titulo
    disponible
  }
}
```

```graphql
mutation {
  agregarPelicula(pelicula: {
    titulo: "Amelie",
    director: "Jean-Pierre Jeunet",
    anio: 2001,
    disponible: true
  }) {
    titulo
    anio
    director { nombre }
  }
}
```

Después de la mutación, detén el servidor (`Ctrl+C`), vuelve a arrancarlo y consulta
`peliculas`: Amelie sigue ahí. En MySQL:

```sql
USE cineclub;
SELECT titulo, director, anio, disponible FROM peliculas;
```

Debe mostrar cuatro filas.
