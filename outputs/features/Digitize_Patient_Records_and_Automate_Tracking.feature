Feature: Digitize Patient Records and Automate Tracking

  # As a Day Health Staff, I want to digitize patient assessments, care plans, and sign-in/out sheets so that I can improve the current physical workflow and automate patient tracking.
  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: 8d672d9a-f2ca-4e9e-be2e-85c0e97afacf_AC1
    Given the Day Health Staff is using the system
    When they upload a patient assessment, care plan, or sign-in/out sheet
    Then the system should store it digitally and associate it with the correct patient record.

  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: 8d672d9a-f2ca-4e9e-be2e-85c0e97afacf_AC2
    Given patient sign-in/out sheets are digitized
    When a patient signs in or out
    Then the system should automatically track their attendance and update their status in the program.

