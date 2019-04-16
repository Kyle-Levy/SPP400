# Created by evanmeyer at 2019-04-16
Feature: Procedure form
  # Enter feature description here

  Scenario: Submit a procedure

    Given a successful login
    When I click on the procedures tab
    Then I am redirected to the procedures page