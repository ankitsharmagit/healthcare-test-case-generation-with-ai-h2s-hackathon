Feature: General

  # As a Doctor, I want to access patient information through a web-based Clinician Portal, so that I can efficiently review patient data and modify information in the database.
  @priority_Must @req_AUTO-1 @FDA21CFR11 @HIPAA
  Scenario: 1c769068-d34b-4f3f-8773-a47b85b317e9_AC1
    Given I am a Doctor logged into the Clinician Portal.
    When I navigate to a patient's record.
    Then I can view and modify patient information in the database.

  @priority_Must @req_AUTO-1 @FDA21CFR11 @HIPAA
  Scenario: 1c769068-d34b-4f3f-8773-a47b85b317e9_AC2
    Given I am a Doctor using the Clinician Portal.
    When I access the application through a browser.
    Then The interface is easy to learn and navigate quickly.

  # As a Doctor, I want to view audit reports of patient data changes, so that I can ensure data integrity and compliance.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: 500e0684-4312-4151-a3b7-c3dd1dcf7009_AC1
    Given I am logged in as a Doctor.
    When I request an audit report for a specific patient.
    Then I should see a report showing the history of additions, changes, and deletions of documents and data, per user.

  # As a Day Health staff member, I want to digitize patient assessments and care plans, so that I can automate tracking of individuals through the program and improve the current physical workflow.
  @priority_Must @req_1
  Scenario: dfdaa63c-66d2-43b9-b9b4-ce5fa47516dc_AC1
    Given I am a Day Health staff member using the Trillium Health Day Health Manager system.
    When I access the system to manage patient information.
    Then I should be able to create and store digital versions of patient assessments and care plans.

  @priority_Must @req_1
  Scenario: dfdaa63c-66d2-43b9-b9b4-ce5fa47516dc_AC2
    Given Digital patient assessments and care plans are stored in the system.
    When A patient signs in or out of the Day Health program.
    Then The system should automatically track the individual's progress through the program.

  # As a Day Health staff member, I want to digitize patient assessments, care plans, and sign in/outs so that I can automate tracking of individuals through the program and improve the current physical workflow.
  @priority_Must @req_1.2
  Scenario: 5aba8e2f-ea8b-49af-851e-9c4e8523fc7a_AC1
    Given I am a Day Health staff member
    When I access the Trillium Health Day Health Manager system
    Then I can digitize patient assessments, care plans, and patient sign in/outs.

  @priority_Must @req_1.2
  Scenario: 5aba8e2f-ea8b-49af-851e-9c4e8523fc7a_AC2
    Given I have digitized patient information
    When The system tracks individuals through the program
    Then The tracking is automated.

  # As a Doctor, I want to access patient data through the Clinician Portal so that I can review patient history and current status.
  @priority_Must @req_1.3 @FDA21CFR11 @HIPAA
  Scenario: 3d21ba8d-59f4-4cdf-998b-7d43d16e41e9_AC1
    Given I am a logged-in Doctor in the Clinician Portal.
    When I search for and select a patient.
    Then I can view the patient's relevant data stored in the database.

  # As a Doctor, I want to add, modify, or check any patient data stored in the system, so that I can effectively manage patient information and provide appropriate care.
  @priority_Must @req_1.5 @FDA21CFR11 @HIPAA
  Scenario: 4635d6f2-0127-4824-a06f-fdd1c02244d6_AC1
    Given I am logged in as a Doctor.
    When I access the patient data management section.
    Then I should be able to add new patient records, modify existing patient information, and view patient details.

  # As a Doctor, I want to view patient data in the clinician portal so that I can effectively manage patient care.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: 43c457f2-1664-4641-9584-575ef7fa8daf_AC1
    Given I am a logged-in Doctor in the clinician portal.
    When I select a patient.
    Then I should see the patient's relevant clinical information and documents organized in a meaningful way.

