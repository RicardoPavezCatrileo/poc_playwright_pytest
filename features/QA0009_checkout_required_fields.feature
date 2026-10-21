# Autor: Ricardo Pavez
# JIRA: QA_0009 Checkout required fields
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user y "Sauce Labs Backpack" en el carrito
#         (lo prepara el Background hasta el inicio del checkout)
#
# Objetivo:
#       Validar que cada dato de envío obligatorio muestra su mensaje de error si falta.
#       Cada fila de Examples es un caso propio (QA_0009_01 .. QA_0009_03).
#
#       Para ejecutar un caso específico:
#         behave features/QA0009_checkout_required_fields.feature --tags=@QA_0009_02
#         pytest -m QA_0009_02
#
# Funcionalidad_QA = Checkout
# Carpeta_Xray = /POC Sauce Demo/Checkout


@checkout
Feature: Checkout required fields

    As a customer with products in the cart
    I want to be told which shipping fields are missing
    So that I can complete the checkout

    Background:
        Given I am logged in as "standard_user"
        And I add the product "Sauce Labs Backpack" to the cart
        And I go to the cart
        And I start the checkout

    @QA_0009 @WEB @Regresion
    Scenario Outline: QA_0009_<case> Shipping information is required
        When I enter first name "<first_name>", last name "<last_name>" and postal code "<postal_code>"
        And I continue to the order overview
        Then I see the error message "<message>"

        @QA_0009_01
        Examples: Missing first name
            | case | first_name | last_name | postal_code | message                       |
            | 01   |            | Pavez     | 8320000     | Error: First Name is required |

        @QA_0009_02
        Examples: Missing last name
            | case | first_name | last_name | postal_code | message                      |
            | 02   | Ricardo    |           | 8320000     | Error: Last Name is required |

        @QA_0009_03
        Examples: Missing postal code
            | case | first_name | last_name | postal_code | message                        |
            | 03   | Ricardo    | Pavez     |             | Error: Postal Code is required |
