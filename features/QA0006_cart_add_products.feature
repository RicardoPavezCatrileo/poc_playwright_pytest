# Autor: Ricardo Pavez
# JIRA: QA_0006 Add products to the cart
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user (la abre el Background)
#
# Objetivo:
#       Validar que al agregar productos el contador del carrito se actualiza
#       y el carrito muestra exactamente los productos agregados.
#
#       Para ejecutar este caso:
#         behave features/QA0006_cart_add_products.feature
#         pytest -m QA_0006
#
# Funcionalidad_QA = Carrito
# Carpeta_Xray = /POC Sauce Demo/Carrito


@cart
Feature: Add products to the cart

    As a logged-in customer
    I want to add products to the cart
    So that I can prepare my purchase

    Background:
        Given I am logged in as "standard_user"

    @QA_0006 @WEB @smoke @Regresion
    Scenario: QA_0006 Add several products to the cart
        When I add the product "Sauce Labs Backpack" to the cart
        And I add the product "Sauce Labs Bike Light" to the cart
        Then the cart badge shows "2"
        When I go to the cart
        Then the cart contains the products:
            | product               |
            | Sauce Labs Backpack   |
            | Sauce Labs Bike Light |
