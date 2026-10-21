# Autor: Ricardo Pavez
# JIRA: QA_0007 Remove products from the cart
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user (la abre el Background)
#
# Objetivo:
#       Validar que al quitar el único producto agregado el carrito queda vacío.
#
#       Para ejecutar este caso:
#         behave features/QA0007_cart_remove_product.feature
#         pytest -m QA_0007
#
# Funcionalidad_QA = Carrito
# Carpeta_Xray = /POC Sauce Demo/Carrito


@cart
Feature: Remove products from the cart

    As a logged-in customer
    I want to remove products from the cart
    So that I only buy what I need

    Background:
        Given I am logged in as "standard_user"

    @QA_0007 @WEB @Regresion
    Scenario: QA_0007 Remove a product from the cart
        When I add the product "Sauce Labs Backpack" to the cart
        And I remove the product "Sauce Labs Backpack" from the cart
        Then the cart is empty
