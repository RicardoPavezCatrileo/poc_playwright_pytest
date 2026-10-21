# Autor: Ricardo Pavez
# JIRA: QA_0003 Logout from Sauce Demo
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#       - Sesión iniciada con standard_user (la abre el Background)
#
# Objetivo:
#       Validar que el usuario cierra sesión desde el menú y vuelve a la página de login.
#
#       Para ejecutar este caso:
#         behave features/QA0003_logout.feature
#         pytest -m QA_0003
#
# Funcionalidad_QA = Login
# Carpeta_Xray = /POC Sauce Demo/Login


@login
Feature: Logout from Sauce Demo

    As a logged-in customer
    I want to log out
    So that nobody else can use my session

    Background:
        Given I am logged in as "standard_user"

    @QA_0003 @WEB @Regresion
    Scenario: QA_0003 Logout
        When I log out
        Then I am back on the login page
