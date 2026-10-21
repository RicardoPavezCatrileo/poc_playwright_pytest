# Autor: Ricardo Pavez
# JIRA: QA_0004 Product catalog
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user (la abre el Background)
#
# Objetivo:
#       Validar que el catálogo muestra los 6 productos de la tienda.
#
#       Para ejecutar este caso:
#         behave features/QA0004_catalog_products.feature
#         pytest -m QA_0004
#
# Funcionalidad_QA = Catálogo
# Carpeta_Xray = /POC Sauce Demo/Catálogo


@inventory
Feature: Product catalog

    As a logged-in customer
    I want to see the full catalog
    So that I can choose what to buy

    Background:
        Given I am logged in as "standard_user"

    @QA_0004 @WEB @smoke @Regresion
    Scenario: QA_0004 The catalog shows all products
        Then I see 6 products in the catalog
