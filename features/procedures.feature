# Created by evanmeyer at 2019-04-16
Feature: Procedure form
  # Enter feature description here

  Scenario: Submit a procedure

    Given a successful login
    When I click on the procedures tab
    Then I am redirected to the procedures page
    When I click on the Add New Procedure button
    Then I am redirected to the procedure form page

    Given a successful login
    When I click on the procedures tab
    Then I am redirected to the procedures page
    When I click on the Add New Procedure button
    Then I am redirected to the procedure form page