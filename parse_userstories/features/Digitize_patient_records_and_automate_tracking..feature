Feature: Digitize patient records and automate tracking.

  # As a Nurse, I want to access digitized patient assessments and care plans so that I can efficiently review patient information and update vitals.
  @priority_Must @req_1.1 @FDA21CFR11 @HIPAA
  Scenario: 7c4c1495-1f6d-4462-bd63-191fd15ea6ba_AC1
    Given I am logged into the Clinician Portal.
    When I search for a patient's record.
    Then I can view digitized assessments and care plans for that patient.

