Feature: Implement EHR system for Trillium Health

  # As a Doctor, I want to access patient data through a clinician portal so that I can efficiently review patient information and provide better care.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: 392654cf-2835-4754-9c38-53193a2f10ba_AC1
    Given the Doctor is logged into the clinician portal
    When the Doctor searches for a patient
    Then the Doctor should be able to view the patient's relevant documents and clinical information in an organized manner.

