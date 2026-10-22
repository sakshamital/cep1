# Data Model & PostgreSQL Database Schema

DocumentReady uses PostgreSQL for persistent data storage on Render (with SQLite for local development and offline testing). All application data is stored in relational database tables.

---

## Database Tables

### 1. `documents` (`DocumentRecord`)
Every physical or logical document, form, or photo.
- `id` (VARCHAR(64), Primary Key): Unique document identifier (e.g. `aadhaar`, `caste_certificate`).
- `name` (VARCHAR(255)): Official name.
- `aliases_json` (TEXT): JSON array of search synonyms.
- `kind` (VARCHAR(64)): `identity`, `certificate`, `educational`, `affidavit`, `photograph`, `form`, `other`.
- `description` (TEXT): Functional summary.
- `issuing_authority` (VARCHAR(255)): Government authority issuing the document.
- `jurisdiction` (VARCHAR(64)): `Central`, `Maharashtra`, etc.
- `prerequisites_json` (TEXT): Array of document IDs required *before* this document can be obtained (DAG edges).
- `guide_id` (VARCHAR(64)): Foreign key reference to instructional guide.
- `verified` (BOOLEAN): Verification status.
- `source_note` (TEXT): Authoritative citation reference.
- `version` (INTEGER): Snapshot revision counter.

### 2. `services` (`ServiceRecord`)
Government services, welfare schemes, or certificate issuances.
- `id` (VARCHAR(64), Primary Key): Service slug (e.g. `caste_validity_certificate`).
- `name` (VARCHAR(255)): Official title.
- `type` (VARCHAR(64)): `certificate`, `scheme`, `service`.
- `department` (VARCHAR(255)): Issuing ministry / department.
- `applicant_categories_json` (TEXT): e.g. `['student', 'employee', 'other']`.
- `application_info_json` (TEXT): Portal URL, offline centers, application steps, statutory fee note.
- `verified` (BOOLEAN): Officially verified flag.

### 3. `service_requirements` (`ServiceRequirementRecord`)
Atomic prerequisites for a service.
- `service_id` (VARCHAR(64), Foreign Key -> `services.id`).
- `necessity` (VARCHAR(32)): `required`, `optional`, `conditional`, `any_of`.
- `document_id` (VARCHAR(64)): Target document ID.
- `group_name` (VARCHAR(64)): Alternative group name (e.g. `address_proof`).
- `options_json` (TEXT): Array of document IDs for `any_of` choice.
- `when_clause_json` (TEXT): Condition matching (e.g. `{"applicant_category": ["student"]}`).

### 4. `guides` (`GuideRecord`)
"How to obtain?" instructional step-by-step guidance.
- `id` (VARCHAR(64), Primary Key).
- `document_id` (VARCHAR(64), Foreign Key -> `documents.id`, Unique).
- `what_it_is` (TEXT): Explanation of document purpose.
- `documents_required_json` (TEXT): Base items needed at counter.
- `procedure_steps_json` (TEXT): Ordered procedure array.
- `where_how_to_apply` (TEXT): Physical office or web portal.
- `precautions_json` (TEXT): Common pitfalls and safety tips.
- `official_link` (VARCHAR(1024)): Official government website.

### 5. `states` (`StateRecord`)
Master registry of 36 Indian States and Union Territories.
- `id` (VARCHAR(8), Primary Key): Two-letter postal code (`MH`, `DL`, `KA`, etc.).
- `name` (VARCHAR(128)): English state name.
- `name_hi` (VARCHAR(128)): Hindi localization.
- `name_mr` (VARCHAR(128)): Marathi localization.

### 6. `state_rules` (`StateRuleRecord`)
State-specific portal URLs, statutory rules, authorities, and additional prerequisites.
- `service_id` (VARCHAR(64), Foreign Key -> `services.id`).
- `state_id` (VARCHAR(8), Foreign Key -> `states.id`).
- `authority` (VARCHAR(255)): Specific state authority.
- `portal_name` (VARCHAR(255)): Designated state citizen portal.
- `portal_url` (VARCHAR(1024)): URL of state portal.
- `statutory_rule` (TEXT): Applicable State Act / cutoff date citation.
- `additional_requirements_json` (TEXT): State-specific extra documents.
- `application_steps_json` (TEXT): State-specific procedure.

### 7. `synonyms` (`SynonymRecord`)
Search term expansions and phonetic mappings.
- `term` (VARCHAR(64), Primary Key): Search keyword.
- `synonyms_json` (TEXT): Synonymous search terms.

### 8. Monitoring & Auditing Tables
- `sources` (`SourceRegistry`): Permitted government sources and monitoring configurations.
- `source_fetch_history` (`SourceFetchHistory`): Execution history and fingerprints.
- `source_documents` (`SourceDocument`): Extracted circular text and hashes.
- `detected_changes` (`DetectedChange`): Audit trail of detected requirement variations.
- `verification_decisions` (`VerificationDecision`): Human approval / rejection logs.
- `service_versions` & `document_versions`: Immutable snapshot rollback history.
- `audit_events` (`AuditEvent`): Security and administrative activity logs.
- `users` (`UserAccount`): Authenticated admin & reviewer credentials.
- `notifications` (`InAppNotification`): Citizen notification feed.
