Feature: Digitize patient records and automate tracking.

  # As a Nurse, I want to access digitized patient assessments and care plans so that I can efficiently review patient information and update vitals.
  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: 08e6b31b-436b-421d-af68-f862c5d528e1_AC1
    Given the Nurse is logged into the Clinician Portal
    When the Nurse selects a patient
    Then the Nurse can view digitized assessments and care plans for that patient.

