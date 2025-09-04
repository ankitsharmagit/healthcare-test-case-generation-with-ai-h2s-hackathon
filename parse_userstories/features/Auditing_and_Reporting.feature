Feature: Auditing and Reporting

  # As a system administrator, I want the system to audit all data modifications so that I can track changes and ensure data integrity and compliance.
  @priority_Must @req_2.3.3.11 @FDA21CFR11 @HIPAA
  Scenario: 25a948ee-f3a0-472b-9cff-560d23ff931f_AC1
    Given The system is running and a user modifies patient data or documents.
    When A user adds, changes, or deletes data.
    Then The system logs the action, including the user, timestamp, and details of the change.

  @priority_Must @req_2.3.3.11 @FDA21CFR11 @HIPAA
  Scenario: 25a948ee-f3a0-472b-9cff-560d23ff931f_AC2
    Given I am a system administrator.
    When I request an audit report.
    Then The system generates a report showing the audit history per user or per patient.

  @priority_Must @req_2.3.3.11 @FDA21CFR11 @HIPAA
  Scenario: 25a948ee-f3a0-472b-9cff-560d23ff931f_AC3
    Given I am viewing an audit report.
    When I choose to export the audit history.
    Then The system exports the audit history in a standard format (e.g., CSV, Excel).

