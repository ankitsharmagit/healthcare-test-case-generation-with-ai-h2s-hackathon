Feature: Digitize patient records and automate tracking.

  # As a Nurse, I want to access digitized patient assessments and care plans so that I can efficiently review patient information and update vitals.
  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: 079385b2-4416-46d0-a3bd-b3435e65d921_AC1
    Given the Nurse is logged into the Clinician Portal
    When the Nurse selects a patient
    Then the system displays the patient's digitized assessments and care plans

