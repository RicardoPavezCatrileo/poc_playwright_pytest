# Autor: Ricardo Pavez
# JIRA: QA_0001 Successful login to Sauce Demo
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#
# Objetivo:
#       Validar que un usuario estándar inicia sesión con credenciales válidas
#       y llega a la página de productos.
#
#       Para ejecutar este caso:
#         behave features/QA0001_login_success.feature
#         pytest -m QA_0001
#
# Funcionalidad_QA = Login
# Carpeta_Xray = /POC Sauce Demo/Login


@login
Feature: Successful login to Sauce Demo

    As a store customer
    I want to log in with valid credentials
    So that I can browse and buy products

    Background:
        Given I am on the login page

    @QA_0001 @WEB @smoke @Regresion
    Scenario: QA_0001 Successful login with standard user
        When I log in with username "standard_user" and password "secret_sauce"
        Then I see the products page
