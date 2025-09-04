Feature: Replace Trillium's current system with a new system including database, clinician portal, and session application.

  # As a Doctor, I want to view patient data stored in the system so that I can effectively manage patient care.
  @priority_Must @req_1.4 @FDA21CFR11 @HIPAA
  Scenario: 07debc6d-0429-41d6-a9f8-9cb6d05235a0_AC1
    Given I am logged into the clinician portal.
    When I select a patient.
    Then I can view all relevant patient data, including scanned documents and session information.

