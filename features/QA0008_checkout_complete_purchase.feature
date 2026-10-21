# Autor: Ricardo Pavez
# JIRA: QA_0008 Complete a purchase
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user y "Sauce Labs Backpack" en el carrito
#         (lo prepara el Background hasta el inicio del checkout)
#
# Objetivo:
#       Validar la compra completa: datos de envío, total de la orden ($32.39)
#       y mensaje de confirmación.
#
#       Para ejecutar este caso:
#         behave features/QA0008_checkout_complete_purchase.feature
#         pytest -m QA_0008
#
# Funcionalidad_QA = Checkout
# Carpeta_Xray = /POC Sauce Demo/Checkout


@checkout
Feature: Complete a purchase

    As a customer with products in the cart
    I want to complete the checkout
    So that I receive my order

    Background:
        Given I am logged in as "standard_user"
        And I add the product "Sauce Labs Backpack" to the cart
        And I go to the cart
        And I start the checkout

    @QA_0008 @WEB @smoke @Regresion
    Scenario: QA_0008 Complete purchase of one product
        When I enter first name "Ricardo", last name "Pavez" and postal code "8320000"
        And I continue to the order overview
        Then the order total is "$32.39"
        When I finish the purchase
        Then I see the confirmation message "Thank you for your order!"
