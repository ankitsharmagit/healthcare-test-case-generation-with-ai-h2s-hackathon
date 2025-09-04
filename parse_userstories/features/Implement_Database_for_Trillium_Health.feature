Feature: Implement Database for Trillium Health

  # As a Doctor, I want to access patient clinical information in the clinician portal so that I can efficiently review patient data and make informed decisions.
  @priority_Must @req_2.1.1 @FDA21CFR11 @HIPAA
  Scenario: a99367a2-ad05-4a4b-a4d2-91390abb0115_AC1
    Given the Doctor is logged into the clinician portal.
    When the Doctor searches for a specific patient.
    Then the Doctor should be able to view the patient's clinical information, including relevant documents and related data.

