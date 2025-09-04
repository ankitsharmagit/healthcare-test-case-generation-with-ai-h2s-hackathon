Feature: Digitize patient records and improve workflow efficiency.

  # As a Doctor, I want to access patient assessments and care plans electronically so that I can review patient information more efficiently and provide better care.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: 631c2a20-e344-4fb7-b16a-6d2d5441d2b6_AC1
    Given I am logged into the clinician portal.
    When I search for and select a patient.
    Then I can view the patient's digitized assessments and care plans.

