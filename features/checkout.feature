# language: es
@checkout
Característica: Proceso de compra
  Como cliente con productos en el carrito
  Quiero completar el checkout
  Para recibir mi pedido

  Antecedentes:
    Dado que inicié sesión como "standard_user"
    Y agrego al carrito el producto "Sauce Labs Backpack"
    Y voy al carrito
    Y inicio el checkout

  @smoke
  Escenario: Compra completa de un producto
    Cuando ingreso nombre "Ricardo", apellido "Pavez" y código postal "8320000"
    Y continúo al resumen de la compra
    Entonces el total de la compra es "$32.39"
    Cuando finalizo la compra
    Entonces veo el mensaje de confirmación "Thank you for your order!"

  Esquema del escenario: Datos de envío obligatorios
    Cuando ingreso nombre "<nombre>", apellido "<apellido>" y código postal "<cp>"
    Y continúo al resumen de la compra
    Entonces veo el mensaje de error "<mensaje>"

    Ejemplos:
      | nombre  | apellido | cp      | mensaje                        |
      |         | Pavez    | 8320000 | Error: First Name is required  |
      | Ricardo |          | 8320000 | Error: Last Name is required   |
      | Ricardo | Pavez    |         | Error: Postal Code is required |
