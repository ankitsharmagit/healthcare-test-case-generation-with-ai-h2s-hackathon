Feature: Replace Trillium's current system with a new system including database, clinician portal, and session application.

  # As a Doctor, I want to view patient data stored in the system so that I can effectively manage patient care.
  @priority_Must @req_1.4 @FDA21CFR11 @HIPAA
  Scenario: e5e412d7-0c63-42d6-9854-180ded7738ff_AC1
    Given the Doctor is logged into the clinician portal
    When the Doctor selects a patient
    Then the Doctor should be able to view all relevant patient data, including scanned documents and session information.

