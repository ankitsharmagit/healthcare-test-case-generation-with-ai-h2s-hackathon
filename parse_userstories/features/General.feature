Feature: General

  # As a Patient, I want to check in to Day Health and specific sessions using a fingerprint scanner, so that I can easily verify my attendance.
  @priority_Must @req_2.1.3 @FDA21CFR11 @HIPAA
  Scenario: bf688cd2-f118-4e36-9bfd-432eebbbf55d_AC1
    Given I am a patient at Day Health and have a scheduled session.
    When I use the fingerprint scanner at check-in.
    Then My attendance for Day Health and the specific session is automatically recorded.

  # As a system, I want to store previous states of all tables with all changes made to them so that data can be recovered and audited.
  @priority_Must @req_2.3.2.1 @FDA21CFR11 @HIPAA
  Scenario: 3d373e82-3575-4b20-9827-bdae31729eb9_AC1
    Given A table in the database has been modified
    When The system saves the changes
    Then The previous state of the table is stored along with the changes made.

  # As a Patient, I want to sign in for the day using a fingerprint scanner, so that my attendance is recorded accurately.
  @priority_Must @req_2.3.2.2
  Scenario: d91e5c35-9555-4982-a8f8-914a055ddd85_AC1
    Given I am a patient arriving for the day.
    When I use the fingerprint scanner.
    Then My attendance is recorded in the system.

  # As a Patient, I want to sign out for the day so that my attendance is accurately recorded.
  @priority_Must @req_2.3.2.3
  Scenario: f97ac7d0-f8b7-4ec7-a54a-59bb9f9413b5_AC1
    Given I am a patient in the system.
    When I sign out for the day.
    Then My sign-out time is stored in the system.

  # As a Patient, I want to sign in for sessions, so that my attendance is recorded.
  @priority_Must @req_2.3.2.4 @FDA21CFR11 @HIPAA
  Scenario: f5517b01-024f-492c-86ba-ac2788e2b5d3_AC1
    Given I am a patient scheduled for a session
    When I use the fingerprint scanner
    Then the system records my attendance for the session

  # As a Facilitator, I want to confirm session attendance taken through fingerprint scanner so that I can ensure accurate records of patient participation.
  @priority_Must @req_2.3.2.5
  Scenario: 527f103d-1603-40cf-8198-6b8dfa457f4d_AC1
    Given The system has recorded session attendance via fingerprint scanner.
    When I access the session attendance records.
    Then I can confirm the attendance data is accurate.

  # As a Clinician, I want to store new documents in the database, so that I can maintain a comprehensive record of patient information.
  @priority_Must @req_2.3.2.6 @FDA21CFR11 @HIPAA
  Scenario: 8a313ed6-cc82-4a0a-aa97-e9cc92a97687_AC1
    Given I am a logged-in Clinician.
    When I upload a new patient document.
    Then The document is successfully stored in the database, adhering to HIPAA and FDA 21 CFR Part 11 constraints.

  # As a Clinician, I want to add a patient's care plan so that I can manage and track their treatment effectively.
  @priority_Must @req_2.3.2.7 @FDA21CFR11 @HIPAA
  Scenario: db06f16a-6a36-452a-9a1f-e617be30c0f6_AC1
    Given I am logged in as a Clinician.
    When I add a new care plan for a patient.
    Then The care plan is stored in the system and linked to the patient's record.

  # As a Doctor, I want to store patient care plans so that I can easily access and manage them within the system.
  @priority_Must @req_2.3.2.8 @HIPAA
  Scenario: 0f91a6e9-817f-46c8-9026-3f6ee1ebd75d_AC1
    Given The doctor is logged into the system and has selected a patient.
    When The doctor creates or updates a patient care plan.
    Then The system should store the care plan securely in the database, adhering to HIPAA regulations.

  # As a Doctor, I want to track reviews of care plans so that I can ensure patient care plans are regularly evaluated and updated.
  @priority_Must @req_2.3.2.9 @FDA21CFR11 @HIPAA
  Scenario: de66dc53-f2fc-4061-b098-f552e7c68520_AC1
    Given A care plan exists for a patient.
    When A doctor reviews the care plan.
    Then The system records the review date and the doctor who performed the review.

  # As a Doctor, I want to track approval of care plans so that I can ensure proper authorization and adherence to treatment protocols.
  @priority_Must @req_2.3.2.10 @FDA21CFR11 @HIPAA
  Scenario: a8bd0686-5690-476f-bb03-1517119db8f3_AC1
    Given A care plan exists for a patient
    When The care plan is submitted for approval
    Then The system should record the approval status, approver, and timestamp.

  # As a Doctor, I want to store care plan updates and changes so that the patient's EHR is up-to-date.
  @priority_Must @req_2.3.2.11 @HIPAA
  Scenario: 44055438-1f5c-4d0a-921c-812679456594_AC1
    Given The doctor has made updates to a patient's care plan
    When The doctor saves the updated care plan
    Then The system stores the care plan updates and changes in the database.

  # As a Doctor, I want to store tracks so that I can monitor patient progress and outcomes.
  @priority_Should @req_2.3.2.12 @FDA21CFR11 @HIPAA
  Scenario: 1affbf21-7111-4374-8fb6-9c1833e7c2d0_AC1
    Given The system is running and accessible.
    When I input track data for a patient.
    Then The track data is stored securely in the database and associated with the correct patient.

  # As a Clinician, I want to store classes so that patient care plans can be comprehensive.
  @priority_Should @req_2.3.2.13 @FDA21CFR11 @HIPAA
  Scenario: 75e23dd8-b344-426e-8a52-b1a317b22673_AC1
    Given The system is running and the clinician is logged in.
    When The clinician creates a new class or updates an existing class.
    Then The system stores the class details in the database.

  # As a Clinician, I want to link patients to classes so that I can manage patient schedules and track their progress in relevant programs.
  @priority_Must @req_2.3.2.14
  Scenario: efef7ae0-f6e9-4102-a783-b9c2f4ec7234_AC1
    Given I am a clinician with appropriate privileges.
    When I am viewing a patient's record or a class schedule.
    Then I can easily link the patient to the class.

  # As a Nurse, I want to store schedules, so that I can manage patient appointments and staff availability.
  @priority_Must @req_2.3.2.15
  Scenario: 48cfc3ec-fb4e-4c02-8792-47151ab03b1c_AC1
    Given I am logged in as a Nurse.
    When I enter the schedule information.
    Then The system stores the schedule information in the database.

  # As a Doctor, I want to access stored patient sessions so that I can review patient progress and adjust care plans.
  @priority_Should @req_2.3.2.16 @FDA21CFR11 @HIPAA
  Scenario: 9021299a-87c3-49df-a0b1-9f52e8aa61f9_AC1
    Given Patient data exists in the system
    When I request to view a patient's sessions
    Then I should see a list of the patient's sessions, including date, time, and session details.

  # As a user, I want to store all data associated with sessions so that the system maintains a complete record of patient activity and attendance.
  @priority_Must @req_2.3.2.17 @FDA21CFR11 @HIPAA
  Scenario: 693d2cf2-1b1c-453e-8edf-55e28808ee46_AC1
    Given The user is interacting with the system
    When The system processes session-related data (e.g., attendance, schedules, modifications)
    Then The system stores all relevant data associated with the session in the database.

  # As a Doctor, I want to store group notes for sessions so that I can easily access and review session details.
  @priority_Should @req_2.3.2.18 @FDA21CFR11 @HIPAA
  Scenario: ec1e7a0f-fb31-4f4a-afcb-c4fd01c5203f_AC1
    Given I am logged into the system and viewing a patient's session.
    When I enter group notes for the session.
    Then The group notes are stored securely in the database and associated with the session.

  # As a Doctor, I want to store individual notes for sessions, so that I can track patient progress and tailor treatment plans effectively.
  @priority_Must @req_2.3.2.19 @HIPAA
  Scenario: 164c07a3-af81-49ba-9fd9-59d22ec0a148_AC1
    Given A session exists for a patient
    When I enter notes related to the session
    Then The notes are stored securely and associated with that specific session and patient, adhering to HIPAA regulations.

  # As a Doctor, I want to track reviews of care plans so that I can ensure quality of patient care.
  @priority_Should @req_2.3.2.9 @HIPAA
  Scenario: 72a7ef77-9f22-4335-acdf-9f51d8460289_AC1
    Given a care plan exists for a patient
    When a review is performed on the care plan
    Then the system should track the review, including the reviewer and date of review

  # As a Doctor, I want to view the Assessment timeline so that I can easily track patient progress.
  @priority_Must @req_2.3.2.21
  Scenario: 15ca43a3-0201-4435-b955-59f36295e576_AC1
    Given I am logged into the system as a Doctor and viewing a patient's record.
    When I navigate to the Assessments section.
    Then I should see a clear and accurate timeline of the patient's assessments, including dates and key milestones.

  # As a Clinician, I want to calculate who is billable based on dates, so that the billing process is streamlined and accurate.
  @priority_Must @req_2.3.2.22
  Scenario: 4a231938-a4a3-4d19-9bdd-cd7cb0cab25c_AC1
    Given The system has patient data, session information, and billing rules.
    When I initiate the billability calculation process.
    Then The system accurately identifies and displays which patients are billable based on the specified dates and billing rules.

  # As a Clinician, I want to keep track of what claims have been sent for, so that I can efficiently manage billing and ensure accurate revenue cycle management.
  @priority_Must @req_2.3.2.23 @HIPAA
  Scenario: bcf39837-9725-4791-8753-c87c1761987e_AC1
    Given A patient session has occurred and a claim needs to be generated.
    When The claim is submitted for processing.
    Then The system should record the details of the claim, including patient, service, date, and amount submitted.

  # As a Doctor, I want to track the status of claims (accepted or denied) so that I can efficiently manage patient billing and revenue cycle.
  @priority_Must @req_2.3.2.24 @HIPAA
  Scenario: 476e2c5d-59ac-4952-b2f8-bba2f7be8026_AC1
    Given A claim has been submitted for a patient
    When The claim is accepted or denied by the insurance provider
    Then The system should update the claim status to reflect the accepted or denied status.

  @priority_Must @req_2.3.2.24 @HIPAA
  Scenario: 476e2c5d-59ac-4952-b2f8-bba2f7be8026_AC2
    Given I am viewing a patient's billing information
    When I access the claims history
    Then I should be able to see the status (accepted or denied) of each claim.

  # As a system, I want to have stored procedures for calculations within the database so that calculations are efficient and consistent.
  @priority_Must @req_2.3.2.25
  Scenario: 53b7fa06-d0da-46d8-9049-62d52f6249e4_AC1
    Given The database is operational
    When A calculation is required
    Then The system uses a stored procedure to perform the calculation

  @priority_Must @req_2.3.2.25
  Scenario: 53b7fa06-d0da-46d8-9049-62d52f6249e4_AC2
    Given A new calculation is needed
    When A developer creates a stored procedure
    Then The stored procedure is stored in the database

  # As a Clinician, I want to keep track of what claims have been sent for, so that I can ensure accurate billing and revenue cycle management.
  @priority_Must @req_2.3.2.23 @req_2.3.3.4.2
  Scenario: 8984bbd5-e444-47a8-94ba-961caf2554c3_AC1
    Given The system has session data and billing information.
    When I view a session or patient record.
    Then I can see a clear indication of whether a claim has been submitted for the services provided.

  # As a Clinician, I want to run a billing report so that I can track billing information.
  @priority_Must @req_2.3.3.5.4
  Scenario: 4aad4433-8ba0-40a0-9ff7-20a106dace69_AC1
    Given I am a Clinician and have access to the system.
    When I request a billing report.
    Then The system generates a report containing billing information.

  # As a user, I want to see a list of sessions in the Portal so that I can easily find and access the sessions I need.
  @priority_Must @req_2.3.3.6
  Scenario: 836b0423-b4f8-45d0-8e69-bbf2dc4cd2f9_AC1
    Given I am logged into the Portal.
    When I navigate to the sessions section.
    Then I should see a list of all available sessions.

  # As a Doctor, I want to view details of a particular session so that I can review patient progress and session specifics.
  @priority_Must @req_2.3.3.7
  Scenario: b98e8f78-679e-4a87-bba2-68bff17b5f07_AC1
    Given I am logged in as a Doctor and viewing a list of sessions.
    When I select a particular session from the list.
    Then I should be able to see more details about the selected session, including facilitator information, time and scheduling, attendance, and group/individual notes.

  # As a Doctor, I want to view session information, so that I can review patient progress and make informed decisions about their care.
  @priority_Must @req_2.3.3.8
  Scenario: 5e5de401-441f-4c08-816b-afcd430de3a6_AC1
    Given I am logged into the system as a Doctor and have selected a specific session.
    When I view the session details
    Then I should see the facilitator information, time and scheduling, attendance, and group and individual notes.

  # As a Doctor, I want to see Group and Individual notes for a session so that I can understand the patient's progress and tailor treatment plans.
  @priority_Must @req_2.3.3.8.4
  Scenario: e8843f4e-d6aa-470f-b008-ae8c38dc930f_AC1
    Given I am viewing the details of a specific session in the Clinician Portal.
    When I navigate to the 'Notes' section.
    Then I should see both Group and Individual notes recorded for that session.

  # As a Nurse, I want to enter and view patient assessments, so that I can effectively manage patient care and track progress.
  @priority_Must @req_2.3.3.9 @FDA21CFR11 @HIPAA
  Scenario: e7576094-cddd-4780-817b-f98355781994_AC1
    Given I am logged into the system as a Nurse.
    When I navigate to a patient's profile.
    Then I can enter new assessment data for Nursing, Nutrition, Health Literacy, Care Management, and Behavioral aspects.

  @priority_Must @req_2.3.3.9 @FDA21CFR11 @HIPAA
  Scenario: e7576094-cddd-4780-817b-f98355781994_AC2
    Given I am viewing a patient's profile.
    When I access the 'Assessments' section.
    Then I can view all previously recorded assessments for the patient.

  # As a Doctor, I want to view patient assessments including Nursing, Nutrition, Health Literacy, Care Management, and Behavioral Health, so that I can make informed decisions about patient care.
  @priority_Must @req_2.3.3.9.1 @FDA21CFR11 @HIPAA
  Scenario: 1c0eff54-c610-43d6-93b9-df2e591e4ff6_AC1
    Given I am logged in as a Doctor and viewing a patient's record.
    When I navigate to the 'Assessments' section.
    Then I can see assessments related to Nursing, Nutrition, Health Literacy, Care Management, and Behavioral Health.

  # As a Nurse, I want to enter and view patient assessments (Nursing, Nutrition, Health Literacy, Care Management, Behavioral) so that I can effectively conduct the Care-plan process.
  @priority_Must @req_2.3.3.9 @req_2.3.3.10 @HIPAA
  Scenario: 8b92bc9c-fa76-4b40-8818-91e71a0a5698_AC1
    Given I am logged into the system as a Nurse.
    When I access a patient's record.
    Then I can view existing assessments (Nursing, Nutrition, Health Literacy, Care Management, Behavioral).

  @priority_Must @req_2.3.3.9 @req_2.3.3.10 @HIPAA
  Scenario: 8b92bc9c-fa76-4b40-8818-91e71a0a5698_AC2
    Given I am logged into the system as a Nurse.
    When I access a patient's record and navigate to the assessments section.
    Then I can enter new assessment data (Nursing, Nutrition, Health Literacy, Care Management, Behavioral).

  # As a Clinician, I want to perform care plan review so that I can ensure the patient's care plan is up-to-date and effective.
  @priority_Must @req_2.3.3.10.1 @FDA21CFR11 @HIPAA
  Scenario: b4bdf2e3-d97f-4dc7-8514-b1e379db0b76_AC1
    Given I am logged in as a Clinician and viewing a patient's record.
    When I initiate a care plan review.
    Then I can access and review the patient's current care plan details.

  # As a Clinician, I want to view a patient's care plan history, so that I can track changes and understand the patient's treatment progression.
  @priority_Must @req_2.3.3.10.3
  Scenario: 11453d48-f38d-42f2-affe-29a275b341d9_AC1
    Given A patient has one or more care plans recorded in the system
    When I navigate to the patient's record and select the option to view care plan history
    Then I should see a chronological list of all care plans for that patient, including the dates they were active.

  @priority_Must @req_2.3.3.10.3
  Scenario: 11453d48-f38d-42f2-affe-29a275b341d9_AC2
    Given I am viewing the care plan history
    When I select a specific care plan from the history
    Then I should be able to view the details of that care plan as it existed at that point in time.

  # As a Clinician, I want to make updates or changes to a Care Plan, so that the patient's care plan is current and accurate.
  @priority_Must @req_2.3.3.10.4
  Scenario: ad301c82-bf7b-4464-aceb-3a564aa7d83b_AC1
    Given A Care Plan exists for a patient
    When I make updates or changes to the Care Plan
    Then The system saves the updated Care Plan with the changes.

  # As a system administrator, I want the system to audit all data changes, so that I can track data modifications for compliance and security purposes.
  @priority_Must @req_2.3.3.11 @FDA21CFR11 @HIPAA
  Scenario: d3b3b842-4b5e-49d7-a51b-55743b9cad9a_AC1
    Given The system is running and a user modifies patient data or documents.
    When A user adds, changes, or deletes data.
    Then The system should record the user's identity, the timestamp of the action, the type of action (add, change, delete), and the specific data that was modified.

  @priority_Must @req_2.3.3.11 @FDA21CFR11 @HIPAA
  Scenario: d3b3b842-4b5e-49d7-a51b-55743b9cad9a_AC2
    Given I need to review the audit history.
    When I request an audit report for a specific user or patient.
    Then The system should generate a report displaying the audit history, including user, timestamp, action, and data modified.

  @priority_Must @req_2.3.3.11 @FDA21CFR11 @HIPAA
  Scenario: d3b3b842-4b5e-49d7-a51b-55743b9cad9a_AC3
    Given I need to export the audit history.
    When I request to export the audit history.
    Then The system should export the audit history in a standard format (e.g., CSV, Excel) for external analysis.

  # As a Doctor, I want the system to track the addition of new documents to a patient's EHR, so that I can maintain an accurate and auditable record of patient information.
  @priority_Must @req_2.3.3.12 @FDA21CFR11 @HIPAA
  Scenario: c8b6c027-9235-4b22-aa0c-0d288fd24850_AC1
    Given A doctor adds a new document to a patient's EHR
    When The document is saved in the system
    Then The system should record the addition of the document, including the user who added it and the timestamp of the addition.

  # As a Facilitator, I want to override the patient sign out for the session, so that I can manage patient sessions effectively.
  @priority_Should @req_2.3.3.13 @FDA21CFR11 @HIPAA
  Scenario: 91c56775-a690-42ef-94f5-c5aba3e3f274_AC1
    Given A patient is signed in for a session
    When I, as a Facilitator, override the patient sign out
    Then The system should record the override action, including the facilitator's identity and timestamp.

  # As a Clinician, I want the system to track deletions of existing documents or data, so that there is an audit trail for data integrity and compliance.
  @priority_Must @req_2.3.3.14 @FDA21CFR11 @HIPAA
  Scenario: c86f20e6-4261-4064-adcc-9452f9e0da3c_AC1
    Given I am a clinician and I delete a patient document.
    When I confirm the deletion.
    Then The system records the deletion event, including the user, timestamp, and document details, in the audit log.

  # As a Doctor, I want to view reports showing auditing history per patient so that I can monitor changes to patient data and ensure data integrity.
  @priority_Must @req_2.3.3.15 @FDA21CFR11 @HIPAA
  Scenario: 06c4fa1f-ea09-4f9a-915a-9e36473db1a3_AC1
    Given I am logged in as a Doctor.
    When I navigate to the patient's record.
    Then I can view a report displaying the audit history for that patient, including additions, changes, and deletions of documents and data.

  # As a Clinician, I want to view the audit history of a document so that I can track changes and ensure data integrity.
  @priority_Must @req_2.3.3.11 @req_2.3.3.12 @req_2.3.3.13 @req_2.3.3.14 @req_2.3.3.15 @req_2.3.3.16 @FDA21CFR11 @HIPAA
  Scenario: c187bd13-bdf5-45db-9b6a-415b06ec88d3_AC1
    Given I am logged in as a Clinician and viewing a patient's document
    When I select the option to view audit history
    Then I should see a detailed log of all additions, changes, and deletions made to the document, including the user who made the change and the timestamp.

  @priority_Must @req_2.3.3.11 @req_2.3.3.12 @req_2.3.3.13 @req_2.3.3.14 @req_2.3.3.15 @req_2.3.3.16 @FDA21CFR11 @HIPAA
  Scenario: c187bd13-bdf5-45db-9b6a-415b06ec88d3_AC2
    Given I am viewing the audit history of a document
    When I request to export the audit history
    Then The audit history should be exported in a standard format (e.g., CSV, PDF) that can be easily reviewed and shared, as per requirement 2.3.3.16.

  # As a Doctor, I want to clearly see the link between patient goals and sessions, so that I can better understand the patient's progress and tailor treatment plans accordingly.
  @priority_Must @req_2.3.3.17
  Scenario: 96ab0005-0457-41fd-a8a5-a96750a0f74e_AC1
    Given A patient has defined goals and is participating in sessions.
    When I view the patient's session details in the portal.
    Then I can clearly see how the session relates to the patient's defined goals.

  # As a Facilitator, I want to confirm session attendance taken through fingerprint scanner, so that I can ensure accurate attendance records.
  @priority_Should @req_2.3.4.5
  Scenario: 81a8d867-2325-4a77-b523-694586862462_AC1
    Given I am a Facilitator with read access to session attendance data.
    When I access the system to review session attendance.
    Then I can confirm the attendance records taken through the fingerprint scanner.

  # As a Clinician, I want to have read access to all documents and write access upon creation or special cases, so that I can view, interpret, create, and add new documents for patient care.
  @priority_Must @req_2.4 @FDA21CFR11 @HIPAA
  Scenario: e69a0b3f-0905-4db8-8a84-a67d8e2cb703_AC1
    Given I am logged in as a Clinician.
    When I attempt to access a patient document.
    Then I should be able to view the document.

  @priority_Must @req_2.4 @FDA21CFR11 @HIPAA
  Scenario: e69a0b3f-0905-4db8-8a84-a67d8e2cb703_AC2
    Given I am logged in as a Clinician.
    When I create a new patient document.
    Then I should be able to save the document.

  @priority_Must @req_2.4 @FDA21CFR11 @HIPAA
  Scenario: e69a0b3f-0905-4db8-8a84-a67d8e2cb703_AC3
    Given I am logged in as a Clinician.
    When A special case allows me write access to an existing document.
    Then I should be able to modify and save the document.

  # As a System Administrator, I want database schema documentation and a guide for running the database setup script, so that I can properly set up and maintain the database.
  @priority_Must @req_2.7.1
  Scenario: 1d6ddadd-128f-4015-8b1e-81ac6b88c648_AC1
    Given I am a System Administrator responsible for database setup and maintenance.
    When I access the user documentation.
    Then I can view the complete database schema.

  @priority_Must @req_2.7.1
  Scenario: 1d6ddadd-128f-4015-8b1e-81ac6b88c648_AC2
    Given I am a System Administrator responsible for database setup and maintenance.
    When I access the user documentation.
    Then I can follow a step-by-step guide to run the database setup script successfully.

  # As a Doctor, Nurse, or Patient, I want tutorial documentation within the application so that I can easily learn how to use the system and understand proper protocols.
  @priority_Must @req_2.7.2 @FDA21CFR11 @HIPAA
  Scenario: 948ee811-b316-4afc-a4a6-7c0b02afce23_AC1
    Given I am a new user of the application.
    When I access a feature for the first time.
    Then I am presented with step-by-step instructions, screenshots, and in-application tooltips to guide me through the process.

  @priority_Must @req_2.7.2 @FDA21CFR11 @HIPAA
  Scenario: 948ee811-b316-4afc-a4a6-7c0b02afce23_AC2
    Given I need to understand a specific procedure within the application.
    When I access the tutorial documentation.
    Then I can find clear explanations of the procedure, including legal and business concerns.

  # As a facilitator, I want clear navigation and tooltips in the session application so that I can easily verify attendance, record notes, and understand the application's functionality.
  @priority_Should @req_2.7.3
  Scenario: 1217893f-85c5-4ee0-bffa-a8cfff9509cc_AC1
    Given I am a new facilitator using the session application
    When I navigate through the application
    Then I can easily understand the purpose of each section and function due to clear navigation and helpful tooltips.

  # As a Doctor, I want to view patient assessments and care plans within the system, so that I can efficiently review patient data and provide appropriate care.
  @priority_Must @req_2.8.2 @FDA21CFR11 @HIPAA
  Scenario: b3db685e-3487-4261-bd01-9e6620626f13_AC1
    Given I am a Doctor with access to the system.
    When I select a patient record.
    Then I can view the patient's assessments and care plans in a digitized format.

  # As a Doctor, I want to quickly access patient information through the Clinician Portal so that I can efficiently review patient data and make informed decisions.
  @priority_Must @req_5.1.1.2
  Scenario: a13ecae7-0abc-4f22-887e-494b9f21867a_AC1
    Given I am logged into the Clinician Portal.
    When I request to view a patient's information.
    Then The patient's information is displayed in a user-friendly and easily navigable interface.

  # As a Facilitator, I want to confirm session attendance taken through fingerprint scanner, so that I can ensure accurate attendance records.
  @priority_Must @req_4.2.1 @FDA21CFR11 @HIPAA
  Scenario: 455bbfe1-7840-471f-a4bc-ba6963ee3d68_AC1
    Given the session application is running and connected to the fingerprint scanner
    When I access the session attendance records
    Then I can view and confirm the attendance data captured by the fingerprint scanner.

  # As a Clinician Portal user, I want the application to respond quickly, so that I can efficiently access and modify patient information.
  @priority_Must @req_5.1.1.3
  Scenario: d2ae83d7-6d7f-4a02-8dd7-f783b7930e56_AC1
    Given I am a user accessing the Clinician Portal.
    When I navigate to a page within the application.
    Then The page should load in under 2 seconds.

  @priority_Must @req_5.1.1.3
  Scenario: d2ae83d7-6d7f-4a02-8dd7-f783b7930e56_AC2
    Given I am a user accessing the Clinician Portal.
    When I navigate to a page within the application.
    Then On average, the page should load in under 0.5 seconds.

  @priority_Must @req_5.1.1.3
  Scenario: d2ae83d7-6d7f-4a02-8dd7-f783b7930e56_AC3
    Given I am a user accessing the Clinician Portal.
    When I navigate to a page within the application.
    Then The page should never take more than 5 seconds to load.

  # As a Doctor, I want the Clinician Portal to load quickly, so that I can efficiently review patient data.
  @priority_Should @req_5.1.1.4 @HIPAA
  Scenario: befdf438-ead0-41c2-abb6-cbc7671a9055_AC1
    Given I am a Doctor using the Clinician Portal
    When I access a page within the portal
    Then the page loads in under 2 seconds

  @priority_Should @req_5.1.1.4 @HIPAA
  Scenario: befdf438-ead0-41c2-abb6-cbc7671a9055_AC2
    Given I am a Doctor using the Clinician Portal
    When I access a page within the portal
    Then on average, the page loads in under 0.5 seconds

  # As a Doctor, I want database queries to execute quickly, so that I can efficiently access patient information and make timely decisions.
  @priority_Must @req_5.1.1.5
  Scenario: b47f2700-db21-45a0-98a5-f8ad4f9e993a_AC1
    Given the system has fewer than 25 active database connections
    When I execute a database query
    Then the query returns results in less than 10 seconds

  # As a Doctor, I want the Clinician Portal pages to load quickly, so that I can efficiently review patient data.
  @priority_Must @req_5.1.2.3 @HIPAA
  Scenario: c3444975-1707-4370-97ab-0c493c116d2f_AC1
    Given I am a Doctor using the Clinician Portal
    When I access a page within the portal
    Then the page loads in under 5 seconds

  # As a Doctor, I want the Clinician Portal to load quickly, so that I can efficiently review patient data.
  @priority_Should @req_5.1.2.4 @HIPAA
  Scenario: 7b482248-47bf-452e-a4a6-edb289cc900d_AC1
    Given I am a Doctor accessing the Clinician Portal
    When I navigate to a page within the portal
    Then the page loads in under 2 seconds on average.

  # As a Doctor, I want the clinician portal to be accessible 99.9% of the time during business hours, so that I can reliably access patient data when needed.
  @priority_Must @req_5.1.2.5 @HIPAA
  Scenario: 8a482e31-4de8-45bc-972e-ffdfc0b82b7a_AC1
    Given The clinician portal is deployed and running
    When I attempt to access the portal during business hours
    Then The portal is accessible 99.9% of the time

  # As a Clinician, I want the system to audit document and data changes so that I can track modifications and maintain data integrity.
  @priority_Must @req_2.3.3.11 @req_2.3.3.12 @req_2.3.3.13 @req_2.3.3.14 @req_2.3.3.15 @req_2.3.3.16 @HIPAA
  Scenario: 4eba10f6-82f0-4a46-9b95-204905491bf0_AC1
    Given I am a clinician using the portal
    When I add, modify, or delete a document or data
    Then the system should track the addition, change, or deletion, including user and timestamp.

  @priority_Must @req_2.3.3.11 @req_2.3.3.12 @req_2.3.3.13 @req_2.3.3.14 @req_2.3.3.15 @req_2.3.3.16 @HIPAA
  Scenario: 4eba10f6-82f0-4a46-9b95-204905491bf0_AC2
    Given I am a clinician using the portal
    When I request an audit report
    Then the system should generate a report showing the auditing history, either per user or per patient.

  @priority_Must @req_2.3.3.11 @req_2.3.3.12 @req_2.3.3.13 @req_2.3.3.14 @req_2.3.3.15 @req_2.3.3.16 @HIPAA
  Scenario: 4eba10f6-82f0-4a46-9b95-204905491bf0_AC3
    Given I am a clinician using the portal
    When I request to export an auditing history
    Then the system should allow me to export the auditing history.

  # As a Clinician, I want fingerprint scanning to return results quickly, so that I can efficiently access the system.
  @priority_Must @req_5.1.3.2
  Scenario: 9c0a8fef-46d8-4db1-a1e9-5b3de8984004_AC1
    Given the clinician is using the fingerprint scanner
    When the clinician initiates a fingerprint scan
    Then the system returns results within 1 second

  # As a Clinician Application, I want to ensure patient information is only accessible to authorized users, so that patient privacy is maintained and HIPAA regulations are met.
  @priority_Must @req_5.2.2.1 @HIPAA
  Scenario: 8217b80d-b3b0-49ef-bc65-12cce6b52deb_AC1
    Given A user attempts to access patient information
    When The user is not authorized to view the patient's information
    Then The application will prevent the user from accessing the information.

  # As a System Administrator, I want the database to be encrypted at rest so that patient data is protected and compliant with HIPAA.
  @priority_Must @req_5.3.1.1 @HIPAA
  Scenario: ce16ca83-5426-4bb3-a58f-f1d109024906_AC1
    Given The system is deployed and running
    When Data is stored in the database
    Then The database is encrypted at rest.

  # As a Clinician Portal User, I want all data transfers to be secured with SSL, so that patient data is protected during transmission.
  @priority_Must @req_5.3.1.2 @HIPAA
  Scenario: a00ebd1f-03ef-4ed0-8841-8fb69979f15d_AC1
    Given I am using the Clinician Portal.
    When I am accessing or modifying patient information.
    Then All data transferred between the server and my application will be done over SSL.

  # As a System Administrator, I want the database to only be accessible by devices on the same network so that unauthorized access to sensitive patient data is prevented.
  @priority_Must @req_5.3.1.3 @HIPAA
  Scenario: 7b3e4bc3-5a4a-4aab-963f-5d1e6b7bec37_AC1
    Given The database server is running
    When A connection is attempted from a device outside the network
    Then The connection is rejected

  @priority_Must @req_5.3.1.3 @HIPAA
  Scenario: 7b3e4bc3-5a4a-4aab-963f-5d1e6b7bec37_AC2
    Given The database server is running
    When A connection is attempted from a device within the same network
    Then The connection is established

  # As a Doctor, I want all communication between the server and Clinician Application to be done over SSL, so that patient data is transmitted securely and complies with HIPAA.
  @priority_Must @req_5.3.2.1 @HIPAA
  Scenario: 0440cb0f-cea5-472b-8382-d59794355a0a_AC1
    Given I am a Doctor using the Clinician Application.
    When I access or modify patient information.
    Then All communication between the Clinician Application and the server is encrypted using SSL.

  # As a Session App User, I want all patient information stored locally on the computer to be encrypted so that patient data is protected and compliant with HIPAA.
  @priority_Must @req_5.3.3.1 @HIPAA
  Scenario: 68231c2d-de07-4259-9c47-0f712303e85a_AC1
    Given The Session App is running on a computer.
    When Patient information is stored locally on the computer.
    Then The patient information is encrypted.

  # As a Session App, I want all communication with the server to be done over SSL so that patient information stored locally is secure.
  @priority_Must @req_5.3.3.2 @HIPAA
  Scenario: fd51ae0f-0178-4c66-9f56-302100997b06_AC1
    Given The Session App is communicating with the server
    When Data is being transmitted between the Session App and the server
    Then The communication must be encrypted using SSL

  # As a Doctor, I want the Clinician Application to have a high aesthetic rating so that I find it visually appealing and easy to use.
  @priority_Should @req_5.4.2.1
  Scenario: ef30b23c-d3b7-44b4-bae4-b205defa015b_AC1
    Given the Doctor is using the Clinician Application
    When they interact with the user interface
    Then the application's aesthetics should be rated at ⅘ or above by at least 85% of clinicians.

  # As a Doctor, I want the Clinician application to be easy to use so that I can efficiently review patient data and improve patient care.
  @priority_Must @req_5.4.2.2 @FDA21CFR11 @HIPAA
  Scenario: 9dba99a4-e4ce-4562-bd61-fe8e4cebee06_AC1
    Given I am a Doctor using the Clinician application.
    When I am performing common tasks such as reviewing patient data, updating notes, and ordering tests.
    Then The application should be intuitive and easy to navigate, allowing me to complete tasks quickly and efficiently.

  @priority_Must @req_5.4.2.2 @FDA21CFR11 @HIPAA
  Scenario: 9dba99a4-e4ce-4562-bd61-fe8e4cebee06_AC2
    Given A survey is conducted with clinicians after using the application.
    When Clinicians are asked to rate the application's ease of use.
    Then At least 80% of clinicians should rate the application at ⅘ or above for ease of use.

  # As a Doctor, I want the Clinician application to be easy to learn so that I can quickly access and interpret patient data.
  @priority_Must @req_5.4.2.3 @FDA21CFR11 @HIPAA
  Scenario: 6fccb2f0-462d-435f-ae62-4cdbba4c7571_AC1
    Given I am a Doctor using the Clinician application.
    When I am learning to use the application.
    Then The application should be intuitive and easy to understand, allowing me to quickly become proficient.

  @priority_Must @req_5.4.2.3 @FDA21CFR11 @HIPAA
  Scenario: 6fccb2f0-462d-435f-ae62-4cdbba4c7571_AC2
    Given We survey Doctors on their experience with the Clinician application.
    When 90% of Doctors rate the application at 4/5 or above for ease of learning.
    Then The application meets the ease of learning requirement.

  # As a Facilitator, I want the Session App to have an appealing aesthetic so that I can effectively engage users during sessions.
  @priority_Should @req_5.4.3.1 @FDA21CFR11 @HIPAA
  Scenario: 3414fb1b-9417-4da1-ad75-5a99e7eaafc4_AC1
    Given the facilitator is using the Session App
    When they are interacting with the user interface
    Then the app's aesthetics should be rated at 4/5 or above by at least 85% of facilitators.

  # As a Nurse, I want to be able to easily add and modify patient data, so that I can accurately maintain patient records.
  @priority_Must @req_5.4.3.2 @FDA21CFR11 @HIPAA
  Scenario: aef5a6f5-4f05-4edc-b7cc-0cc2400483e1_AC1
    Given I am a nurse logged into the system.
    When I add or modify patient data.
    Then The system should allow me to do so easily and efficiently.

  @priority_Must @req_5.4.3.2 @FDA21CFR11 @HIPAA
  Scenario: aef5a6f5-4f05-4edc-b7cc-0cc2400483e1_AC2
    Given I am a nurse.
    When I add, modify, or delete patient data.
    Then The system should track these changes for auditing purposes, including user, timestamp, and specific data changed.

  # As a Facilitator, I want the Session App to be easy to learn so that I can quickly and effectively use it to manage sessions.
  @priority_Must @req_5.4.3.3 @FDA21CFR11 @HIPAA
  Scenario: 0d1844fe-1194-402f-982c-5ef87217e3f4_AC1
    Given The facilitator is a new user of the Session App.
    When The facilitator completes the initial training and uses the app for a few sessions.
    Then The facilitator rates the Session App at 4/5 or above for ease of learning.

  @priority_Must @req_5.4.3.3 @FDA21CFR11 @HIPAA
  Scenario: 0d1844fe-1194-402f-982c-5ef87217e3f4_AC2
    Given A survey is conducted among facilitators after using the Session App.
    When The survey results are analyzed.
    Then At least 90% of facilitators rate the Session App at 4/5 or above for ease of learning.

  # As a Doctor, I want to access patient information through a web-based Clinician Portal, so that I can efficiently review patient data and modify information in the database.
  @priority_Must @req_AUTO-1 @FDA21CFR11 @HIPAA
  Scenario: 2f19080b-c4fc-4ee7-ae1a-149ad532b791_AC1
    Given I am a Doctor logged into the Clinician Portal.
    When I navigate to a patient's record.
    Then I should be able to view and modify patient information in the database.

  @priority_Must @req_AUTO-1 @FDA21CFR11 @HIPAA
  Scenario: 2f19080b-c4fc-4ee7-ae1a-149ad532b791_AC2
    Given I am a Doctor using the Clinician Portal.
    When I access the portal through a web browser.
    Then The interface should be easy to learn and navigate quickly.

  # As a Doctor, I want to view audit reports of patient data changes, so that I can ensure data integrity and compliance with regulations.
  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: cff2a72e-425d-4891-9277-503b84810b84_AC1
    Given I am a Doctor logged into the system.
    When I request an audit report for a specific patient.
    Then I should see a report showing the history of additions, changes, and deletions to the patient's documents and data, including the user who made the changes and the timestamp.

  @priority_Must @req_2 @FDA21CFR11 @HIPAA
  Scenario: cff2a72e-425d-4891-9277-503b84810b84_AC2
    Given I am a Doctor logged into the system.
    When I request an audit report for all patients.
    Then I should see a report showing the history of additions, changes, and deletions to all patients' documents and data, including the user who made the changes and the timestamp.

  # As a Day Health Staff, I want to digitize patient assessments and care plans, so that I can automate tracking of individuals through the program and improve the current physical workflow.
  @priority_Must @req_1
  Scenario: 2630be87-92a0-4589-a775-c5f4e26e35e2_AC1
    Given I am a Day Health Staff member.
    When I access the Trillium Health Day Health Manager system.
    Then I can create and store patient assessments and care plans digitally.

  @priority_Must @req_1
  Scenario: 2630be87-92a0-4589-a775-c5f4e26e35e2_AC2
    Given Patient assessments and care plans are stored digitally.
    When A patient signs in/out.
    Then The system automatically tracks the individual's progress through the program.

  # As a Day Health staff member, I want to digitize patient assessments and care plans, so that I can automate tracking of individuals through the program.
  @priority_Must @req_1.2
  Scenario: 2d2bb89c-8b78-43c3-9333-ca79f10c694c_AC1
    Given I am a Day Health staff member.
    When I access the system.
    Then I can create and store patient assessments and care plans digitally.

  # As a Doctor, I want to access the Clinician Portal so that I can review patient data stored in the database.
  @priority_Must @req_1.3 @FDA21CFR11 @HIPAA
  Scenario: 569600a7-d599-433d-a8da-45e6a042c640_AC1
    Given I am a Doctor with appropriate credentials.
    When I log into the system via the Clinician Portal.
    Then I can view patient data stored in the database.

  # As a Doctor, I want to add, modify, or check any patient data stored in the system, so that I can effectively manage patient information.
  @priority_Must @req_1.5 @FDA21CFR11 @HIPAA
  Scenario: b70ee240-a075-4aca-a337-7677bfa78d11_AC1
    Given I am logged into the system as a Doctor.
    When I access the patient data section.
    Then I should be able to add, modify, or check patient data.

  # As a Doctor, I want the application to have tutorial documentation so that I can quickly learn how to use the system and understand proper protocols.
  @priority_Should @req_2.3
  Scenario: 9303be75-30e5-4ffc-b9a4-1649388674aa_AC1
    Given I am a new Doctor user of the application.
    When I access the application for the first time.
    Then I am presented with tutorial documentation that explains procedures in step-by-step instructions with screenshots.

  # As a Trillium IT Administrator, I want a way to install the database so that the system can be set up and ready for use.
  @priority_Must @req_2.3.1.1
  Scenario: 974710c5-6117-46d6-b719-2e3bae299c38_AC1
    Given I am a Trillium IT Administrator with access to the installation package
    When I run the database setup script
    Then the database is installed correctly and ready to host patient and clinical information.

  # As a Doctor, I want to access patient data in the clinician portal so that I can review patient information efficiently.
  @priority_Must @req_2.3.1.2 @FDA21CFR11 @HIPAA
  Scenario: c1f650d5-cdd6-4e38-b0e1-37b7d276c133_AC1
    Given I am logged into the clinician portal.
    When I select a patient.
    Then I can view the patient's relevant documents and clinical information.

  # As a Clinician, I want to access a clinician portal so that I can present and organize patient data from the database.
  @priority_Must @req_2.3.1.3 @FDA21CFR11 @HIPAA
  Scenario: d5bd9469-1afb-4b4d-8647-626c661b4569_AC1
    Given The database contains patient and clinical information.
    When I log into the system.
    Then I should be able to access a clinician portal to view and organize patient data.

  # As a Doctor, I want to access patient care plans through the Clinician Portal, so that I can review and track updates to the plans efficiently.
  @priority_Must @req_5.1.1 @FDA21CFR11 @HIPAA
  Scenario: 9e5fc573-ffd1-4f42-b8c0-ab93d354f3fd_AC1
    Given I am logged into the Clinician Portal.
    When I select a patient.
    Then I can view the patient's care plan, including updates and changes.

  # As a Doctor, I want to view the audit history of patient documents and data, so that I can ensure data integrity and compliance.
  @priority_Must @req_2.3.3 @FDA21CFR11 @HIPAA
  Scenario: a36c5efa-4c57-495a-af53-3195aca5e963_AC1
    Given I am logged into the Clinician Portal and viewing a patient's record.
    When I request to view the audit history for a specific document or data element.
    Then I should see a report showing additions, changes, and deletions, including the user and timestamp for each action.

  @priority_Must @req_2.3.3 @FDA21CFR11 @HIPAA
  Scenario: a36c5efa-4c57-495a-af53-3195aca5e963_AC2
    Given I am logged into the Clinician Portal.
    When I request an audit history report for a specific user or patient.
    Then I should be able to export the audit history in a standard format.

  # As an IT person, I want to configure a new data piece, so that I can integrate new data sources into the system.
  @priority_Should @req_2.3.3.1
  Scenario: 0727dc20-8963-42dd-8568-6c8e8ab4d42f_AC1
    Given I am an IT person with access to the configuration settings.
    When I configure a new data piece.
    Then The system stores the configuration and allows the data piece to be used for data integration.

  # As an IT person, I want to edit an external data source configuration so that I can ensure the system receives the correct data.
  @priority_Should @req_2.3.3.2
  Scenario: 10bf77db-2d1a-429d-aeae-c9f90c4b5759_AC1
    Given I am logged in as an IT person.
    When I navigate to the external data source configuration page.
    Then I can modify the configuration settings and save the changes.

  # As a user, I want to view a list of sessions so that I can select a particular session to see more details.
  @priority_Must @req_2.3.3.3
  Scenario: b0c0a546-d260-4c3c-9fce-24983bb6c668_AC1
    Given The user is logged into the portal
    When I navigate to the sessions page
    Then I should see a list of sessions displayed

  @priority_Must @req_2.3.3.3
  Scenario: b0c0a546-d260-4c3c-9fce-24983bb6c668_AC2
    Given I am viewing the list of sessions
    When I select a session from the list
    Then I should be able to see more details about the selected session

  # As a Doctor, I want to view a Metrics page, so that I can easily review patient data and track progress.
  @priority_Should @req_2.3.3.4
  Scenario: 05294210-26f5-4f73-a50c-5ad0e89e1bf4_AC1
    Given I am logged into the system as a Doctor.
    When I navigate to the Metrics page.
    Then I should be able to view relevant patient metrics.

  # As a Clinician, I want to view overall program statistics, so that I can monitor patient progress and program effectiveness.
  @priority_Should @req_2.3.3.4.1
  Scenario: 933bb33d-1099-4396-8d5b-edf0bc4ce8f1_AC1
    Given I am logged into the Clinician Portal.
    When I navigate to the program statistics section.
    Then I can view overall program statistics.

  # As a Clinician, I want to run a billing report so that I can track total dollars billed.
  @priority_Must @req_2.3.3.4.3 @HIPAA
  Scenario: 89ae4778-6dcb-43e6-b867-5dd9183b2348_AC1
    Given I am a logged-in Clinician
    When I initiate the billing report generation
    Then I should be able to view a report displaying the total dollars billed.

  # As a Clinician, I want to view overall program statistics, so that I can monitor patient progress and program effectiveness.
  @priority_Should @req_2.3.3.4.4 @req_DHM_UC_24
  Scenario: 1f2a3c55-f8fe-4c4c-a080-9e102ecf6e5d_AC1
    Given I am logged into the Clinician Portal.
    When I navigate to the program statistics section.
    Then I should see overall program statistics, including average percentage attendance for ADHP (2.3.3.4.4).

  # As a Clinician, I want to store individual notes for a session so that I can accurately document patient progress and treatment plans.
  @priority_Must @req_2.3.3.4.5 @HIPAA
  Scenario: 6301fe0d-a335-4298-9495-b2c4a17b0331_AC1
    Given The clinician is logged into the system and viewing a specific session.
    When The clinician enters and saves individual notes for the session.
    Then The system stores the notes securely and associates them with the correct session and clinician, adhering to HIPAA regulations.

  # As a Clinician, I want to view the audit history of a document, so that I can track changes and ensure data integrity.
  @priority_Should @req_2.3.3.4.6 @FDA21CFR11 @HIPAA
  Scenario: a122b9a4-7f69-4f76-b45c-18b743c08d48_AC1
    Given I am a logged-in Clinician
    When I select a document
    Then I can view the audit history of the document, including who made changes and when

  # As a Doctor, I want to see Session information, so that I can review patient progress and make informed decisions.
  @priority_Should @req_2.3.3.4.7
  Scenario: 427e47c7-4cc3-4766-b332-87afd3ee144e_AC1
    Given I am logged into the system as a Doctor.
    When I select a particular session from the list of sessions.
    Then I can see Session information including Facilitator information, Time and scheduling, Attendance, and Group and Individual notes.

  # As a Doctor, I want to view session information including facilitator, time, scheduling, attendance, and notes, so that I can effectively review patient progress and plan future care.
  @priority_Should @req_2.3.3.5
  Scenario: 6734ab19-4f4b-44c6-93d5-723d892ead5e_AC1
    Given I am logged into the system as a Doctor and viewing a patient's page.
    When I select a specific session from the list of sessions.
    Then I should be able to see detailed session information, including facilitator information, time and scheduling, attendance, and group and individual notes.

  # As a Doctor, I want to view a patient's care plan, so that I can review their treatment and progress.
  @priority_Must @req_2.3.3.5.1 @FDA21CFR11 @HIPAA
  Scenario: aca0aadf-e3fa-44eb-add5-d5d9249890cf_AC1
    Given I am logged in as a Doctor and viewing a patient's record.
    When I select the option to view the patient's care plan.
    Then I should be able to see the patient's care plan details.

  # As a Doctor, I want to access links to other patient documents within the EHR, so that I can have a comprehensive view of the patient's medical history.
  @priority_Must @req_2.3.3.5.2 @FDA21CFR11 @HIPAA
  Scenario: a259f8fc-3fa7-4309-ac71-6ad41aefeaee_AC1
    Given I am a Doctor viewing a patient's EHR.
    When I am viewing a specific document within the EHR.
    Then I should see clearly labeled links to other relevant documents for that patient.

  @priority_Must @req_2.3.3.5.2 @FDA21CFR11 @HIPAA
  Scenario: a259f8fc-3fa7-4309-ac71-6ad41aefeaee_AC2
    Given I click on a link to another patient document.
    When The system redirects me.
    Then The linked document should open within the EHR.

  # As a Facilitator, I want to check in to a session or day through a fingerprint scanner so that I can quickly and accurately record attendance.
  @priority_Must @req_2.3.3.5.3 @FDA21CFR11 @HIPAA
  Scenario: 29783f7c-b8d7-4a25-a66a-f7c5c51282bf_AC1
    Given I am a Facilitator with low system experience.
    When I use the fingerprint scanner to check in a participant.
    Then The system accurately records the participant's attendance for the session or day.

  # As a Clinician, I want to view the audit history of a document, so that I can track changes and ensure data integrity.
  @priority_Must @req_2.3.3.8.1 @FDA21CFR11 @HIPAA
  Scenario: 50eeeacd-1394-4391-a4ea-c590a9af6fed_AC1
    Given I am a Clinician accessing the system.
    When I view a specific document.
    Then I can access and view the audit history for that document, including additions, changes, and deletions.

  # As a user, I want to create new assessment types so that I can support various patient needs and data collection requirements.
  @priority_Must @req_2.3.3.9.2 @FDA21CFR11 @HIPAA
  Scenario: 437404f5-333f-4a54-a14a-704709b66367_AC1
    Given I am a user with the appropriate permissions.
    When I navigate to the assessment types management section.
    Then I can create a new assessment type with relevant details (e.g., name, description, data fields).

  # As a Clinician, I want to approve a Care Plan so that the patient's treatment can proceed.
  @priority_Must @req_2.3.3.10.2 @FDA21CFR11 @HIPAA
  Scenario: ab33f4ea-adbb-48ed-82f8-0077692a3a02_AC1
    Given A Care Plan is submitted for approval.
    When I, as a Clinician, review the Care Plan.
    Then I can approve the Care Plan.

  # As a Doctor, I want to view patient documents within the application, so that I can easily access all relevant information for patient care.
  @priority_Must @req_2.3.3.18 @FDA21CFR11 @HIPAA
  Scenario: 7ae58607-e46c-467c-b188-535e0fdf7d99_AC1
    Given I am logged in as a Doctor and viewing a patient's record.
    When I navigate to the 'Documents' section.
    Then I should be able to view the patient's documents directly within the application.

  # As a Facilitator, I want to confirm session attendance taken through fingerprint scanner, so that I can ensure accurate attendance records.
  @priority_Should @req_2.3.3.19
  Scenario: 9fe1d458-8b92-42c7-85e9-5ca13163fca7_AC1
    Given The fingerprint scanner has recorded session attendance.
    When I access the system as a Facilitator.
    Then I can review and confirm the attendance records captured by the fingerprint scanner.

  # As a user, I want to add, modify, or check patient data stored in the system so that I can manage patient information effectively.
  @priority_Must @req_2.6.3 @FDA21CFR11 @HIPAA
  Scenario: 641f9962-307c-49f3-9364-1340cdb36c84_AC1
    Given I have access to the system.
    When I attempt to add, modify, or check patient data.
    Then The system allows me to perform these actions while adhering to HIPAA regulations.

  # As a Clinician, I want to easily access and modify patient information through a web-based application, so that I can efficiently manage patient data.
  @priority_Must @req_2.3.4.1 @FDA21CFR11 @HIPAA
  Scenario: 08d4a8cc-84f3-47d4-aff1-028a8dc99c58_AC1
    Given I am a clinician using the Clinician Portal
    When I access or modify patient information
    Then the application should be easy to learn and navigate quickly.

  # As a Facilitator, I want a backup way to sign-in and out in case of fingerprint scanner error, so that session attendance can be accurately recorded even when the primary method fails.
  @priority_Must @req_2.3.4.3 @HIPAA
  Scenario: 3d340595-c6c5-4100-a1dc-395b2bcb141a_AC1
    Given The fingerprint scanner is unavailable or malfunctioning.
    When The Facilitator attempts to record session attendance.
    Then The system provides an alternative method for signing in and out, such as manual entry or code.

  # As a Facilitator, I want to be able to override sign-in or sign-out in case of fingerprint or backup error, so that attendance can be accurately recorded even with technical issues.
  @priority_Must @req_2.3.4.4 @FDA21CFR11 @HIPAA
  Scenario: cd35ba62-501e-4019-8c87-03b32b21f49f_AC1
    Given The fingerprint scanner is unavailable or a backup error has occurred during sign-in/sign-out.
    When The Facilitator attempts to override the sign-in/sign-out process.
    Then The system allows the Facilitator to manually record the attendance, while maintaining an audit log of the override action.

  # As a Facilitator, I want the ability to create a new session so that I can schedule and manage patient activities.
  @priority_Must @req_2.3.4.6
  Scenario: e03258f7-4795-47b2-ae78-bd33e98deb8f_AC1
    Given I am logged in as a Facilitator.
    When I navigate to the session management section.
    Then I can create a new session with details such as date, time, participants, and session leader.

  # As a Doctor, I want to check patient data stored in the system so that I can review patient information efficiently.
  @priority_Must @req_2.5.3 @FDA21CFR11 @HIPAA
  Scenario: 3375a838-a8be-4fe0-adaa-b87b2c9f3fdb_AC1
    Given I am logged in as a Doctor.
    When I access the patient data section.
    Then I can view patient information.

  # As a Doctor, I want to access patient information through the Clinician Portal so that I can review patient data efficiently.
  @priority_Must @req_2.6.1 @HIPAA
  Scenario: c9716534-06d3-47d8-ae79-4f2f64353527_AC1
    Given I am a Doctor logged into the Clinician Portal.
    When I search for a patient.
    Then I can view the patient's relevant documents and clinical information.

  # As a Doctor, I want to access patient data through a web-based Clinician Portal so that I can easily review patient information.
  @priority_Must @req_2.6.2 @HIPAA
  Scenario: 00641622-bb3d-445e-a065-7f391d153bae_AC1
    Given I am a logged-in Doctor
    When I access the Clinician Portal
    Then I should be able to view patient data.

  @priority_Must @req_2.6.2 @HIPAA
  Scenario: 00641622-bb3d-445e-a065-7f391d153bae_AC2
    Given I am a logged-in Doctor
    When I access the Clinician Portal
    Then The interface must be easy to learn and navigate quickly.

  # As a new user, I want tutorial documentation so that I can learn how to use the application and understand legal and business concerns.
  @priority_Must @req_2.7
  Scenario: df1f87b6-3cde-4d68-b994-b21d2150b588_AC1
    Given I am a new user of the application.
    When I access the application's documentation.
    Then I should find step-by-step instructions with screenshots and in-app guidance.

  # As a Doctor, I want to access tutorial documentation within the application, so that I can quickly learn how to use the system and understand proper protocols.
  @priority_Should @req_2.8
  Scenario: 1f15797c-47ab-48b3-b4a0-3b9ee8624683_AC1
    Given I am a new Doctor user of the application.
    When I access the application for the first time.
    Then I am presented with tutorial documentation, including step-by-step instructions, screenshots, and in-app guidance.

  # As a Clinician, I want to access the system through a web-based Clinician Portal so that I can easily access and modify patient information.
  @priority_Must @req_2.8.3 @FDA21CFR11 @HIPAA
  Scenario: be545b08-b533-4efd-b075-79462cbd632f_AC1
    Given I am a Clinician with appropriate credentials
    When I access the Clinician Portal
    Then I should be able to easily navigate and learn the interface to access and modify patient information.

  # As a Clinician, I want to add a new patient, so that I can manage their care within the system.
  @priority_Must @req_3 @FDA21CFR11 @HIPAA
  Scenario: 65c3f511-b6a1-4f6c-8bf8-60ce424133c2_AC1
    Given I am logged into the system as a Clinician.
    When I enter all required patient information and save.
    Then The new patient record is created and stored in the system.

  # As a Clinician, I want to run a billing report so that I can track revenue and ensure accurate billing.
  @priority_Should @req_4
  Scenario: 084b874b-e00d-4f7c-aabc-8161029574d1_AC1
    Given I am logged into the Clinician Portal.
    When I request to run a billing report.
    Then The system generates a report with relevant billing information.

  # As a Clinician, I want to log in so that I can access patient information and manage care plans.
  @priority_Must @req_4.1 @HIPAA
  Scenario: 65fa9a40-2b58-4a22-a4ab-c1a86c3509d1_AC1
    Given I am a registered clinician with valid credentials
    When I enter my username and password into the clinician portal
    Then I am successfully logged into the system and can access my dashboard

  # As a Doctor, I want to view auditing history reports per patient so that I can track changes to patient data and ensure data integrity.
  @priority_Must @req_4.3.1 @FDA21CFR11 @HIPAA
  Scenario: 8cbe08d1-8690-4095-9dda-3282c54ce51c_AC1
    Given I am logged into the Clinician Portal as a Doctor.
    When I select a patient and navigate to the auditing history report.
    Then I should see a report displaying the history of additions, changes, and deletions of documents and data for that patient.

  # As a Clinician, I want all communication between the server and Clinician Application to be done over SSL, so that patient data is secure and compliant with HIPAA.
  @priority_Must @req_4.4.1 @HIPAA
  Scenario: dadaf903-68a9-4c4f-ada8-2c1d183f6d35_AC1
    Given The Clinician is using the Clinician Application
    When The Clinician Application communicates with the server
    Then The communication is encrypted using SSL

  # As a Doctor, I want to quickly access patient information through the Clinician Portal so that I can efficiently review patient data.
  @priority_Must @req_5
  Scenario: bd869b36-1221-43db-aaff-36ad08100b5f_AC1
    Given I am logged into the Clinician Portal.
    When I request to view a patient's record.
    Then The patient's information is displayed within 2 seconds.

  # As a Doctor, I want the Clinician Portal to load pages quickly so that I can efficiently access patient information and provide timely care.
  @priority_Must @req_5.1
  Scenario: 4aa7ed69-11ff-4ecd-9870-904762d26a1d_AC1
    Given I am a Doctor using the Clinician Portal with one user online
    When I access a page within the portal
    Then the page loads in under 2 seconds

  @priority_Must @req_5.1
  Scenario: 4aa7ed69-11ff-4ecd-9870-904762d26a1d_AC2
    Given I am a Doctor using the Clinician Portal with one user online
    When I access a page within the portal
    Then on average, the page loads in under 0.5 seconds

  @priority_Must @req_5.1
  Scenario: 4aa7ed69-11ff-4ecd-9870-904762d26a1d_AC3
    Given I am a Doctor using the Clinician Portal
    When I access a page within the portal
    Then the page never takes more than 5 seconds to load

  # As a Doctor, I want to access patient data quickly through the Clinician Portal so that I can efficiently review patient information and make informed decisions.
  @priority_Must @req_5.1.1.1 @HIPAA
  Scenario: ff37c065-154f-4c46-b014-b99fb12e4316_AC1
    Given I am a Doctor logged into the Clinician Portal.
    When I request to view a patient's data.
    Then The patient's data should load in under 2 seconds.

  # As a Nurse, I want to update patient vitals so that patient records are accurate and up-to-date.
  @priority_Must @req_5.1.2 @FDA21CFR11 @HIPAA
  Scenario: 9a36b1ee-200a-4aae-80fc-554f662a5240_AC1
    Given the Nurse is logged into the system and has selected a patient
    When the Nurse enters new vital signs data
    Then the system should save the data to the patient's EHR and display a confirmation message

  # As a user, I want to add, modify, or check on any session data so that I can manage sessions effectively.
  @priority_Must @req_5.1.3
  Scenario: 3bd45bdc-52a5-4dcf-ad05-78cb739eb528_AC1
    Given I have access to the system.
    When I navigate to the session section.
    Then I can add a new session, modify a session leader, or check which classes are scheduled on a specific day.

  # As a User, I want the Session app to be operational 99.99% of the time, so that I can reliably access and manage session data.
  @priority_Must @req_5.1.3.3 @HIPAA
  Scenario: 9699e889-b138-497f-8da6-c8f2c546d64c_AC1
    Given The Session app is deployed
    When there is an internet connection or no internet connection
    Then the app remains operational 99.99% of the time.

  # As a Doctor, I want the application to load quickly, so that I can efficiently review patient data.
  @priority_Should @req_5.2
  Scenario: 85418a4e-446b-4143-b597-1e50fcd349cd_AC1
    Given I am a Doctor using the application
    When I access a page within the application
    Then the page loads in under 2 seconds

  @priority_Should @req_5.2
  Scenario: 85418a4e-446b-4143-b597-1e50fcd349cd_AC2
    Given I am a Doctor using the application
    When I access a page within the application
    Then on average, the page loads in under 0.5 seconds

  @priority_Should @req_5.2
  Scenario: 85418a4e-446b-4143-b597-1e50fcd349cd_AC3
    Given I am a Doctor using the application
    When I access a page within the application
    Then the page never takes more than 5 seconds to load

  # As a Doctor, I want to access patient care plans through the Clinician Portal so that I can efficiently review and manage patient treatment (6).
  @priority_Must @req_5.2.1 @FDA21CFR11 @HIPAA
  Scenario: b92a4e5f-a742-4785-8420-334e719684ab_AC1
    Given I am a logged-in Doctor using the Clinician Portal (13)
    When I select a patient
    Then I can view the patient's care plan, including updates and changes (6)

  # As a Clinician Portal user, I want all communication between the server and the application to be done over SSL, so that patient data is protected during transmission.
  @priority_Must @req_5.2.1.1 @HIPAA
  Scenario: dc3d8271-c4be-4dbd-840c-db204664d3a9_AC1
    Given I am a user of the Clinician Portal.
    When I access or modify information in the database.
    Then All communication between the server and the application is encrypted using SSL.

  # As a Day Health staff member, I want to digitize patient assessments, care plans, and sign-in/outs, so that I can improve the tracking and care of patients in the Day Health program.
  @priority_Must @req_5.2.2 @FDA21CFR11 @HIPAA
  Scenario: ef9b62f9-1265-4c4d-aed0-dee12c80aefc_AC1
    Given I am a Day Health staff member
    When I access the Trillium Health Day Health Manager
    Then I can input and store patient assessments, care plans, and sign-in/out information digitally.

  # As a Doctor, I want to view reports showing auditing history, so that I can track changes to patient data and ensure data integrity.
  @priority_Must @req_5.2.3.1 @FDA21CFR11 @HIPAA
  Scenario: 1ac23ddd-f53b-4206-ad19-3ca5605a90b1_AC1
    Given I am a Doctor with access to the system.
    When I request an audit report for a specific patient.
    Then I should see a report detailing additions, modifications, and deletions of documents and data related to that patient, including the user who made the changes and the timestamps.

  # As a Clinician Portal user, I want all communication between the server and the application to be done over SSL, so that patient data is transmitted securely.
  @priority_Must @req_5.3
  Scenario: 3271bd4a-0bc7-460c-a392-7b618509a8f2_AC1
    Given The user is accessing the Clinician Portal application.
    When Data is being transmitted between the server and the application.
    Then The communication must be encrypted using SSL.

  # As a Doctor, I want to access patient care plans through the clinician portal, so that I can review and track patient progress.
  @priority_Must @req_5.3.1 @HIPAA
  Scenario: b15bcd67-787b-445e-8b42-c21c5bb270fa_AC1
    Given I am logged into the Clinician Portal.
    When I select a patient.
    Then I can view the patient's care plan, including updates and changes.

  # As a Nurse, I want to update patient vitals so that the EHR contains the most current patient information.
  @priority_Must @req_5.3.2 @FDA21CFR11 @HIPAA
  Scenario: f06ef03b-9632-42c6-b117-4d0ad8c098f8_AC1
    Given the Nurse is logged into the system and has selected a patient
    When the Nurse enters new vital signs data
    Then the system should save the data to the EHR, adhering to HIPAA regulations.

  # As a user, I want to add, modify, or check on any session data so that I can manage sessions effectively.
  @priority_Must @req_5.3.3
  Scenario: 4dbede1a-3d42-4949-a4a3-5aa5bec93eab_AC1
    Given I have access to the session section of the application
    When I attempt to add a new session
    Then the system allows me to input all required session details.

  @priority_Must @req_5.3.3
  Scenario: 4dbede1a-3d42-4949-a4a3-5aa5bec93eab_AC2
    Given I have access to the session section of the application
    When I attempt to modify a session leader
    Then the system allows me to select a new session leader from a list of available users.

  @priority_Must @req_5.3.3
  Scenario: 4dbede1a-3d42-4949-a4a3-5aa5bec93eab_AC3
    Given I have access to the session section of the application
    When I attempt to check which classes are scheduled on a specific day
    Then the system displays a list of all classes scheduled for that day.

  # As a System Administrator, I want the system to audit all data changes so that we can maintain data integrity and comply with regulations.
  @priority_Must @req_5.4 @FDA21CFR11 @HIPAA
  Scenario: 1f0babdc-7ab3-4acb-9476-e4c829c6f662_AC1
    Given The system is running and a user modifies patient data.
    When The user adds, changes, or deletes a document or data.
    Then The system should track the addition, change, or deletion, including the user and timestamp.

  @priority_Must @req_5.4 @FDA21CFR11 @HIPAA
  Scenario: 1f0babdc-7ab3-4acb-9476-e4c829c6f662_AC2
    Given The system has auditing data.
    When A user requests an audit report.
    Then The system should generate reports showing auditing history, per user or per patient, and allow export of auditing histories.

  # As a Doctor, I want to access patient care plans through the clinician portal so that I can efficiently review and manage patient treatment (EHR).
  @priority_Must @req_5.4.1 @FDA21CFR11 @HIPAA
  Scenario: 3918a7a1-8d89-44ef-84e1-f6c86c5d7b66_AC1
    Given I am logged into the Clinician Portal.
    When I select a patient.
    Then I can view the patient's care plan.

  # As a Clinician, I want to be able to view a patient's care plan so that I can monitor their progress and make necessary adjustments. 
  @priority_Must @req_5.4.1.1
  Scenario: 4246c8f4-e5ad-4a05-a704-fe8c5127152e_AC1
    Given I am a logged-in Clinician
    When I select a patient
    Then I can view the patient's care plan, including updates and changes.

  # As a Clinician, I want the application to communicate with the server over SSL so that patient data is transmitted securely.
  @priority_Must @req_5.4.1.2
  Scenario: 4b3aa627-8d93-433f-9189-fcd1de80e9c8_AC1
    Given I am a Clinician using the application.
    When I am accessing or modifying patient information.
    Then All communication between the application and the server must be done over SSL.

  # As a Nurse, I want to update patient vitals, so that the EHR contains the most current patient information.
  @priority_Must @req_5.4.2 @FDA21CFR11 @HIPAA
  Scenario: dcca3410-e2cd-48f3-8658-325a412eb531_AC1
    Given The nurse is logged into the system and has selected a patient.
    When The nurse enters new vital signs data.
    Then The system saves the data to the EHR, adhering to HIPAA regulations.

  # As a user, I want to add, modify, or check patient data stored in the system so that I can manage patient information effectively.
  @priority_Must @req_5.4.3 @FDA21CFR11 @HIPAA
  Scenario: 85a4042f-8972-40b9-8def-ef8d803315ab_AC1
    Given I have access to the system
    When I attempt to add, modify, or check patient data
    Then the system allows me to perform these actions while adhering to HIPAA and FDA 21 CFR Part 11 constraints.

  # As a Doctor, I want to easily access patient assessments and care plans in a digitized format so that I can efficiently track and manage patient care within the Day Health program.
  @priority_Must @req_1 @FDA21CFR11 @HIPAA
  Scenario: 4cacda81-286c-46f1-be12-7ff5626221dd_AC1
    Given I am a Doctor using the Clinician Portal
    When I access a patient's record
    Then I can view digitized patient assessments and care plans.

