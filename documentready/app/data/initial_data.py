"""Initial dataset seeded into the PostgreSQL / relational database."""

DOCUMENTS_SEED = [{'id': 'aadhaar',
  'name': 'Aadhaar Card',
  'aliases': ['aadhar', 'uid card', 'uidai card', 'aadhar card', 'e-aadhaar', 'uid'],
  'kind': 'identity',
  'description': '12-digit unique biometric identity number issued by UIDAI to residents of India, serving as the '
                 'foundational proof of identity and address across India.',
  'issuing_authority': 'UIDAI (Unique Identification Authority of India)',
  'jurisdiction': 'India',
  'prerequisites': [],
  'guide_id': 'guide_aadhaar',
  'verified': True,
  'source_note': 'Verified against UIDAI official supporting documents circular and Aadhaar Act, 2016',
  'official_link': 'https://uidai.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'pan_card',
  'name': 'PAN Card (Permanent Account Number)',
  'aliases': ['pan', 'pan card', 'pan number', 'permanent account number', 'nsdl pan', 'uti pan', 'e-pan'],
  'kind': 'identity',
  'description': '10-digit alphanumeric identifier issued by the Income Tax Department, mandatory for opening bank '
                 'accounts, receiving salaries, financial transactions, and filing tax returns.',
  'issuing_authority': 'Income Tax Department, Government of India (via Protean/NSDL or UTIITSL)',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_pan_card',
  'verified': True,
  'source_note': 'Verified against Income Tax Department Form 49A guidelines and Instant e-PAN regulations',
  'official_link': 'https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html',
  'last_reviewed': '2026-10-22'},
 {'id': 'voter_id',
  'name': 'Voter ID Card (EPIC)',
  'aliases': ['voter id', 'epic', 'voter card', 'election card', 'matdan card', 'voters identity card'],
  'kind': 'identity',
  'description': 'Electors Photo Identity Card (EPIC) issued by the Election Commission of India confirming electoral '
                 'enrollment, legal voting rights, and recognized as universal identity and residence proof.',
  'issuing_authority': 'Election Commission of India (ECI)',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'photograph', 'residence_proof'],
  'guide_id': 'guide_voter_id',
  'verified': True,
  'source_note': 'Verified against ECI Registration of Electors Rules (Form 6)',
  'official_link': 'https://voters.eci.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'passport',
  'name': 'Indian Passport',
  'aliases': ['passport', 'indian passport', 'ordinary passport', 'tatkaal passport', 'travel passport'],
  'kind': 'identity',
  'description': 'Official travel and citizenship document issued by the Ministry of External Affairs for '
                 'international travel, study abroad, and foreign employment.',
  'issuing_authority': 'Ministry of External Affairs (Passport Seva), Government of India',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'pan_card', 'birth_certificate'],
  'guide_id': 'guide_passport',
  'verified': True,
  'source_note': 'Verified against Passport Seva PSP Guidelines and Passports Act, 1967',
  'official_link': 'https://www.passportindia.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'driving_licence',
  'name': 'Driving Licence (DL)',
  'aliases': ['dl', 'driving license', 'driver licence', 'driving licence', 'learner licence', 'rto licence'],
  'kind': 'certificate',
  'description': 'Official legal authorization issued by the Regional Transport Office (RTO) permitting operation of '
                 'motor vehicles on public roads.',
  'issuing_authority': 'Ministry of Road Transport and Highways (MoRTH) / State Transport Department (RTO)',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'photograph', 'residence_proof'],
  'guide_id': 'guide_driving_licence',
  'verified': True,
  'source_note': 'Verified against Motor Vehicles Act and Parivahan Sarathi Standards',
  'official_link': 'https://sarathi.parivahan.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'birth_certificate',
  'name': 'Birth Certificate',
  'aliases': ['janam praman patra', 'birth cert', 'dob certificate', 'birth proof', 'municipal birth certificate'],
  'kind': 'certificate',
  'description': 'Statutory civil record documenting date, time, and location of birth and parentage, serving as '
                 'primary proof of age and date of birth.',
  'issuing_authority': 'Registrar of Births & Deaths / Municipal Corporation / Nagar Palika / Gram Panchayat',
  'jurisdiction': 'India',
  'prerequisites': [],
  'guide_id': 'guide_birth_certificate',
  'verified': True,
  'source_note': 'Verified against Registration of Births and Deaths (RBD) Act, 1969 and CRS portal rules',
  'official_link': 'https://crsorgi.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'death_certificate',
  'name': 'Death Certificate',
  'aliases': ['mrityu praman patra', 'death cert', 'death proof', 'municipal death certificate'],
  'kind': 'certificate',
  'description': 'Official certification recording the death of an individual, vital for legal succession, insurance '
                 'claims, bank account transfers, and property mutation.',
  'issuing_authority': 'Registrar of Births & Deaths / Municipal Corporation / Gram Panchayat',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_death_certificate',
  'verified': True,
  'source_note': 'Verified against Registration of Births and Deaths (RBD) Act, 1969',
  'official_link': 'https://crsorgi.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'marriage_certificate',
  'name': 'Marriage Registration Certificate',
  'aliases': ['vivah nodani', 'marriage cert', 'vivah praman patra', 'marriage registration'],
  'kind': 'certificate',
  'description': 'Legal document establishing the legal solemnization of a marriage, required for spouse visas, '
                 'insurance nomination, joint property ownership, and passport surname change.',
  'issuing_authority': 'Registrar of Marriages / Municipal Corporation / Sub-Registrar of Assurances',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'photograph', 'residence_proof'],
  'guide_id': 'guide_marriage_certificate',
  'verified': True,
  'source_note': 'Verified against Hindu Marriage Act 1955 / Special Marriage Act 1954 and State Marriage Rules',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'caste_certificate',
  'name': 'Caste Certificate',
  'aliases': ['jaati praman patra',
              'caste proof',
              'jaati certificate',
              'sc certificate',
              'st certificate',
              'obc certificate'],
  'kind': 'certificate',
  'description': "Certificate issued by the competent revenue authority stating the applicant's recognized caste or "
                 'tribe, required for reservations and welfare entitlements.',
  'issuing_authority': 'Sub-Divisional Officer (SDO) / Tahsildar / District Magistrate',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'residence_proof', 'affidavit_stamp_paper'],
  'guide_id': 'guide_caste_certificate',
  'verified': True,
  'source_note': 'Verified against State Revenue Department Guidelines and Right to Services Act',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'caste_validity_certificate',
  'name': 'Caste Validity Certificate',
  'aliases': ['caste validity', 'validity certificate', 'cvc', 'caste validity cert', 'barti validity'],
  'kind': 'certificate',
  'description': 'Statutory validation confirming the authenticity of a caste claim after judicial scrutiny by the '
                 'Scrutiny Committee, mandatory for professional admissions (CAP) and reserved jobs.',
  'issuing_authority': 'Divisional Caste Certificate Scrutiny Committee / Social Justice Department',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'caste_certificate', 'school_leaving_certificate', 'photograph'],
  'guide_id': 'guide_caste_validity_certificate',
  'verified': True,
  'source_note': 'Verified against Maharashtra Scheduled Castes / Scheduled Tribes / OBC Scrutiny Act XXIII of 2001',
  'official_link': 'https://bartievalidity.maharashtra.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'non_creamy_layer_certificate',
  'name': 'Non-Creamy Layer (NCL) Certificate',
  'aliases': ['ncl', 'non creamy layer', 'obc ncl certificate', 'creamy layer certificate', 'ncl cert'],
  'kind': 'certificate',
  'description': 'Mandatory certificate for OBC, VJNT, and SBC candidates proving their annual family income is below '
                 'the creamy layer threshold (Rs. 8 Lakh/yr for 3 consecutive years) to claim quota benefits.',
  'issuing_authority': 'Sub-Divisional Officer (SDO) / Tahsildar, Revenue Department',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['caste_certificate', 'income_proof', 'residence_proof'],
  'guide_id': 'guide_non_creamy_layer_certificate',
  'verified': True,
  'source_note': 'Verified against Government Resolution on Creamy Layer Criteria and Revenue Service Standards',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'ews_certificate',
  'name': 'Economically Weaker Section (EWS) Certificate',
  'aliases': ['ews', 'ews certificate', 'economically weaker section', 'general ews'],
  'kind': 'certificate',
  'description': 'Certificate granting 10% reservation in educational admissions and central/state government '
                 'employment to General category candidates whose gross family income is below Rs. 8 Lakh/yr.',
  'issuing_authority': 'Tahsildar / Sub-Divisional Magistrate (SDM), Revenue Department',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'residence_proof', 'income_proof'],
  'guide_id': 'guide_ews_certificate',
  'verified': True,
  'source_note': 'Verified against Ministry of Personnel, Public Grievances & Pensions O.M. on EWS reservation',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'domicile_certificate',
  'name': 'State Domicile / Permanent Residence Certificate',
  'aliases': ['domicile', 'prc', 'permanent residence certificate', 'domicile certificate', 'adhivas praman patra'],
  'kind': 'certificate',
  'description': 'Legal document certifying that an individual has lived in the state for the statutory duration '
                 '(typically 10 to 15 years), required for state quota admissions and government jobs.',
  'issuing_authority': 'Sub-Divisional Magistrate (SDM) / Tahsildar / Revenue Department',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'residence_proof'],
  'guide_id': 'guide_domicile_certificate',
  'verified': True,
  'source_note': 'Verified against State Domicile & Permanent Residence Rules and RTS Act',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'income_proof',
  'name': 'Income Proof / Income Certificate',
  'aliases': ['income certificate', 'salary slip', 'income document', 'utpanna dakhla', 'annual income certificate'],
  'kind': 'certificate',
  'description': 'Document certifying annual family income from all legitimate sources, issued by Tahsildar/Executive '
                 'Magistrate or employer Form 16, needed for scholarships, fee concessions, and schemes.',
  'issuing_authority': 'Executive Magistrate / Tahsildar / Employer Form 16',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'residence_proof'],
  'guide_id': 'guide_income_proof',
  'verified': True,
  'source_note': 'Verified against Revenue Department income determination rules and RTS Act',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'disability_certificate',
  'name': 'Unique Disability ID (UDID) & Disability Certificate',
  'aliases': ['udid',
              'disability certificate',
              'pwd certificate',
              'divyang card',
              'swavlamban card',
              'handicapped certificate'],
  'kind': 'certificate',
  'description': 'National biometric disability card and certificate issued under Rights of Persons with Disabilities '
                 'Act, 2016 for 4% reservation, travel concessions, assistive devices, and scholarships.',
  'issuing_authority': 'Department of Empowerment of Persons with Disabilities (DEPwD) / District Medical Authority',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'photograph'],
  'guide_id': 'guide_disability_certificate',
  'verified': True,
  'source_note': 'Verified against Swavlamban Portal Standards and RPwD Act 2016',
  'official_link': 'https://www.swavlambancard.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'senior_citizen_card',
  'name': 'Senior Citizen Identity Card / Certificate',
  'aliases': ['senior citizen card', 'senior citizen certificate', 'vyeshtha nagarik card', 'elderly identity card'],
  'kind': 'identity',
  'description': 'Identity card issued to citizens aged 60 and above, conferring railway/air concessions, bus fare '
                 'rebates, prioritized healthcare, and social security pension benefits.',
  'issuing_authority': 'Social Welfare Department / Tahsildar / District Collectorate',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'photograph', 'residence_proof'],
  'guide_id': 'guide_senior_citizen_card',
  'verified': True,
  'source_note': 'Verified against Maintenance and Welfare of Parents and Senior Citizens Act and Social Welfare Rules',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'police_clearance_certificate',
  'name': 'Police Clearance Certificate (PCC) / Character Certificate',
  'aliases': ['pcc', 'police clearance', 'police verification', 'character certificate', 'charitra praman patra'],
  'kind': 'certificate',
  'description': 'Official verification certifying applicant has no adverse criminal antecedents or pending '
                 'prosecutions, essential for government employment, defense jobs, and foreign visas.',
  'issuing_authority': 'District Superintendent of Police / Police Commissionerate / Regional Passport Office',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'residence_proof', 'photograph'],
  'guide_id': 'guide_police_clearance_certificate',
  'verified': True,
  'source_note': 'Verified against State Police Citizen Services Portal & Passport Seva Guidelines',
  'official_link': 'https://pcs.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'ration_card',
  'name': 'Ration Card',
  'aliases': ['ration book', 'food card', 'pds card', 'ration card', 'ration dakhla', 'bpl card', 'apl card'],
  'kind': 'identity',
  'description': 'Household identity and entitlement document issued by Food & Civil Supplies Department for '
                 'subsidized food grains and recognized address proof.',
  'issuing_authority': 'Food, Civil Supplies & Consumer Protection Department',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'residence_proof', 'photograph'],
  'guide_id': 'guide_ration_card',
  'verified': True,
  'source_note': 'Verified against National Food Security Act (NFSA) and RCMS portal guidelines',
  'official_link': 'https://rcms.mahafood.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'electricity_bill',
  'name': 'Electricity Bill',
  'aliases': ['light bill', 'power bill', 'bijli bill', 'electric bill', 'discom bill'],
  'kind': 'other',
  'description': 'Recent power consumption bill (not older than 3 months) showing registered consumer name and '
                 'premises address, universally accepted as utility address proof.',
  'issuing_authority': 'State Electricity Distribution Company (Discom e.g. MSEDCL, Adani, Tata Power)',
  'jurisdiction': 'India',
  'prerequisites': [],
  'guide_id': 'guide_electricity_bill',
  'verified': True,
  'source_note': 'Verified utility address proof standard across central and state authorities',
  'official_link': 'https://www.mahadiscom.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'rent_agreement',
  'name': 'Registered Rent Agreement (Leave and License)',
  'aliases': ['lease agreement', 'rental agreement', 'tenancy agreement', 'registered rent agreement'],
  'kind': 'other',
  'description': 'Registered Leave and License agreement executed under the Registration Act with biometric '
                 'verification, establishing legal tenancy and valid address proof.',
  'issuing_authority': 'Department of Registration and Stamps (IGR) / Sub-Registrar Office',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_rent_agreement',
  'verified': True,
  'source_note': 'Verified under Maharashtra Rent Control Act and Indian Registration Act, 1908',
  'official_link': 'https://igrmaharashtra.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'bank_passbook',
  'name': 'Bank Passbook / Account Statement',
  'aliases': ['bank passbook', 'passbook', 'bank statement', 'bank account proof', 'cancelled cheque'],
  'kind': 'other',
  'description': 'First page of bank passbook or certified statement showing account number, IFSC code, and address, '
                 'with Aadhaar seeding for Direct Benefit Transfer (DBT).',
  'issuing_authority': 'Scheduled Commercial Bank / Public Sector Bank / IPPB',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'pan_card', 'photograph'],
  'guide_id': 'guide_bank_passbook',
  'verified': True,
  'source_note': 'Verified RBI KYC guidelines and NPCI DBT mapper standards',
  'official_link': 'https://www.rbi.org.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'school_leaving_certificate',
  'name': 'School Leaving Certificate (SLC / TC)',
  'aliases': ['slc', 'transfer certificate', 'tc', 'leaving certificate', 'shala sodlyacha dakhla'],
  'kind': 'educational',
  'description': 'Official academic record issued upon leaving an educational institution, recording student date of '
                 'birth, caste entry, and conduct.',
  'issuing_authority': 'Headmaster / Principal of Recognized School or Junior College',
  'jurisdiction': 'Maharashtra',
  'prerequisites': [],
  'guide_id': 'guide_school_leaving_certificate',
  'verified': True,
  'source_note': 'Verified under Secondary School Code and Education Department Regulations',
  'official_link': 'https://education.maharashtra.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'relative_validity_record',
  'name': "Relative's Caste Validity Record",
  'aliases': ['relative validity', 'relation validity', 'parent validity record', 'rakta sambandhi validity'],
  'kind': 'certificate',
  'description': "Certified copy of a paternal blood relative's (father, sibling, paternal uncle) caste validity "
                 'order, providing conclusive evidentiary weight.',
  'issuing_authority': 'Divisional Caste Certificate Scrutiny Committee',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['caste_certificate'],
  'guide_id': 'guide_relative_validity_record',
  'verified': True,
  'source_note': 'Verified under Maharashtra Caste Scrutiny Act XXIII of 2001',
  'official_link': 'https://bartievalidity.maharashtra.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'admission_letter',
  'name': 'Admission Allotment Letter / Offer Letter',
  'aliases': ['offer letter', 'admission confirmation', 'allotment letter', 'cap allotment letter'],
  'kind': 'educational',
  'description': 'Official confirmation letter from competent admission authority or college registrar confirming seat '
                 'allotment and course admission.',
  'issuing_authority': 'Competent Admission Authority (e.g. State CET Cell, CAP, University Registrar)',
  'jurisdiction': 'India',
  'prerequisites': [],
  'guide_id': 'guide_admission_letter',
  'verified': True,
  'source_note': 'Verified against Centralized Admission Process (CAP) Rules',
  'official_link': 'https://cetcell.mahacet.org',
  'last_reviewed': '2026-10-22'},
 {'id': 'gap_certificate',
  'name': 'Educational Gap Certificate / Affidavit',
  'aliases': ['gap certificate', 'gap affidavit', 'education gap affidavit', 'gap certificate format'],
  'kind': 'affidavit',
  'description': 'Sworn legal affidavit on non-judicial stamp paper stating the reason for an academic gap between '
                 'degrees and affirming non-enrollment elsewhere.',
  'issuing_authority': 'Notary Public / Executive Magistrate',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar', 'affidavit_stamp_paper'],
  'guide_id': 'guide_gap_certificate',
  'verified': True,
  'source_note': 'Verified under Indian Stamp Act and State University Admission Rules',
  'official_link': 'https://gras.mahakosh.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'land_7_12_extract',
  'name': 'Land 7/12 Extract & 8A Record (Satbara Utara)',
  'aliases': ['7/12', 'satbara', '7 12 utara', 'saat baara', '8a extract', 'bhulekh satbara', 'digital satbara'],
  'kind': 'revenue',
  'description': 'Land revenue registry extract in Maharashtra documenting ownership, survey number, area, crop '
                 'details, and encumbrances.',
  'issuing_authority': 'Revenue and Forest Department / Mahabhumi Bhulekh / Village Talati',
  'jurisdiction': 'Maharashtra',
  'prerequisites': [],
  'guide_id': 'guide_land_7_12_extract',
  'verified': True,
  'source_note': 'Verified against Maharashtra Land Revenue Code, 1966 and Mahabhumi Portal',
  'official_link': 'https://digitalsatbara.mahabhumi.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'photograph',
  'name': 'Passport-Size Photograph',
  'aliases': ['photo', 'passport photo', 'photograph', 'passport size photo'],
  'kind': 'photograph',
  'description': 'Recent color photograph of applicant (3.5 cm x 4.5 cm) on light background compliant with standard '
                 'ICAO specifications.',
  'issuing_authority': 'Registered Photo Studio / Standard ICAO Format',
  'jurisdiction': 'India',
  'prerequisites': [],
  'guide_id': 'guide_photograph',
  'verified': True,
  'source_note': 'Standard passport photograph specifications (3.5cm x 4.5cm)',
  'official_link': 'https://uidai.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'affidavit_stamp_paper',
  'name': 'Affidavit on Stamp Paper',
  'aliases': ['stamp paper', 'affidavit', 'notarised affidavit', 'shapath patra'],
  'kind': 'affidavit',
  'description': 'Sworn legal statement executed on non-judicial stamp paper of prescribed denomination, attested by a '
                 'Notary Public or Executive Magistrate.',
  'issuing_authority': 'Licensed Stamp Vendor & Notary Public / Executive Magistrate',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_affidavit_stamp_paper',
  'verified': True,
  'source_note': 'Verified under Indian Stamp Act and State Stamp Rules',
  'official_link': 'https://gras.mahakosh.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'residence_proof',
  'name': 'Residence Proof',
  'aliases': ['address proof', 'domicile proof', 'proof of residence', 'rahavasi dakhla'],
  'kind': 'certificate',
  'description': 'Government accepted proof verifying current residential address of applicant (utility bill, ration '
                 'card, rent agreement, or residence certificate).',
  'issuing_authority': 'Revenue Department / Municipal Corporation / Competent Authority',
  'jurisdiction': 'India',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_residence_proof',
  'verified': True,
  'source_note': 'Verified against State Public Service Guarantee Standards',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'self_declaration_form',
  'name': 'Self-Declaration Form',
  'aliases': ['self declaration', 'declaration form', 'self-attested declaration', 'swayam ghoshana'],
  'kind': 'form',
  'description': 'Statutory filled and signed declaration confirming truth of statements under Right to Public '
                 'Services Act without notarization.',
  'issuing_authority': 'Self-declaration under Right to Public Services Act',
  'jurisdiction': 'India',
  'prerequisites': [],
  'guide_id': 'guide_self_declaration_form',
  'verified': True,
  'source_note': 'Verified statutory self-declaration format under Right to Public Services',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'pre_1950_caste_proof',
  'name': 'Pre-1950 / Pre-1967 Ancestral Caste Proof',
  'aliases': ['pre 1950 proof', '1950 record', '1967 proof', 'ancestral caste proof', 'old school lc', '1950 dakhla'],
  'kind': 'educational',
  'description': 'Primary school record, birth registry extract, or land record of father/grandfather before cutoff '
                 'date (1950 for SC/ST, 1967 for OBC/VJNT).',
  'issuing_authority': 'Zilla Parishad School / Municipality / Land Revenue Records',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_pre_1950_caste_proof',
  'verified': True,
  'source_note': 'Verified historical evidentiary requirements under Maharashtra Caste Rules',
  'official_link': 'https://bartievalidity.maharashtra.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'pedhinama',
  'name': 'Pedhinama (Certified Family Genealogy Tree)',
  'aliases': ['pedhinama', 'pedinama', 'genealogy tree', 'family tree certificate', 'vanshavali'],
  'kind': 'affidavit',
  'description': 'Formal genealogical pedigree tree certified by Talati cum Mantri or Executive Magistrate proving '
                 'ancestral lineage.',
  'issuing_authority': 'Talati cum Mantri / Executive Magistrate / Mamlatdar Office',
  'jurisdiction': 'Gujarat',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_pedhinama',
  'verified': True,
  'source_note': 'Verified under Gujarat Revenue Department genealogical rules',
  'official_link': 'https://digitalgujarat.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'parivar_register_nakal',
  'name': 'Parivar Register Nakal (Family Register Copy)',
  'aliases': ['parivar register', 'kutumb register', 'family register nakal', 'panchayat register'],
  'kind': 'certificate',
  'description': 'Certified extract of the Family Register maintained by Gram Panchayat Secretary or Nagar Palika '
                 'recording all family members.',
  'issuing_authority': 'Gram Panchayat / Block Development Office / Nagar Palika',
  'jurisdiction': 'Uttar Pradesh',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_parivar_register_nakal',
  'verified': True,
  'source_note': 'Verified under UP Panchayati Raj Department Rules',
  'official_link': 'https://edistrict.up.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'talati_verification_report',
  'name': 'Talati / Patwari / Lekhpal Verification Report',
  'aliases': ['talati report', 'patwari inquiry report', 'lekhpal report', 'panchnama', 'talati dakhla'],
  'kind': 'form',
  'description': 'Spot inquiry and field panchnama prepared by local village revenue officer certifying income, '
                 'residence, or landholding.',
  'issuing_authority': 'Village Revenue Officer (Talati / Patwari / Lekhpal)',
  'jurisdiction': 'Maharashtra',
  'prerequisites': ['aadhaar', 'residence_proof'],
  'guide_id': 'guide_talati_verification_report',
  'verified': True,
  'source_note': 'Verified village revenue administration standards',
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'nadakacheri_rd_number',
  'name': 'Nadakacheri RD Application / Certificate Number',
  'aliases': ['nadakacheri rd', 'rd number', 'karnataka rd slip', 'nadakacheri barcode'],
  'kind': 'form',
  'description': '15-digit RD barcode acknowledgement number generated by Atalji Janasnehi Kendra (Nadakacheri) in '
                 'Karnataka.',
  'issuing_authority': 'Atalji Janasnehi Kendra (Nadakacheri) / Tahsildar, Karnataka',
  'jurisdiction': 'Karnataka',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_nadakacheri_rd_number',
  'verified': True,
  'source_note': 'Verified under Karnataka Revenue Services (Sakala)',
  'official_link': 'https://nadakacheri.karnataka.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'kutumba_sats_id',
  'name': 'Kutumba Family ID / SATS Student ID',
  'aliases': ['kutumba id', 'sats id', 'student achievement tracking id', 'karnataka family id'],
  'kind': 'identity',
  'description': 'Unified Karnataka family entitlement ID (Kutumba) and Student Achievement Tracking System (SATS) '
                 'enrollment ID.',
  'issuing_authority': 'Centre for e-Governance / Department of School Education, Karnataka',
  'jurisdiction': 'Karnataka',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_kutumba_sats_id',
  'verified': True,
  'source_note': 'Verified Karnataka e-Governance Kutumba Portal standards',
  'official_link': 'https://kutumba.karnataka.gov.in',
  'last_reviewed': '2026-10-22'},
 {'id': 'delhi_3yr_residence_proof',
  'name': 'Proof of 3 Years Continuous Residence in Delhi',
  'aliases': ['delhi 3 year proof', 'delhi stay proof', 'delhi residence proof 3 years'],
  'kind': 'certificate',
  'description': 'Utility bills, voter ID, or school attendance certificate demonstrating continuous residency in '
                 'Delhi for at least 3 years.',
  'issuing_authority': 'Electricity Discom / Election Commission / Educational Institution',
  'jurisdiction': 'Delhi',
  'prerequisites': ['aadhaar'],
  'guide_id': 'guide_delhi_3yr_residence_proof',
  'verified': True,
  'source_note': 'Verified under e-District Delhi Revenue Department Rules',
  'official_link': 'https://edistrict.delhigovt.nic.in',
  'last_reviewed': '2026-10-22'}]

