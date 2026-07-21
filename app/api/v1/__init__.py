from fastapi import APIRouter

from app.api.v1 import auth, staff

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(staff.router)

# Day 2+: patients, queues, billing, triage, consultations, service_rooms,
# pharmacy, admissions, ward_rounds, discharge routers will each be added here.
