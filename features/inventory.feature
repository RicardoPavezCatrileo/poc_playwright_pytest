# language: es
@inventory
Característica: Catálogo de productos
  Como cliente autenticado
  Quiero ver y ordenar el catálogo
  Para encontrar fácilmente lo que busco

  Antecedentes:
    Dado que inicié sesión como "standard_user"

  @smoke
  Escenario: El catálogo muestra todos los productos
    Entonces veo 6 productos en el catálogo

  Esquema del escenario: Ordenar productos
    Cuando ordeno los productos por "<orden>"
    Entonces los productos quedan ordenados por "<orden>"

    Ejemplos:
      | orden               |
      | Name (A to Z)       |
      | Name (Z to A)       |
      | Price (low to high) |
      | Price (high to low) |
