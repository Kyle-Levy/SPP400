# Created by Alex at 4/14/2019
Feature: Patient's Page
  # Enter feature description here

  Scenario: Create a New Patient

    Given I am on the patients page
    When I click on add a new patient
    Then I am redirected to the new patients page
    When I submit a valid new patient
