import pytest
from core.user.models import User
from core.post.models import Post

# Defines a reusable setup function for tests; helps initialize data or state before each test runs
@pytest.fixture
def post(db, user):
    return Post.objects.create(author=user, body="Test Post body")


#Even though db isn't directly used in the function body, it's required by pytest-django to ensure
# the database is set up and accessible during the fixture's execution. 
#Without db, you'd get an error like Database access not allowed, use the "django_db" mark or "db" fixture
