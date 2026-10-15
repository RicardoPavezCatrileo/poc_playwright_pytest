# language: es
@login
Característica: Inicio de sesión en Sauce Demo
  Como cliente de la tienda
  Quiero iniciar sesión con mis credenciales
  Para poder ver y comprar productos

  Antecedentes:
    Dado que estoy en la página de login

  @smoke
  Escenario: Login exitoso con usuario estándar
    Cuando inicio sesión con usuario "standard_user" y contraseña "secret_sauce"
    Entonces veo la página de productos

  Esquema del escenario: Login fallido muestra un mensaje de error
    Cuando inicio sesión con usuario "<usuario>" y contraseña "<clave>"
    Entonces veo el mensaje de error "<mensaje>"

    Ejemplos:
      | usuario         | clave        | mensaje                                                                   |
      | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | standard_user   | incorrecta   | Epic sadface: Username and password do not match any user in this service |
      |                 | secret_sauce | Epic sadface: Username is required                                        |
      | standard_user   |              | Epic sadface: Password is required                                        |

  Escenario: Cerrar sesión
    Cuando inicio sesión con usuario "standard_user" y contraseña "secret_sauce"
    Y cierro sesión
    Entonces vuelvo a la página de login
