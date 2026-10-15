@login
Feature: Login error messages
  As a store customer
  I want to see a clear error when my login fails
  So that I know how to fix it

  Background:
    Given I am on the login page

  Scenario Outline: QA_0002_<case> Failed login shows an error message
    When I log in with username "<username>" and password "<password>"
    Then I see the error message "<message>"

    Examples:
      | case | username        | password     | message                                                                   |
      | 01   | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | 02   | standard_user   | wrong_pass   | Epic sadface: Username and password do not match any user in this service |
      | 03   |                 | any_password | Epic sadface: Username is required                                        |
      | 04   | standard_user   |              | Epic sadface: Password is required                                        |
      | 05   |                 |              | Epic sadface: Username is required                                        |
