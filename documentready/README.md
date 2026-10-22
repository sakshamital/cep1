# DocumentReady — Know Before You Go
## Evidence-Backed Government Information Monitoring & Citizen Readiness Platform

DocumentReady helps Indian citizens prepare before applying for government services, certificates, educational services and welfare schemes by providing verified, up-to-date document checklists, step-by-step prerequisite guides, and automated official-source monitoring.

---

### ⚠ Disclaimer
**DocumentReady is an independent informational and readiness-support platform. It is NOT an official government portal and is not affiliated with any government department.**
All initial records are explicitly flagged as illustrative unverified demo records until verified against authoritative government publications. Always confirm final requirements with the competent official authority.

---

## Key Features

1. **Service Search & Synonym Expansion**: Search services by popular names, synonyms (e.g. *aadhar*, *jaati praman patra*), department, and jurisdiction (Maharashtra / Central).
2. **Category-Specific Requirements**: Automatic resolution of required, optional, conditional (e.g. student vs employee), and alternative (*any-of*) document groups.
3. **Prerequisite Dependency DAG**: Topological sorting and cycle detection ensuring users know which base documents (e.g. Aadhaar, residence proof) to obtain first.
4. **Interactive Readiness Evaluation**: Real-time evaluation of document statuses, missing blocker detection, and actionable step-by-step obtain plans.
5. **Automated Official-Source Monitoring**: Modular monitoring engine tracking changes from permitted government sources (Maharashtra Aaple Sarkar, Social Justice, Revenue Dept, MahaDBT, UIDAI).
6. **Government PDF & Document Processing**: Safe stream-downloading with 15MB size caps, SSRF shields, text and metadata extraction via `pypdf`, and scanned PDF detection.
7. **Structured Change Analysis & Evidence Grounding**: Classifies detected differences into new requirements, fee revisions, procedure updates, and link changes with exact verbatim quotes and official source URLs.
8. **Human-in-the-Loop Verification & Safe Rollback**: Immutable version snapshots with 1-click administrative rollback restoring previous states without destroying audit history.
9. **Administrative Dashboard**: Server-side session authentication, CSRF protection, source health monitoring, manual check triggers, and verification review queue.
10. **Citizen Notification Feed**: In-app notifications alerting citizens whenever officially verified requirement changes are published.

---

## Tech Stack

- **Backend**: Python 3.12+ with Flask 3.0.3
- **Production Server**: Gunicorn 21.2+ WSGI server
- **Database & ORM**: PostgreSQL (production on Render) & SQLite (local dev/test) via SQLAlchemy 2.0+ and `psycopg2-binary`
- **Containerization**: Docker (multi-platform production container, non-root user, dynamic `$PORT`)
- **Document Processing**: `pypdf` for government circular text & metadata extraction
- **HTML Parsing**: BeautifulSoup4 for HTML normalization and fingerprinting
- **Frontend**: HTML5, Vanilla CSS (Design system with custom properties), Vanilla JavaScript ES Modules
- **Testing**: `pytest` with synthetic offline fixtures

---

## Deploying to Render (Docker + Managed PostgreSQL)

DocumentReady includes out-of-the-box support for Render deployment using the provided `Dockerfile` and `render.yaml` Blueprint.

### Option 1: 1-Click Blueprint Deployment via `render.yaml`
1. Push this repository to GitHub or GitLab.
2. In the Render Dashboard, click **New** &rarr; **Blueprint**.
3. Connect your repository. Render automatically reads `render.yaml` and provisions:
   - A managed **PostgreSQL Database** (`documentready-postgres`).
   - A **Web Service** (`documentready`) running the Docker container.
4. Render automatically binds the database connection string to `DATABASE_URL` and starts Gunicorn.

### Option 2: Manual Web Service Setup on Render
1. Create a **PostgreSQL Database** on Render:
   - Name: `documentready-postgres`
   - Database: `documentready`
   - Note the **Internal Database URL**.
2. Create a **Web Service**:
   - Environment: **Docker**
   - Repository: Connect your repository.
   - Root Directory: `documentready` (or leave empty if repo root is the app directory).
   - Add Environment Variables:
     - `DATABASE_URL`: Set to your Render PostgreSQL Internal Connection String.
     - `FLASK_ENV`: `production`
     - `SECRET_KEY`: Set a long random string.
     - `SESSION_COOKIE_SECURE`: `True`
     - `INITIAL_ADMIN_PASSWORD`: Your desired admin password.
