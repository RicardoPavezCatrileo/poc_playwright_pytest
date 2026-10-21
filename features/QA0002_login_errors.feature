# Autor: Ricardo Pavez
# JIRA: QA_0002 Login error messages
#
# Precondiciones:
#       - SAUCE_BASE_URL y SAUCE_PASSWORD definidos en .env
#
# Objetivo:
#       Validar que cada intento de login fallido muestra el mensaje de error correcto.
#       Cada fila de Examples es un caso propio (QA_0002_01 .. QA_0002_05).
#
#       Para ejecutar un caso específico:
#         behave features/QA0002_login_errors.feature --tags=@QA_0002_03
#         pytest -m QA_0002_03
#
# Funcionalidad_QA = Login
# Carpeta_Xray = /POC Sauce Demo/Login


@login
Feature: Login error messages

    As a store customer
    I want to see a clear error when my login fails
    So that I know how to fix it

    Background:
        Given I am on the login page

    @QA_0002 @WEB @Regresion
    Scenario Outline: QA_0002_<case> Failed login shows an error message
        When I log in with username "<username>" and password "<password>"
        Then I see the error message "<message>"

        @QA_0002_01
        Examples: Locked out user
            | case | username        | password     | message                                             |
            | 01   | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out. |

        @QA_0002_02
        Examples: Wrong password
            | case | username      | password   | message                                                                   |
            | 02   | standard_user | wrong_pass | Epic sadface: Username and password do not match any user in this service |

        @QA_0002_03
        Examples: Empty username
            | case | username | password     | message                            |
            | 03   |          | any_password | Epic sadface: Username is required |

        @QA_0002_04
        Examples: Empty password
            | case | username      | password | message                            |
            | 04   | standard_user |          | Epic sadface: Password is required |

        @QA_0002_05
        Examples: Empty username and password
            | case | username | password | message                            |
            | 05   |          |          | Epic sadface: Username is required |
