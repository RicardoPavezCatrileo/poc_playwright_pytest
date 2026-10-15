@cart
Feature: Shopping cart
  As a logged-in customer
  I want to add and remove products from the cart
  So that I can prepare my purchase

  Background:
    Given I am logged in as "standard_user"

  @smoke
  Scenario: Add several products to the cart
    When I add the product "Sauce Labs Backpack" to the cart
    And I add the product "Sauce Labs Bike Light" to the cart
    Then the cart badge shows "2"
    When I go to the cart
    Then the cart contains the products:
      | product               |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |

  Scenario: Remove a product from the cart
    When I add the product "Sauce Labs Backpack" to the cart
    And I remove the product "Sauce Labs Backpack" from the cart
    Then the cart is empty
