@inventory
Feature: Product catalog
  As a logged-in customer
  I want to see the full catalog
  So that I can choose what to buy

  Background:
    Given I am logged in as "standard_user"

  @smoke
  Scenario: QA_0004 The catalog shows all products
    Then I see 6 products in the catalog
