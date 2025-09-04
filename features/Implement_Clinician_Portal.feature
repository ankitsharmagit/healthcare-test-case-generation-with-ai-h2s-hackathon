Feature: Implement Clinician Portal

  # As a Doctor, I want to view patient data in the clinician portal so that I can efficiently review patient information and make informed decisions.
  @priority_Must @req_2 @HIPAA
  Scenario: 1da2101e-acbc-4ca4-98f2-7b9566d90d37_AC1
    Given I am logged into the clinician portal.
    When I select a patient.
    Then I can view the patient's relevant documents and clinical information in an organized manner.

  # As a Doctor, I want to view organized patient data in the clinician portal so that I can efficiently review patient information and make informed decisions.
  @priority_Must @req_2.1 @HIPAA
  Scenario: 469c1b9c-a536-4cf4-9284-e69ad1aa7887_AC1
    Given I am logged into the clinician portal as a Doctor.
    When I select a patient.
    Then I can view the patient's relevant documents and clinical information organized in a meaningful way.

