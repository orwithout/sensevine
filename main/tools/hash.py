from passlib.context import CryptContext
# pip install bcrypt passlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

if __name__ == "__main__":
    password = input("Enter password to hash: ")
    hashed_password = hash_password(password)
    print("Hashed password:", hashed_password)
