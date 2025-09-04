Feature: Digitize Patient Records and Automate Tracking

  # As a Day Health staff member, I want to digitize patient assessments, care plans, and sign-in/out sheets so that I can improve the current physical workflow and automate patient tracking.
  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: acc17413-d88d-4d21-9511-31847a76780b_AC1
    Given I am a Day Health staff member
    When I access the system
    Then I can scan and store patient assessments, care plans, and sign-in/out sheets digitally.

  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: acc17413-d88d-4d21-9511-31847a76780b_AC2
    Given Patient assessments, care plans, and sign-in/out sheets are stored digitally
    When A patient signs in or out
    Then The system automatically updates the patient's status and tracks their program participation.

