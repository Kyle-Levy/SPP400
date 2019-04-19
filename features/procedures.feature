# Created by evanmeyer at 2019-04-16
Feature: Procedure form
  # Enter feature description here

  Scenario: Submit a procedure

    Given a successful login
    When I click on the procedures tab
    Then I am redirected to the procedures page
    When I click on the Add New Procedure button
    Then I am redirected to the procedure form page
    When I successfully fill out and submit the procedure form
    Then I am redirected to the procedures landing page

    When I click on the Add New Procedure button
    Then I am redirected to the procedure form page
    When I fail to fill out the procedure form correctly
    Then I will remain on the create procedure page