@login
Feature: Login to Sauce Demo
  As a store customer
  I want to log in with my credentials
  So that I can browse and buy products

  Background:
    Given I am on the login page

  @smoke
  Scenario: Successful login with standard user
    When I log in with username "standard_user" and password "secret_sauce"
    Then I see the products page

  Scenario Outline: Failed login shows an error message
    When I log in with username "<username>" and password "<password>"
    Then I see the error message "<message>"

    Examples:
      | username        | password     | message                                                                   |
      | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | standard_user   | wrong_pass   | Epic sadface: Username and password do not match any user in this service |
      |                 | secret_sauce | Epic sadface: Username is required                                        |
      | standard_user   |              | Epic sadface: Password is required                                        |

  Scenario: Logout
    When I log in with username "standard_user" and password "secret_sauce"
    And I log out
    Then I am back on the login page
