@inventory
Feature: Product catalog
  As a logged-in customer
  I want to view and sort the catalog
  So that I can easily find what I am looking for

  Background:
    Given I am logged in as "standard_user"

  @smoke
  Scenario: QA_0004 The catalog shows all products
    Then I see 6 products in the catalog

  Scenario Outline: QA_0005 Sort products
    When I sort the products by "<order>"
    Then the products are sorted by "<order>"

    Examples:
      | order               |
      | Name (A to Z)       |
      | Name (Z to A)       |
      | Price (low to high) |
      | Price (high to low) |
