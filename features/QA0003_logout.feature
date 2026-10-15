@login
Feature: Logout from Sauce Demo
  As a logged-in customer
  I want to log out
  So that nobody else can use my session

  Background:
    Given I am logged in as "standard_user"

  Scenario: QA_0003 Logout
    When I log out
    Then I am back on the login page
