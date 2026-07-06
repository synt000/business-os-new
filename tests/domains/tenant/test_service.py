import pytest
from fastapi import HTTPException
from domains.tenant.service import TenantService
from domains.tenant.schema import TenantCreate
from unittest.mock import MagicMock

def test_create_tenant_success():
    repo = MagicMock()
    repo.get_by_slug.return_value = None
    repo.get_by_name.return_value = None
    repo.create.return_value = {"id": "uuid", "name": "Test Company", "slug": "test-company"}
    
    service = TenantService(repo)
    data = TenantCreate(name="Test Company", slug="test-company")
    result = service.create_tenant(data)
    
    assert result["name"] == "Test Company"
    repo.create.assert_called_once()
