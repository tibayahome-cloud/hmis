"""
Creates the first super_admin account. Run once after `alembic upgrade head`.
The super_admin has no hospital_id — they exist above the tenant layer and are
the only role that can create hospitals (and each hospital's first admin).

Usage:
    python -m scripts.seed_super_admin --name "Dennis" --email you@yourdomain.com --password "changeme123"
"""
import argparse
import asyncio

from sqlalchemy import select

from core.security import hash_password
from db.session import AsyncSessionLocal
from models.role import Role
from models.staff import Staff


async def seed_super_admin(full_name: str, email: str, password: str) -> None:
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(Staff).where(Staff.email == email))
        if existing.scalar_one_or_none() is not None:
            print(f"Staff with email {email} already exists — skipping.")
            return

        role = (await db.execute(select(Role).where(Role.name == "super_admin"))).scalar_one()
        staff = Staff(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role_id=role.id,
            hospital_id=None,
        )
        db.add(staff)
        await db.commit()
        print(f"super_admin created: {email} (id={staff.id})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    asyncio.run(seed_super_admin(args.name, args.email, args.password))
