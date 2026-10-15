@cart
Feature: Remove products from the cart
  As a logged-in customer
  I want to remove products from the cart
  So that I only buy what I need

  Background:
    Given I am logged in as "standard_user"

  Scenario: QA_0007 Remove a product from the cart
    When I add the product "Sauce Labs Backpack" to the cart
    And I remove the product "Sauce Labs Backpack" from the cart
    Then the cart is empty