SERVICES_SEED = [{'id': 'caste_validity_certificate',
  'name': 'Caste Validity Certificate',
  'aliases': ['caste validity', 'validity certificate', 'cvc', 'caste validity cert'],
  'type': 'certificate',
  'department': 'Divisional Caste Scrutiny Committee, Social Justice & Special Assistance Department, Government of '
                'Maharashtra',
  'description': "A Caste Validity Certificate confirms the authenticity of an applicant's caste claim after detailed "
                 'scrutiny by the Divisional Caste Certificate Scrutiny Committee. Required for professional degree '
                 'admissions (CAP rounds), government service reservations, and local governance elections.',
  'applicant_categories': ['student', 'employee', 'other'],
  'requirements': [{'document_id': 'aadhaar', 'necessity': 'required'},
                   {'document_id': 'caste_certificate', 'necessity': 'required'},
                   {'document_id': 'school_leaving_certificate',
                    'necessity': 'required',
                    'note': 'Educational record showing caste entry'},
                   {'document_id': 'photograph', 'necessity': 'required'},
                   {'document_id': 'relative_validity_record',
                    'necessity': 'optional',
                    'note': 'If any blood relative already holds a validity order'},
                   {'document_id': 'admission_letter',
                    'necessity': 'conditional',
                    'when': {'applicant_category': ['student']},
                    'note': 'Required only for students'},
                   {'group': 'address_proof',
                    'necessity': 'any_of',
                    'options': ['ration_card', 'electricity_bill', 'rent_agreement'],
                    'note': 'Any one current address proof'}],
  'application_info': {'where': 'Divisional Caste Certificate Scrutiny Committee Office or CCVIS Online Portal '
                                '(bartievalidity.maharashtra.gov.in)',
                       'mode': 'Online submission via CCVIS / BARTI portal with physical scrutiny submission',
                       'steps': ['Gather all required documents listed in the checklist',
                                 'Register and fill the application form on the CCVIS online portal',
                                 'Upload self-attested scanned copies of required proofs',
                                 'Submit physical dossier to the Divisional Caste Scrutiny Committee office',
                                 'Collect acknowledgement receipt and track application status online',
                                 'Attend scrutiny hearing if called by the committee',
                                 'Download digital certificate or collect physical certificate upon approval'],
                       'fee_note': 'No government fee for students applying through recognized academic institutions; '
                                   'nominal processing fee per government resolution for employees/others'},
  'verified': True,
  'official_source_url': 'https://bartievalidity.maharashtra.gov.in',
  'source_note': 'Verified against Maharashtra Act No. XXIII of 2001 and CCVIS / BARTI portal guidelines',
  'last_reviewed': '2026-10-19'},
 {'id': 'caste_certificate',
  'name': 'Caste Certificate',
  'aliases': ['caste cert', 'jaati certificate service', 'jaati praman patra'],
  'type': 'certificate',
  'department': 'Revenue and Forest Department, Government of Maharashtra',
  'description': 'A Caste Certificate certifies the caste, tribe, or community of an individual citizen. Issued by the '
                 'Sub-Divisional Officer (SDO) / Deputy Collector / Tahsildar under the Revenue Department. '
                 'Prerequisite for affirmative action benefits, scholarships, and the Caste Validity Certificate.',
  'applicant_categories': ['student', 'employee', 'other'],
  'requirements': [{'document_id': 'aadhaar', 'necessity': 'required'},
                   {'document_id': 'residence_proof', 'necessity': 'required'},
                   {'document_id': 'affidavit_stamp_paper',
                    'necessity': 'required',
                    'note': 'Self-declaration affidavit on prescribed stamp paper'},
                   {'document_id': 'photograph', 'necessity': 'required'},
                   {'document_id': 'self_declaration_form',
                    'necessity': 'required',
                    'note': 'Prescribed format under Maharashtra Right to Public Services Act'}],
  'application_info': {'where': 'Aaple Sarkar Citizen Services Portal (aaplesarkar.mahaonline.gov.in) or Tahsildar / '
                                'Setu Kendra / CSC',
                       'mode': 'Online via Aaple Sarkar Portal or offline via Setu / Maha e-Seva Kendra',
                       'steps': ['Login to Aaple Sarkar portal or visit the nearest Maha e-Seva Kendra / Setu office',
                                 'Fill the application form for Caste Certificate under Revenue Services',
                                 'Upload verified identity proof, address proof, and self-declaration affidavit',
                                 'Pay statutory service charge online or at the counter',
                                 'Collect system-generated acknowledgement receipt and application tracking number',
                                 'Revenue enquiry and verification conducted by Talati / Circle Officer',
                                 'Download digitally signed certificate from the portal once approved'],
                       'fee_note': 'Statutory fee of Rs. 33.60 via Aaple Sarkar portal under Maharashtra Right to '
                                   'Public Services Act'},
  'verified': True,
  'official_source_url': 'https://aaplesarkar.mahaonline.gov.in',
  'source_note': 'Verified against Aaple Sarkar Revenue Department Service Standards and RTS Act',
  'last_reviewed': '2026-10-19'},
 {'id': 'income_certificate',
  'name': 'Income Certificate',
  'aliases': ['income cert', 'annual income certificate', 'family income certificate'],
  'type': 'certificate',
  'department': 'Revenue and Forest Department, Government of Maharashtra',
  'description': 'An Income Certificate certifies the annual family income of an applicant from all legitimate '
                 'sources. Issued by the Executive Magistrate / Tahsildar for scholarships, fee concessions, EWS '
                 'reservations, and public welfare schemes.',
  'applicant_categories': ['student', 'employee', 'other'],
  'requirements': [{'document_id': 'aadhaar', 'necessity': 'required'},
                   {'document_id': 'residence_proof', 'necessity': 'required'},
                   {'document_id': 'income_proof',
                    'necessity': 'required',
                    'note': 'Salary slip, Form 16, or Talati income verification report'},
                   {'document_id': 'photograph', 'necessity': 'required'},
                   {'document_id': 'self_declaration_form',
                    'necessity': 'required',
                    'note': 'Self-declaration of annual income'},
                   {'document_id': 'bank_passbook',
                    'necessity': 'optional',
                    'note': 'Bank statement / passbook copy for financial verification'}],
  'application_info': {'where': 'Aaple Sarkar Portal (aaplesarkar.mahaonline.gov.in) or Sub-Divisional / Tahsil Office '
                                'Setu Kendra',
                       'mode': 'Online via Aaple Sarkar or offline via Maha e-Seva Kendra',
                       'steps': ['Create an account or login to Aaple Sarkar Maharashtra portal',
                                 "Select Revenue Department and choose 'Income Certificate'",
                                 'Fill applicant details and declare total annual income across all family members',
                                 'Attach salary certificate, Form 16, or Talati income enquiry report',
                                 'Submit application and pay the prescribed fee online',
                                 'Receive SMS update with tracking ID upon submission',
                                 'Download verified digitally signed certificate within 15 working days'],
                       'fee_note': 'Statutory service fee of Rs. 33.60 via Aaple Sarkar portal'},
  'verified': True,
  'official_source_url': 'https://aaplesarkar.mahaonline.gov.in',
  'source_note': 'Verified against Maharashtra Right to Public Services Act and Aaple Sarkar Portal Guidelines',
  'last_reviewed': '2026-10-19'},
 {'id': 'sample_scholarship_scheme',
  'name': 'Post-Matric Scholarship Scheme (MahaDBT)',
  'aliases': ['scholarship', 'merit scholarship', 'govt scholarship', 'state scholarship', 'mahadbt scholarship'],
  'type': 'scheme',
  'department': 'Social Justice & Special Assistance Department, Government of Maharashtra',
  'description': 'Government Post-Matric Scholarship Scheme for eligible students belonging to reserved categories '
                 '(SC, ST, VJNT, OBC, SBC) and economically weaker sections pursuing recognized post-secondary '
                 'education. Provides full tuition waiver, exam fee reimbursement, and maintenance allowance.',
  'applicant_categories': ['student'],
  'requirements': [{'document_id': 'aadhaar', 'necessity': 'required'},
                   {'document_id': 'caste_certificate', 'necessity': 'required'},
                   {'document_id': 'income_proof',
                    'necessity': 'required',
                    'note': 'Annual family income certificate issued by Tahsildar'},
                   {'document_id': 'school_leaving_certificate', 'necessity': 'required'},
                   {'document_id': 'admission_letter',
                    'necessity': 'required',
                    'note': 'College admission confirmation and fee receipt'},
                   {'document_id': 'photograph', 'necessity': 'required'},
                   {'document_id': 'bank_passbook',
                    'necessity': 'required',
                    'note': 'Aadhaar-seeded bank account for scholarship DBT disbursement'},
                   {'document_id': 'self_declaration_form',
                    'necessity': 'required',
                    'note': 'Self-declaration form of applicant and parent'},
                   {'group': 'address_proof',
                    'necessity': 'any_of',
                    'options': ['ration_card', 'electricity_bill', 'rent_agreement'],
                    'note': 'Any one address proof'}],
  'application_info': {'where': 'MahaDBT Portal (mahadbt.maharashtra.gov.in)',
                       'mode': 'Online application via MahaDBT Portal',
                       'steps': ['Register on the MahaDBT portal using Aadhaar authentication',
                                 'Fill profile information including personal, caste, and income details',
                                 'Select the applicable Post-Matric Scholarship scheme for your category',
                                 'Upload scanned copies of required documents and enter bank details',
                                 'Submit the application and forward printout to college administration',
                                 'College verifies and forwards application to District Welfare Officer',
                                 'Scholarship funds transferred directly to Aadhaar-seeded bank account via DBT'],
                       'fee_note': 'Free of cost. No application or registration fee on MahaDBT'},
  'verified': True,
  'official_source_url': 'https://mahadbt.maharashtra.gov.in',
  'source_note': 'Verified against MahaDBT portal rules and Social Justice Department circulars',
  'last_reviewed': '2026-10-19'}]

