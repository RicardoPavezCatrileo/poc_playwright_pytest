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

  Scenario Outline: QA_0009_<case> Shipping information is required
    When I enter first name "<first_name>", last name "<last_name>" and postal code "<postal_code>"
    And I continue to the order overview
    Then I see the error message "<message>"

    Examples:
      | case | first_name | last_name | postal_code | message                        |
      | 01   |            | Pavez     | 8320000     | Error: First Name is required  |
      | 02   | Ricardo    |           | 8320000     | Error: Last Name is required   |
      | 03   | Ricardo    | Pavez     |             | Error: Postal Code is required |
