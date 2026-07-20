# System Architecture

## 1. High-Level Architecture

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Web["Next.js Web App<br/>(Reception / Triage / Consultation /<br/>Service Rooms / Pharmacy / Admission / Ward / Admin)"]
        Board["Queue Display Boards<br/>(WebSocket clients)"]
    end

    subgraph Edge["Edge"]
        Nginx["Nginx<br/>reverse proxy + SSL"]
    end

    subgraph API["Application Layer"]
        FastAPI["FastAPI backend<br/>REST + WebSocket"]
        Celery["Celery workers<br/>async jobs"]
    end

    subgraph Data["Data Layer"]
        PG[("PostgreSQL")]
        Redis[("Redis<br/>cache / broker / pub-sub")]
    end

    subgraph External["External Integrations"]
        Mpesa["M-Pesa Daraja<br/>(STK Push)"]
        Pesapal["Pesapal"]
        Insurance["Insurance Gateways<br/>(eligibility / claims)"]
        SMS["SMS / Email"]
    end

    Web -->|HTTPS| Nginx
    Board -->|WSS| Nginx
    Nginx --> FastAPI
    FastAPI --> PG
    FastAPI --> Redis
    FastAPI -->|enqueue| Celery
    Celery --> PG
    Celery --> Redis
    Celery --> Mpesa
    Celery --> Pesapal
    Celery --> Insurance
    Celery --> SMS
    FastAPI -.->|pub/sub queue events| Redis
    Redis -.->|broadcast| FastAPI
```

## 2. Why This Split

- **FastAPI over Flask**: async I/O matters here — STK Push callbacks, insurance
  eligibility checks, and queue-board WebSocket pushes are all I/O-bound and benefit
  from native `async`/`await` instead of blocking workers.
- **Next.js over plain React**: multiple distinct staff-facing surfaces (reception,
  triage, consultation, service rooms, pharmacy, admission, ward, admin) share auth
  and layout but are logically separate route groups — App Router route groups
  (`(reception)`, `(triage)`, …) fit this directly, plus server components reduce
  the payload on shared-workstation hospital PCs.
- **Celery + Redis**: M-Pesa/Pesapal callbacks and insurance claim submissions are
  retried, rate-limited, and sometimes slow (external API) — kept off the request/response
  path.
- **WebSockets for queues**: the source workflow has a queue in front of nearly every
  station (triage, consultation, service rooms, billing, pharmacy, admission,
  receiving nurse). Queue state changes need to reach the relevant station and the
  public display board in real time, so it is modeled as a first-class service, not
  an incidental DB flag.

## 3. Module → Service Mapping

| Module (from workflow) | Backend service | Key responsibilities |
|---|---|---|
| Patient Registration | `patients` | MRN issuance, demographics, insurance card capture |
| Billing | `billing` | Eligibility check, invoice/receipt, STK Push, co-pay logic |
| Triage | `triage` | Vitals capture, routes patient into Consultation Queue |
| Consultation | `consultations` | Doctor notes, session recording metadata, "book next room" |
| Service Rooms | `service_rooms` | Lab / Dental / Minor Theatre / Optical / Imagery sub-queues + results |
| Pharmacy | `pharmacy` | Outpatient & inpatient dispensing, stock deduction |
| Admission | `admissions` | Admission desk workflow, insurance pre-auth, bed assignment, receiving nurse intake |
| Ward Rounds | `ward_rounds` | Nurse vitals, doctor notes, optional specialist notes, loop into service rooms/inpatient pharmacy |
| Discharge | `discharge` | Discharge summary, final billing trigger |
| Queues (cross-cutting) | `queues` | Generic queue entries consumed by every module above; drives WebSocket board updates |

## 4. Queue Engine (Cross-Cutting)

Every station in the source diagram (Triage Queue, Consultation Queue, Service
Rooms Queue, Billing, Inpatient Pharmacy Queue, Admission Queue, Receiving Nurse
Queue) is an instance of the same underlying entity, not a bespoke table per
station:

```mermaid
flowchart LR
    A[Visit reaches a station] --> B[queues.enqueue visit_id, station]
    B --> C{Station worker calls next}
    C --> D[queues.mark_in_progress]
    D --> E[Station completes work]
    E --> F[queues.mark_done]
    F --> G[Service decides next station]
    G --> B
    F -.->|WS broadcast| H[Display board / next station]
```

This lets a single `queues` table + service drive routing for outpatient, service
rooms, and the whole admission/ward loop, instead of duplicating queue logic per
module.

## 5. Deployment

```mermaid
flowchart LR
    subgraph VPS["Single VPS (Docker Compose)"]
        Nginx2[Nginx + Certbot]
        FE[Next.js container]
        BE[FastAPI container]
        CW[Celery worker container]
        CB[Celery beat container]
        PGc[(Postgres container/volume)]
        RDc[(Redis container)]
    end
    Internet((Internet)) --> Nginx2
    Nginx2 --> FE
    Nginx2 --> BE
    BE --> PGc
    BE --> RDc
    CW --> PGc
    CW --> RDc
    CB --> RDc
```

Mirrors the Dockerized deployment pattern already used on other Mobiclick Systems
projects — Nginx + Certbot for TLS, Postgres and Redis as long-lived volumes,
Celery worker/beat as separate containers so payment/insurance jobs don't compete
with API request handling.
