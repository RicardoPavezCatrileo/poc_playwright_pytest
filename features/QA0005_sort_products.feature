@inventory
Feature: Sort the product catalog
  As a logged-in customer
  I want to sort the catalog
  So that I can easily find what I am looking for

  Background:
    Given I am logged in as "standard_user"

  Scenario Outline: QA_0005_<case> Sort products
    When I sort the products by "<order>"
    Then the products are sorted by "<order>"

    Examples:
      | case | order               |
      | 01   | Name (A to Z)       |
      | 02   | Name (Z to A)       |
      | 03   | Price (low to high) |
      | 04   | Price (high to low) |
