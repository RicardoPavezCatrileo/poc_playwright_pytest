# language: es
@cart
Característica: Carrito de compras
  Como cliente autenticado
  Quiero agregar y quitar productos del carrito
  Para preparar mi compra

  Antecedentes:
    Dado que inicié sesión como "standard_user"

  @smoke
  Escenario: Agregar varios productos al carrito
    Cuando agrego al carrito el producto "Sauce Labs Backpack"
    Y agrego al carrito el producto "Sauce Labs Bike Light"
    Entonces el contador del carrito muestra "2"
    Cuando voy al carrito
    Entonces el carrito contiene los productos:
      | producto              |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |

  Escenario: Quitar un producto del carrito
    Cuando agrego al carrito el producto "Sauce Labs Backpack"
    Y quito del carrito el producto "Sauce Labs Backpack"
    Entonces el carrito está vacío
