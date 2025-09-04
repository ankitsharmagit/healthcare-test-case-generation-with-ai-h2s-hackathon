Feature: General

  # As a Doctor, I want to access patient information through the Clinician Portal, so that I can efficiently review patient data and make informed decisions.
  @priority_Must @req_AUTO-1 @HIPAA
  Scenario: 460ee28f-96eb-4eef-b811-dfc81370084d_AC1
    Given I am a logged-in Doctor using the Clinician Portal.
    When I navigate to a patient's record.
    Then I should be able to view all relevant patient information in an easy-to-navigate format.

  # As a Doctor, I want to view audit reports of patient data changes so that I can ensure data integrity and compliance with regulations.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: b98534fc-6d60-4891-8c24-eeb09545d284_AC1
    Given I am logged in as a Doctor.
    When I request an audit report for a specific patient.
    Then I should see a report showing the history of additions, changes, and deletions of documents and data, per user.

  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: b98534fc-6d60-4891-8c24-eeb09545d284_AC2
    Given I am viewing an audit report.
    When I request to export the audit history.
    Then The system should allow me to export the audit history.

  # As a Nurse, I want to digitize patient assessments and care plans, so that I can improve tracking and care of patients in the Day Health program.
  @priority_Must @req_1 @FDA21CFR11 @HIPAA
  Scenario: 0f3b316d-bc71-403c-bba3-79ee51c2b312_AC1
    Given I am a nurse in the Day Health program.
    When I access the Trillium Health Day Health Manager system.
    Then I can create and update patient assessments and care plans digitally.

  # As a Day Health staff member, I want to digitize patient assessments, care plans, and sign in/outs so that I can automate tracking of individuals through the program and improve the current physical workflow.
  @priority_Must @req_1.2
  Scenario: 91ddee59-35c7-46a5-ba77-9e7e1d5a1fa6_AC1
    Given I am a Day Health staff member
    When I access the Trillium Health Day Health Manager system
    Then I can digitize patient assessments, care plans, and patient sign in/outs.

  @priority_Must @req_1.2
  Scenario: 91ddee59-35c7-46a5-ba77-9e7e1d5a1fa6_AC2
    Given I have digitized patient information
    When The system tracks individuals through the program
    Then The tracking is automated.

  # As a Doctor, I want to access the Clinician Portal so that I can review patient data efficiently.
  @priority_Must @req_1.3 @FDA21CFR11 @HIPAA
  Scenario: 617c68ce-6fcd-451f-ada4-dac4570deb7a_AC1
    Given I am a Doctor with appropriate credentials
    When I log into the system
    Then I should be able to access the Clinician Portal and view patient data.

  # As a Doctor, I want to add, modify, or check any patient data stored in the system so that I can effectively manage patient information and provide appropriate care.
  @priority_Must @req_1.5 @FDA21CFR11 @HIPAA
  Scenario: 2eb15241-ef36-4556-8426-c6c401ee4952_AC1
    Given I am logged in as a Doctor.
    When I access the patient data section.
    Then I should be able to add new patient information, modify existing patient information, and view all patient data stored in the system.

