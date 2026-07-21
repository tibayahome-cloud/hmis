from fastapi import APIRouter

from api.v1 import auth, hospitals, staff

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(hospitals.router)
api_router.include_router(staff.router)

# Day 2+: patients, queues, billing, triage, consultations, service_rooms,
# pharmacy, admissions, ward_rounds, discharge routers will each be added here.
