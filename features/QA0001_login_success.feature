@login
Feature: Successful login to Sauce Demo
  As a store customer
  I want to log in with valid credentials
  So that I can browse and buy products

  Background:
    Given I am on the login page

  @smoke
  Scenario: QA_0001 Successful login with standard user
    When I log in with username "standard_user" and password "secret_sauce"
    Then I see the products page
