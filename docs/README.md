# HMIS — Hospital Management Information System

A modular HMIS covering the full patient journey — registration, billing/insurance,
triage, outpatient consultation, ancillary service rooms (lab, dental, minor theatre,
optical, imagery), pharmacy, inpatient admission, ward rounds, and discharge — built
for the Kenyan healthcare market with M-Pesa (STK Push) and insurance billing built in.

> Design reference: see [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) for the source patient
> dataflow this system implements.

## Tech Stack

| Layer | Choice |
|---|---|
| Backend API | FastAPI (Python 3.12), Pydantic v2, SQLAlchemy 2.0 (async) |
| Frontend | Next.js (TypeScript, App Router) |
| Database | PostgreSQL 16 |
| Queueing / async jobs | Celery + Redis (payments, notifications, insurance batch jobs) |
| Payments | M-Pesa Daraja (STK Push), Pesapal (card/insurance top-up) |
| Auth | JWT (access + refresh), role-based access control (RBAC) |
| Infra | Docker + Docker Compose, Nginx reverse proxy, Certbot (SSL) |
| Realtime | WebSockets (queue/board updates at reception, triage, service rooms) |

## Repository Structure

```
hmis/
├── backend/
│   ├── app/
│   │   ├── api/                # FastAPI routers, versioned (v1)
│   │   │   ├── patients/
│   │   │   ├── billing/
│   │   │   ├── triage/
│   │   │   ├── consultations/
│   │   │   ├── service_rooms/
│   │   │   ├── pharmacy/
│   │   │   ├── admissions/
│   │   │   ├── ward_rounds/
│   │   │   ├── discharge/
│   │   │   └── queues/
│   │   ├── core/                # config, security, RBAC, exceptions
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── services/             # business logic per module
│   │   ├── integrations/         # mpesa, pesapal, insurance gateways, sms/email
│   │   ├── workers/               # Celery tasks
│   │   └── db/                    # session, migrations (Alembic)
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── app/                       # Next.js App Router
│   │   ├── (reception)/
│   │   ├── (triage)/
│   │   ├── (consultation)/
│   │   ├── (service-rooms)/
│   │   ├── (pharmacy)/
│   │   ├── (admission)/
│   │   ├── (ward)/
│   │   └── (admin)/
│   ├── components/
│   ├── lib/                       # api client, auth, websocket hooks
│   ├── Dockerfile
│   └── package.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── WORKFLOWS.md
│   └── API_DESIGN.md
├── docker-compose.yml
├── docker-compose.prod.yml
└── .env.example
```

## Core Modules

1. **Registration** — new/returning patient capture, MRN assignment.
2. **Billing** — insurance eligibility check, invoicing, M-Pesa STK Push, cash receipts, co-pay handling.
3. **Triage** — vitals capture (weight, height, BP, BMI), queue routing.
4. **Consultation** — doctor's notes, dictation/recording, next-room booking.
5. **Service Rooms** — Lab, Dental, Minor Theatre, Optical, Imagery, each with its own sub-queue and result capture.
6. **Pharmacy** — outpatient and inpatient dispensing, stock deduction.
7. **Admission** — admission desk (insurance notification, claim forms, pre-auth, bed assignment), receiving nurse intake.
8. **Ward Rounds** — nurse vitals, doctor notes, optional specialist/consultant notes, looped service room / inpatient pharmacy access.
9. **Discharge** — discharge summary generation, final billing.
10. **Queue Engine** — a shared, cross-cutting service that every module above reads/writes to; drives the reception/triage/service-room display boards.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for how these modules are decomposed into services, and [`docs/DATABASE_SCHEMA.md`](docs/DATABASE_SCHEMA.md) for the data model.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (local dev without Docker)
- Node 20+ (local dev without Docker)

### Local development

```bash
cp .env.example .env
docker compose up --build
```

- API: http://localhost:8000 (docs at `/docs`)
- Web: http://localhost:3000
- Postgres: localhost:5432
- Redis: localhost:6379

### Running migrations

```bash
docker compose exec backend alembic upgrade head
```

### Running tests

```bash
docker compose exec backend pytest
docker compose exec frontend npm run test
```

## Environment Variables

See `.env.example` for the full list. Key groups:
- `DATABASE_URL`, `REDIS_URL`
- `JWT_SECRET`, `JWT_EXPIRY_MINUTES`
- `MPESA_CONSUMER_KEY`, `MPESA_CONSUMER_SECRET`, `MPESA_SHORTCODE`, `MPESA_PASSKEY`
- `PESAPAL_CONSUMER_KEY`, `PESAPAL_CONSUMER_SECRET`
- `INSURANCE_GATEWAY_URL` (per-provider eligibility/claims API)

## Roles (RBAC)

`admin`, `receptionist`, `billing_clerk`, `triage_nurse`, `doctor`, `lab_tech`,
`pharmacist`, `admission_officer`, `ward_nurse`, `consultant`, `records_officer`.
Each API route is scoped to one or more roles; see `backend/app/core/rbac.py`.

## Status

🚧 Early-stage design — architecture and schema defined, implementation in progress.

## License

Proprietary — © Mobiclick Systems.
