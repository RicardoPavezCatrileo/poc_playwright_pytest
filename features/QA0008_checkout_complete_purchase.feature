@checkout
Feature: Complete a purchase
  As a customer with products in the cart
  I want to complete the checkout
  So that I receive my order

  Background:
    Given I am logged in as "standard_user"
    And I add the product "Sauce Labs Backpack" to the cart
    And I go to the cart
    And I start the checkout

  @smoke
  Scenario: QA_0008 Complete purchase of one product
    When I enter first name "Ricardo", last name "Pavez" and postal code "8320000"
    And I continue to the order overview
    Then the order total is "$32.39"
    When I finish the purchase
    Then I see the confirmation message "Thank you for your order!"
