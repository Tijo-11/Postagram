import pytest
from core.user.models import User

data_user = {
    "username":"test_user",
    "email": "test@gmail.com",
   "first_name": "Test",
   "last_name": "User",
   "password": "test_password"
}
# Defines a reusable setup function for tests; helps initialize data or state before each test runs
@pytest.fixture
def user(db) -> User:
   return User.objects.create_user(**data_user)
