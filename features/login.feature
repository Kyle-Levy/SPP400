# Created by evanmeyer at 2019-03-01
Feature: Login form
  # Enter feature description here

  Scenario: Access the login form

    Given an anonymous user
    When I submit a valid login page
    Then I am redirected to the homepage

    Given an anonymous user
    When I submit an invalid login page
    Then I am redirected to the login