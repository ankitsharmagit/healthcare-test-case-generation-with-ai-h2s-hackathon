Feature: Digitize Patient Records

  # As a Nurse, I want to update patient vitals in the system so that patient information is readily available and accurate.
  @priority_Must @req_1 @FDA21CFR11 @HIPAA
  Scenario: 3d7b1582-845a-4bfc-a38f-53898344ff48_AC1
    Given I am logged into the Trillium Health Day Health Manager system.
    When I enter patient vitals into the system.
    Then The vitals are saved securely and associated with the correct patient record.

  @priority_Must @req_1 @FDA21CFR11 @HIPAA
  Scenario: 3d7b1582-845a-4bfc-a38f-53898344ff48_AC2
    Given I am logged into the Trillium Health Day Health Manager system.
    When I update existing patient vitals.
    Then The system tracks the changes and maintains an audit log.

