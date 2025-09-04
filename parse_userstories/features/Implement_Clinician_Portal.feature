Feature: Implement Clinician Portal

  # As a Doctor, I want to view patient data in the clinician portal so that I can efficiently review patient information and provide better care.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: a13a3f38-09bb-424e-86a2-89d59342669a_AC1
    Given I am logged into the clinician portal.
    When I select a patient.
    Then I can view the patient's relevant documents and clinical information in an organized manner.

  # As a Doctor, I want to view organized patient data in the clinician portal so that I can efficiently review patient information and make informed decisions.
  @priority_Must @req_2.1 @HIPAA
  Scenario: f0d52e99-1fe9-4d95-90ed-a582b8426fda_AC1
    Given I am logged into the clinician portal as a Doctor.
    When I select a patient.
    Then I can view the patient's relevant documents and clinical information organized in a meaningful way.

  # As a Doctor, I want to view patient care plans so that I can effectively review and manage patient treatment.
  @priority_Must @req_2.2 @req_2.3.2.8 @req_2.3.2.11 @FDA21CFR11 @HIPAA
  Scenario: 2d3c7e56-665c-4979-9bea-46655b6f5722_AC1
    Given I am logged into the clinician portal as a Doctor.
    When I select a patient from the patient list.
    Then I can view the patient's current care plan, including updates and changes.

