Feature: Replace Trillium's current system with a new system including database, clinician portal, and session application.

  # As a Doctor, I want to access patient data through the clinician portal so that I can review patient information efficiently.
  @priority_Must @req_1.4 @FDA21CFR11 @HIPAA
  Scenario: 855160d4-16c6-4f25-a186-5279dcbbcfd3_AC1
    Given I am logged into the clinician portal.
    When I search for and select a patient.
    Then I can view the patient's data, including scanned documents and session information.

