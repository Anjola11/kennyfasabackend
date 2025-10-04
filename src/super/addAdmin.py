"""run: python -m src.super.addAdmin"""

import asyncio
from src.auth.services import AdminService
from src.db.main import get_session
from src.auth.models import Admin
from sqlalchemy.exc import DatabaseError

adminService = AdminService()

async def create_admin(admin_name: str, email: str, admin_role: str):
    """Create a new admin account"""
    # Get async session generator
    session_gen = get_session()
    session = await anext(session_gen)
    
    try:
        # Check if admin already exists
        admin = await adminService.admin_exists(email, session)
        if admin:
            return f'Admin with email {email} already exists'
        
        # Create new admin
        new_admin = Admin(
            name=admin_name.strip().title(),
            email=email.strip().lower(),
            role=admin_role
        )
        
        session.add(new_admin)
        
        try:
            await session.commit()
            # Don't refresh after commit - it starts a new transaction
            return f"Admin '{admin_name}' account created successfully with role '{admin_role}'"
        except DatabaseError as e:
            await session.rollback()
            return f"Failed to create admin: {str(e)}"
    
    except Exception as e:
        await session.rollback()
        return f"An error occurred: {str(e)}"
    
    finally:
        # Close the session cleanly
        await session.close()

async def main():
    """Main function to run the admin creation script"""
    print("=== Admin Account Creation ===\n")
    
    admin_name = input("Enter Admin name: ")
    email = input("Enter Admin email: ")
    
    while True:
        try:
            role = int(input("Enter Admin role (1. Owner, 2. Staff): "))
            
            if role not in [1, 2]:
                print("Invalid input. Please enter 1 or 2\n")
                continue
            
            admin_role = "owner" if role == 1 else "staff"
            
            # Create admin account
            result = await create_admin(admin_name, email, admin_role)
            print(f"\n{result}")
            break
            
        except ValueError:
            print("Invalid input. Please enter 1 or 2\n")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            break

if __name__ == "__main__":
    asyncio.run(main())