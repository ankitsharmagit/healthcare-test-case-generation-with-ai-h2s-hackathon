Feature: Implement Clinician Portal

  # As a Doctor, I want to access patient data through the clinician portal so that I can efficiently review patient information and provide better care.
  @priority_Must @req_2.1 @HIPAA
  Scenario: afcd9496-0c34-4f0a-9ad5-c9a1b3bdd461_AC1
    Given I am logged into the clinician portal as a Doctor.
    When I search for and select a patient.
    Then I can view the patient's relevant clinical information and documents stored in the database.