3. Click **Deploy**. Tables are automatically created and seeded on first startup.

---

---

## Local Setup & Run Instructions

### 1. Environment Setup
```bash
# Clone the repository and enter the directory
cd documentready

# Create and activate a virtual environment
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
python -m pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

### 3. Initialize Persistent Database & Seed Data
Initialize database tables and import initial services, documents, guides, and source registry idempotently:
```bash
flask db-admin init
```
This automatically provisions the default administrator account:
- **Username**: `admin`
- **Default Password**: `Admin@DocReady2026` *(change in production via `INITIAL_ADMIN_PASSWORD` or CLI)*

### 4. Run the Web Application
```bash
python run.py
```
Visit the application:
- **Public Citizen Portal**: `http://127.0.0.1:5000/`
- **Verified Updates Feed**: `http://127.0.0.1:5000/updates`
- **Administrative Console**: `http://127.0.0.1:5000/admin/login`

---

## CLI & Background Worker Commands

DocumentReady includes dedicated CLI command groups for administration, database maintenance, and source monitoring:

```bash
# Execute monitoring check across all enabled official sources once
flask monitor run-all

# Execute a monitoring check on a specific registered source ID
flask monitor check src_aaplesarkar_caste_validity --force

# Create or update an administrative user account
flask admin create-user --username reviewer1 --role reviewer

# Re-run idempotent database synchronization
flask db-admin init
```

---

## Permitted Official Government Sources

The following legitimate official sources are configured in the Source Registry:

| Source ID | Authority / Department | Jurisdiction | Type | Adapter | Monitored URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `src_aaplesarkar_caste_validity` | Social Justice & Special Assistance Dept | Maharashtra | HTML | `aaplesarkar_table` | `https://aaplesarkar.mahaonline.gov.in/en/Department/Index/28` |
| `src_aaplesarkar_revenue` | Revenue & Forest Department | Maharashtra | HTML | `aaplesarkar_table` | `https://aaplesarkar.mahaonline.gov.in/en/Department/Index/11` |
| `src_uidai_aadhaar_guidelines` | Unique Identification Authority of India | Central | PDF | `pdf_circular` | `https://uidai.gov.in/.../List_of_Supporting_Document...pdf` |
| `src_mahadbt_scholarships` | Higher & Technical Education / Social Justice | Maharashtra | HTML | `generic_html` | `https://mahadbt.maharashtra.gov.in/...` |

---

## Running the Automated Test Suite

Run the full pytest suite (including unit tests, SSRF security tests, PDF processing, verification workflow, and the 12-step end-to-end monitoring lifecycle):

```bash
python -m pytest
```

All mock fixtures run offline with zero dependency on external government networks or paid APIs.

---

## Manual Acceptance-Test Checklist

- [x] **Search**: Search for "Caste Validity" on homepage; confirm autocomplete and redirect to `/service/caste_validity_certificate`.
- [x] **Category Filtering**: Switch between "student" and "employee" categories; verify conditional items (e.g. Admission Letter) appear or hide.
- [x] **Readiness Evaluation**: Mark documents as Available or Missing; click "Verify Checklist" and confirm progress bar, blocker badges, and topological obtain sequence.
- [x] **Freshness & Verification Metadata**: Verify that the service page displays official verification status, jurisdiction, and official portal links.
- [x] **Admin Authentication**: Access `/admin/` unauthenticated; verify redirect to `/admin/login`. Login with `admin` / `Admin@DocReady2026`.
- [x] **Source Check Execution**: In Admin &rarr; Source Registry, click "Check Now" for an official source; confirm fetch log and status update.
- [x] **Change Approval & Publication**: In Admin &rarr; Verification Queue, review a proposed change diff and grounded evidence; click "Approve & Publish"; verify that the live service checklist updates and version increments.
- [x] **Rollback**: In Admin &rarr; Version History, select a service and click "Rollback to this"; confirm the service checklist restores cleanly.
- [x] **SSRF Shield**: In Admin &rarr; Add Source, attempt adding `http://127.0.0.1:5000` or `http://169.254.169.254`; verify SSRF block with security alert.
