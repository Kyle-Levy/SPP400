# Created by Alex at 4/14/2019
Feature: Patient's Page
  # Enter feature description here

  Scenario: Create a Valid New Patient

    Given a successful login
    When I click on the patients tab
    Then I am redirected to the patients page
    When I click on add a new patient
    Then I am redirected to the new patients page
    When I submit a valid new patient
    Then I am redirected to the patients landing page

  Scenario: Create an invalid New Patient
    Given a successful login
    When I click on the patients tab
    Then I am redirected to the patients page
    When I click on add a new patient
    Then I am redirected to the new patients page
    When I submit an invalid patients form
    Then I will remain on the create a patient page

  #TODO: successful search scenario
  #TODO: unsuccessful search scenario