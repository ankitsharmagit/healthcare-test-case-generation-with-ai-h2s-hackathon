Feature: Clinician Portal Development

  # As a Doctor, I want to access and view patient data quickly and efficiently through the clinician portal, so that I can make informed decisions about patient care.
  @priority_Must @req_2.1.2 @HIPAA
  Scenario: 5dd0d188-2605-4668-8305-d3155760a7e6_AC1
    Given I am logged into the clinician portal.
    When I search for a patient.
    Then I can view the patient's relevant clinical information and documents in an organized manner.

  @priority_Must @req_2.1.2 @HIPAA
  Scenario: 5dd0d188-2605-4668-8305-d3155760a7e6_AC2
    Given I am viewing a patient's record.
    When I navigate to different sections of the record (e.g., vitals, medications, history).
    Then The information loads quickly and is presented in a clear and understandable format.

