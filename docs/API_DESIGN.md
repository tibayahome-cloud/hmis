# API Design

Base path: `/api/v1`. All endpoints require a JWT bearer token except `/auth/*`.
Roles noted in brackets restrict access via RBAC dependency injection.

## Auth

| Method | Path | Notes |
|---|---|---|
| POST | `/auth/login` | Staff login, returns access + refresh token |
| POST | `/auth/refresh` | Rotate access token |
| POST | `/auth/logout` | Revoke refresh token |

## Patients [receptionist, admin, records_officer]

| Method | Path | Notes |
|---|---|---|
| POST | `/patients` | Register new patient, issues MRN |
| GET | `/patients/{id}` | Full patient record |
| GET | `/patients?search=` | Search by MRN, name, phone, national ID |
| PATCH | `/patients/{id}` | Update demographics |
| POST | `/patients/{id}/insurance-policies` | Attach an insurance policy |
| POST | `/patients/{id}/visits` | Open a new visit (outpatient or admission) |

## Billing [billing_clerk, admin]

| Method | Path | Notes |
|---|---|---|
| POST | `/billing/eligibility-check` | Insurance eligibility lookup |
| POST | `/billing/invoices` | Create invoice for a visit |
| GET | `/billing/invoices/{id}` | Invoice detail with lines |
| POST | `/billing/invoices/{id}/stk-push` | Trigger M-Pesa STK Push |
| POST | `/billing/mpesa/callback` | M-Pesa Daraja webhook (unauthenticated, signature-verified) |
| POST | `/billing/invoices/{id}/receipt` | Issue cash receipt |
| POST | `/billing/claims` | Submit insurance claim against an invoice |
| GET | `/billing/claims/{id}` | Claim status |

## Queues [all clinical roles, scoped by station]

| Method | Path | Notes |
|---|---|---|
| POST | `/queues/{station}/enqueue` | Add a visit to a station's queue |
| GET | `/queues/{station}` | List current queue (for staff view + display board) |
| POST | `/queues/{station}/next` | Pull next patient, marks `in_progress` |
| POST | `/queues/entries/{id}/complete` | Mark queue entry done, optionally auto-enqueue next station |
| WS | `/ws/queues/{station}` | Live queue updates for staff view / public board |

## Triage [triage_nurse]

| Method | Path | Notes |
|---|---|---|
| POST | `/triage/{visit_id}/vitals` | Record vitals, auto-enqueues to `consultation` |

## Consultations [doctor]

| Method | Path | Notes |
|---|---|---|
| POST | `/consultations/{visit_id}` | Record doctor's notes / recording reference |
| POST | `/consultations/{visit_id}/book-next` | Route to a service room or straight to billing |

## Service Rooms [lab_tech, doctor, admin]

| Method | Path | Notes |
|---|---|---|
| POST | `/service-rooms/{type}/orders` | Create order (lab / dental / minor_theatre / optical / imagery) |
| GET | `/service-rooms/orders/{id}` | Order detail |
| POST | `/service-rooms/orders/{id}/result` | Attach result / notes |

## Pharmacy [pharmacist]

| Method | Path | Notes |
|---|---|---|
| POST | `/pharmacy/prescriptions` | Create prescription (outpatient or inpatient) |
| GET | `/pharmacy/prescriptions/{id}` | Prescription detail |
| POST | `/pharmacy/prescriptions/{id}/dispense` | Dispense item(s), deducts stock |
| GET | `/pharmacy/drugs?search=` | Drug catalog / stock lookup |

## Admissions [admission_officer, ward_nurse]

| Method | Path | Notes |
|---|---|---|
| POST | `/admissions` | Open admission from a visit |
| GET | `/admissions/{id}` | Full admission record |
| PATCH | `/admissions/{id}/checklist` | Update admission desk checklist item (print, notify insurance, claim forms, pre-auth, approval, doctor's notes, investigation) |
| POST | `/admissions/{id}/receiving-nurse` | Record intake vitals, assign bed, start dose, pick consultant |
| GET | `/admissions/beds/available` | Free beds by ward |

## Ward Rounds [ward_nurse, doctor, consultant]

| Method | Path | Notes |
|---|---|---|
| POST | `/ward-rounds` | Create a round entry (nurse vitals + doctor notes + optional specialist notes) |
| GET | `/ward-rounds/admission/{admission_id}` | Round history for an admission |
| POST | `/ward-rounds/{id}/route-service-room` | Loop patient out to a service room |
| POST | `/ward-rounds/{id}/route-pharmacy` | Loop patient out to inpatient pharmacy |

## Discharge [doctor, consultant, billing_clerk]

| Method | Path | Notes |
|---|---|---|
| POST | `/discharge/{admission_id}` | Generate discharge summary, triggers final billing |
| GET | `/discharge/{id}/summary` | Fetch discharge summary (printable) |

## Admin

| Method | Path | Notes |
|---|---|---|
| CRUD | `/admin/staff` | Staff and role management |
| CRUD | `/admin/wards`, `/admin/beds` | Ward/bed configuration |
| CRUD | `/admin/service-rooms` | Service room configuration |
| GET | `/admin/reports/*` | Operational + financial reports |

## Conventions

- Pagination: cursor-based (`?cursor=`, `?limit=`) on all list endpoints.
- Errors: RFC7807-style problem responses (`{type, title, status, detail}`).
- Idempotency: payment-initiating endpoints (`stk-push`) accept an
  `Idempotency-Key` header to prevent duplicate charges on retry.
- All monetary amounts are `decimal`, transported as strings in JSON.
