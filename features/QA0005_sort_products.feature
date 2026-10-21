# Autor: Ricardo Pavez
# JIRA: QA_0005 Sort the product catalog
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user (la abre el Background)
#
# Objetivo:
#       Validar cada opción de ordenamiento del catálogo (nombre y precio).
#       Cada fila de Examples es un caso propio (QA_0005_01 .. QA_0005_04).
#
#       Para ejecutar un caso específico:
#         behave features/QA0005_sort_products.feature --tags=@QA_0005_03
#         pytest -m QA_0005_03
#
# Funcionalidad_QA = Catálogo
# Carpeta_Xray = /POC Sauce Demo/Catálogo


@inventory
Feature: Sort the product catalog

    As a logged-in customer
    I want to sort the catalog
    So that I can easily find what I am looking for

    Background:
        Given I am logged in as "standard_user"

    @QA_0005 @WEB @Regresion
    Scenario Outline: QA_0005_<case> Sort products
        When I sort the products by "<order>"
        Then the products are sorted by "<order>"

        @QA_0005_01
        Examples: Name A to Z
            | case | order         |
            | 01   | Name (A to Z) |

        @QA_0005_02
        Examples: Name Z to A
            | case | order         |
            | 02   | Name (Z to A) |

        @QA_0005_03
        Examples: Price low to high
            | case | order               |
            | 03   | Price (low to high) |

        @QA_0005_04
        Examples: Price high to low
            | case | order               |
            | 04   | Price (high to low) |
