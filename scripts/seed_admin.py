"""
Creates the first admin staff account. Run once after `alembic upgrade head`,
since every other staff account must be created via the API by an admin,
which requires one to already exist.

Usage:
    python -m scripts.seed_admin --name "Dennis Admin" --email admin@yourdomain.com --password "changeme123"
"""
import argparse
import asyncio

from sqlalchemy import select

from core.security import hash_password
from db.session import AsyncSessionLocal
from models.role import Role
from models.staff import Staff


async def seed_admin(full_name: str, email: str, password: str) -> None:
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(Staff).where(Staff.email == email))
        if existing.scalar_one_or_none() is not None:
            print(f"Staff with email {email} already exists — skipping.")
            return

        role = (await db.execute(select(Role).where(Role.name == "admin"))).scalar_one()
        staff = Staff(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role_id=role.id,
        )
        db.add(staff)
        await db.commit()
        print(f"Admin created: {email} (id={staff.id})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    asyncio.run(seed_admin(args.name, args.email, args.password))
