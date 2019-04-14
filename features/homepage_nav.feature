# Created by Alex at 4/14/2019
Feature: Patients Page Access
  # Enter feature description here

  Scenario: Home Page to Patients

    Given I am in the homepage
    When I click the patients tab
    Then I am directed to the patients page

    Given I am in the homepage
    When I click the procedures tab
    Then I am directed to the procedures page

    Given I am in the homepage
    When I click the roadmaps tab
    Then I am directed to the roadmaps page

    Given I am in the homepage
    When I click the profile tab
    Then The dropdown opens
    When I click logout
    Then I am logged out