GUIDES_SEED = [{'id': 'guide_aadhaar',
  'document_id': 'aadhaar',
  'what_it_is': 'Aadhaar is a 12-digit unique identification number issued by the Unique Identification Authority of '
                'India (UIDAI) based on biometric (fingerprints and iris) and demographic data. It serves as universal '
                'proof of identity and residence across India for all government and private services.',
  'documents_required': ['Proof of Identity (PAN Card, Voter ID, Passport, Driving Licence, or Ration Card)',
                         'Proof of Address (Electricity bill, Water bill, Registered Rent Agreement, Bank Passbook, or '
                         'Voter ID)',
                         'Proof of Date of Birth (Birth Certificate, School Leaving Certificate, or Passport)'],
  'procedure_steps': ['Locate the nearest Aadhaar Seva Kendra (ASK) or authorized bank/post office enrollment centre '
                      'via appointments.uidai.gov.in.',
                      'Book an online appointment to save queue time, or visit directly as a walk-in applicant.',
                      'Fill the Aadhaar Enrolment / Update Form accurately with your full demographic details.',
                      'Present original Proof of Identity (PoI), Proof of Address (PoA), and Proof of Date of Birth '
                      '(DoB) for physical verification (originals are verified and returned immediately).',
                      'Undergo biometric capture: 10 fingerprints, both iris scans, and a live facial photograph.',
                      'Review your details on the operator screen and collect the printed Enrolment ID (EID) '
                      'acknowledgement slip containing the 28-digit tracking number.',
                      'Track status at uidai.gov.in; once generated, download your digital password-protected '
                      'e-Aadhaar PDF or order a PVC Smart Card for Rs. 50 delivered by Speed Post.'],
  'where_how_to_apply': 'UIDAI Aadhaar Seva Kendras, designated Nationalized Bank branches, Post Offices, or BSNL '
                        'customer service centres. Locate at uidai.gov.in.',
  'precautions': ['Carry original documents — uncertified photocopies are rejected at the enrolment counter.',
                  "Ensure spelling of name, date of birth, and parents' names match consistently across all proofs.",
                  'Never share your Aadhaar OTP or biometric access with unauthorized third parties.',
                  'Keep the 28-digit Enrolment ID slip safely until your card is generated.'],
  'official_link': 'https://uidai.gov.in',
  'verified': True},
 {'id': 'guide_pan_card',
  'document_id': 'pan_card',
  'what_it_is': 'A PAN (Permanent Account Number) is a 10-digit unique alphanumeric identifier issued by the Income '
                'Tax Department. It is legally mandatory for opening bank accounts, receiving taxable income, '
                'conducting property and vehicle transactions, mutual funds investments, and filing income tax '
                'returns.',
  'documents_required': ['Aadhaar Card (serves as complete Proof of Identity, Address, and Date of Birth for paperless '
                         'e-KYC)',
                         'Recent passport-size colour photograph (if applying via non-paperless mode)',
                         'Active mobile number linked with Aadhaar for OTP verification'],
  'procedure_steps': ['For instant digital e-PAN (Free, takes 10 minutes): Visit the Income Tax e-Filing Portal '
                      "(eportal.incometax.gov.in) > Quick Links > 'Instant E-PAN' > 'Get New e-PAN'.",
                      'Enter your 12-digit Aadhaar number, accept declaration, and enter the 6-digit OTP received on '
                      'your Aadhaar-linked mobile number.',
                      'Confirm demographic details pulled directly from UIDAI database and submit; your digitally '
                      'signed e-PAN is issued instantly in PDF format.',
                      'For physical plastic laminated card: Visit the Protean (formerly NSDL) PAN portal '
                      '(onlineservices.nsdl.com) or UTIITSL portal.',
                      "Select Application Type 'Form 49A' (Indian Citizen) and Category 'Individual'.",
                      "Choose 'Submit digitally through e-KYC & e-Sign (Paperless)' for the quickest dispatch without "
                      'sending physical documents.',
                      'Pay the nominal government processing fee of Rs. 107 (online via UPI, Netbanking, or Debit '
                      'Card).',
                      'Download your e-PAN acknowledgment PDF; the physical laminated PAN card is delivered by India '
                      'Post Speed Post to your registered Aadhaar address within 7-12 working days.'],
  'where_how_to_apply': 'Online via Income Tax e-Filing Portal (eportal.incometax.gov.in) or Protean NSDL / UTIITSL '
                        'portals. Offline at authorized TIN-Facilitation Centres / PAN Centres across India.',
  'precautions': ['Your mobile number must be active and linked with Aadhaar to utilize instant paperless e-KYC.',
                  'Holding more than one PAN card is illegal under Section 272B of Income Tax Act and attracts a '
                  'penalty of Rs. 10,000.',
                  'Verify that your name and date of birth match your Aadhaar exactly before applying.'],
  'official_link': 'https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html',
  'verified': True},
 {'id': 'guide_voter_id',
  'document_id': 'voter_id',
  'what_it_is': 'The Electors Photo Identity Card (EPIC), widely known as the Voter ID Card, is issued by the Election '
                "Commission of India. It certifies an individual's enrollment on the electoral roll, guarantees the "
                'constitutional right to vote in parliamentary and assembly elections, and serves as premier proof of '
                'Indian identity and address.',
  'documents_required': ['Proof of Age / Date of Birth (Birth Certificate, Aadhaar Card, PAN Card, or 10th School '
                         'Leaving Marksheet)',
                         'Proof of Residence (Aadhaar Card, recent Electricity/Water/Gas bill, Bank Passbook, or '
                         'Registered Rent Agreement)',
                         'One recent passport-size photograph (3.5 cm x 4.5 cm with white background)'],
  'procedure_steps': ['Visit the official Election Commission of India National Voter Services Portal '
                      "(voters.eci.gov.in) or download the 'Voter Helpline' mobile application.",
                      'Sign up or log in using your mobile number and password.',
                      "Click on 'Fill Form 6' (Application for New Voters / First-Time Voters).",
                      'Select your State, District, and Parliamentary / Assembly Constituency.',
                      "Enter personal details: Full Name, Father's / Mother's / Spouse's Name, Date of Birth, and "
                      'Current Residential Address.',
                      'Upload self-attested copies of your Age Proof, Address Proof, and Passport Photograph.',
                      'Enter details of family members already enrolled in the same electoral roll (if available) to '
                      'ensure registration in the same polling booth.',
                      'Review summary, submit application, and note the unique 14-character alphanumeric Reference '
                      'Tracking Number.',
                      'The local Booth Level Officer (BLO) may visit your residence for physical verification or '
                      'verify your documents telephonically.',
                      'Once approved by the Electoral Registration Officer (ERO), download the digital color e-EPIC '
                      'PDF from voters.eci.gov.in; a high-security PVC Voter ID card is posted free of cost via Speed '
                      'Post.'],
  'where_how_to_apply': 'Online at voters.eci.gov.in or Voter Helpline App. Offline by submitting physical Form 6 to '
                        'the local Electoral Registration Officer (ERO) or Booth Level Officer (BLO) at the Tehsil / '
                        'Municipal Corporation voter facilitation counter.',
  'precautions': ['Applicant must be at least 18 years of age (qualifying dates are 1st Jan, 1st April, 1st July, and '
                  '1st October of the year).',
                  'Enrollment in multiple constituencies or holding two Voter IDs is a criminal offence under '
                  'Representation of the People Act.',
                  'Ensure the house/flat number and lane name match your utility bills to avoid BLO field rejection.'],
  'official_link': 'https://voters.eci.gov.in',
  'verified': True},
 {'id': 'guide_passport',
  'document_id': 'passport',
  'what_it_is': 'An Indian Passport is an official sovereign travel document issued by the Ministry of External '
                "Affairs, certifying the holder's citizenship, nationality, and identity for international travel, "
                'foreign residency, and overseas employment.',
  'documents_required': ['Proof of Date of Birth (Birth Certificate, School Leaving Certificate, or Matriculation '
                         'Certificate)',
                         'Proof of Present Residential Address (Aadhaar Card, Electricity Bill, Water Bill, Bank '
                         'Passbook with photo, or Rent Agreement)',
                         'Proof of Identity (Aadhaar Card, PAN Card, or Voter ID)',
                         'Non-ECR (Emigration Check Not Required) Proof: 10th standard passing certificate / higher '
                         'degree marksheets'],
  'procedure_steps': ['Register on the official Passport Seva Portal (passportindia.gov.in) and create a user account.',
                      "Click 'Apply for Fresh Passport / Re-issue of Passport' and complete the application form "
                      '(selecting Normal or Tatkaal).',
                      'Fill demographic details, family details, present and permanent addresses, and emergency '
                      'contact.',
                      'Declare Non-ECR status and submit details of educational qualifications (matriculation or '
                      'higher qualifies for Non-ECR).',
                      'Pay the passport fee online (Rs. 1,500 for standard 36-page booklet; Rs. 2,000 for 60-page '
                      'jumbo booklet; Tatkaal requires an additional Rs. 2,000).',
                      'Schedule an appointment slot at your nearest Passport Seva Kendra (PSK) or Post Office Passport '
                      'Seva Kendra (POPSK).',
                      'Visit the PSK/POPSK on the appointment date with all original documents and their self-attested '
                      'photocopies.',
                      'Complete biometrics, photograph capture, and document scrutiny across Counters A, B, and C.',
                      'Collect the Exit Slip / Acknowledgement and track status online; local police station conducts '
                      'residential verification.',
                      'Upon police verification approval, your passport is printed, laminated, and dispatched via '
                      'India Post Speed Post.'],
  'where_how_to_apply': 'Online appointment via passportindia.gov.in. In-person biometric appearance at designated '
                        'Passport Seva Kendra (PSK) or Post Office Passport Seva Kendra (POPSK).',
  'precautions': ['Carry all original documents — applications are put on hold if any original proof is missing.',
                  'Do not engage middlemen or unofficial travel agents promising unauthorized fast-track issuance.',
                  'Ensure accurate disclosure of all residential addresses lived at during the preceding 12 months to '
                  'avoid police verification penalties.'],
  'official_link': 'https://www.passportindia.gov.in',
  'verified': True},
 {'id': 'guide_driving_licence',
  'document_id': 'driving_licence',
  'what_it_is': 'A Driving Licence (DL) is an official legal authorization issued by the Regional Transport Authority '
                '/ Regional Transport Office (RTO) under the Motor Vehicles Act, 1988, permitting an individual to '
                'drive designated categories of motor vehicles (Motorcycle with/without gear, Light Motor Vehicle '
                'cars, or Transport/Commercial vehicles) on public roads.',
  'documents_required': ['Proof of Age (Aadhaar Card, Birth Certificate, PAN Card, or 10th School Leaving Certificate)',
                         'Proof of Current Address (Aadhaar Card, Electricity Bill, Voter ID, or Registered Rent '
                         'Agreement)',
                         'Passport-size colour photographs (3-4 copies)',
                         'Form 1 (Self-declaration of physical fitness) or Form 1A Medical Certificate (for commercial '
                         'vehicles or applicants over 40 years)'],
  'procedure_steps': ['Phase 1: Learner Licence (LL) — Visit Parivahan Sarathi portal (sarathi.parivahan.gov.in), '
                      "select your State, and click 'Apply for Learner Licence'.",
                      'Fill personal and address details and select class of vehicles (MCWG - Motorcycle with Gear, '
                      'LMV - Light Motor Vehicle).',
                      'Upload Age Proof, Address Proof, and photo/signature.',
                      'Pay the Learner Licence test fee online (approx. Rs. 150-200 per category).',
                      'Take the online computer-based Learner Licence test from home (via Aadhaar authentication) or '
                      'book slot at RTO; test covers road signs, lane rules, and safety regulations.',
                      'Download your digital Learner Licence immediately upon passing the test (valid for 6 months '
                      'across India).',
                      'Phase 2: Permanent Driving Licence (DL) — After a mandatory 30-day practice period, return to '
                      "sarathi.parivahan.gov.in and select 'Apply for Driving Licence'.",
                      'Enter your LL application number, choose the practical driving test appointment date at your '
                      'local RTO, and pay the DL fee.',
                      'Appear at the RTO test track on the scheduled day with the corresponding vehicle class and '
                      'perform the driving test (including reversing, gradient stop, and figure-8 maneuvers).',
                      "Upon the Motor Vehicle Inspector's approval, biometrics are recorded, and your chip-embedded "
                      'Smart Card Driving Licence is delivered via Speed Post.'],
  'where_how_to_apply': 'Parivahan Sarathi Portal (sarathi.parivahan.gov.in) and your designated District Regional '
                        'Transport Office (RTO) / Sub-RTO.',
  'precautions': ['You cannot apply for a permanent DL before 30 days from the date of Learner Licence issuance.',
                  'Your Learner Licence expires after 180 days — ensure you pass the practical test before expiry.',
                  'Ensure the test vehicle has valid insurance, PUC certificate, and fitness/registration documents '
                  'when appearing for the RTO driving test.'],
  'official_link': 'https://sarathi.parivahan.gov.in',
  'verified': True},
 {'id': 'guide_birth_certificate',
  'document_id': 'birth_certificate',
  'what_it_is': "A Birth Certificate is the permanent legal record of a child's birth, documenting the child's date, "
                "time, and sex, along with parents' names and place of occurrence. Regulated under the Registration of "
                'Births and Deaths Act, 1969, it is the primary foundational document for school admission, passport '
                'issuance, Aadhaar registration, and voter enrollment.',
  'documents_required': ['Hospital Discharge Summary / Birth Report Form issued by the Medical Officer / Hospital',
                         'Aadhaar Cards of both Father and Mother',
                         'Marriage Certificate of parents or joint affidavit (if requested)',
                         'Address Proof of Parents (Aadhaar, Electricity Bill, Ration Card)'],
  'procedure_steps': ['For Institutional Births: Hospitals, nursing homes, and maternity centres report the birth '
                      'event directly to the local Registrar of Births & Deaths within 21 days; collect the hospital '
                      'birth reporting slip.',
                      'For Home Births: The head of household or Gram Panchayat Anganwadi worker must report the birth '
                      'to the local registrar within 21 days.',
                      'Online Application: Visit the Civil Registration System (CRS) portal (crsorgi.gov.in) or state '
                      'citizen portal (e.g. Aaple Sarkar in Maharashtra, e-District in Delhi/UP, Seva Sindhu in '
                      'Karnataka).',
                      'Log in, navigate to Birth Certificate services, and enter hospital name, date of birth, child '
                      'name, and parent details.',
                      "Upload parents' Aadhaar cards and hospital discharge birth slip.",
                      "Child Name Inclusion: If the child was not named at initial registration, apply for 'Child Name "
                      "Addition' online or at the municipal ward health department within 12 months free of fee.",
                      'Delayed Registration: Births reported after 21 days but within 30 days require late fee; up to '
                      '1 year requires Tehsildar / District Health Officer permission; after 1 year requires an order '
                      'from the Sub-Divisional Magistrate (SDM) / Executive Magistrate.',
                      'Download digitally signed QR-coded Birth Certificate PDF or collect sealed physical copies from '
                      'the Municipal Ward Office / Gram Panchayat.'],
  'where_how_to_apply': 'Civil Registration System (crsorgi.gov.in), State Citizen Services Portals (Aaple Sarkar, '
                        'eDistrict), or local Municipal Corporation Health Department / Gram Panchayat Office.',
  'precautions': ['Register the birth within 21 days to avoid complex magistrate inquiry procedures.',
                  "Check spelling of parents' names against their official Aadhaar and educational certificates before "
                  'final submission.',
                  "Always include the child's formal legal name in the register before using the certificate for "
                  'school admission or passport.'],
  'official_link': 'https://crsorgi.gov.in',
  'verified': True},
 {'id': 'guide_death_certificate',
  'document_id': 'death_certificate',
  'what_it_is': 'A Death Certificate is the official document issued by the Registrar of Births and Deaths confirming '
                "the demise of an individual, recording the deceased's name, date, time, cause, and location of death. "
                'It is mandatory for claiming life insurance, transferring bank balances, releasing pensions, settling '
                'provident funds, and mutating ancestral land/property titles.',
  'documents_required': ['Form 4 / 4A: Medical Certificate of Cause of Death (MCCD) signed by attending physician or '
                         'hospital superintendent',
                         'Crematorium / Burial Ground receipt or cemetery certificate confirming disposal of mortal '
                         'remains',
                         'Aadhaar Card of the deceased person',
                         'Aadhaar Card and relationship proof of the applicant (spouse, child, or next of kin)'],
  'procedure_steps': ['Obtain the Medical Certificate of Cause of Death (MCCD Form 4/4A) from the treating hospital or '
                      'registered medical practitioner.',
                      'Obtain the original receipt/slip from the municipal crematorium or burial ground recording date '
                      'and cremation registration number.',
                      'Report the death to the local Municipal Corporation / Nagar Palika Health Office or Gram '
                      'Panchayat within 21 days.',
                      'Apply online through the State Citizen Services Portal (e.g. Aaple Sarkar in Maharashtra, '
                      'e-District in Delhi/UP) or crsorgi.gov.in.',
                      "Upload the medical death summary, crematorium slip, Aadhaar of deceased, and applicant's "
                      'identity proof.',
                      'Pay the nominal statutory fee (Rs. 5 to Rs. 30 per copy).',
                      'Municipal health inspector verifies records against crematorium logs.',
                      'Download the digitally signed, QR-coded Death Certificate PDF or collect stamped physical '
                      'copies from the ward health office.'],
  'where_how_to_apply': 'Municipal Corporation Health Department, Nagar Palika office, Gram Panchayat, or State '
                        'Citizen Services Portals (crsorgi.gov.in, Aaple Sarkar, eDistrict).',
  'precautions': ['Ensure the death is registered within 21 days — delayed reporting beyond 1 year requires an order '
                  'from the Sub-Divisional Magistrate.',
                  "Check that the deceased person's name, age, and father's/spouse's name match bank and property "
                  'records exactly.',
                  'Retain multiple original certified stamped copies, as separate copies are needed for banks, '
                  'insurance, pension, and property mutation.'],
  'official_link': 'https://crsorgi.gov.in',
  'verified': True},
 {'id': 'guide_marriage_certificate',
  'document_id': 'marriage_certificate',
  'what_it_is': 'A Marriage Registration Certificate is the legal proof of the solemnization and validity of a '
                'marriage, registered under the Hindu Marriage Act, 1955 or Special Marriage Act, 1954. It is '
                'essential for obtaining a spouse visa, joint bank accounts, insurance nominations, passport spouse '
                'name endorsement, and legal inheritance.',
  'documents_required': ['Wedding Invitation Card (original printed invitation card)',
                         'Joint Wedding Photographs (clearly displaying the bride and groom performing wedding rituals '
                         'or garland exchange)',
                         'Proof of Age for both Husband (minimum 21 years) and Wife (minimum 18 years): Birth '
                         'Certificate, 10th LC, or Passport',
                         'Proof of Residence of both parties (Aadhaar Card, Electricity Bill, or Voter ID)',
                         'Aadhaar Cards and Passport-size photographs of 3 adult witnesses who attended the wedding '
                         'ceremony'],
  'procedure_steps': ['Visit the State Citizen Services Portal (e.g. Aaple Sarkar in Maharashtra, e-District in Delhi) '
                      'or Municipal Corporation Marriage Portal.',
                      "Select 'Marriage Registration' and choose the applicable Act (Hindu Marriage Act for already "
                      'solemnized marriages; Special Marriage Act for court marriages).',
                      'Enter details of the husband, wife, marriage date, and religious/ceremonial solemnization '
                      'venue.',
                      'Upload wedding card, joint wedding photos, age proofs, address proofs, and witness details.',
                      'Pay the prescribed statutory registration fee online (approx. Rs. 100-300).',
                      'Book an appointment slot for personal appearance before the Registrar of Marriages / '
                      'Sub-Registrar.',
                      'Both husband and wife, accompanied by the 3 registered witnesses carrying original Aadhaar '
                      'cards, appear in person before the Marriage Registrar.',
                      'Sign the official marriage register in the presence of the Registrar.',
                      'Collect the embossed physical Certificate of Marriage or download the digitally signed '
                      'certificate with QR code from the portal.'],
  'where_how_to_apply': 'State Citizen Services Portals (Aaple Sarkar, e-District), Office of the Sub-Registrar of '
                        'Assurances, or Municipal Corporation Marriage Registration Department.',
  'precautions': ['All 3 witnesses must be adults (18+) and must carry original photo identification (preferably '
                  'Aadhaar Card).',
                  'Ensure the wedding ceremony photos clearly show the faces of both partners exchanging garlands or '
                  'rings.',
                  'Ensure spelling of names on the application matches educational marksheets and Aadhaar cards '
                  'exactly.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_caste_certificate',
  'document_id': 'caste_certificate',
  'what_it_is': 'A Caste Certificate is a statutory document issued by the Revenue Department (Sub-Divisional Officer '
                '/ Tahsildar) certifying that a citizen belongs to a recognized Scheduled Caste (SC), Scheduled Tribe '
                '(ST), Other Backward Class (OBC), or Nomadic Tribe (VJNT). It is required for affirmative action '
                'benefits, scholarships, and fee waivers.',
  'documents_required': ['Aadhaar Card of the applicant and father',
                         'Proof of Residence (Ration Card, Electricity Bill, or Registered Rent Agreement)',
                         'School Leaving Certificate (SLC) of applicant showing caste entry',
                         "Father's or paternal grandfather's School Leaving Certificate or primary school record "
                         'showing caste',
                         'Self-declaration affidavit on non-judicial stamp paper declaring caste lineage',
                         'Ancestral residence proof before the statutory cutoff date (1950 for SC/ST, 1967 for '
                         'OBC/VJNT in Maharashtra)'],
  'procedure_steps': ['Log in to the State Citizen Portal (e.g. Aaple Sarkar in Maharashtra: '
                      'aaplesarkar.mahaonline.gov.in) or visit your local Tehsil Setu Kendra / CSC.',
                      'Select Revenue Department > Caste Certificate and select your sub-category (SC, ST, OBC, VJNT, '
                      'or SBC).',
                      'Fill applicant details, family pedigree, and ancestral village/district information.',
                      "Upload scanned copies of Aadhaar, residence proof, applicant's school leaving certificate, and "
                      "father's/grandfather's school records.",
                      'Pay the statutory service charge online (approx. Rs. 33.60 on Aaple Sarkar) and print the '
                      'acknowledgement receipt with the application tracking number.',
                      'The application is routed to the local Talati / Circle Officer for ancestral verification and '
                      'spot inquiry.',
                      'Upon inquiry approval, the Sub-Divisional Officer (SDO) or Deputy Collector digitally signs and '
                      'issues the Caste Certificate within 21 working days.',
                      'Download the digitally signed certificate with official barcode and QR code directly from your '
                      'portal dashboard.'],
  'where_how_to_apply': 'Online via Aaple Sarkar (aaplesarkar.mahaonline.gov.in) or offline at Sub-Divisional Officer '
                        '(SDO) / Tahsil Setu Kendra / CSC Maha e-Seva Kendra.',
  'precautions': ['Caste must be proved through the paternal lineage (father, paternal uncle, paternal grandfather). '
                  'Maternal records are not legally acceptable.',
                  'The caste name must match the official Presidential Order / State Government Gazette notification '
                  'letter for letter.',
                  'Retain your application tracking ID to track status within the 21-day timeline guaranteed by the '
                  'Right to Services Act.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_caste_validity_certificate',
  'document_id': 'caste_validity_certificate',
  'what_it_is': 'A Caste Validity Certificate is an essential judicial confirmation issued by the Divisional Caste '
                "Certificate Scrutiny Committee, certifying that an applicant's Caste Certificate is genuine and "
                'legally authentic. In Maharashtra, it is strictly mandatory for admission to all professional '
                'undergraduate/postgraduate degree courses (CAP rounds for Engineering, Medicine, Pharmacy, MBA, Law) '
                'and government jobs.',
  'documents_required': ['Original Caste Certificate issued by competent Sub-Divisional Officer (SDO)',
                         "Applicant's School Leaving Certificate (SLC) showing caste and date of birth",
                         "Father's / Paternal Grandfather's Primary School Leaving Certificate or General Register "
                         '(GR) extract showing caste prior to cutoff date (1950 for SC/ST, 1967 for OBC/VJNT)',
                         'Certified copy of Caste Validity Certificate of father, sibling, or paternal relative (if '
                         'already issued)',
                         'College Bonafide Certificate / Allotment Letter (Form 16 recommendation from educational '
                         'institution)',
                         'Genealogical Family Tree (Vanshavali) on Rs. 100 stamp paper with notarised affidavit'],
  'procedure_steps': ['Register on the CCVIS online portal (barti.maharashtra.gov.in) maintained by Dr. Babasaheb '
                      'Ambedkar Research and Training Institute (BARTI).',
                      'Select Form 16 (for educational admissions) or Form 17 (for employment) and fill in personal, '
                      'educational, and ancestral pedigree data.',
                      'Upload self-attested scanned copies of the underlying caste certificate, school records, and '
                      'ancestral documents.',
                      'Generate and print the online application dossier.',
                      'Get the college principal or employer to attest and endorse the institutional recommendation '
                      'section.',
                      'Submit the physical dossier along with self-attested document copies to the Divisional Caste '
                      'Scrutiny Committee Office in your administrative district.',
                      'Collect acknowledgement receipt and track vigilance cell verification status online.',
                      'Attend the scrutiny committee hearing if summoned by the vigilance officer for statement '
                      'recording.',
                      'Upon committee approval, download the digital validity order or collect the physical embossed '
                      'Caste Validity Certificate from the committee office.'],
  'where_how_to_apply': 'Online at CCVIS BARTI Portal (bartievalidity.maharashtra.gov.in) and physical dossier '
                        'submission to the respective Divisional Caste Scrutiny Committee Office.',
  'precautions': ['Pre-1950 (for SC/ST) or pre-1967 (for OBC/VJNT) evidence of paternal ancestors residing in '
                  'Maharashtra is mandatory under Act XXIII of 2001.',
                  'If a paternal blood relative holds a valid validity certificate, attach it prominently to expedite '
                  'clearance.',
                  'Never submit altered or overwritten school records — the vigilance cell conducts spot forensic '
                  'inspections at original school archives.'],
  'official_link': 'https://bartievalidity.maharashtra.gov.in',
  'verified': True},
 {'id': 'guide_non_creamy_layer_certificate',
  'document_id': 'non_creamy_layer_certificate',
  'what_it_is': 'A Non-Creamy Layer (NCL) Certificate certifies that an individual belonging to an OBC, VJNT, NT, or '
                "SBC category does not fall into the 'creamy layer' category, meaning their family's gross annual "
                'income from non-agricultural sources does not exceed the statutory ceiling of Rs. 8 Lakh per annum '
                'for 3 consecutive financial years. It is mandatory to claim reservation benefits in state and central '
                'educational admissions (NEET, JEE, MHT-CET, UPSC) and recruitment.',
  'documents_required': ['Existing valid Caste Certificate issued by Sub-Divisional Officer / Tahsildar',
                         'Proof of Income for the last 3 consecutive financial years (Income Certificate from '
                         'Tahsildar, Form 16, or IT Returns)',
                         'Proof of Residence (Electricity Bill, Ration Card, or Domicile Certificate)',
                         "Applicant's and Father's School Leaving Certificate showing caste entry",
                         'Self-declaration affidavit of non-creamy layer status on prescribed format'],
  'procedure_steps': ['Log in to the State Citizen Portal (e.g. Aaple Sarkar in Maharashtra: '
                      'aaplesarkar.mahaonline.gov.in) or visit your nearest Maha e-Seva Kendra.',
                      "Select Revenue Department > Services > 'Non-Creamy Layer Certificate'.",
                      'Enter details of your existing Caste Certificate (certificate number, issuing officer, and '
                      'date).',
                      'Declare total family income broken down across each of the preceding 3 financial years.',
                      'Upload income proofs, caste certificate, residence proof, and self-declaration.',
                      'Pay the online processing fee (Rs. 33.60 on Aaple Sarkar) and receive the application tracking '
                      'ID.',
                      'The local Talati and Circle Inspector review family landholdings and financial declarations.',
                      'Tahsildar / Sub-Divisional Officer issues the digitally signed Non-Creamy Layer Certificate '
                      'valid for 1 or 3 financial years (typically ending March 31 of the validity cycle).',
                      'Download the verified digital certificate with QR code seal from your citizen dashboard.'],
  'where_how_to_apply': 'Online at Aaple Sarkar Portal (aaplesarkar.mahaonline.gov.in) or offline at Sub-Divisional '
                        'Officer / Tahsil Setu Kendra.',
  'precautions': ['Income from agricultural land and salaries of Class I / II government officers have specific '
                  'exclusion/inclusion rules under DoPT guidelines — verify guidelines carefully.',
                  'Ensure your NCL certificate is valid through the entire academic admission cycle (admissions '
                  'require certificate valid up to March 31 of the admission academic year).',
                  'SC and ST categories do not require Non-Creamy Layer certificates; NCL applies only to OBC, VJNT, '
                  'NT, and SBC.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_ews_certificate',
  'document_id': 'ews_certificate',
  'what_it_is': 'An Economically Weaker Section (EWS) Certificate provides 10% reservation in government jobs and '
                'central/state educational admissions to citizens belonging to the General (unreserved) category whose '
                'gross annual family income is below Rs. 8 Lakh per annum and who meet prescribed asset ceiling '
                'criteria under the 103rd Constitutional Amendment Act, 2019.',
  'documents_required': ['Aadhaar Card of applicant and parents',
                         'Proof of Annual Family Income from all sources for the preceding financial year (Tahsildar '
                         'Income Certificate, Salary Slips / Form 16, or ITR)',
                         'Land revenue record (7/12 extract or Khatauni) proving family does not hold 5 acres or more '
                         'of agricultural land',
                         'Property ownership document / municipal tax receipt proving residential flat is under 1,000 '
                         'sq ft (or residential plot under prescribed limits)',
                         'Proof of Residence (Electricity Bill, Domicile Certificate, or Ration Card)',
                         'Self-declaration affidavit of belonging to General Category and satisfying EWS income & '
                         'asset criteria'],
  'procedure_steps': ['Obtain the prescribed Central or State EWS application format from the State Citizen Services '
                      'Portal (Aaple Sarkar / e-District) or local Tehsil office.',
                      'Declare total family income across all earning members (parents, spouse, siblings below 18) for '
                      'the previous financial year.',
                      'Attach agricultural land records (7/12 extract) and residential property documents showing '
                      'compliance with asset ceilings.',
                      'Attach Aadhaar, residence proof, and notarised self-declaration affidavit on stamp paper.',
                      'Submit the application online via the State Citizen Portal or in person at the Tahsil Setu '
                      'Kendra / SDM office counter.',
                      'Revenue Inspector (Lekhpal/Talati) verifies asset declarations against land revenue records.',
                      'Sub-Divisional Magistrate (SDM) or Tehsildar signs and issues the Income and Asset Certificate '
                      'for EWS.',
                      'Download the digitally signed certificate or collect the physical stamped copy with '
                      'registration barcode.'],
  'where_how_to_apply': 'State Citizen Services Portals (Aaple Sarkar, e-District) or Tahsil / Sub-Divisional '
                        'Magistrate (SDM) Office.',
  'precautions': ['Reserved category citizens (SC, ST, OBC) cannot apply for EWS; EWS is exclusively for unreserved '
                  'General category citizens.',
                  'The certificate is valid for only one financial year (1st April to 31st March) and must be renewed '
                  'annually.',
                  'Family income includes income from all sources: salary, business, agriculture, profession, and bank '
                  'interest.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_domicile_certificate',
  'document_id': 'domicile_certificate',
  'what_it_is': 'A Domicile Certificate (also called Residence / Permanent Resident Certificate) proves that an '
                'individual is a bona fide permanent resident of a particular state, having resided there continuously '
                'for the statutory duration (typically 10 to 15 years). It is required for state quota seats in '
                'engineering and medical colleges, state government employment, and scholarship disbursements.',
  'documents_required': ['Aadhaar Card with local state address',
                         'Birth Certificate or School Leaving Certificate confirming birthplace in the state',
                         'Proof of Continuous Residence for 10-15 years: Consecutive school/college marksheets, '
                         "parents' ration card, property tax receipts, electricity bills, or voter ID",
                         'Self-declaration affidavit on stamp paper declaring unbroken residency and that no domicile '
                         'of any other state is held',
                         'Recent passport-size photographs'],
  'procedure_steps': ['Log in to your State Citizen Services Portal (e.g. Aaple Sarkar in Maharashtra, e-District in '
                      'Delhi/UP, Seva Sindhu in Karnataka).',
                      "Select Revenue Department > 'Age, Nationality & Domicile Certificate'.",
                      'Enter personal details, educational history spanning primary to secondary schooling, and '
                      'residential addresses.',
                      'Upload birth certificate, continuous residence proof spanning the statutory duration, and '
                      'self-declaration affidavit.',
                      'Pay the online processing fee (approx. Rs. 33.60 on Aaple Sarkar) and receive your application '
                      'receipt.',
                      'The application is scrutinized by the Talati / Circle Officer to verify uninterrupted '
                      'residential history.',
                      'Tahsildar / Sub-Divisional Magistrate issues the digitally signed Domicile Certificate with QR '
                      'code seal within 15-21 working days.',
                      'Download the verified certificate directly from your citizen portal inbox.'],
  'where_how_to_apply': 'State Citizen Services Portals (Aaple Sarkar, e-District, Seva Sindhu) or local Tahsil / '
                        'Sub-Divisional Magistrate (SDM) Office Setu Kendra.',
  'precautions': ['A citizen can legally hold the domicile of only ONE state in India at any given time. Holding dual '
                  'domiciles is a punishable offence.',
                  'Ensure the documents submitted provide evidence of continuous residence without unexplained '
                  'multi-year gaps.',
                  "In Maharashtra, the combined 'Age, Nationality & Domicile Certificate' is the standard composite "
                  'document issued by the Revenue Department.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_income_proof',
  'document_id': 'income_proof',
  'what_it_is': 'An Income Proof / Income Certificate certifies the annual family income of an individual citizen from '
                'all sources (employment, business, agricultural land, investments). Issued by the Executive '
                'Magistrate / Tahsildar, it is necessary to qualify for government scholarships, tuition fee waivers, '
                'ration cards, healthcare schemes (Ayushman Bharat), and housing subsidies.',
  'documents_required': ['Aadhaar Card of the applicant and breadwinner',
                         'Proof of Residence (Electricity Bill, Ration Card, or Rent Agreement)',
                         'Income Verification Proof: Form 16 / Salary Slips (for salaried employees), Income Tax '
                         'Returns (for business owners), or Talati Income Panchnama (for farmers/unorganized sector)',
                         'Self-declaration of family income on prescribed statutory format',
                         'Bank passbook statement of the preceding 3-6 months'],
  'procedure_steps': ['Log in to the State Citizen Portal (e.g. Aaple Sarkar in Maharashtra) or visit the local Tahsil '
                      'Setu Kendra.',
                      "Select Revenue Department > 'Income Certificate (1 Year or 3 Years)'.",
                      "Enter applicant personal details, family members' names, occupations, and respective annual "
                      'income breakdown.',
                      'Upload Aadhaar card, residence proof, self-declaration, and salary certificate / Talati '
                      'agricultural income panchnama.',
                      'Pay the statutory application fee online (Rs. 33.60 on Aaple Sarkar) and save the tracking '
                      'acknowledgement receipt.',
                      'Local Talati / Lekhpal conducts inquiry to verify financial circumstances and land revenue '
                      'records.',
                      'The Tahsildar or Executive Magistrate signs and issues the digitally certified Income '
                      'Certificate with QR verification code within 15 working days.',
                      'Download and print the certificate directly from the citizen portal.'],
  'where_how_to_apply': 'State Citizen Services Portal (Aaple Sarkar, e-District, Seva Sindhu) or local Tahsildar / '
                        'Sub-Divisional Office Setu Kendra / CSC Kendra.',
  'precautions': ['Under-reporting income is an offence under the Indian Penal Code and causes immediate '
                  'disqualification from schemes and cancellation of admissions.',
                  'Income certificates are typically issued for 1 financial year or 3 financial years — ensure you '
                  'choose the validity period required by your scheme.',
                  'Gross family income must include income of both parents/spouse, not merely the applicant student.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_disability_certificate',
  'document_id': 'disability_certificate',
  'what_it_is': 'The Unique Disability ID (UDID) Card and Disability Certificate is a single, national-level identity '
                'document issued to Persons with Disabilities (PwD) under the Rights of Persons with Disabilities Act, '
                '2016. It certifies the percentage of permanent or temporary disability and entitles the holder to 4% '
                'reservation in government jobs, 5% reservation in higher education, assistive aids, railway/bus '
                'concessions, and disability pensions.',
  'documents_required': ['Aadhaar Card of the applicant',
                         'Passport-size colour photograph (3.5 cm x 4.5 cm with clear frontal view)',
                         "Scanned copy of applicant's signature or thumb impression",
                         'Existing medical diagnosis reports, hospital treatment summaries, or clinical surgery '
                         'records (if available)'],
  'procedure_steps': ['Visit the official Swavlamban Portal (swavlambancard.gov.in) maintained by the Department of '
                      'Empowerment of Persons with Disabilities (DEPwD).',
                      "Click on 'Apply for Disability Certificate & UDID Card'.",
                      'Fill in personal details, educational qualifications, employment status, and details of '
                      'disability (e.g. Locomotor, Visual, Hearing, Intellectual, Multiple).',
                      'Upload Aadhaar card, photograph, signature/thumbprint, and previous medical documents.',
                      'Submit the application and note your unique UDID Enrolment Number.',
                      'The portal automatically assigns your case to the District Civil Hospital / Medical Board.',
                      'Visit the designated District Hospital on the scheduled medical board date for clinical '
                      'assessment by specialist doctors.',
                      'The Medical Board determines the percentage of disability (minimum 40% benchmark disability '
                      'required for reservation and welfare concessions) and enters assessment into the portal.',
                      'Download your digital e-Disability Certificate and e-UDID Card from swavlambancard.gov.in; a '
                      'tamper-proof plastic laminated smart card with QR code is delivered via India Post Speed Post.'],
  'where_how_to_apply': 'Online at Swavlamban Portal (swavlambancard.gov.in) and medical assessment at designated '
                        'District Civil Hospital / District Disability Medical Board.',
  'precautions': ['Benchmark disability benefits (reservations, pensions, concessions) require a certified disability '
                  'of 40% or higher.',
                  "UDID smart cards are issued with 'Permanent' validity for irreversible conditions, and 'Temporary' "
                  'validity (requiring re-assessment) for progressive conditions.',
                  'UDID card is universally recognized across all states and ministries in India without requiring '
                  'separate local state certificates.'],
  'official_link': 'https://www.swavlambancard.gov.in',
  'verified': True},
 {'id': 'guide_senior_citizen_card',
  'document_id': 'senior_citizen_card',
  'what_it_is': 'A Senior Citizen Identity Card / Certificate is an official document issued by the Social Welfare '
                'Department certifying that an individual is 60 years of age or older. It provides priority services '
                'at government hospitals, concessions on state transport buses, discounts on municipal utility '
                'charges, and eligibility for old age pension schemes.',
  'documents_required': ['Proof of Age (Aadhaar Card, Birth Certificate, PAN Card, or Passport confirming 60+ years)',
                         'Proof of Residence (Ration Card, Electricity Bill, or Voter ID)',
                         'Two recent passport-size colour photographs',
                         'Certified blood group report from a registered pathological laboratory'],
  'procedure_steps': ['Log in to the State Citizen Portal (e.g. Aaple Sarkar in Maharashtra under Social Justice & '
                      'Special Assistance) or visit your local Tahsil / District Social Welfare Office.',
                      'Fill the Senior Citizen Certificate / Card application form with name, date of birth, emergency '
                      'contact, and blood group.',
                      'Upload Aadhaar card, residence proof, passport photograph, and blood group report.',
                      'Submit the application and receive the acknowledgment slip.',
                      'Social Welfare officer verifies age and address proofs against database.',
                      'Download the digitally signed certificate or collect the laminated photo identity card from the '
                      'Tahsil / Social Welfare Department counter.'],
  'where_how_to_apply': 'State Citizen Services Portal (Aaple Sarkar, eDistrict), District Social Welfare Officer, or '
                        'local Tahsildar Office.',
  'precautions': ['Applicant must be at least 60 complete years of age on the date of application.',
                  'Ensure emergency contact person and blood group are correctly stated for medical safety.',
                  'Laminated card is accepted for interstate bus travel concessions and hospital priority counters.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_police_clearance_certificate',
  'document_id': 'police_clearance_certificate',
  'what_it_is': 'A Police Clearance Certificate (PCC) / Character Verification Certificate is an official document '
                'issued by the police authorities certifying that an individual has no criminal background, pending '
                'FIRs, or legal convictions. It is required for government appointments, armed forces recruitment, '
                'school van drivers, security clearances, and foreign immigration/work visas.',
  'documents_required': ['Aadhaar Card of the applicant',
                         'Proof of Current Address (Electricity Bill, Registered Rent Agreement, or Voter ID)',
                         'Recent passport-size colour photograph',
                         'Official letter / requisition from the employer, department, or foreign embassy mandating '
                         'the PCC'],
  'procedure_steps': ['For domestic employment/character certificate: Visit your State Police Citizen Portal (e.g. '
                      'Maharashtra Police pcs.mahaonline.gov.in or UP Police cctns.uppolice.gov.in).',
                      "For foreign visa/travel: Apply via the Passport Seva Portal (passportindia.gov.in) under 'Apply "
                      "for Police Clearance Certificate'.",
                      'Register an account, select the issuing Police Commissionerate / District Superintendent of '
                      'Police, and choose purpose of verification.',
                      'Enter personal details, employment details, and exact addresses where you have resided over the '
                      'past 12 months.',
                      'Upload Aadhaar card, residence proof, photo, and employer/embassy letter.',
                      'Pay the prescribed online verification fee (approx. Rs. 100 to Rs. 500 depending on purpose).',
                      'The application is transmitted to your local police station; an inquiry officer contacts you or '
                      'visits your residence to record statements and verify original proofs.',
                      'Following local station and Special Branch / Crime Branch record screening, the digitally '
                      'signed Police Clearance Certificate with QR code is generated.',
                      'Download the certificate PDF directly from the citizen portal dashboard.'],
  'where_how_to_apply': 'State Police Citizen Services Portal (pcs.mahaonline.gov.in, cctns.uppolice.gov.in) for '
                        'domestic verification; Passport Seva Portal (passportindia.gov.in) for overseas employment '
                        'and visas.',
  'precautions': ['Accurately declare all addresses resided at during the preceding 12 months to avoid police report '
                  'rejection.',
                  'Carry original identity and address proofs when reporting to the local police station for physical '
                  'verification.',
                  'Domestic PCCs generally carry a validity of 6 months from the date of issue.'],
  'official_link': 'https://pcs.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_ration_card',
  'document_id': 'ration_card',
  'what_it_is': 'A Ration Card is an official legal entitlement and household document issued by the State Food, Civil '
                'Supplies and Consumer Protection Department under the National Food Security Act (NFSA). It provides '
                'subsidized food grains (rice, wheat, coarse grains) and kerosene through the Public Distribution '
                'System (PDS) and serves as universal proof of family composition and residential address.',
  'documents_required': ['Aadhaar Cards of all family members to be listed on the card',
                         'Proof of Residential Address (Electricity Bill, Registered Rent Agreement, or Property Tax '
                         'Receipt)',
                         'Income Certificate or Salary Slip / Employer Certificate of family head',
                         'Surrender Certificate / Deletion Certificate from previous ration card (if names were '
                         'previously included elsewhere)',
                         'Passport-size group family photograph or photo of female head of household',
                         'Bank passbook of female head of household'],
  'procedure_steps': ['Visit the State Food, Civil Supplies Portal (e.g. rcms.mahafood.gov.in or Aaple Sarkar in '
                      'Maharashtra) or collect Form 1 from the Tahsil Food Distribution Office.',
                      'Designate the eldest adult female member of the family (aged 18+) as the Head of Household as '
                      'mandated under NFSA.',
                      'Enter demographic details of all family members: Names, Aadhaar numbers, relationships, dates '
                      'of birth, and occupations.',
                      'Upload Aadhaar cards of all members, residential proof, income certificate, and surrender '
                      'certificate from previous ration card (if migrating/transferring).',
                      'Pay the nominal application fee (Rs. 20 to Rs. 50) and collect the system-generated RCMS '
                      'acknowledgement receipt.',
                      'The Food & Civil Supplies Inspector conducts local field inquiry to verify family cooking setup '
                      'and residence.',
                      'Upon approval by the District Supply Officer (DSO) or Tehsildar, a unique 12-digit Ration Card '
                      'Number is generated.',
                      'Download the Digital Ration Card (e-Ration Card) from the RCMS portal or collect the printed '
                      'booklet from the Tahsil supply office.'],
  'where_how_to_apply': 'Online via State Food & Civil Supplies RCMS Portal (rcms.mahafood.gov.in, Aaple Sarkar) or '
                        'offline at the District Supply Office / Tahsil Food Grain Distribution Counter.',
  'precautions': ['Aadhaar seeding is legally mandatory for all family members on the ration card to enable '
                  'biometrically authenticated grain distribution.',
                  "Ensure a member's name is legally deleted from their parents' ration card before adding it to a new "
                  'card post-marriage.',
                  'Under NFSA, cards are categorized into Antyodaya (AAY), Priority Household (PHH/BPL), and '
                  'Non-Priority (APL/White) based on income limits.'],
  'official_link': 'https://rcms.mahafood.gov.in',
  'verified': True},
 {'id': 'guide_electricity_bill',
  'document_id': 'electricity_bill',
  'what_it_is': 'An Electricity Bill is an official monthly utility invoice issued by the state power distribution '
                'company (Discom) indicating consumer number, meter serial number, billing address, and consumption '
                'units. Because meters are physically connected to residential premises, electricity bills (issued '
                'within the last 3 months) are universally accepted across all government and commercial authorities '
                'as premier proof of address.',
  'documents_required': ['For downloading existing bill: 12-digit Consumer Number (printed on existing bill/meter) and '
                         'Billing Unit',
                         'For applying for new connection: Proof of Property Ownership (Sale Deed, Index II, Property '
                         'Tax Receipt) or Tenant NOC with Registered Rent Agreement, plus Aadhaar Card'],
  'procedure_steps': ['To download your latest official paid electricity bill: Visit your power discom consumer web '
                      'portal (e.g. mahadiscom.in for MSEDCL / Mahavitaran in Maharashtra, bsesdelhi.com for BSES in '
                      'Delhi, or tatapower.com).',
                      "Click on 'View / Pay Bill' and enter your 12-digit Consumer Number and Billing Unit.",
                      "Click 'View Bill' to download the official full monthly electricity bill in PDF format bearing "
                      'QR code, barcode, payment transaction details, and complete premises address.',
                      "To apply for a new electricity connection: Navigate to 'New Connection Registration' on the "
                      'Discom portal (Form A-1).',
                      'Select consumer category (LT-Residential) and enter required load in KW.',
                      'Upload property ownership document (Index II/Tax receipt) or tenant consent letter with '
                      "registered rent agreement, and applicant's Aadhaar.",
                      'Pay the new service connection application fee and security deposit online.',
                      'Discom field junior engineer inspects wiring installation and installs electronic meter; first '
                      'regular monthly bill serves as permanent proof of residence.'],
  'where_how_to_apply': 'State Discom Consumer Portals (mahadiscom.in, bsesdelhi.com, tatapower.com, etc.), discom '
                        'mobile applications, or local Discom Sub-Divisional Office / Customer Care Centre.',
  'precautions': ['For address proof purposes, government authorities and banks require an electricity bill not older '
                  'than 3 months.',
                  "Ensure the bill displays payment status as 'Paid' or attach the corresponding online payment "
                  'transaction receipt.',
                  'If living in rented premises, ensure the address on the electricity bill matches the property '
                  'description in your registered rent agreement.'],
  'official_link': 'https://www.mahadiscom.in',
  'verified': True},
 {'id': 'guide_rent_agreement',
  'document_id': 'rent_agreement',
  'what_it_is': 'A Registered Rent Agreement (Leave and License Agreement) is a legally binding contract executed '
                'under the Indian Registration Act, 1908 and state Rent Control acts between a property owner '
                '(licensor) and tenant (licensee). Recorded electronically with biometric authentication, it '
                'establishes legal tenancy rights, monthly rent obligations, security deposit terms, and serves as '
                'statutory address proof for tenants for passports, bank accounts, and driving licences.',
  'documents_required': ['Aadhaar Card and PAN Card of Property Owner (Licensor)',
                         'Aadhaar Card and PAN Card of Tenant (Licensee)',
                         'Aadhaar Cards of two independent adult witnesses',
                         'Latest paid Electricity Bill and Property Tax receipt of the rented premises to verify '
                         'property description'],
  'procedure_steps': ['Draft the Leave and License Agreement specifying the license term (standard 11 to 36 months), '
                      'monthly license fee, refundable deposit amount, lock-in period, and exact premises address.',
                      'Utilize the Department of Registration and Stamps e-Registration portal (e.g. '
                      'igrmaharashtra.gov.in in Maharashtra) or book an appointment with an authorized e-Registration '
                      'service provider (ASP).',
                      'Calculate non-judicial stamp duty and government registration fee (in Maharashtra: Rs. 1,000 '
                      'registration fee for municipal corporation areas plus stamp duty calculated on total rent & '
                      'deposit).',
                      'Pay stamp duty and registration fees online through the Government Receipt Accounting System '
                      '(GRAS / e-Challan).',
                      'Complete digital biometric verification: Owner (licensor), tenant (licensee), and 2 witnesses '
                      'scan their thumbprints and capture live webcam photos using UIDAI-compliant biometric devices.',
                      'Submit the electronic dossier directly to the Joint Sub-Registrar Office for electronic '
                      'scrutiny.',
                      'The Sub-Registrar officer reviews the document and approves it within 24 to 48 hours.',
                      'Download the legally registered Leave & License Agreement PDF bearing the official digital '
                      'signature, Registration Number, and government QR barcode.'],
  'where_how_to_apply': 'Department of Registration and Stamps Portal (igrmaharashtra.gov.in) via authorized '
                        'e-Registration service providers or directly at the local Sub-Registrar Office.',
  'precautions': ['Notarised rent agreements on plain stamp paper without registration are NOT legally valid address '
                  'proofs for passports or bank accounts in many jurisdictions.',
                  'All parties (owner, tenant, and both witnesses) must have active Aadhaar cards linked with mobile '
                  'numbers for biometric authentication.',
                  'Ensure the agreement specifies the full flat/house number, building name, street, taluka, and pin '
                  'code matching utility bills.'],
  'official_link': 'https://igrmaharashtra.gov.in',
  'verified': True},
 {'id': 'guide_bank_passbook',
  'document_id': 'bank_passbook',
  'what_it_is': 'A Bank Passbook or Bank Account Statement is an official record issued by a scheduled commercial bank '
                'or post office displaying account number, IFSC code, account holder photograph, and residential '
                'address. Seeding it with Aadhaar on the NPCI mapper enables Direct Benefit Transfer (DBT) of '
                'scholarships, agricultural subsidies, pensions, and welfare scheme funds.',
  'documents_required': ['Aadhaar Card (serves as primary KYC document for biometric / OTP authentication)',
                         'PAN Card (or Form 60 if PAN is not held)',
                         'Proof of Residence (if different from Aadhaar address: electricity bill, voter ID, rent '
                         'agreement)',
                         'Two recent passport-size colour photographs'],
  'procedure_steps': ['Select a nationalized, public sector, or scheduled commercial bank (e.g. State Bank of India, '
                      'Bank of Baroda, Bank of India, PNB) or India Post Payments Bank (IPPB).',
                      "Visit the bank branch in person or open an account digitally using the bank's mobile "
                      'application (e.g. SBI YONO, BoB World) via Video KYC.',
                      'Fill the Account Opening Form for a Regular Savings Bank Account or Basic Savings Bank Deposit '
                      'Account (Jan Dhan).',
                      'Submit self-attested copies of Aadhaar Card and PAN Card along with passport-size photographs.',
                      'Complete in-person biometric authentication at the branch or complete live Video KYC.',
                      'Deposit the nominal minimum balance (or Rs. 0 for Jan Dhan accounts).',
                      "Crucial step for government scholarships/schemes: Submit the 'Aadhaar Seeding / NPCI Mapping "
                      "Mandate Form' requesting the branch manager to seed your account with the National Payments "
                      'Corporation of India (NPCI) mapper for DBT transfers.',
                      "Collect your physical Bank Passbook with branch manager's stamp and signature over your "
                      'photograph, along with Debit Card and Cheque Book.'],
  'where_how_to_apply': 'Any branch of a Nationalized Bank, Scheduled Commercial Bank, Regional Rural Bank (RRB), or '
                        'India Post Payments Bank (IPPB).',
  'precautions': ["Ensure the branch officer explicitly enables the 'NPCI Aadhaar Mapping' flag; merely linking "
                  'Aadhaar for KYC does not guarantee DBT enablement.',
                  'The name spelling on your bank account must match your Aadhaar Card and Caste / Income certificates '
                  'letter for letter to avoid DBT rejection.',
                  'Keep the passbook updated with regular transaction prints to serve as valid recent financial '
                  'proof.'],
  'official_link': 'https://www.rbi.org.in',
  'verified': True},
 {'id': 'guide_school_leaving_certificate',
  'document_id': 'school_leaving_certificate',
  'what_it_is': 'A School Leaving Certificate (SLC) or Transfer Certificate (TC) is the formal scholastic record '
                'issued by the school or junior college last attended. Governed by the Secondary School Code, it '
                "documents the student's full name, date of birth in words and figures, parentage, recognized caste "
                'entry, and date of leaving. In reservation and validity procedures, it serves as the earliest '
                'recorded evidence of caste and age.',
  'documents_required': ['Original fee clearance / No-Dues certificate from school library, laboratory, and fee '
                         'counter',
                         "Student's Aadhaar Card",
                         'Application letter addressed to the Principal requesting issuance of SLC/TC'],
  'procedure_steps': ['Obtain the prescribed SLC / TC requisition form from the school administrative office or write '
                      'a formal application addressed to the Principal / Headmaster.',
                      'State your full student name, roll number, admission/General Register (GR) number, and last '
                      'academic year attended.',
                      'Clear all outstanding school tuition fees, return borrowed library books, and collect '
                      'signatures on the No-Dues slip.',
                      'Submit the application along with the No-Dues slip at the administrative counter.',
                      'Pay the nominal certificate fee (typically Rs. 20 to Rs. 100) if prescribed.',
                      'The school clerk extracts details from the General Register (GR) and drafts the School Leaving '
                      'Certificate.',
                      'The Principal / Headmaster verifies entries against the original admission ledger, signs the '
                      'document, and affixes the official institutional seal.',
                      'Collect the original signed SLC and obtain multiple certified true copies counter-signed by the '
                      'Principal.'],
  'where_how_to_apply': 'Administrative office of the school or junior college last attended. For closed schools, '
                        'approach the District Education Officer (Zilla Parishad).',
  'precautions': ["Carefully examine the 'Caste' and 'Sub-Caste' column before leaving the school office to verify it "
                  'matches your caste certificate exactly without abbreviations.',
                  'Verify that the Date of Birth in figures matches the date written in words.',
                  'Never laminate the original School Leaving Certificate if subsequent educational institutions '
                  'require physical endorsements on the reverse.'],
  'official_link': 'https://education.maharashtra.gov.in',
  'verified': True},
 {'id': 'guide_relative_validity_record',
  'document_id': 'relative_validity_record',
  'what_it_is': "A Relative's Caste Validity Record is a certified copy of a Caste Validity Certificate held by a "
                'blood relative from the paternal lineage (father, real brother, sister, paternal uncle, or paternal '
                "grandfather). Under the law laid down by the Supreme Court in Madhuri Patil's case and Maharashtra "
                "Act XXIII of 2001, a paternal blood relative's validity certificate serves as prime conclusive "
                "evidence to substantiate an applicant's validity claim.",
  'documents_required': ["Original or certified copy of the blood relative's Caste Validity Certificate",
                         'Genealogical Family Tree (Vanshavali) showing exact relationship to the relative from common '
                         'paternal ancestor',
                         "Relationship Proof: Relative's school LC showing father's name matching applicant's "
                         "grandfather's name",
                         'Affidavit on Rs. 100 stamp paper swearing paternal blood relationship and affirming no '
                         'cancellation orders exist'],
  'procedure_steps': ["Obtain a clear copy of the qualifying paternal blood relative's Caste Validity Certificate.",
                      'Apply to the Divisional Caste Scrutiny Committee that issued the original order for an official '
                      'Certified True Copy (Duplicate Extract) if the original is held in another department.',
                      'Draft a detailed genealogical tree (Vanshavali) on Rs. 100 stamp paper tracing lineage from the '
                      'paternal grandfather/great-grandfather down to both the relative and the applicant.',
                      'Gather corroborative relationship proofs (such as school leaving certificates showing matching '
                      'father/grandfather names).',
                      'Swear an affidavit before a Notary Public affirming that the relative is a blood relation and '
                      'that their validity order has not been challenged or quashed by any court.',
                      'Attach the certified validity copy and relationship proofs to your Caste Validity application '
                      'on the CCVIS portal.'],
  'where_how_to_apply': 'Office of the Divisional Caste Certificate Scrutiny Committee that issued the original '
                        "relative's validity order.",
  'precautions': ['Only PATERNAL blood relatives qualify. Relatives from the maternal side (mother, maternal uncle, '
                  'maternal grandfather) or in-laws are legally inadmissible.',
                  'Ensure the relationship chain is unbroken and supported by matching names in school general '
                  'registers.',
                  "The relative's validity certificate must be clear, legible, and show the committee order number and "
                  'date.'],
  'official_link': 'https://bartievalidity.maharashtra.gov.in',
  'verified': True},
 {'id': 'guide_admission_letter',
  'document_id': 'admission_letter',
  'what_it_is': 'An Admission Letter (or Centralized Admission Process CAP Allotment Letter / Offer Letter) is the '
                'formal document issued by a competent university or state admission authority confirming that a '
                'student has been merit-allotted and enrolled in a specific degree, diploma, or certificate course.',
  'documents_required': ['Entrance exam scorecard / merit rank card (e.g. MHT-CET, NEET, JEE Main)',
                         'CAP Round choice code submission confirmation',
                         'Fee payment receipt for seat acceptance'],
  'procedure_steps': ['Participate in the Centralized Admission Process (CAP) rounds conducted by the State Common '
                      'Entrance Test Cell (CET Cell) or University.',
                      'Submit and lock your college preference option form online.',
                      'When seat allotment results are published, log in to the admission portal using your candidate '
                      'credentials.',
                      'Verify the allotted institution, course, and category quota.',
                      'Accept the seat by paying the seat acceptance fee online via payment gateway.',
                      'Download and print the official Provisional Seat Allotment Letter bearing barcode and authority '
                      'stamp.',
                      'Report to the allotted college / Scrutiny Center with original documents within the reporting '
                      'window.',
                      'Collect the final college admission confirmation letter and fee receipt signed by the Principal '
                      '/ Registrar.'],
  'where_how_to_apply': 'State CET Cell Admission Portal (cetcell.mahacet.org) or the administrative office of the '
                        'allotted university/college.',
  'precautions': ['Ensure the letter mentions the correct reservation category under which the seat is allotted (e.g., '
                  'General, OBC, SC, ST, EWS).',
                  'Keep digital PDF copies backed up, as original allotment letters must be submitted for scholarship '
                  'applications.',
                  'Check reporting deadlines carefully — missing the reporting window results in forfeiture of the '
                  'allotted seat.'],
  'official_link': 'https://cetcell.mahacet.org',
  'verified': True},
 {'id': 'guide_gap_certificate',
  'document_id': 'gap_certificate',
  'what_it_is': 'An Educational Gap Certificate is a sworn legal affidavit on non-judicial stamp paper stating the '
                'reason for an interruption or break in academic studies between two educational courses. It affirms '
                'that during the gap period, the student was preparing for entrance exams, recuperating from illness, '
                'or facing financial hardship, and did not engage in unlawful activities or enroll in another degree.',
  'documents_required': ['Aadhaar Card of the student',
                         'Last attended school / college Leaving Certificate (SLC) and passing marksheets showing year '
                         'of completion',
                         'Medical certificate or entrance exam coaching receipt / admit cards (if citing medical '
                         'reasons or entrance preparation)'],
  'procedure_steps': ['Purchase a non-judicial stamp paper of prescribed denomination (standard Rs. 100 stamp paper in '
                      'Maharashtra) from a licensed vendor or generate e-Stamp via GRAS / StockHolding.',
                      'Draft the gap affidavit text including: Student full name, permanent residential address, '
                      'details of last course completed and passing year, exact gap duration (e.g., July 2024 to June '
                      '2026), and genuine reason for the gap (e.g., preparation for NEET/JEE entrance examinations).',
                      'Include statutory clause swearing that during this gap period the applicant was not involved in '
                      'any criminal activity and was not admitted to any other educational institution.',
                      'Print the drafted text onto the non-judicial stamp paper.',
                      'Carry the printed stamp paper and original Aadhaar card to a Notary Public advocate or '
                      'Executive Magistrate.',
                      'Sign the affidavit in the physical presence of the Notary Public.',
                      'The Notary verifies identity, enters the matter into the Notarial Register, affixes notarial '
                      'adhesive stamps, and applies their official seal and signature.'],
  'where_how_to_apply': 'Licensed stamp vendors and any registered Notary Public advocate office located near '
                        'civil/district courts, or Tehsil Executive Magistrate.',
  'precautions': ['Ensure the starting and ending months and years of the gap match the completion date on your '
                  'previous marksheet and current admission year.',
                  'Do not sign the affidavit beforehand — your signature or thumb impression must be appended in the '
                  'presence of the Notary.',
                  'Colleges require the original stamped affidavit; make photocopies for your personal record before '
                  'submission.'],
  'official_link': 'https://gras.mahakosh.gov.in',
  'verified': True},
 {'id': 'guide_land_7_12_extract',
  'document_id': 'land_7_12_extract',
  'what_it_is': 'A 7/12 Extract (Saat Baara Utara) is an essential land revenue record maintained under the '
                'Maharashtra Land Revenue Code, combining Village Form VII (land ownership, occupant rights, survey '
                'number, and area) and Village Form XII (cultivator details, crops grown, and liabilities/loans). It '
                'is required for agricultural schemes, farmer certificates, Kisan Credit Cards, crop insurance, and '
                'property transactions.',
  'documents_required': ['Survey Number / Gat Number / ULPIN of the agricultural land',
                         'Name of District, Taluka, and Village where land is situated',
                         'Name of the land titleholder (as recorded in revenue records)'],
  'procedure_steps': ['Visit the official Mahabhumi Digital Satbara Portal (digitalsatbara.mahabhumi.gov.in) or '
                      'Mahabhumi Bhulekh (bhulekh.mahabhumi.gov.in).',
                      'Register an account with your mobile number and log in.',
                      'Select your District, Taluka, and Village from the dropdown menus.',
                      'Search for your land parcel by Survey Number / Gat Number, ULPIN (Unique Land Parcel '
                      'Identification Number), or Owner Name.',
                      "Select 'Digitally Signed 7/12' or 'Digitally Signed 8A' (Form 8A lists total land holdings of "
                      'an owner).',
                      'Pay the nominal statutory fee of Rs. 15 per document via UPI, Netbanking, or Debit Card.',
                      'Download the digitally signed 7/12 PDF featuring the official 16-digit ULPIN, cryptographic '
                      'digital signature, and verification QR code.',
                      'For offline collection: Visit the local Village Talati / Sajja office and obtain a physically '
                      'stamped copy from the Talati register.'],
  'where_how_to_apply': 'Online at Mahabhumi Digital Satbara Portal (digitalsatbara.mahabhumi.gov.in) or offline at '
                        'the local Village Talati / Revenue Circle Office.',
  'precautions': ["Only the 'Digitally Signed 7/12' downloaded from digitalsatbara.mahabhumi.gov.in with QR code is "
                  'legally valid in courts, banks, and government offices without manual Talati signature.',
                  'The free viewing extract on bhulekh.mahabhumi.gov.in is for informational purposes only and cannot '
                  'be submitted as legal evidence.',
                  "Check the 'Other Rights' (Itar Hakka) column for any bank mortgages, crop loans, or court "
                  'injunctions recorded against the property.'],
  'official_link': 'https://digitalsatbara.mahabhumi.gov.in',
  'verified': True},
 {'id': 'guide_photograph',
  'document_id': 'photograph',
  'what_it_is': 'A Passport-Size Photograph is a standardized colour photograph (typically 3.5 cm x 4.5 cm) showing '
                "the applicant's frontal facial view with neutral expression on a plain white or light off-white "
                'background. Compliant with international ICAO standards, it is required on all government application '
                'forms, smart cards, and certificates.',
  'documents_required': ["Applicant's physical presence at photo studio or digital camera upload"],
  'procedure_steps': ['Visit a registered professional photo studio or use a high-resolution smartphone camera against '
                      'a plain white wall with uniform lighting.',
                      'Ensure frontal face view with both ears visible, eyes open, neutral facial expression, and no '
                      'head coverings (unless for religious reasons).',
                      'Photographs should be recent (taken within the preceding 6 months).',
                      'Request printed passport-size photographs (standard 3.5 cm x 4.5 cm format) on glossy or matte '
                      'photo paper.',
                      'Obtain a digital soft copy (JPEG format, 20 KB to 100 KB, 300 DPI) for online portal uploads.'],
  'where_how_to_apply': 'Any registered commercial photo studio, authorized CSC center, or self-capture using mobile '
                        'photo passport formatting apps.',
  'precautions': ['Do not wear tinted glasses, sunglasses, or uniforms; clear prescription spectacles without glare '
                  'reflection are permissible.',
                  'Ensure the background is clean white or light grey without shadows or patterns.',
                  'Keep multiple prints and a digital copy saved on your phone for online portal submissions.'],
  'official_link': 'https://uidai.gov.in',
  'verified': True},
 {'id': 'guide_affidavit_stamp_paper',
  'document_id': 'affidavit_stamp_paper',
  'what_it_is': 'An Affidavit on Non-Judicial Stamp Paper is a formal written statement of facts voluntarily made by '
                'an affiant under oath or affirmation, attested by an authorized Notary Public or Executive '
                'Magistrate. Regulated by the Indian Stamp Act and State Stamp Rules, the denomination of stamp paper '
                '(e.g. Rs. 100, Rs. 200, Rs. 500) varies based on state schedules and the specific legal purpose.',
  'documents_required': ['Aadhaar Card of the deponent / applicant',
                         'Draft of the affidavit text matching the prescribed legal format of the receiving department',
                         'Supporting documents substantiating the statements made in the affidavit'],
  'procedure_steps': ['Obtain the prescribed affidavit format from the relevant government department or portal '
                      'guidelines.',
                      'Purchase a non-judicial stamp paper of the prescribed denomination from a licensed stamp vendor '
                      'or generate an e-Stamp through the state stamp portal (GRAS / StockHolding).',
                      'Get the affidavit text typed on the stamp paper by a registered typist or computer document '
                      'writer.',
                      'Take the printed stamp paper and original Aadhaar card to an authorized Notary Public advocate '
                      'or Executive Magistrate.',
                      'Read the affidavit carefully and sign or affix thumbprint in the physical presence of the '
                      'Notary.',
                      'The Notary records the transaction in their Notarial Register, verifies identity, affixes '
                      'notarial adhesive stamps, and applies their official seal and signature.',
                      'Make photocopies of the notarised affidavit before submitting the original.'],
  'where_how_to_apply': 'Licensed stamp vendors (court premises/Tehsil) and Notary Public advocates / Executive '
                        'Magistrates.',
  'precautions': ['Verify the exact stamp paper denomination required by the receiving authority before purchase.',
                  'Do not sign the affidavit in advance — signing must take place in the physical presence of the '
                  'Notary Public.',
                  'Ensure names, dates, and addresses match your identity proof exactly.'],
  'official_link': 'https://gras.mahakosh.gov.in',
  'verified': True},
 {'id': 'guide_residence_proof',
  'document_id': 'residence_proof',
  'what_it_is': 'Residence Proof refers to any legally valid government-recognized document establishing an '
                "individual's current physical address. Across public services, a range of documents are accepted as "
                'address proof, including recent utility bills (electricity, water, piped gas), Aadhaar Card, Ration '
                'Card, Bank Passbook, or a registered Rent Agreement.',
  'documents_required': ['Aadhaar Card (if address is up to date)',
                         'Or any one of: Electricity Bill (last 3 months), Water Bill, Bank Passbook first page, '
                         'Ration Card, or Registered Rent Agreement'],
  'procedure_steps': ['Check whether your current residential address is accurately reflected on your Aadhaar Card. If '
                      'yes, Aadhaar itself serves as complete address proof for almost all services.',
                      'If your Aadhaar address is outdated, use a recent electricity bill, piped gas bill, or water '
                      "bill in your or your parent's name.",
                      'If residing in rented accommodation, produce a registered Leave and License agreement along '
                      "with the landlord's electricity bill.",
                      'If no utility bill exists in your name, obtain a Residence / Domicile Certificate from your '
                      'local Tehsil Revenue Office by submitting an application and self-declaration.'],
  'where_how_to_apply': 'Existing documents in your possession (utility bills, Aadhaar, ration card) or apply for a '
                        'Residence Certificate at the Tehsil / Municipal Ward Office.',
  'precautions': ['Utility bills must not be older than 3 months from the date of submission.',
                  'Ensure your name and address are legible and complete with house number, locality, and pin code.',
                  'Unregistered informal rent receipts on plain paper are usually rejected by government authorities.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_self_declaration_form',
  'document_id': 'self_declaration_form',
  'what_it_is': 'A Self-Declaration Form is a statutory document prescribed under the Right to Public Services Act '
                'replacing unnecessary notarised affidavits for routine citizen services. The applicant affirms the '
                'truth of personal details under their own signature, carrying full legal liability under the Indian '
                'Penal Code if found false.',
  'documents_required': ['Aadhaar Card (for identity details and reference while completing the declaration)'],
  'procedure_steps': ['Download the prescribed Self-Declaration Form from the state citizen portal (e.g. Aaple Sarkar '
                      'in Maharashtra) or collect it from the department counter.',
                      "Fill in all fields legibly: Full Name, Father's/Spouse's Name, Age, Occupation, and Residential "
                      'Address.',
                      'Carefully review the declaration statements regarding caste, income, or residence.',
                      'Paste a recent passport-size photograph in the designated box.',
                      'Sign and date the form with the place of declaration.',
                      'Attach the signed self-declaration form to your main service application.'],
  'where_how_to_apply': 'Downloadable from state citizen portals (aaplesarkar.mahaonline.gov.in, '
                        'edistrict.delhigovt.nic.in) or collected at the issuing department counter.',
  'precautions': ['Use only the official prescribed format issued by the specific department.',
                  'Making a false self-declaration is a criminal offence punishable under Section 199 and 200 of the '
                  'Indian Penal Code.',
                  'Sign the form yourself — proxy signatures by family members or agents are invalid.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_pre_1950_caste_proof',
  'document_id': 'pre_1950_caste_proof',
  'what_it_is': 'Pre-1950 / Pre-1967 Ancestral Caste Proof consists of historical documentary evidence proving that '
                "the applicant's paternal forefather resided in the state and belonged to the declared caste before "
                'the statutory cutoff dates specified in reservation acts (10 August 1950 for SC, 6 September 1950 for '
                'ST, and 13 October 1967 for OBC/VJNT in Maharashtra).',
  'documents_required': ["Applicant's and Father's Aadhaar Cards",
                         'Genealogical Family Tree connecting applicant to the ancestor',
                         "Father's, Grandfather's, or Great-Grandfather's primary school leaving certificate, "
                         'birth/death extract, or land revenue record prior to cutoff date'],
  'procedure_steps': ['Identify the primary school attended by your father, grandfather, or great-grandfather prior to '
                      'the cutoff date (1950/1967).',
                      'Apply in writing to the Headmaster of the primary school or Zilla Parishad Education Officer '
                      'requesting an attested extract of the General Register (GR / Dakhil Kharij Register).',
                      'Alternatively, visit the Municipal / Tehsil Record Room (Abhilekhagar) to search historical '
                      'Birth & Death Register extracts prior to 1950/1967 (Kotwal Book extract / Birth Register).',
                      "Inspect the entry to confirm the 'Caste' column mentions the recognized community name matching "
                      'constitutional orders without ambiguity.',
                      'Obtain a certified duplicate copy signed and officially sealed by the competent authority '
                      '(Headmaster, Tehsildar, or Municipal Health Officer).',
                      'Submit the certified copy along with your genealogical family tree affidavit.'],
  'where_how_to_apply': 'Primary school archives, Zilla Parishad Education Office, District Collectorate Record Room, '
                        'or Tehsil Archives.',
  'precautions': ['Ensure the caste entry has no alterations, fluid corrections, or overwritten ink.',
                  'Records must pertain strictly to paternal ancestors (father, grandfather, great-grandfather).',
                  'If school is defunct, approach the Block Education Officer (BEO) who holds archived records.'],
  'official_link': 'https://bartievalidity.maharashtra.gov.in',
  'verified': True},
 {'id': 'guide_pedhinama',
  'document_id': 'pedhinama',
  'what_it_is': 'A Pedhinama is a certified family genealogy chart establishing direct ancestral lineage from the '
                'forefather down to the applicant, certified by the Talati cum Mantri or Executive Magistrate in '
                'Gujarat and western states for caste verification and agricultural land succession.',
  'documents_required': ['Aadhaar Cards of all living family members',
                         'Death certificates of deceased ancestors in the pedigree tree',
                         'Affidavit on stamp paper stating full genealogical pedigree',
                         'Panchkyas: Statements of two respected village elders / Panchas recorded before the Talati'],
  'procedure_steps': ['Draw the complete genealogical tree starting from the ancestral patriarch down to all living '
                      'legal heirs.',
                      'Draft a sworn affidavit on Rs. 100/300 stamp paper stating the pedigree tree.',
                      'Appear before the Talati cum Mantri along with two local village elders (Panchas).',
                      'Talati verifies entries against village revenue records (Form 7/12, 8A, or Hakka Patrak).',
                      'Talati prepares the Rojkam and signs the Pedhinama.',
                      'Counter-signed and endorsed by the Mamlatdar / Executive Magistrate.'],
  'where_how_to_apply': 'Office of the Talati cum Mantri (e-Gram Panchayat) or Mamlatdar Office, Gujarat.',
  'precautions': ['Include all legal heirs including married daughters where required by state revenue code.',
                  'Do not omit any deceased ancestor in the direct line.'],
  'official_link': 'https://digitalgujarat.gov.in',
  'verified': True},
 {'id': 'guide_parivar_register_nakal',
  'document_id': 'parivar_register_nakal',
  'what_it_is': 'Parivar Register Nakal (Family Register Extract) is a certified copy of the family record maintained '
                'by the Panchayati Raj or Urban Development authority in Uttar Pradesh and northern states, recording '
                'household composition, relationships, and caste.',
  'documents_required': ['Aadhaar Card of head of household',
                         'Application form specifying Gram Panchayat / Ward name',
                         'Ration Card or previous family register reference'],
  'procedure_steps': ['Visit the Gram Panchayat Secretary (Gram Vikas Adhikari) in rural areas, or the Executive '
                      'Officer of Nagar Palika / Nigam in urban areas.',
                      'Submit an application requesting a certified copy of the Parivar Register Nakal.',
                      'Alternatively, apply online through the eSathi Uttar Pradesh portal (esathi.up.gov.in).',
                      'Secretary verifies entries in the Kutumb Register and prepares the certified extract with seal.',
                      'Pay the nominal fee (Rs. 5 to Rs. 20) and collect the stamped certified copy.'],
  'where_how_to_apply': 'Gram Panchayat Office (Village Secretary), Nagar Palika / Nigam office, or eSathi UP portal.',
  'precautions': ['Verify all family members are listed with correct ages and relationships.',
                  "Ensure the head of family's name matches your official identity records."],
  'official_link': 'https://edistrict.up.gov.in',
  'verified': True},
 {'id': 'guide_talati_verification_report',
  'document_id': 'talati_verification_report',
  'what_it_is': 'An official spot inquiry report and panchnama issued by the Village Revenue Officer (Talati / Patwari '
                '/ Lekhpal) documenting agricultural income, residential occupation, or family landholdings for '
                'revenue certificates.',
  'documents_required': ['Aadhaar Card of the applicant',
                         'Electricity bill or village house tax receipt',
                         'Self-declaration of annual family income'],
  'procedure_steps': ['Apply at the Tehsil office or online citizen portal for income/caste verification.',
                      'The application is automatically routed to the local Talati / Lekhpal of your circle.',
                      'Talati conducts a local inquiry with neighbors and examines revenue records.',
                      'Talati writes the Panchnama / spot inquiry report and records findings.',
                      'Report is uploaded to the portal or forwarded to the Tehsildar for final certificate issuance.'],
  'where_how_to_apply': 'Local Village Talati / Patwari Office or Village Panchayat / Tehsil office.',
  'precautions': ['Present genuine income documents (salary slips, agricultural J-Form, or returns).',
                  'Ensure phone number is active for the officer to contact you for the site visit.'],
  'official_link': 'https://aaplesarkar.mahaonline.gov.in',
  'verified': True},
 {'id': 'guide_nadakacheri_rd_number',
  'document_id': 'nadakacheri_rd_number',
  'what_it_is': 'A 15-digit unique RD acknowledgment number issued by the Karnataka Revenue Department when applying '
                'for caste, income, or residence certificates through Atalji Janasnehi Kendra (Nadakacheri).',
  'documents_required': ['Aadhaar Card', 'Ration Card', 'Mobile number linked with Aadhaar'],
  'procedure_steps': ['Visit the Nadakacheri portal (nadakacheri.karnataka.gov.in) or Seva Sindhu.',
                      'Click Online Application and select the revenue service.',
                      'Enter your details and upload supporting documents.',
                      'On submission, an acknowledgment slip containing a unique 15-digit RD barcode number (e.g., '
                      'RD0038...) is generated.',
                      'Note down or print this RD number for tracking and verification.'],
  'where_how_to_apply': 'nadakacheri.karnataka.gov.in or any Atalji Janasnehi Kendra (AJSK) counter across Karnataka.',
  'precautions': ['Keep the acknowledgment PDF saved safely with the barcode visible.',
                  'Check application status online using this RD number.'],
  'official_link': 'https://nadakacheri.karnataka.gov.in',
  'verified': True},
 {'id': 'guide_kutumba_sats_id',
  'document_id': 'kutumba_sats_id',
  'what_it_is': "Kutumba is Karnataka's Entitlement Management System assigning a single unified Family ID, while SATS "
                'is the Student Achievement Tracking System ID used for scholarship disbursement.',
  'documents_required': ['Aadhaar of student and family members', 'Ration Card', 'School enrollment number'],
  'procedure_steps': ['Check existing Kutumba ID at kutumba.karnataka.gov.in using your Ration Card or Aadhaar.',
                      'If not registered, update family details through the Grama One or Bangalore One center.',
                      'Obtain your 9-digit SATS Student ID from your school or college administrative office.',
                      'Both IDs automatically pre-populate your family income and caste data on the State Scholarship '
                      'Portal (SSP).'],
  'where_how_to_apply': 'kutumba.karnataka.gov.in, ssp.postmatric.karnataka.gov.in, or nearest Grama One center.',
  'precautions': ['Ensure Aadhaar name matches school enrollment records exactly.',
                  'Confirm your bank account is active and seeded with Aadhaar on NPCI mapper.'],
  'official_link': 'https://kutumba.karnataka.gov.in',
  'verified': True},
 {'id': 'guide_delhi_3yr_residence_proof',
  'document_id': 'delhi_3yr_residence_proof',
  'what_it_is': 'Proof demonstrating continuous physical residence within the National Capital Territory of Delhi for '
                'a consecutive period of at least 3 years, required for caste, income, and welfare services on '
                'e-District Delhi.',
  'documents_required': ['Aadhaar Card with Delhi address',
                         'Electricity or water bills for the last 3 consecutive years',
                         'Registered rent agreement or Voter ID'],
  'procedure_steps': ["Gather consecutive electricity or water bills in your or parent's name covering the last 3 "
                      'years.',
                      'If living in rented premises, gather registered rent agreements or landlord verification letter '
                      'with electricity meters.',
                      'Download previous 3 years utility bills from BSES/TPDDL consumer portal.',
                      'Compile into chronological order ready for e-District upload.'],
  'where_how_to_apply': 'BSES Rajdhani/Yamuna or Tata Power DDL portal, or respective discom customer care office.',
  'precautions': ['Ensure address spelling matches your Aadhaar and identity proof exactly.',
                  'Do not provide bills with gaps exceeding 6 months without explanation.'],
  'official_link': 'https://edistrict.delhigovt.nic.in',
  'verified': True}]

STATES_SEED = [{'id': 'AN',
  'name': 'Andaman & Nicobar Islands',
  'name_hi': 'अंडमान और निकोबार द्वीपसमूह',
  'name_mr': 'अंदमान आणि निकोबार बेटे'},
 {'id': 'AP', 'name': 'Andhra Pradesh', 'name_hi': 'आंध्र प्रदेश', 'name_mr': 'आंध्र प्रदेश'},
 {'id': 'AR', 'name': 'Arunachal Pradesh', 'name_hi': 'अरुणाचल प्रदेश', 'name_mr': 'अरुणाचल प्रदेश'},
 {'id': 'AS', 'name': 'Assam', 'name_hi': 'असम', 'name_mr': 'आसाम'},
 {'id': 'BR', 'name': 'Bihar', 'name_hi': 'बिहार', 'name_mr': 'बिहार'},
 {'id': 'CH', 'name': 'Chandigarh', 'name_hi': 'चंडीगढ़', 'name_mr': 'चंदीगड'},
 {'id': 'CG', 'name': 'Chhattisgarh', 'name_hi': 'छत्तीसगढ़', 'name_mr': 'छत्तीसगड'},
 {'id': 'DD',
  'name': 'Dadra & Nagar Haveli and Daman & Diu',
  'name_hi': 'दादरा और नगर हवेली और दमन और दीव',
  'name_mr': 'दादरा आणि नगर हवेली आणि दमण आणि दीव'},
 {'id': 'DL', 'name': 'Delhi', 'name_hi': 'दिल्ली', 'name_mr': 'दिल्ली'},
 {'id': 'GA', 'name': 'Goa', 'name_hi': 'गोवा', 'name_mr': 'गोवा'},
 {'id': 'GJ', 'name': 'Gujarat', 'name_hi': 'गुजरात', 'name_mr': 'गुजरात'},
 {'id': 'HR', 'name': 'Haryana', 'name_hi': 'हरियाणा', 'name_mr': 'हरियाणा'},
 {'id': 'HP', 'name': 'Himachal Pradesh', 'name_hi': 'हिमाचल प्रदेश', 'name_mr': 'हिमाचल प्रदेश'},
 {'id': 'JK', 'name': 'Jammu & Kashmir', 'name_hi': 'जम्मू और कश्मीर', 'name_mr': 'जम्मू आणि काश्मीर'},
 {'id': 'JH', 'name': 'Jharkhand', 'name_hi': 'झारखंड', 'name_mr': 'झारखंड'},
 {'id': 'KA', 'name': 'Karnataka', 'name_hi': 'कर्नाटक', 'name_mr': 'कर्नाटक'},
 {'id': 'KL', 'name': 'Kerala', 'name_hi': 'केरल', 'name_mr': 'केरळ'},
 {'id': 'LA', 'name': 'Ladakh', 'name_hi': 'लद्दाख़', 'name_mr': 'लडाख'},
 {'id': 'LD', 'name': 'Lakshadweep', 'name_hi': 'लक्षद्वीप', 'name_mr': 'लक्षद्वीप'},
 {'id': 'MP', 'name': 'Madhya Pradesh', 'name_hi': 'मध्य प्रदेश', 'name_mr': 'मध्य प्रदेश'},
 {'id': 'MH', 'name': 'Maharashtra', 'name_hi': 'महाराष्ट्र', 'name_mr': 'महाराष्ट्र'},
 {'id': 'MN', 'name': 'Manipur', 'name_hi': 'मणिपुर', 'name_mr': 'मणिपूर'},
 {'id': 'ML', 'name': 'Meghalaya', 'name_hi': 'मेघालय', 'name_mr': 'मेघालय'},
 {'id': 'MZ', 'name': 'Mizoram', 'name_hi': 'मिज़ोरम', 'name_mr': 'मिझोराम'},
 {'id': 'NL', 'name': 'Nagaland', 'name_hi': 'नागालैंड', 'name_mr': 'नागालँड'},
 {'id': 'OD', 'name': 'Odisha', 'name_hi': 'ओडिशा', 'name_mr': 'ओडिशा'},
 {'id': 'PY', 'name': 'Puducherry', 'name_hi': 'पुडुचेरी', 'name_mr': 'पुडुचेरी'},
 {'id': 'PB', 'name': 'Punjab', 'name_hi': 'पंजाब', 'name_mr': 'पंजाब'},
 {'id': 'RJ', 'name': 'Rajasthan', 'name_hi': 'राजस्थान', 'name_mr': 'राजस्थान'},
 {'id': 'SK', 'name': 'Sikkim', 'name_hi': 'सिक्किम', 'name_mr': 'सिक्कीम'},
 {'id': 'TN', 'name': 'Tamil Nadu', 'name_hi': 'तमिलनाडु', 'name_mr': 'तामिळनाडू'},
 {'id': 'TS', 'name': 'Telangana', 'name_hi': 'तेलंगाना', 'name_mr': 'तेलंगणा'},
 {'id': 'TR', 'name': 'Tripura', 'name_hi': 'त्रिपुरा', 'name_mr': 'त्रिपुरा'},
 {'id': 'UP', 'name': 'Uttar Pradesh', 'name_hi': 'उत्तर प्रदेश', 'name_mr': 'उत्तर प्रदेश'},
 {'id': 'UK', 'name': 'Uttarakhand', 'name_hi': 'उत्तराखंड', 'name_mr': 'उत्तराखंड'},
 {'id': 'WB', 'name': 'West Bengal', 'name_hi': 'पश्चिम बंगाल', 'name_mr': 'पश्चिम बंगाल'}]

STATE_RULES_SEED = {'caste_validity_certificate': {'MH': {'state_id': 'MH',
                                       'state_name': 'Maharashtra',
                                       'authority': 'Divisional Caste Scrutiny Committee / Social Justice & Special '
                                                    'Assistance Dept.',
                                       'portal_name': 'CCVIS / Barti Maharashtra',
                                       'portal_url': 'https://barti.maharashtra.gov.in',
                                       'statutory_rule': 'Under Maharashtra Scheduled Castes, Scheduled Tribes, '
                                                         'De-notified Tribes (Vimukta Jatis), Nomadic Tribes, Other '
                                                         'Backward Classes and Special Backward Category (Regulation '
                                                         'of Issuance and Verification of) Caste Certificate Act, 2000 '
                                                         '(Mah. Act XXIII of 2001), applicant must produce documentary '
                                                         'evidence of residence and caste entry in Maharashtra prior '
                                                         'to statutory cutoff dates: 10 Aug 1950 (for SC), 6 Sept 1950 '
                                                         '(for ST), or 13 Oct 1967 (for OBC/VJNT/SBC). If a blood '
                                                         'relative holds a valid caste validity certificate, scrutiny '
                                                         'is expedited.',
                                       'additional_requirements': [{'document_id': 'pre_1950_caste_proof',
                                                                    'necessity': 'required',
                                                                    'note': 'Primary school LC, birth extract, or land '
                                                                            'record of father/grandfather before '
                                                                            'cutoff date (1950 for SC, 1967 for OBC)'},
                                                                   {'document_id': 'relative_validity_record',
                                                                    'necessity': 'optional',
                                                                    'note': 'Certified copy of Caste Validity '
                                                                            'Certificate of father, real brother, '
                                                                            'paternal uncle or grandfather (if '
                                                                            'available)'}],
                                       'application_steps': ['Register online on CCVIS portal '
                                                             '(barti.maharashtra.gov.in)',
                                                             'Fill Form 16 (for educational admissions) or Form 17 '
                                                             '(for government employment / election)',
                                                             'Upload scanned primary school records of self and '
                                                             'father/paternal grandfather',
                                                             'Submit printed physical dossier with self-attested '
                                                             'documents to the District Scrutiny Committee',
                                                             'Attend vigilance cell hearing if inquiry is initiated by '
                                                             'the committee',
                                                             'Collect or download sanctioned Caste Validity '
                                                             'Certificate']},
                                'DL': {'state_id': 'DL',
                                       'state_name': 'Delhi',
                                       'authority': 'Revenue Department, Government of NCT of Delhi / SDM Office',
                                       'portal_name': 'e-District Delhi',
                                       'portal_url': 'https://edistrict.delhigovt.nic.in',
                                       'statutory_rule': 'Government of NCT of Delhi mandates proof of continuous '
                                                         'residence in Delhi for at least 3 years. For Delhi State SC '
                                                         'reservation list benefits, ancestral family residence in '
                                                         'Delhi prior to 1951 must be proven; otherwise certificate is '
                                                         'issued on Delhi migrants basis under Government of India '
                                                         'guidelines.',
                                       'additional_requirements': [{'document_id': 'delhi_3yr_residence_proof',
                                                                    'necessity': 'required',
                                                                    'note': 'Documentary proof of continuous stay in '
                                                                            'Delhi for minimum 3 years (electricity '
                                                                            'bill, voter ID, or school attendance '
                                                                            'certificate)'}],
                                       'application_steps': ['Register on e-District Delhi portal using Aadhaar number',
                                                             'Apply under Revenue Dept > Caste Certificate '
                                                             'Verification',
                                                             'Upload Delhi 3-year residence proof, self-declaration, '
                                                             'and existing caste certificate',
                                                             'Book physical verification slot at the respective '
                                                             'Sub-Divisional Magistrate (SDM) office',
                                                             'Verify biometrics & documents before SDM inquiry officer',
                                                             'Download digitally signed verification certificate']},
                                'KA': {'state_id': 'KA',
                                       'state_name': 'Karnataka',
                                       'authority': 'Directorate of Social Welfare & Backward Classes / Tahsildar',
                                       'portal_name': 'Seva Sindhu Karnataka',
                                       'portal_url': 'https://sevasindhu.karnataka.gov.in',
                                       'statutory_rule': 'Verification is processed under Karnataka Act 29 of 1991. '
                                                         'The 15-digit RD barcode number from the underlying '
                                                         'Nadakacheri caste certificate is mandatory. Spot '
                                                         'verification is conducted by the area Revenue Inspector and '
                                                         'scrutinized by the District Caste Verification Committee '
                                                         'headed by Deputy Commissioner.',
                                       'additional_requirements': [{'document_id': 'nadakacheri_rd_number',
                                                                    'necessity': 'required',
                                                                    'note': 'Nadakacheri 15-digit RD barcode '
                                                                            'acknowledgment slip / certificate '
                                                                            'number'}],
                                       'application_steps': ['Log in to Seva Sindhu portal '
                                                             '(sevasindhu.karnataka.gov.in) or visit Atalji Janasnehi '
                                                             'Kendra',
                                                             'Submit Nadakacheri RD number to fetch caste verification '
                                                             'case',
                                                             'Upload school transfer certificate showing caste entry '
                                                             'and family tree',
                                                             'Revenue Inspector conducts spot enquiry at ancestral '
                                                             'residence',
                                                             'District Verification Committee scrutinizes report and '
                                                             'approves validity',
                                                             'Download verification certificate with digital signature '
                                                             'from Seva Sindhu']},
                                'UP': {'state_id': 'UP',
                                       'state_name': 'Uttar Pradesh',
                                       'authority': 'Board of Revenue, Uttar Pradesh / Tehsil Scrutiny Cell',
                                       'portal_name': 'eDistrict Uttar Pradesh',
                                       'portal_url': 'https://edistrict.up.gov.in',
                                       'statutory_rule': 'Requires mandatory local inquiry by the area Lekhpal '
                                                         '(Patwari) and Revenue Inspector, along with an attested copy '
                                                         'of the Parivar Register Nakal from Gram Panchayat / Nagar '
                                                         'Palika certifying ancestral settlement in Uttar Pradesh.',
                                       'additional_requirements': [{'document_id': 'parivar_register_nakal',
                                                                    'necessity': 'required',
                                                                    'note': 'Attested copy of Parivar Register Nakal '
                                                                            'issued by Gram Panchayat Secretary / '
                                                                            'Nagar Palika'}],
                                       'application_steps': ['Log in to eDistrict UP Citizen Portal or apply via CSC '
                                                             'Kendra',
                                                             'Fill online application and attach Parivar Register '
                                                             'Nakal and caste affidavit',
                                                             'Application is forwarded to local Lekhpal for ancestral '
                                                             'verification',
                                                             'Lekhpal submits spot inquiry report to Tehsildar within '
                                                             '10 days',
                                                             'Tehsildar issues digital verification certificate with '
                                                             'QR code']},
                                'GJ': {'state_id': 'GJ',
                                       'state_name': 'Gujarat',
                                       'authority': 'Developing Castes Welfare Dept / Mamlatdar Office',
                                       'portal_name': 'Digital Gujarat',
                                       'portal_url': 'https://www.digitalgujarat.gov.in',
                                       'statutory_rule': 'Gujarat requires a certified Pedhinama (genealogical family '
                                                         'tree) attested by Talati or Executive Magistrate, certifying '
                                                         'ancestry prior to 1960 state reorganization cutoff date. In '
                                                         'addition, two witness statements (Panchkyas) are recorded by '
                                                         'the Talati.',
                                       'additional_requirements': [{'document_id': 'pedhinama',
                                                                    'necessity': 'required',
                                                                    'note': 'Pedhinama (genealogical family tree) '
                                                                            'attested by Talati cum Mantri / Executive '
                                                                            'Magistrate'}],
                                       'application_steps': ['Register on Digital Gujarat portal with mobile number',
                                                             'Select Caste Scrutiny / Verification service under '
                                                             'Developing Castes Welfare',
                                                             'Upload attested Pedhinama and ancestral school leaving '
                                                             'certificates',
                                                             'Talati conducts village verification and submits Rojkam '
                                                             'to Mamlatdar',
                                                             'Download verified certificate from Digital Gujarat '
                                                             'citizen inbox']}},
 'caste_certificate': {'MH': {'state_id': 'MH',
                              'state_name': 'Maharashtra',
                              'authority': 'Revenue Department / Tahsildar / Sub-Divisional Officer (SDO)',
                              'portal_name': 'Aaple Sarkar Maharashtra',
                              'portal_url': 'https://aaplesarkar.mahaonline.gov.in',
                              'statutory_rule': 'Application submitted under Right to Services Act (RTS). Mandatory '
                                                'proof of ancestral residence in Maharashtra before 1950 (SC/ST) or '
                                                '1967 (OBC/VJNT). Certificate is issued by Sub-Divisional Officer '
                                                '(Revenue) within 21 days.',
                              'additional_requirements': [{'document_id': 'pre_1950_caste_proof',
                                                           'necessity': 'required',
                                                           'note': 'Primary school LC or birth record of '
                                                                   'father/grandfather before 1950/1967'}],
                              'application_steps': ['Create profile on Aaple Sarkar portal '
                                                    '(aaplesarkar.mahaonline.gov.in)',
                                                    'Select Revenue Department > Caste Certificate',
                                                    'Fill applicant details and attach self-declaration & ancestral '
                                                    'proof',
                                                    'Pay statutory service charge online (approx. Rs. 33)',
                                                    'Tahsildar / SDO issues digitally signed certificate within 21 '
                                                    'days']},
                       'DL': {'state_id': 'DL',
                              'state_name': 'Delhi',
                              'authority': 'Revenue Department, Govt of NCT of Delhi / SDM Office',
                              'portal_name': 'e-District Delhi',
                              'portal_url': 'https://edistrict.delhigovt.nic.in',
                              'statutory_rule': 'Delhi Revenue Department requires proof of stay in Delhi for minimum '
                                                "3 consecutive years. If applying on basis of father's Delhi caste "
                                                'certificate, issuance timeline is 14 days; without Delhi certificate, '
                                                'field inquiry is mandatory.',
                              'additional_requirements': [{'document_id': 'delhi_3yr_residence_proof',
                                                           'necessity': 'required',
                                                           'note': 'Proof of 3 years continuous residence in Delhi '
                                                                   '(bills, voter card, or school ID)'}],
                              'application_steps': ['Log in to edistrict.delhigovt.nic.in using Aadhaar',
                                                    'Select Apply Online > Issuance of SC/ST/OBC Certificate',
                                                    'Upload self-declaration form, photo, and 3-year Delhi residence '
                                                    'proof',
                                                    'Visit SDM office if required for field report verification',
                                                    'Download digitally signed certificate from portal']},
                       'KA': {'state_id': 'KA',
                              'state_name': 'Karnataka',
                              'authority': 'Revenue Department / Tahsildar (Nadakacheri)',
                              'portal_name': 'Nadakacheri / Seva Sindhu',
                              'portal_url': 'https://nadakacheri.karnataka.gov.in',
                              'statutory_rule': 'Karnataka issues Caste and Income Certificate combined or Form D/E/F. '
                                                'Application is verified through Revenue Inspector spot inspection. '
                                                '15-digit RD barcode is assigned on application.',
                              'additional_requirements': [{'document_id': 'nadakacheri_rd_number',
                                                           'necessity': 'required',
                                                           'note': 'Nadakacheri RD application acknowledgment slip'}],
                              'application_steps': ['Open nadakacheri.karnataka.gov.in > Online Application',
                                                    'Select Caste Certificate / Category 1 / 2A / 2B / 3A / 3B',
                                                    'Fill family tree details and upload school transfer certificate',
                                                    'Revenue Inspector visits residence for spot inspection',
                                                    'Tahsildar signs digital certificate; download via RD number']},
                       'UP': {'state_id': 'UP',
                              'state_name': 'Uttar Pradesh',
                              'authority': 'Revenue Department, Uttar Pradesh / Tehsildar',
                              'portal_name': 'eDistrict UP',
                              'portal_url': 'https://edistrict.up.gov.in',
                              'statutory_rule': 'Requires mandatory verification from area Lekhpal (Patwari) and '
                                                'attested copy of Parivar Register Nakal from Village Panchayat or '
                                                'Urban Nagar Palika.',
                              'additional_requirements': [{'document_id': 'parivar_register_nakal',
                                                           'necessity': 'required',
                                                           'note': 'Attested copy of Parivar Register Nakal from '
                                                                   'Village Secretary / Nagar Palika'}],
                              'application_steps': ['Log in to eDistrict UP Citizen Portal or CSC Jan Seva Kendra',
                                                    'Fill Caste Certificate application form with Gram/Ward name',
                                                    'Attach Parivar Register extract, photo, and self-declaration',
                                                    'Lekhpal conducts inquiry and submits report to Tehsildar within 7 '
                                                    'days',
                                                    'Download digitally approved certificate from portal']},
                       'GJ': {'state_id': 'GJ',
                              'state_name': 'Gujarat',
                              'authority': 'Revenue & Social Justice Dept / Mamlatdar Office',
                              'portal_name': 'Digital Gujarat',
                              'portal_url': 'https://www.digitalgujarat.gov.in',
                              'statutory_rule': 'Gujarat requires a certified Pedhinama (pedigree family tree) '
                                                'certified by Talati cum Mantri, and proof of residence prior to 1960.',
                              'additional_requirements': [{'document_id': 'pedhinama',
                                                           'necessity': 'required',
                                                           'note': 'Pedhinama (genealogical family tree) attested by '
                                                                   'Talati / Executive Magistrate'}],
                              'application_steps': ['Register on Digital Gujarat portal',
                                                    'Apply for SC / ST / SEBC (OBC) Certificate',
                                                    "Upload Pedhinama, father's school LC, and photo",
                                                    'Talati verifies documents and submits inquiry report',
                                                    'Mamlatdar approves and issues digital certificate']}},
 'income_certificate': {'MH': {'state_id': 'MH',
                               'state_name': 'Maharashtra',
                               'authority': 'Revenue Department / Tahsildar Office',
                               'portal_name': 'Aaple Sarkar Maharashtra',
                               'portal_url': 'https://aaplesarkar.mahaonline.gov.in',
                               'statutory_rule': 'Issued for 1 year or 3 years. Verified by local Talati/Circle '
                                                 'Officer based on agricultural land records, employer salary '
                                                 'certificate, or business self-declaration. Issued within 15 days '
                                                 'under RTS.',
                               'additional_requirements': [{'document_id': 'talati_verification_report',
                                                            'necessity': 'required',
                                                            'note': 'Talati inquiry report / circle inspector income '
                                                                    'recommendation'}],
                               'application_steps': ['Log in to Aaple Sarkar portal',
                                                     'Select Revenue Department > Income Certificate (1 or 3 years)',
                                                     'Attach Form 16 / salary slip / Talati punchkyas and '
                                                     'self-declaration',
                                                     'Pay online fee of Rs. 33',
                                                     'Download digital certificate with barcoded security seal']},
                        'DL': {'state_id': 'DL',
                               'state_name': 'Delhi',
                               'authority': 'Revenue Department, Govt of NCT of Delhi / SDM Office',
                               'portal_name': 'e-District Delhi',
                               'portal_url': 'https://edistrict.delhigovt.nic.in',
                               'statutory_rule': 'Income certificate valid for 1 financial year. Requires 3-year '
                                                 'continuous Delhi residence proof, electricity bills of last 3 '
                                                 'months, and employer salary slip or Form 16.',
                               'additional_requirements': [{'document_id': 'delhi_3yr_residence_proof',
                                                            'necessity': 'required',
                                                            'note': 'Proof of 3 years continuous Delhi stay (utility '
                                                                    'bill, voter ID)'}],
                               'application_steps': ['Log in to e-District Delhi portal',
                                                     'Select Issuance of Income Certificate under Revenue Department',
                                                     'Upload 3 years Delhi proof, 3 months electricity bill, and '
                                                     'income self-declaration',
                                                     'Field inspection conducted by Executive Magistrate '
                                                     'representative if required',
                                                     'Certificate issued within 14 working days']},
                        'KA': {'state_id': 'KA',
                               'state_name': 'Karnataka',
                               'authority': 'Revenue Department / Tahsildar (Nadakacheri)',
                               'portal_name': 'Nadakacheri / Seva Sindhu',
                               'portal_url': 'https://nadakacheri.karnataka.gov.in',
                               'statutory_rule': 'Integrated with Kutumba Family ID database. Income is validated '
                                                 'against agricultural holding records (Bhoomi) and GST/salary data. '
                                                 'Valid for 5 years in Karnataka.',
                               'additional_requirements': [{'document_id': 'kutumba_sats_id',
                                                            'necessity': 'required',
                                                            'note': 'Karnataka Kutumba Family ID / Ration card '
                                                                    'linking'}],
                               'application_steps': ['Open Nadakacheri portal and select Income Certificate',
                                                     'Provide Aadhaar and Kutumba/Ration card number',
                                                     'System fetches landholding and family records',
                                                     'Revenue Inspector completes inquiry if manual review triggered',
                                                     'Download certificate digitally via RD number']},
                        'UP': {'state_id': 'UP',
                               'state_name': 'Uttar Pradesh',
                               'authority': 'Board of Revenue, Uttar Pradesh / Tehsildar',
                               'portal_name': 'eDistrict UP',
                               'portal_url': 'https://edistrict.up.gov.in',
                               'statutory_rule': 'Income certificate valid for 3 years. Inquiry conducted by area '
                                                 'Lekhpal evaluating family agricultural land (Khatauni), business, or '
                                                 'private employment.',
                               'additional_requirements': [{'document_id': 'parivar_register_nakal',
                                                            'necessity': 'required',
                                                            'note': 'Parivar Register Nakal showing all family '
                                                                    'members'}],
                               'application_steps': ['Log in to eDistrict UP Citizen Portal or apply through CSC '
                                                     'Kendra',
                                                     'Fill income declaration form specifying income from all sources',
                                                     'Attach Parivar Register copy, salary slip/affidavit, and photo',
                                                     'Lekhpal verifies family income and enters report into portal',
                                                     'Tehsildar signs and issues digital certificate']},
                        'GJ': {'state_id': 'GJ',
                               'state_name': 'Gujarat',
                               'authority': 'Revenue Department / Mamlatdar Office',
                               'portal_name': 'Digital Gujarat',
                               'portal_url': 'https://www.digitalgujarat.gov.in',
                               'statutory_rule': 'Valid for 3 financial years. Requires Talati punchkyas report, '
                                                 'self-declaration affidavit, and electricity bill or employer '
                                                 'statement.',
                               'additional_requirements': [{'document_id': 'talati_verification_report',
                                                            'necessity': 'required',
                                                            'note': 'Talati verification punchkyas / circle report'}],
                               'application_steps': ['Log in to Digital Gujarat portal',
                                                     'Select Revenue > Income Certificate',
                                                     'Upload income proof, affidavit, and utility bill',
                                                     'Talati verifies and signs recommendation report',
                                                     'Download certificate from citizen portal']}},
 'sample_scholarship_scheme': {'MH': {'state_id': 'MH',
                                      'state_name': 'Maharashtra',
                                      'authority': 'Social Justice & Special Assistance / Higher Education Dept.',
                                      'portal_name': 'MahaDBT (Direct Benefit Transfer)',
                                      'portal_url': 'https://mahadbt.maharashtra.gov.in',
                                      'statutory_rule': 'Post-Matric Scholarship guidelines require applicant to hold '
                                                        'Maharashtra Domicile and Caste Validity Certificate (for '
                                                        'professional/reserved category courses). Bank account must be '
                                                        'seeded with Aadhaar in NPCI mapper.',
                                      'additional_requirements': [{'document_id': 'domicile_certificate',
                                                                   'necessity': 'required',
                                                                   'note': 'Maharashtra Domicile / Residence '
                                                                           'Certificate'}],
                                      'application_steps': ['Register on MahaDBT portal (mahadbt.maharashtra.gov.in) '
                                                            'with Aadhaar',
                                                            'Complete personal, address, and caste profile details',
                                                            'Link college admission allotment and fee receipt',
                                                            'Submit scheme application before annual deadline',
                                                            'College scrutinizes and forwards to Social Welfare '
                                                            'Officer',
                                                            'Scholarship and fee reimbursement disbursed directly into '
                                                            'bank account via DBT']},
                               'DL': {'state_id': 'DL',
                                      'state_name': 'Delhi',
                                      'authority': 'Department for the Welfare of SC/ST/OBC/Minorities, Govt of NCT of '
                                                   'Delhi',
                                      'portal_name': 'e-District Delhi (Scholarship Portal)',
                                      'portal_url': 'https://edistrict.delhigovt.nic.in',
                                      'statutory_rule': 'Student must have studied or be enrolled in a recognized '
                                                        'educational institution in Delhi and hold Delhi residence '
                                                        'proof. Maximum family income ceiling applies as per annual '
                                                        'notification.',
                                      'additional_requirements': [{'document_id': 'delhi_3yr_residence_proof',
                                                                   'necessity': 'required',
                                                                   'note': 'Proof of residence in Delhi (minimum 3 '
                                                                           'years)'}],
                                      'application_steps': ['Log in to e-District Delhi portal',
                                                            'Select Post-Matric Scholarship for SC/ST/OBC Students',
                                                            'Upload fee receipt, previous year marksheets, and '
                                                            'institution verification form',
                                                            'Institution nodal officer verifies student attendance and '
                                                            'enrollment',
                                                            'State department approves DBT transfer to Aadhaar-seeded '
                                                            'bank account']},
                               'KA': {'state_id': 'KA',
                                      'state_name': 'Karnataka',
                                      'authority': 'Social Welfare & Backward Classes Welfare Dept.',
                                      'portal_name': 'State Scholarship Portal (SSP Karnataka)',
                                      'portal_url': 'https://ssp.postmatric.karnataka.gov.in',
                                      'statutory_rule': 'Karnataka Post-Matric Scholarship mandates Student '
                                                        'Achievement Tracking System (SATS) ID and Kutumba Family ID. '
                                                        'Both Caste and Income RD barcode numbers are verified '
                                                        'electronically.',
                                      'additional_requirements': [{'document_id': 'kutumba_sats_id',
                                                                   'necessity': 'required',
                                                                   'note': 'Kutumba Family ID and 9-digit SATS Student '
                                                                           'Enrollment ID'}],
                                      'application_steps': ['Create student account on SSP portal using Aadhaar and '
                                                            'SATS ID',
                                                            'Enter Kutumba ID — family income and caste data '
                                                            'auto-fetches',
                                                            'Enter college enrollment number and hostel status',
                                                            'E-attestation of documents completed by college nodal '
                                                            'verification officer',
                                                            'District officer sanctions amount; DBT payment '
                                                            'processed']},
                               'UP': {'state_id': 'UP',
                                      'state_name': 'Uttar Pradesh',
                                      'authority': 'Social Welfare Department, Uttar Pradesh',
                                      'portal_name': 'UP Scholarship Portal',
                                      'portal_url': 'https://scholarship.up.gov.in',
                                      'statutory_rule': 'UP Post-Matric Scholarship requires UP Domicile, valid Income '
                                                        'Certificate verified via eDistrict database, and institute '
                                                        'registered in UP Master Data.',
                                      'additional_requirements': [{'document_id': 'domicile_certificate',
                                                                   'necessity': 'required',
                                                                   'note': 'Uttar Pradesh Domicile / Niwas Praman '
                                                                           'Patra'}],
                                      'application_steps': ['Register on scholarship.up.gov.in using High School Roll '
                                                            'No and Mobile',
                                                            'Fill academic, caste, and income certificate application '
                                                            'numbers',
                                                            'System verifies certificate data directly with eDistrict '
                                                            'UP server',
                                                            'Submit hard copy with fee receipt to college for '
                                                            'verification',
                                                            'District Social Welfare Officer sanctions scholarship via '
                                                            'PFMS']},
                               'GJ': {'state_id': 'GJ',
                                      'state_name': 'Gujarat',
                                      'authority': 'Social Justice & Empowerment Dept, Govt of Gujarat',
                                      'portal_name': 'Digital Gujarat Scholarships',
                                      'portal_url': 'https://www.digitalgujarat.gov.in',
                                      'statutory_rule': 'Gujarat Domicile required. Student bank account must be '
                                                        'seeded with Aadhaar on NPCI mapper. Verified digitally with '
                                                        'institute records.',
                                      'additional_requirements': [{'document_id': 'domicile_certificate',
                                                                   'necessity': 'required',
                                                                   'note': 'Gujarat State Domicile Certificate'}],
                                      'application_steps': ['Log in to Digital Gujarat portal with student profile',
                                                            'Apply under Post-Matric Scholarship for SC/ST/SEBC',
                                                            'Upload fee structure, hostel certificate, and previous '
                                                            'marksheets',
                                                            'Principal / College verification team approves '
                                                            'application online',
                                                            'Treasury disburses scholarship via DBT']}}}

SYNONYMS_SEED = {'cert': ['certificate'],
 'validity': ['validation', 'valid'],
 'aadhar': ['aadhaar'],
 'aadher': ['aadhaar'],
 'cvc': ['caste validity certificate'],
 'slc': ['school leaving certificate'],
 'tc': ['transfer certificate'],
 'jaati': ['caste'],
 'praman': ['certificate', 'proof'],
 'patra': ['certificate', 'document'],
 'income': ['earning', 'salary'],
 'scholarship': ['scholarship scheme', 'merit scholarship'],
 'stamp': ['stamp paper', 'affidavit'],
 'affidavit': ['affidavit on stamp paper'],
 'photo': ['passport-size photograph', 'photograph'],
 'ration': ['ration card'],
 'electricity': ['electricity bill'],
 'rent': ['rent agreement'],
 'bank': ['bank passbook'],
 'passbook': ['bank passbook'],
 'pan': ['pan card', 'permanent account number', 'nsdl pan', 'uti pan'],
 'voter': ['voter id', 'epic', 'election card', 'voters identity card'],
 'epic': ['voter id', 'voter card', 'election card'],
 'passport': ['indian passport', 'passport seva', 'tatkaal passport'],
 'driving': ['driving licence', 'driver licence', 'learner licence'],
 'licence': ['license', 'driving licence', 'learner licence'],
 'license': ['licence', 'driving licence'],
 'dl': ['driving licence', 'driving license'],
 'birth': ['birth certificate', 'janam praman patra'],
 'death': ['death certificate', 'mrityu praman patra'],
 'marriage': ['marriage certificate', 'vivah nodani', 'vivah praman patra'],
 'ncl': ['non creamy layer certificate', 'obc ncl', 'non creamy layer'],
 'creamy': ['non creamy layer certificate', 'ncl'],
 'ews': ['economically weaker section certificate', 'ews certificate'],
 'disability': ['disability certificate', 'udid', 'pwd certificate', 'divyang card'],
 'udid': ['disability certificate', 'swavlamban card', 'udid card'],
 'senior': ['senior citizen card', 'senior citizen certificate', 'elderly identity card'],
 'pcc': ['police clearance certificate', 'character certificate', 'police verification'],
 'police': ['police clearance certificate', 'character certificate'],
 'character': ['police clearance certificate', 'character certificate'],
 '7/12': ['land 7/12 extract', 'satbara', '7 12 utara', 'saat baara'],
 'satbara': ['land 7/12 extract', '7/12', '7 12 utara'],
 'gap': ['gap certificate', 'gap affidavit', 'education gap affidavit']}

SOURCES_SEED = [{'id': 'src_aaplesarkar_caste_validity',
  'name': 'Aaple Sarkar — Social Justice & Special Assistance',
  'department': 'Social Justice and Special Assistance Department',
  'jurisdiction': 'Maharashtra',
  'official_base_url': 'https://aaplesarkar.mahaonline.gov.in',
  'monitored_url': 'https://aaplesarkar.mahaonline.gov.in/en/Department/Index/28',
  'source_type': 'html',
  'adapter': 'aaplesarkar_table',
  'associated_service_ids': ['caste_validity_certificate', 'caste_certificate'],
  'associated_document_ids': ['caste_certificate', 'affidavit_stamp_paper'],
  'check_frequency_minutes': 720,
  'enabled': True,
  'priority': 'high',
  'verification_policy': 'manual_review'},
 {'id': 'src_aaplesarkar_revenue',
  'name': 'Aaple Sarkar — Revenue Department Services',
  'department': 'Revenue and Forest Department, Government of Maharashtra',
  'jurisdiction': 'Maharashtra',
  'official_base_url': 'https://aaplesarkar.mahaonline.gov.in',
  'monitored_url': 'https://aaplesarkar.mahaonline.gov.in/en/Department/Index/11',
  'source_type': 'html',
  'adapter': 'aaplesarkar_table',
  'associated_service_ids': ['income_certificate', 'domicile_certificate'],
  'associated_document_ids': ['income_proof', 'residence_proof', 'ration_card'],
  'check_frequency_minutes': 720,
  'enabled': True,
  'priority': 'high',
  'verification_policy': 'manual_review'},
 {'id': 'src_uidai_aadhaar_guidelines',
  'name': 'UIDAI Official Aadhaar Supporting Documents',
  'department': 'Unique Identification Authority of India (UIDAI)',
  'jurisdiction': 'Central',
  'official_base_url': 'https://uidai.gov.in',
  'monitored_url': 'https://uidai.gov.in/images/commDetails/List_of_Supporting_Document_for_Aadhaar_Enrolment_and_Update.pdf',
  'source_type': 'pdf',
  'adapter': 'pdf_circular',
  'associated_service_ids': [],
  'associated_document_ids': ['aadhaar', 'residence_proof'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'high',
  'verification_policy': 'manual_review'},
 {'id': 'src_mahadbt_scholarships',
  'name': 'MahaDBT Post-Matric Scholarship Scheme Guidelines',
  'department': 'Higher & Technical Education / Social Justice, Maharashtra',
  'jurisdiction': 'Maharashtra',
  'official_base_url': 'https://mahadbt.maharashtra.gov.in',
  'monitored_url': 'https://mahadbt.maharashtra.gov.in/SchemeData/SchemeData?str=E9DDFA977C3C3D6C',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': ['post_matric_scholarship'],
  'associated_document_ids': ['caste_validity_certificate', 'income_certificate', 'domicile_certificate'],
  'check_frequency_minutes': 720,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'},
 {'id': 'src_incometax_pan',
  'name': 'Income Tax Department — PAN Services',
  'department': 'Income Tax Department, Ministry of Finance, Government of India',
  'jurisdiction': 'Central',
  'official_base_url': 'https://www.incometax.gov.in',
  'monitored_url': 'https://eportal.incometax.gov.in',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': [],
  'associated_document_ids': ['pan_card'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'},
 {'id': 'src_eci_voters',
  'name': 'Election Commission of India — Voter Services',
  'department': 'Election Commission of India',
  'jurisdiction': 'Central',
  'official_base_url': 'https://voters.eci.gov.in',
  'monitored_url': 'https://voters.eci.gov.in',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': [],
  'associated_document_ids': ['voter_id'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'},
 {'id': 'src_mea_passport',
  'name': 'Ministry of External Affairs — Passport Seva',
  'department': 'Consular, Passport and Visa Division, Ministry of External Affairs',
  'jurisdiction': 'Central',
  'official_base_url': 'https://www.passportindia.gov.in',
  'monitored_url': 'https://www.passportindia.gov.in',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': [],
  'associated_document_ids': ['passport'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'},
 {'id': 'src_morth_sarathi',
  'name': 'MoRTH — Parivahan Sarathi Driving Licence Services',
  'department': 'Ministry of Road Transport and Highways',
  'jurisdiction': 'Central',
  'official_base_url': 'https://sarathi.parivahan.gov.in',
  'monitored_url': 'https://sarathi.parivahan.gov.in',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': [],
  'associated_document_ids': ['driving_licence'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'},
 {'id': 'src_crs_vital_records',
  'name': 'Civil Registration System — Birth and Death Registration',
  'department': 'Office of the Registrar General & Census Commissioner, India',
  'jurisdiction': 'Central',
  'official_base_url': 'https://crsorgi.gov.in',
  'monitored_url': 'https://crsorgi.gov.in',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': [],
  'associated_document_ids': ['birth_certificate', 'death_certificate'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'},
 {'id': 'src_swavlamban_udid',
  'name': 'Swavlamban — Unique Disability ID Portal',
  'department': 'Department of Empowerment of Persons with Disabilities, Ministry of Social Justice',
  'jurisdiction': 'Central',
  'official_base_url': 'https://www.swavlambancard.gov.in',
  'monitored_url': 'https://www.swavlambancard.gov.in',
  'source_type': 'html',
  'adapter': 'generic_html',
  'associated_service_ids': [],
  'associated_document_ids': ['disability_certificate'],
  'check_frequency_minutes': 1440,
  'enabled': True,
  'priority': 'normal',
  'verification_policy': 'manual_review'}]
