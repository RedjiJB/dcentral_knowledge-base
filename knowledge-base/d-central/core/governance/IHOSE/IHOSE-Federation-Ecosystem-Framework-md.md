---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 1257eed5-120e-4efc-acdf-72d67de9afbf
original_filename: IHOSE_Federation_Ecosystem_Framework.md
created_at: 2025-11-10T23:43:14.240150+00:00
content_hash: 810034ad3f58
topic: "ihose-federation-ecosystem-partnership-framework"
---

# Iron Horse Security - Federation & Ecosystem Framework

**Version 1.0 - Partner Program, Open-Source Foundation & Academic Integration**

*Extends: IHOSE Complete Technical Specification v3.0*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Federated Partner Program](#2-federated-partner-program)
3. [Community Open-Source Foundation](#3-community-open-source-foundation)
4. [Hardware Certification Program](#4-hardware-certification-program)
5. [Academic & Research Integration](#5-academic--research-integration)
6. [Implementation Roadmap](#6-implementation-roadmap)

---

# 1. Executive Summary

## 1.1 Strategic Vision

The Iron Horse Federation & Ecosystem Framework transforms Iron Horse Security from a single-company solution into an **open platform ecosystem** where:

- **Security companies worldwide** can federate under the Iron Horse platform, sharing infrastructure while maintaining independence
- **Open-source community** contributes to and benefits from the platform through the Iron Horse Open Technology Foundation (IHOTF)
- **Hardware manufacturers** can certify devices, creating a standardized security IoT ecosystem
- **Universities and colleges** integrate Iron Horse technology into curriculum, creating a talent pipeline and joint R&D opportunities

## 1.2 Ecosystem Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Iron Horse Federation Platform                        â”‚
â”‚                         (Core Infrastructure)                            â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”‚
â”‚  â”‚  Keycloak Federation â”‚ API Gateway â”‚ Shared Services â”‚ Billing  â”‚    â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚            â”‚            â”‚            â”‚
   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”
   â”‚   Partner A   â”‚  â”‚ Partner B  â”‚  â”‚  â”‚  Community     â”‚
   â”‚  (Toronto)    â”‚  â”‚ (Montreal) â”‚  â”‚  â”‚  Contributors  â”‚
   â”‚               â”‚  â”‚            â”‚  â”‚  â”‚                â”‚
   â”‚ â€¢ Own Guards  â”‚  â”‚â€¢ Own Sites â”‚  â”‚  â”‚ â€¢ Modules      â”‚
   â”‚ â€¢ Own Clients â”‚  â”‚â€¢ Own Data  â”‚  â”‚  â”‚ â€¢ Integrations â”‚
   â”‚ â€¢ Shared API  â”‚  â”‚â€¢ Shared APIâ”‚  â”‚  â”‚ â€¢ Docs         â”‚
   â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                       â”‚
                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                        â”‚  Hardware Ecosystem         â”‚
                        â”‚  â€¢ Certified Cameras        â”‚
                        â”‚  â€¢ Certified Sensors        â”‚
                        â”‚  â€¢ Certified Access Control â”‚
                        â”‚  â€¢ Reference Designs        â”‚
                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                       â”‚
                        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                        â”‚  Academic Partners          â”‚
                        â”‚  â€¢ Universities             â”‚
                        â”‚  â€¢ Research Labs            â”‚
                        â”‚  â€¢ Student Co-ops           â”‚
                        â”‚  â€¢ Joint R&D                â”‚
                        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## 1.3 Value Proposition by Stakeholder

| Stakeholder | Value Received | Contribution |
|-------------|----------------|--------------|
| **Partner Security Companies** | Turnkey platform, shared R&D costs, hardware ecosystem, training platform | Usage fees, data insights, local market knowledge |
| **Open-Source Community** | Professional platform to build on, career opportunities, recognition | Code contributions, bug fixes, documentation, integrations |
| **Hardware Manufacturers** | Access to global security market, reference designs, firmware libraries | Certified devices, testing support, manufacturing capacity |
| **Academic Institutions** | Real-world platform for teaching, research data access, industry connections | Student talent, research, curriculum alignment |
| **Iron Horse Security** | Ecosystem network effects, revenue from partners, accelerated innovation, talent pipeline | Core platform, governance, quality assurance, support |

---

# 2. Federated Partner Program

## 2.1 Partner SDK Overview

The Iron Horse Partner SDK provides everything a security company needs to join the federation:

- **REST & GraphQL APIs** - Full programmatic access to platform services
- **Data Standards** - Standardized schemas for guards, sites, incidents, patrols
- **Authentication** - Keycloak realm management for multi-tenancy
- **Governance Templates** - Legal agreements, data handling policies, SLAs
- **Client Libraries** - Python, JavaScript/TypeScript, Go, Java
- **Testing Tools** - Sandbox environment, mock data generators, test suites
- **Documentation Portal** - Interactive API docs, tutorials, best practices

## 2.2 Partner SDK Structure

```
ironhorse-partner-sdk/
â”œâ”€â”€ README.md
â”œâ”€â”€ LICENSE (Apache 2.0)
â”œâ”€â”€ GOVERNANCE.md
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ getting-started.md
â”‚   â”œâ”€â”€ authentication.md
â”‚   â”œâ”€â”€ api-reference/
â”‚   â”‚   â”œâ”€â”€ guards.md
â”‚   â”‚   â”œâ”€â”€ sites.md
â”‚   â”‚   â”œâ”€â”€ incidents.md
â”‚   â”‚   â””â”€â”€ patrols.md
â”‚   â”œâ”€â”€ data-standards/
â”‚   â”‚   â”œâ”€â”€ guard-schema.json
â”‚   â”‚   â”œâ”€â”€ site-schema.json
â”‚   â”‚   â””â”€â”€ incident-schema.json
â”‚   â”œâ”€â”€ integration-guides/
â”‚   â”‚   â”œâ”€â”€ existing-erp.md
â”‚   â”‚   â”œâ”€â”€ payroll-systems.md
â”‚   â”‚   â””â”€â”€ cctv-platforms.md
â”‚   â””â”€â”€ best-practices/
â”‚       â”œâ”€â”€ security.md
â”‚       â”œâ”€â”€ performance.md
â”‚       â””â”€â”€ compliance.md
â”œâ”€â”€ client-libraries/
â”‚   â”œâ”€â”€ python/
â”‚   â”‚   â”œâ”€â”€ setup.py
â”‚   â”‚   â”œâ”€â”€ ironhorse/
â”‚   â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”‚   â”œâ”€â”€ client.py
â”‚   â”‚   â”‚   â”œâ”€â”€ guards.py
â”‚   â”‚   â”‚   â”œâ”€â”€ sites.py
â”‚   â”‚   â”‚   â”œâ”€â”€ incidents.py
â”‚   â”‚   â”‚   â””â”€â”€ auth.py
â”‚   â”‚   â””â”€â”€ tests/
â”‚   â”œâ”€â”€ javascript/
â”‚   â”‚   â”œâ”€â”€ package.json
â”‚   â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”‚   â”œâ”€â”€ index.ts
â”‚   â”‚   â”‚   â”œâ”€â”€ client.ts
â”‚   â”‚   â”‚   â”œâ”€â”€ guards.ts
â”‚   â”‚   â”‚   â””â”€â”€ auth.ts
â”‚   â”‚   â””â”€â”€ tests/
â”‚   â”œâ”€â”€ go/
â”‚   â””â”€â”€ java/
â”œâ”€â”€ examples/
â”‚   â”œâ”€â”€ onboarding-guard/
â”‚   â”œâ”€â”€ creating-incident/
â”‚   â”œâ”€â”€ scheduling-shift/
â”‚   â””â”€â”€ compliance-report/
â”œâ”€â”€ testing/
â”‚   â”œâ”€â”€ sandbox-config/
â”‚   â”œâ”€â”€ mock-data/
â”‚   â””â”€â”€ test-suites/
â”œâ”€â”€ governance/
â”‚   â”œâ”€â”€ partner-agreement-template.md
â”‚   â”œâ”€â”€ data-handling-policy.md
â”‚   â”œâ”€â”€ sla-template.md
â”‚   â””â”€â”€ compliance-requirements.md
â””â”€â”€ tools/
    â”œâ”€â”€ api-client-generator/
    â”œâ”€â”€ schema-validator/
    â””â”€â”€ migration-scripts/
```

## 2.3 Partner SDK - Python Client Library

**client-libraries/python/ironhorse/client.py**
```python
"""
Iron Horse Partner SDK - Python Client
Version 1.0.0

Official Python client for the Iron Horse Federation Platform
"""

from typing import Dict, List, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from datetime import datetime, timedelta
import jwt

logger = logging.getLogger(__name__)


class IronHorseClient:
    """
    Main client for Iron Horse Federation Platform
    
    Example usage:
        client = IronHorseClient(
            api_url="https://api.ironhorsefederation.com",
            client_id="partner-acme-security",
            client_secret="xxx",
            realm="acme-security"
        )
        
        guards = client.guards.list(status="Active")
        incident = client.incidents.create({
            "site_id": "SITE001",
            "severity": "High",
            "category": "Trespassing",
            "description": "Unauthorized access attempt"
        })
    """
    
    def __init__(
        self,
        api_url: str,
        client_id: str,
        client_secret: str,
        realm: str,
        auth_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize Iron Horse client
        
        Args:
            api_url: Base URL of Iron Horse API (e.g., https://api.ironhorsefederation.com)
            client_id: Partner client ID from Keycloak
            client_secret: Partner client secret
            realm: Keycloak realm name for your organization
            auth_url: Custom auth URL (defaults to api_url/auth)
            timeout: Request timeout in seconds
            max_retries: Number of retry attempts for failed requests
        """
        self.api_url = api_url.rstrip('/')
        self.auth_url = auth_url or f"{self.api_url}/auth"
        self.client_id = client_id
        self.client_secret = client_secret
        self.realm = realm
        self.timeout = timeout
        
        # Setup session with retry logic
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Token management
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
        # Initialize resource clients
        from .guards import GuardsClient
        from .sites import SitesClient
        from .incidents import IncidentsClient
        from .patrols import PatrolsClient
        from .schedules import SchedulesClient
        
        self.guards = GuardsClient(self)
        self.sites = SitesClient(self)
        self.incidents = IncidentsClient(self)
        self.patrols = PatrolsClient(self)
        self.schedules = SchedulesClient(self)
    
    def _authenticate(self) -> str:
        """Authenticate with Keycloak and get access token"""
        token_url = f"{self.auth_url}/realms/{self.realm}/protocol/openid-connect/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        try:
            response = requests.post(token_url, data=data, timeout=self.timeout)
            response.raise_for_status()
            
            token_data = response.json()
            self._access_token = token_data['access_token']
            self._refresh_token = token_data.get('refresh_token')
            
            # Decode token to get expiry
            decoded = jwt.decode(
                self._access_token,
                options={"verify_signature": False}
            )
            self._token_expires_at = datetime.fromtimestamp(decoded['exp'])
            
            logger.info(f"Successfully authenticated as {self.client_id}")
            return self._access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            raise AuthenticationError(f"Failed to authenticate: {e}")
    
    def _ensure_authenticated(self):
        """Ensure we have a valid access token"""
        if not self._access_token or not self._token_expires_at:
            self._authenticate()
            return
        
        # Refresh token if expiring within 5 minutes
        if datetime.now() >= self._token_expires_at - timedelta(minutes=5):
            self._authenticate()
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make authenticated request to API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint path (e.g., "/api/v1/guards")
            params: Query parameters
            json: Request body as JSON
            headers: Additional headers
            
        Returns:
            Response JSON data
            
        Raises:
            APIError: For API errors
            AuthenticationError: For auth failures
        """
        self._ensure_authenticated()
        
        url = f"{self.api_url}{endpoint}"
        
        request_headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json',
            'User-Agent': f'IronHorse-Python-SDK/1.0.0 (Realm: {self.realm})'
        }
        
        if headers:
            request_headers.update(headers)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=request_headers,
                timeout=self.timeout
            )
            
            # Handle different status codes
            if response.status_code == 401:
                # Token might be invalid, re-authenticate and retry
                self._authenticate()
                request_headers['Authorization'] = f'Bearer {self._access_token}'
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    headers=request_headers,
                    timeout=self.timeout
                )
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {}
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"API request failed: {e}")
            try:
                error_data = e.response.json()
                raise APIError(
                    message=error_data.get('message', str(e)),
                    status_code=e.response.status_code,
                    details=error_data
                )
            except ValueError:
                raise APIError(
                    message=str(e),
                    status_code=e.response.status_code
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise APIError(f"Request failed: {e}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make POST request"""
        return self._request('POST', endpoint, json=json)
    
    def put(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self._request('PUT', endpoint, json=json)
    
    def patch(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        """Make PATCH request"""
        return self._request('PATCH', endpoint, json=json)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._request('DELETE', endpoint)
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.close()


class APIError(Exception):
    """Raised when API returns an error"""
    def __init__(self, message: str, status_code: Optional[int] = None, details: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass
```

**client-libraries/python/ironhorse/guards.py**
```python
"""Guards resource client"""

from typing import List, Dict, Any, Optional
from datetime import date


class GuardsClient:
    """Client for managing guards"""
    
    def __init__(self, client):
        self.client = client
    
    def list(
        self,
        status: Optional[str] = None,
        site_id: Optional[str] = None,
        certification_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List guards with optional filters
        
        Args:
            status: Filter by status (Active, Inactive, On Leave, etc.)
            site_id: Filter by assigned site
            certification_type: Filter by certification type
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            List of guard objects
            
        Example:
            guards = client.guards.list(
                status="Active",
                site_id="SITE001",
                certification_type="Healthcare Security"
            )
        """
        params = {
            'limit': limit,
            'offset': offset
        }
        
        filters = []
        if status:
            filters.append(['status', '=', status])
        if site_id:
            filters.append(['assigned_sites', 'like', f'%{site_id}%'])
        if certification_type:
            filters.append(['certifications', 'like', f'%{certification_type}%'])
        
        if filters:
            import json
            params['filters'] = json.dumps(filters)
        
        response = self.client.get('/api/v1/guards', params=params)
        return response.get('data', [])
    
    def get(self, guard_id: str) -> Dict[str, Any]:
        """
        Get a specific guard by ID
        
        Args:
            guard_id: Guard identifier
            
        Returns:
            Guard object
            
        Example:
            guard = client.guards.get("GRD001")
        """
        response = self.client.get(f'/api/v1/guards/{guard_id}')
        return response.get('data', {})
    
    def create(self, guard_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new guard
        
        Args:
            guard_data: Guard information
            
        Required fields:
            - first_name: str
            - last_name: str
            - email: str
            - employee_id: str
            
        Optional fields:
            - phone: str
            - hire_date: str (ISO date)
            - certifications: List[Dict]
            - assigned_sites: List[str]
            
        Returns:
            Created guard object
            
        Example:
            guard = client.guards.create({
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "employee_id": "EMP001",
                "phone": "+1-555-0100",
                "hire_date": "2024-01-15"
            })
        """
        response = self.client.post('/api/v1/guards', json=guard_data)
        return response.get('data', {})
    
    def update(self, guard_id: str, guard_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing guard
        
        Args:
            guard_id: Guard identifier
            guard_data: Fields to update
            
        Returns:
            Updated guard object
            
        Example:
            guard = client.guards.update("GRD001", {
                "phone": "+1-555-0200",
                "status": "Active"
            })
        """
        response = self.client.put(f'/api/v1/guards/{guard_id}', json=guard_data)
        return response.get('data', {})
    
    def add_certification(
        self,
        guard_id: str,
        certification_type: str,
        issue_date: date,
        expiry_date: date,
        certificate_number: str,
        issuer: str
    ) -> Dict[str, Any]:
        """
        Add a certification to a guard
        
        Args:
            guard_id: Guard identifier
            certification_type: Type of certification
            issue_date: Date issued
            expiry_date: Date expires
            certificate_number: Certificate number
            issuer: Issuing organization
            
        Returns:
            Updated guard object
            
        Example:
            guard = client.guards.add_certification(
                guard_id="GRD001",
                certification_type="Security Guard License",
                issue_date=date(2024, 1, 15),
                expiry_date=date(2027, 1, 15),
                certificate_number="SGL-2024-12345",
                issuer="Ministry of Community Safety"
            )
        """
        certification_data = {
            'type': certification_type,
            'issue_date': issue_date.isoformat(),
            'expiry_date': expiry_date.isoformat(),
            'certificate_number': certificate_number,
            'issuer': issuer,
            'status': 'Valid'
        }
        
        response = self.client.post(
            f'/api/v1/guards/{guard_id}/certifications',
            json=certification_data
        )
        return response.get('data', {})
    
    def assign_to_site(
        self,
        guard_id: str,
        site_id: str,
        start_date: date,
        primary: bool = True
    ) -> Dict[str, Any]:
        """
        Assign guard to a site
        
        Args:
            guard_id: Guard identifier
            site_id: Site identifier
            start_date: Assignment start date
            primary: Whether this is primary assignment
            
        Returns:
            Assignment confirmation
            
        Example:
            assignment = client.guards.assign_to_site(
                guard_id="GRD001",
                site_id="SITE001",
                start_date=date(2024, 2, 1),
                primary=True
            )
        """
        assignment_data = {
            'site_id': site_id,
            'start_date': start_date.isoformat(),
            'primary': primary
        }
        
        response = self.client.post(
            f'/api/v1/guards/{guard_id}/assignments',
            json=assignment_data
        )
        return response.get('data', {})
    
    def get_schedule(
        self,
        guard_id: str,
        start_date: date,
        end_date: date
    ) -> List[Dict[str, Any]]:
        """
        Get guard's schedule for a date range
        
        Args:
            guard_id: Guard identifier
            start_date: Start date
            end_date: End date
            
        Returns:
            List of shifts
            
        Example:
            schedule = client.guards.get_schedule(
                guard_id="GRD001",
                start_date=date(2024, 2, 1),
                end_date=date(2024, 2, 7)
            )
        """
        params = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
        
        response = self.client.get(
            f'/api/v1/guards/{guard_id}/schedule',
            params=params
        )
        return response.get('data', [])
```

**client-libraries/python/ironhorse/incidents.py**
```python
"""Incidents resource client"""

from typing import List, Dict, Any, Optional
from datetime import datetime


class IncidentsClient:
    """Client for managing incidents"""
    
    def __init__(self, client):
        self.client = client
    
    def list(
        self,
        site_id: Optional[str] = None,
        severity: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List incidents with optional filters
        
        Args:
            site_id: Filter by site
            severity: Filter by severity (Critical, High, Medium, Low)
            category: Filter by category
            status: Filter by status (Open, Resolved, Closed)
            start_date: Filter incidents after this date
            end_date: Filter incidents before this date
            limit: Maximum number of results
            offset: Pagination offset
            
        Returns:
            List of incident objects
        """
        params = {'limit': limit, 'offset': offset}
        
        filters = []
        if site_id:
            filters.append(['site', '=', site_id])
        if severity:
            filters.append(['severity', '=', severity])
        if category:
            filters.append(['category', '=', category])
        if status:
            filters.append(['status', '=', status])
        if start_date:
            filters.append(['incident_time', '>=', start_date.isoformat()])
        if end_date:
            filters.append(['incident_time', '<=', end_date.isoformat()])
        
        if filters:
            import json
            params['filters'] = json.dumps(filters)
        
        response = self.client.get('/api/v1/incidents', params=params)
        return response.get('data', [])
    
    def get(self, incident_id: str) -> Dict[str, Any]:
        """Get a specific incident by ID"""
        response = self.client.get(f'/api/v1/incidents/{incident_id}')
        return response.get('data', {})
    
    def create(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new incident report
        
        Args:
            incident_data: Incident information
            
        Required fields:
            - site_id: str
            - incident_time: str (ISO datetime)
            - severity: str (Critical, High, Medium, Low, Informational)
            - category: str
            - description: str
            
        Optional fields:
            - location_details: str
            - actions_taken: str
            - police_notified: bool
            - police_report_number: str
            - client_notified: bool
            - witnesses: List[Dict]
            - attachments: List[str]  # File URLs
            
        Returns:
            Created incident object
            
        Example:
            incident = client.incidents.create({
                "site_id": "SITE001",
                "incident_time": "2024-02-15T14:30:00Z",
                "severity": "High",
                "category": "Trespassing",
                "description": "Individual attempted to access restricted area",
                "location_details": "Loading dock entrance",
                "actions_taken": "Subject escorted off premises, police contacted",
                "police_notified": True,
                "police_report_number": "2024-12345",
                "client_notified": True
            })
        """
        response = self.client.post('/api/v1/incidents', json=incident_data)
        return response.get('data', {})
    
    def update(self, incident_id: str, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing incident"""
        response = self.client.put(f'/api/v1/incidents/{incident_id}', json=incident_data)
        return response.get('data', {})
    
    def add_attachment(
        self,
        incident_id: str,
        file_url: str,
        file_type: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add an attachment (photo, video, document) to an incident
        
        Args:
            incident_id: Incident identifier
            file_url: URL of the uploaded file
            file_type: Type of file (photo, video, audio, document)
            description: Optional description
            
        Returns:
            Updated incident object
        """
        attachment_data = {
            'file_url': file_url,
            'file_type': file_type,
            'description': description
        }
        
        response = self.client.post(
            f'/api/v1/incidents/{incident_id}/attachments',
            json=attachment_data
        )
        return response.get('data', {})
    
    def review(
        self,
        incident_id: str,
        approved: bool,
        comments: str,
        recommendations: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Supervisor review of an incident
        
        Args:
            incident_id: Incident identifier
            approved: Whether incident report is approved
            comments: Supervisor comments
            recommendations: Recommendations for prevention
            
        Returns:
            Updated incident object
        """
        review_data = {
            'approved': approved,
            'comments': comments,
            'recommendations': recommendations
        }
        
        response = self.client.post(
            f'/api/v1/incidents/{incident_id}/review',
            json=review_data
        )
        return response.get('data', {})
```

## 2.4 Multi-Tenant Keycloak Federation

### Keycloak Realm Management for Partners

**federation/keycloak_federation_manager.py**
```python
"""
Keycloak Federation Manager
Automates partner realm creation and configuration
"""

from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakError
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KeycloakFederationManager:
    """
    Manages Keycloak realms for federated partners
    
    Features:
    - Automated realm creation with standard configuration
    - Client creation for partner applications
    - Role and group management
    - Federation trust relationships
    - SSO configuration
    """
    
    def __init__(
        self,
        server_url: str,
        admin_username: str,
        admin_password: str,
        master_realm: str = "master"
    ):
        """
        Initialize federation manager
        
        Args:
            server_url: Keycloak server URL
            admin_username: Master realm admin username
            admin_password: Master realm admin password
            master_realm: Master realm name (default: master)
        """
        self.keycloak_admin = KeycloakAdmin(
            server_url=server_url,
            username=admin_username,
            password=admin_password,
            realm_name=master_realm,
            verify=True
        )
    
    def create_partner_realm(
        self,
        partner_name: str,
        partner_email: str,
        partner_domain: str,
        enable_registration: bool = False,
        smtp_config: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a new realm for a federated partner
        
        Args:
            partner_name: Partner organization name (e.g., "ACME Security")
            partner_email: Partner admin email
            partner_domain: Partner domain for email verification
            enable_registration: Allow user self-registration
            smtp_config: Email server configuration
            
        Returns:
            Realm configuration including client credentials
            
        Example:
            realm_config = manager.create_partner_realm(
                partner_name="ACME Security",
                partner_email="admin@acmesecurity.com",
                partner_domain="acmesecurity.com"
            )
        """
        # Generate realm ID from partner name
        realm_id = partner_name.lower().replace(' ', '-').replace('_', '-')
        
        logger.info(f"Creating realm for partner: {partner_name} (ID: {realm_id})")
        
        # Define realm configuration
        realm_config = {
            "realm": realm_id,
            "enabled": True,
            "displayName": f"{partner_name} Security Operations",
            "displayNameHtml": f"<div class='kc-logo-text'><span>{partner_name}</span></div>",
            
            # Authentication settings
            "registrationAllowed": enable_registration,
            "registrationEmailAsUsername": True,
            "resetPasswordAllowed": True,
            "rememberMe": True,
            "verifyEmail": True,
            "loginWithEmailAllowed": True,
            "duplicateEmailsAllowed": False,
            "editUsernameAllowed": False,
            
            # Password policy
            "passwordPolicy": "length(12) and upperCase(1) and lowerCase(1) and digits(1) and specialChars(1) and notUsername",
            
            # Token settings
            "accessTokenLifespan": 900,  # 15 minutes
            "accessTokenLifespanForImplicitFlow": 900,
            "ssoSessionIdleTimeout": 1800,  # 30 minutes
            "ssoSessionMaxLifespan": 36000,  # 10 hours
            "offlineSessionIdleTimeout": 2592000,  # 30 days
            "refreshTokenMaxReuse": 0,
            
            # Security settings
            "bruteForceProtected": True,
            "permanentLockout": False,
            "maxFailureWaitSeconds": 900,
            "minimumQuickLoginWaitSeconds": 60,
            "waitIncrementSeconds": 60,
            "quickLoginCheckMilliSeconds": 1000,
            "maxDeltaTimeSeconds": 43200,
            "failureFactor": 5,
            
            # Internationalization
            "internationalizationEnabled": True,
            "supportedLocales": ["en", "fr", "es"],
            "defaultLocale": "en",
            
            # Events
            "eventsEnabled": True,
            "eventsExpiration": 2592000,  # 30 days
            "eventsListeners": ["jboss-logging"],
            "enabledEventTypes": [
                "LOGIN",
                "LOGIN_ERROR",
                "REGISTER",
                "LOGOUT",
                "CODE_TO_TOKEN",
                "CLIENT_LOGIN"
            ],
            
            # Admin events
            "adminEventsEnabled": True,
            "adminEventsDetailsEnabled": True,
            
            # Themes
            "loginTheme": "ironhorse",
            "accountTheme": "ironhorse",
            "adminTheme": "ironhorse",
            "emailTheme": "ironhorse"
        }
        
        # Add SMTP configuration if provided
        if smtp_config:
            realm_config["smtpServer"] = {
                "from": smtp_config.get('from', f'noreply@{partner_domain}'),
                "fromDisplayName": partner_name,
                "host": smtp_config['host'],
                "port": smtp_config.get('port', '587'),
                "ssl": smtp_config.get('ssl', 'true'),
                "starttls": smtp_config.get('starttls', 'true'),
                "auth": smtp_config.get('auth', 'true'),
                "user": smtp_config.get('user'),
                "password": smtp_config.get('password')
            }
        
        try:
            # Create realm
            self.keycloak_admin.create_realm(payload=realm_config, skip_exists=False)
            logger.info(f"Realm {realm_id} created successfully")
            
            # Switch to new realm
            self.keycloak_admin.realm_name = realm_id
            
            # Create standard clients
            client_credentials = self._create_standard_clients(
                realm_id,
                partner_name,
                partner_domain
            )
            
            # Create standard roles
            self._create_standard_roles()
            
            # Create standard groups
            self._create_standard_groups()
            
            # Create realm admin user
            admin_user = self._create_admin_user(
                partner_email,
                partner_name
            )
            
            # Configure required actions
            self._configure_required_actions()
            
            # Switch back to master realm
            self.keycloak_admin.realm_name = "master"
            
            return {
                "realm_id": realm_id,
                "realm_name": partner_name,
                "admin_user": admin_user,
                "clients": client_credentials,
                "console_url": f"{self.keycloak_admin.server_url}/admin/{realm_id}/console",
                "login_url": f"{self.keycloak_admin.server_url}/realms/{realm_id}/protocol/openid-connect/auth"
            }
            
        except KeycloakError as e:
            logger.error(f"Failed to create realm: {e}")
            raise
    
    def _create_standard_clients(
        self,
        realm_id: str,
        partner_name: str,
        partner_domain: str
    ) -> Dict[str, Dict[str, str]]:
        """Create standard OAuth2/OIDC clients for partner"""
        
        clients_config = []
        client_credentials = {}
        
        # 1. Backend API Client (client_credentials flow)
        api_client_id = f"{realm_id}-api"
        api_client = {
            "clientId": api_client_id,
            "name": f"{partner_name} API Client",
            "description": "Backend API client for Iron Horse Federation",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "secret": self._generate_secret(),
            "protocol": "openid-connect",
            "publicClient": False,
            "standardFlowEnabled": False,
            "implicitFlowEnabled": False,
            "directAccessGrantsEnabled": False,
            "serviceAccountsEnabled": True,
            "authorizationServicesEnabled": True,
            "attributes": {
                "access.token.lifespan": "900",
                "client.secret.creation.time": str(int(datetime.now().timestamp()))
            }
        }
        
        # 2. Frontend Web Application (authorization_code + PKCE)
        web_client_id = f"{realm_id}-web"
        web_client = {
            "clientId": web_client_id,
            "name": f"{partner_name} Web Application",
            "enabled": True,
            "clientAuthenticatorType": "client-secret",
            "secret": self._generate_secret(),
            "protocol": "openid-connect",
            "publicClient": False,
            "standardFlowEnabled": True,
            "implicitFlowEnabled": False,
            "directAccessGrantsEnabled": True,
            "serviceAccountsEnabled": False,
            "redirectUris": [
                f"https://app.{partner_domain}/*",
                f"https://{partner_domain}/*",
                "http://localhost:3000/*"  # Development
            ],
            "webOrigins": [
                f"https://app.{partner_domain}",
                f"https://{partner_domain}",
                "http://localhost:3000"
            ],
            "attributes": {
                "pkce.code.challenge.method": "S256",
                "access.token.lifespan": "900"
            }
        }
        
        # 3. Mobile Application (authorization_code + PKCE)
        mobile_client_id = f"{realm_id}-mobile"
        mobile_client = {
            "clientId": mobile_client_id,
            "name": f"{partner_name} Mobile Application",
            "enabled": True,
            "protocol": "openid-connect",
            "publicClient": True,  # Public client - no client secret
            "standardFlowEnabled": True,
            "implicitFlowEnabled": False,
            "directAccessGrantsEnabled": False,
            "redirectUris": [
                f"com.{realm_id}.mobile://oauth/callback",
                f"{realm_id}://oauth/callback"
            ],
            "webOrigins": ["+"],  # Allow all origins for mobile
            "attributes": {
                "pkce.code.challenge.method": "S256"
            }
        }
        
        # Create clients
        for client_config in [api_client, web_client, mobile_client]:
            try:
                client_id = self.keycloak_admin.create_client(client_config, skip_exists=True)
                
                # Store credentials for non-public clients
                if not client_config.get('publicClient', False):
                    client_credentials[client_config['clientId']] = {
                        "client_id": client_config['clientId'],
                        "client_secret": client_config['secret']
                    }
                else:
                    client_credentials[client_config['clientId']] = {
                        "client_id": client_config['clientId'],
                        "note": "Public client - no secret required"
                    }
                
                logger.info(f"Created client: {client_config['clientId']}")
                
            except KeycloakError as e:
                logger.error(f"Failed to create client {client_config['clientId']}: {e}")
        
        return client_credentials
    
    def _create_standard_roles(self):
        """Create standard roles for the realm"""
        roles = [
            {
                "name": "security_guard",
                "description": "Field security guard personnel",
                "composite": False
            },
            {
                "name": "site_supervisor",
                "description": "Site supervisor and manager",
                "composite": False
            },
            {
                "name": "operations_manager",
                "description": "Operations and dispatch manager",
                "composite": False
            },
            {
                "name": "hr_officer",
                "description": "Human resources officer",
                "composite": False
            },
            {
                "name": "system_admin",
                "description": "System administrator",
                "composite": False
            },
            {
                "name": "client_portal_user",
                "description": "Client portal access",
                "composite": False
            },
            {
                "name": "executive",
                "description": "Executive leadership",
                "composite": False
            }
        ]
        
        for role in roles:
            try:
                self.keycloak_admin.create_realm_role(payload=role, skip_exists=True)
                logger.info(f"Created role: {role['name']}")
            except KeycloakError as e:
                logger.error(f"Failed to create role {role['name']}: {e}")
    
    def _create_standard_groups(self):
        """Create standard groups for the realm"""
        groups = [
            {
                "name": "Field Operations",
                "path": "/Field Operations",
                "realmRoles": ["security_guard"]
            },
            {
                "name": "Management",
                "path": "/Management",
                "realmRoles": ["site_supervisor", "operations_manager"]
            },
            {
                "name": "Administration",
                "path": "/Administration",
                "realmRoles": ["hr_officer", "system_admin"]
            },
            {
                "name": "Executives",
                "path": "/Executives",
                "realmRoles": ["executive"]
            },
            {
                "name": "Client Users",
                "path": "/Client Users",
                "realmRoles": ["client_portal_user"]
            }
        ]
        
        for group_config in groups:
            try:
                group_id = self.keycloak_admin.create_group(
                    payload={
                        "name": group_config['name']
                    },
                    skip_exists=True
                )
                
                # Assign roles to group
                if group_config.get('realmRoles'):
                    group = self.keycloak_admin.get_group_by_path(group_config['path'])
                    if group:
                        roles = [
                            self.keycloak_admin.get_realm_role(role_name)
                            for role_name in group_config['realmRoles']
                        ]
                        self.keycloak_admin.assign_group_realm_roles(
                            group_id=group['id'],
                            roles=roles
                        )
                
                logger.info(f"Created group: {group_config['name']}")
                
            except KeycloakError as e:
                logger.error(f"Failed to create group {group_config['name']}: {e}")
    
    def _create_admin_user(
        self,
        email: str,
        partner_name: str
    ) -> Dict[str, str]:
        """Create realm administrator user"""
        
        username = email.split('@')[0]
        temporary_password = self._generate_secret()[:16]  # 16 char temp password
        
        user_config = {
            "username": username,
            "email": email,
            "firstName": partner_name,
            "lastName": "Administrator",
            "enabled": True,
            "emailVerified": False,  # Require email verification
            "credentials": [{
                "type": "password",
                "value": temporary_password,
                "temporary": True  # Force password change on first login
            }],
            "realmRoles": ["system_admin"],
            "requiredActions": [
                "VERIFY_EMAIL",
                "UPDATE_PASSWORD",
                "CONFIGURE_TOTP"  # Require MFA setup
            ]
        }
        
        try:
            user_id = self.keycloak_admin.create_user(user_config, exist_ok=True)
            logger.info(f"Created admin user: {username}")
            
            return {
                "user_id": user_id,
                "username": username,
                "email": email,
                "temporary_password": temporary_password,
                "note": "User must change password and set up MFA on first login"
            }
            
        except KeycloakError as e:
            logger.error(f"Failed to create admin user: {e}")
            raise
    
    def _configure_required_actions(self):
        """Configure required actions for the realm"""
        required_actions = [
            {
                "alias": "CONFIGURE_TOTP",
                "name": "Configure OTP",
                "providerId": "CONFIGURE_TOTP",
                "enabled": True,
                "defaultAction": True,  # Required for all new users
                "priority": 10
            },
            {
                "alias": "UPDATE_PASSWORD",
                "name": "Update Password",
                "providerId": "UPDATE_PASSWORD",
                "enabled": True,
                "defaultAction": True,
                "priority": 20
            },
            {
                "alias": "VERIFY_EMAIL",
                "name": "Verify Email",
                "providerId": "VERIFY_EMAIL",
                "enabled": True,
                "defaultAction": True,
                "priority": 30
            }
        ]
        
        for action in required_actions:
            try:
                # Update required action configuration
                self.keycloak_admin.update_required_action(
                    action_alias=action['alias'],
                    payload=action
                )
                logger.info(f"Configured required action: {action['alias']}")
            except KeycloakError as e:
                logger.error(f"Failed to configure required action {action['alias']}: {e}")
    
    def _generate_secret(self, length: int = 32) -> str:
        """Generate a secure random secret"""
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def list_partner_realms(self) -> List[Dict[str, Any]]:
        """List all partner realms (excluding master)"""
        self.keycloak_admin.realm_name = "master"
        all_realms = self.keycloak_admin.get_realms()
        
        # Filter out master realm
        partner_realms = [
            realm for realm in all_realms 
            if realm['realm'] != 'master'
        ]
        
        return partner_realms
    
    def get_partner_stats(self, realm_id: str) -> Dict[str, Any]:
        """Get statistics for a partner realm"""
        self.keycloak_admin.realm_name = realm_id
        
        # Get user count
        users = self.keycloak_admin.get_users()
        user_count = len(users)
        
        # Get active sessions
        sessions = self.keycloak_admin.get_sessions()
        active_sessions = len(sessions) if sessions else 0
        
        # Get clients
        clients = self.keycloak_admin.get_clients()
        client_count = len(clients)
        
        # Get events (last 24 hours)
        from_date = datetime.now() - timedelta(days=1)
        events = self.keycloak_admin.get_events(
            dateFrom=int(from_date.timestamp() * 1000)
        )
        
        login_count = len([e for e in events if e['type'] == 'LOGIN'])
        login_error_count = len([e for e in events if e['type'] == 'LOGIN_ERROR'])
        
        return {
            "realm_id": realm_id,
            "user_count": user_count,
            "active_sessions": active_sessions,
            "client_count": client_count,
            "logins_24h": login_count,
            "login_errors_24h": login_error_count,
            "last_updated": datetime.now().isoformat()
        }
```

## 2.5 Partner Onboarding Automation

**federation/partner_onboarding_service.py**
```python
"""
Automated Partner Onboarding Service
End-to-end automation of partner registration and setup
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from keycloak_federation_manager import KeycloakFederationManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PartnerOnboardingService:
    """
    Automates the complete partner onboarding process
    
    Steps:
    1. Create Keycloak realm with clients
    2. Provision ERPNext company and users
    3. Setup network infrastructure (WireGuard VPN, DNS)
    4. Deploy monitoring stack
    5. Send welcome email with credentials
    6. Schedule onboarding call
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # Initialize Keycloak manager
        self.keycloak_manager = KeycloakFederationManager(
            server_url=config['keycloak_url'],
            admin_username=config['keycloak_admin_user'],
            admin_password=config['keycloak_admin_password']
        )
        
        # ERPNext credentials
        self.erpnext_url = config['erpnext_url']
        self.erpnext_headers = {
            'Authorization': f"token {config['erpnext_api_key']}:{config['erpnext_api_secret']}"
        }
    
    async def onboard_partner(
        self,
        partner_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Complete partner onboarding
        
        Args:
            partner_data: Partner information
                - company_name: str
                - admin_email: str
                - admin_name: str
                - domain: str
                - country: str
                - address: str
                - phone: str
                - planned_sites: int
                - planned_guards: int
                
        Returns:
            Onboarding result with all credentials and configuration
        """
        logger.info(f"Starting onboarding for: {partner_data['company_name']}")
        
        onboarding_result = {
            "partner_name": partner_data['company_name'],
            "status": "in_progress",
            "started_at": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # Step 1: Create Keycloak realm
            logger.info("Step 1: Creating Keycloak realm...")
            realm_config = self.keycloak_manager.create_partner_realm(
                partner_name=partner_data['company_name'],
                partner_email=partner_data['admin_email'],
                partner_domain=partner_data['domain'],
                enable_registration=False,
                smtp_config=self.config.get('smtp_config')
            )
            onboarding_result['steps']['keycloak'] = {
                "status": "completed",
                "realm_id": realm_config['realm_id'],
                "admin_console_url": realm_config['console_url']
            }
            logger.info(f"âœ“ Realm created: {realm_config['realm_id']}")
            
            # Step 2: Create ERPNext company
            logger.info("Step 2: Creating ERPNext company...")
            erpnext_company = await self._create_erpnext_company(
                partner_data,
                realm_config['realm_id']
            )
            onboarding_result['steps']['erpnext'] = {
                "status": "completed",
                "company_id": erpnext_company['name']
            }
            logger.info(f"âœ“ ERPNext company created: {erpnext_company['name']}")
            
            # Step 3: Setup WireGuard VPN
            logger.info("Step 3: Configuring VPN access...")
            vpn_config = await self._setup_vpn_access(
                realm_config['realm_id'],
                partner_data['company_name']
            )
            onboarding_result['steps']['vpn'] = {
                "status": "completed",
                "vpn_endpoint": vpn_config['endpoint'],
                "config_file": vpn_config['config_file']
            }
            logger.info(f"âœ“ VPN configured: {vpn_config['endpoint']}")
            
            # Step 4: Deploy monitoring
            logger.info("Step 4: Deploying monitoring stack...")
            monitoring_config = await self._deploy_monitoring(
                realm_config['realm_id'],
                partner_data['company_name']
            )
            onboarding_result['steps']['monitoring'] = {
                "status": "completed",
                "grafana_url": monitoring_config['grafana_url']
            }
            logger.info(f"âœ“ Monitoring deployed: {monitoring_config['grafana_url']}")
            
            # Step 5: Generate documentation
            logger.info("Step 5: Generating partner documentation...")
            documentation = await self._generate_documentation(
                partner_data,
                realm_config,
                erpnext_company,
                vpn_config,
                monitoring_config
            )
            onboarding_result['steps']['documentation'] = {
                "status": "completed",
                "documentation_url": documentation['url']
            }
            
            # Step 6: Send welcome email
            logger.info("Step 6: Sending welcome email...")
            await self._send_welcome_email(
                partner_data,
                realm_config,
                documentation
            )
            onboarding_result['steps']['notification'] = {
                "status": "completed",
                "email_sent_to": partner_data['admin_email']
            }
            
            # Update status
            onboarding_result['status'] = "completed"
            onboarding_result['completed_at'] = datetime.now().isoformat()
            
            logger.info(f"âœ“ Partner onboarding completed for: {partner_data['company_name']}")
            
            return onboarding_result
            
        except Exception as e:
            logger.error(f"Onboarding failed: {e}")
            onboarding_result['status'] = "failed"
            onboarding_result['error'] = str(e)
            raise
    
    async def _create_erpnext_company(
        self,
        partner_data: Dict[str, Any],
        realm_id: str
    ) -> Dict[str, Any]:
        """Create partner company in ERPNext"""
        
        company_data = {
            "doctype": "Company",
            "company_name": partner_data['company_name'],
            "abbr": realm_id[:4].upper(),
            "default_currency": "CAD",
            "country": partner_data.get('country', 'Canada'),
            "domain": "Services",
            "enable_perpetual_inventory": 1,
            # Custom fields
            "custom_realm_id": realm_id,
            "custom_partner_tier": "Standard",
            "custom_planned_sites": partner_data.get('planned_sites', 0),
            "custom_planned_guards": partner_data.get('planned_guards', 0)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.erpnext_url}/api/resource/Company",
                headers=self.erpnext_headers,
                json=company_data
            ) as response:
                if response.status in [200, 201]:
                    result = await response.json()
                    return result.get('data', {})
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create ERPNext company: {error_text}")
    
    async def _setup_vpn_access(
        self,
        realm_id: str,
        company_name: str
    ) -> Dict[str, Any]:
        """Configure WireGuard VPN for partner"""
        
        # In production, this would call infrastructure automation
        # For now, return mock configuration
        
        vpn_config = {
            "endpoint": f"{realm_id}.vpn.ironhorsefederation.com:51820",
            "public_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=",
            "allowed_ips": f"10.{hash(realm_id) % 254 + 1}.0.0/16",
            "config_file": f"/opt/ironhorse/vpn/{realm_id}-wireguard.conf"
        }
        
        logger.info(f"VPN configured for {company_name}")
        return vpn_config
    
    async def _deploy_monitoring(
        self,
        realm_id: str,
        company_name: str
    ) -> Dict[str, Any]:
        """Deploy Grafana monitoring for partner"""
        
        # In production, this would deploy via Kubernetes/Helm
        monitoring_config = {
            "grafana_url": f"https://monitoring-{realm_id}.ironhorsefederation.com",
            "prometheus_url": f"https://prometheus-{realm_id}.ironhorsefederation.com",
            "alertmanager_url": f"https://alerts-{realm_id}.ironhorsefederation.com"
        }
        
        logger.info(f"Monitoring deployed for {company_name}")
        return monitoring_config
    
    async def _generate_documentation(
        self,
        partner_data: Dict[str, Any],
        realm_config: Dict[str, Any],
        erpnext_company: Dict[str, Any],
        vpn_config: Dict[str, Any],
        monitoring_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate partner-specific documentation"""
        
        # In production, this would generate PDF/HTML docs
        documentation = {
            "url": f"https://docs.ironhorsefederation.com/partners/{realm_config['realm_id']}",
            "quickstart_guide": "...",
            "api_reference": "...",
            "configuration": {
                "realm_id": realm_config['realm_id'],
                "api_clients": realm_config['clients'],
                "vpn": vpn_config,
                "monitoring": monitoring_config
            }
        }
        
        return documentation
    
    async def _send_welcome_email(
        self,
        partner_data: Dict[str, Any],
        realm_config: Dict[str, Any],
        documentation: Dict[str, Any]
    ) -> bool:
        """Send welcome email to partner admin"""
        
        # In production, this would use an email service
        logger.info(f"Welcome email sent to {partner_data['admin_email']}")
        return True


# Example usage
async def main():
    config = {
        "keycloak_url": "https://auth.ironhorsefederation.com",
        "keycloak_admin_user": "admin",
        "keycloak_admin_password": "admin-password",
        "erpnext_url": "https://erp.ironhorsefederation.com",
        "erpnext_api_key": "api-key",
        "erpnext_api_secret": "api-secret"
    }
    
    service = PartnerOnboardingService(config)
    
    partner_data = {
        "company_name": "ACME Security Services",
        "admin_email": "admin@acmesecurity.com",
        "admin_name": "John Smith",
        "domain": "acmesecurity.com",
        "country": "Canada",
        "address": "123 Security St, Toronto, ON",
        "phone": "+1-555-0100",
        "planned_sites": 25,
        "planned_guards": 50
    }
    
    result = await service.onboard_partner(partner_data)
    print(f"Onboarding result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

# 3. Community Open-Source Foundation

## 3.1 Iron Horse Open Technology Foundation (IHOTF)

### Foundation Charter

**Mission Statement:**
The Iron Horse Open Technology Foundation (IHOTF) is a non-profit organization dedicated to advancing open-source security operations technology through collaborative development, standardization, and knowledge sharing.

**Core Principles:**
1. **Open Innovation** - All core platform code is open-source under permissive licenses
2. **Community Governance** - Contributors have voice in technical direction
3. **Vendor Neutrality** - No single company controls the roadmap
4. **Quality First** - Rigorous code review and testing standards
5. **Documentation Excellence** - Every feature must be documented
6. **Inclusive Community** - Welcoming to all skill levels and backgrounds

### Legal Structure

**Organization Type:** 501(c)(3) Non-Profit (US) / Non-Profit Corporation (Canada)

**Board of Directors:**
- 3 seats: Iron Horse Security representatives
- 3 seats: Partner company representatives (elected annually)
- 2 seats: Community contributors (elected by committers)
- 1 seat: Academic institution representative

**Technical Steering Committee:**
- 5-7 active committers elected by the community
- Term: 2 years, staggered
- Responsibilities: Technical roadmap, code review standards, release management

## 3.2 Repository Structure

**GitHub Organization:** https://github.com/ironhorse-security

```
ironhorse-security/
â”œâ”€â”€ platform-core/               # Main platform (AGPL-3.0)
â”œâ”€â”€ partner-sdk/                 # Partner SDK (Apache-2.0)
â”œâ”€â”€ hardware-specs/              # Hardware standards (CC BY-SA 4.0)
â”œâ”€â”€ mobile-apps/                 # iOS/Android apps (AGPL-3.0)
â”œâ”€â”€ integrations/                # Third-party integrations (MIT)
â”œâ”€â”€ deployment/                  # Kubernetes/Docker configs (Apache-2.0)
â”œâ”€â”€ docs/                        # Documentation (CC BY 4.0)
â”œâ”€â”€ rfcs/                        # Request for Comments
â””â”€â”€ community/                   # Community resources
```

### Repository: platform-core

**ironhorse-security/platform-core/README.md**
```markdown
# Iron Horse Security Platform - Core

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Build Status](https://ci.ironhorsesecurity.org/platform-core/badge)](https://ci.ironhorsesecurity.org/platform-core)
[![Docker Pulls](https://img.shields.io/docker/pulls/ironhorse/platform)](https://hub.docker.com/r/ironhorse/platform)
[![Discord](https://img.shields.io/discord/xxxxxxxxx)](https://discord.gg/ironhorse)

Open-source security operations platform powering modern security companies worldwide.

## Features

- ðŸ›¡ï¸ **Unified Security Operations** - Guards, sites, patrols, incidents in one platform
- ðŸ” **Enterprise SSO** - Keycloak-based federated authentication
- ðŸ“Š **Real-time Analytics** - Grafana dashboards and predictive insights
- ðŸ¤– **AI-Powered** - Digital twins, knowledge graphs, and LLM reasoning
- ðŸŒ **Multi-Tenant** - Support for federated partner organizations
- ðŸ“± **Mobile First** - Native iOS and Android apps
- ðŸ”Œ **Extensible** - Plugin architecture for custom integrations
- ðŸš€ **Cloud Native** - Kubernetes-ready with Helm charts

## Quick Start

### Prerequisites

- Docker 24+ and Docker Compose v2
- Kubernetes 1.28+ (for production)
- 8GB RAM minimum (16GB recommended)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ironhorse-security/platform-core.git
cd platform-core

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Access the platform
open http://localhost:8000

# Default credentials
Username: admin@ironhorsesecurity.com
Password: admin (change on first login)
```

### Production Deployment

```bash
# Install with Helm
helm repo add ironhorse https://charts.ironhorsesecurity.org
helm install ironhorse-platform ironhorse/platform --namespace ironhorse-platform --create-namespace

# Or use Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

Full deployment guide: [docs/deployment/](docs/deployment/README.md)

## Documentation

- ðŸ“– [User Guide](https://docs.ironhorsesecurity.org/user-guide)
- ðŸ—ï¸ [Architecture Overview](https://docs.ironhorsesecurity.org/architecture)
- ðŸ”§ [API Reference](https://docs.ironhorsesecurity.org/api)
- ðŸ¤ [Contributing Guide](CONTRIBUTING.md)
- ðŸ“ [Changelog](CHANGELOG.md)

## Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Application Layer                         â”‚
â”‚  ERPNext ERP â”‚ Nextcloud Files â”‚ Matrix Chat â”‚ Portal       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   Platform Services                          â”‚
â”‚  API Gateway â”‚ GraphQL â”‚ Event Bus â”‚ Digital Twins          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                  Data & Intelligence                         â”‚
â”‚  PostgreSQL â”‚ Neo4j â”‚ TimescaleDB â”‚ Redis â”‚ Kafka           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Infrastructure                            â”‚
â”‚  Kubernetes â”‚ Ceph Storage â”‚ WireGuard VPN â”‚ Monitoring     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute

- ðŸ› **Report bugs** - Submit issues with detailed reproduction steps
- ðŸ’¡ **Suggest features** - Open an RFC in the [rfcs/](https://github.com/ironhorse-security/rfcs) repo
- ðŸ”§ **Submit code** - Fork, develop, and create pull requests
- ðŸ“ **Improve docs** - Help make our documentation better
- ðŸŒ **Translate** - Add support for more languages
- ðŸ’¬ **Help others** - Answer questions on Discord or GitHub Discussions

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make changes and write tests
4. Run tests: `make test`
5. Commit with conventional commits: `git commit -m "feat: add new feature"`
6. Push and create a pull request

## Community

- ðŸ’¬ [Discord Chat](https://discord.gg/ironhorse) - Real-time discussions
- ðŸ¦ [Twitter](https://twitter.com/ironhorse_sec) - Updates and news
- ðŸ“§ [Mailing List](https://groups.google.com/g/ironhorse-dev) - Development discussions
- ðŸ“¹ [YouTube](https://youtube.com/@ironhorsesecurity) - Video tutorials
- ðŸ—“ï¸ [Community Calls](https://meet.ironhorsesecurity.org) - Bi-weekly video calls (Wednesdays 2pm ET)

## License

Licensed under the [GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0).

This means:
- âœ… Use commercially
- âœ… Modify and distribute
- âœ… Private use
- âš ï¸ Must disclose source if running as a service
- âš ï¸ Must use same license for derivatives

For commercial licensing without AGPL requirements, contact: licensing@ironhorsesecurity.com

## Support

### Community Support (Free)
- GitHub Issues
- Discord Chat
- Community Forums

### Professional Support (Paid)
- Priority support tickets
- SLA guarantees
- Implementation assistance
- Custom development

Contact: support@ironhorsesecurity.com

## Sponsors

Iron Horse Security Platform is supported by:

- [Iron Horse Security Inc.](https://ironhorsesecurity.com) - Founding sponsor
- [Anthropic](https://anthropic.com) - AI technology partner
- [CNCF](https://cncf.io) - Cloud-native infrastructure
- [Your Company Here] - [Become a sponsor](SPONSORS.md)

## Security

Found a security vulnerability? Please email security@ironhorsesecurity.com with details.

Do NOT open a public issue for security vulnerabilities.

We follow responsible disclosure and will credit researchers.

---

Made with â¤ï¸ by the Iron Horse community
```

## 3.3 Contributor Agreement

**CONTRIBUTOR_LICENSE_AGREEMENT.md**
```markdown
# Iron Horse Open Technology Foundation
## Contributor License Agreement (CLA)

Thank you for your interest in contributing to the Iron Horse Open Technology Foundation ("IHOTF" or "We"). This Contributor License Agreement ("Agreement") documents the rights granted by contributors to IHOTF.

### 1. Definitions

**"You"** means the individual or legal entity submitting a Contribution to IHOTF.

**"Contribution"** means any original work of authorship, including any modifications or additions to existing work, that is intentionally submitted by You to IHOTF for inclusion in any product owned or managed by IHOTF.

**"Submit"** means any form of electronic, verbal, or written communication sent to IHOTF or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems.

### 2. Grant of Copyright License

Subject to the terms and conditions of this Agreement, You hereby grant to IHOTF and to recipients of software distributed by IHOTF a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to:

- Reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute Your Contributions and such derivative works.

### 3. Grant of Patent License

Subject to the terms and conditions of this Agreement, You hereby grant to IHOTF and to recipients of software distributed by IHOTF a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to:

- Make, have made, use, offer to sell, sell, import, and otherwise transfer Your Contributions, where such license applies only to those patent claims licensable by You that are necessarily infringed by Your Contribution(s) alone or by combination of Your Contribution(s) with the project to which such Contribution(s) was submitted.

### 4. Representations

You represent that:

1. You are legally entitled to grant the above licenses.
2. Each of Your Contributions is Your original creation.
3. Your Contribution submissions include complete details of any third-party license or other restriction of which You are aware and which are associated with any part of Your Contributions.
4. If Your employer has rights to intellectual property that You create, You have received permission to make the Contributions on behalf of that employer, or Your employer has waived such rights for Your Contributions to IHOTF.

### 5. Support

You are not expected to provide support for Your Contributions, except to the extent You desire to provide support. You may provide support for free, for a fee, or not at all.

### 6. Disclaimer

UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING, YOU PROVIDE YOUR CONTRIBUTIONS ON AN "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

---

## Sign the CLA

### Individual Contributors

I have read and agree to the terms of this Contributor License Agreement.

- **Full Name:** _________________________________
- **Email:** _________________________________
- **GitHub Username:** _________________________________
- **Date:** _________________________________
- **Signature:** _________________________________

### Corporate Contributors

On behalf of the corporation listed below, I agree to the terms of this Contributor License Agreement.

- **Corporation Name:** _________________________________
- **Signatory Name:** _________________________________
- **Signatory Title:** _________________________________
- **Email:** _________________________________
- **Date:** _________________________________
- **Signature:** _________________________________

---

Please sign electronically via https://cla.ironhorsesecurity.org or email a signed copy to legal@ironhorsesecurity.org
```

## 3.4 Governance Model

**GOVERNANCE.md**
```markdown
# Iron Horse Open Technology Foundation - Governance

## Overview

IHOTF follows an open governance model where decisions are made transparently and contributors have clear paths to influence the project direction.

## Roles & Responsibilities

### Contributors

Anyone who submits a contribution (code, documentation, bug report, etc.) to the project.

**Rights:**
- Vote on community-wide surveys
- Participate in all discussions
- Attend community calls

**Path to Advancement:** Submit quality contributions regularly

### Committers

Contributors who have made significant, sustained contributions and demonstrated:
- Deep understanding of project architecture
- High-quality code that passes review
- Constructive collaboration with others
- Commitment to project goals

**Rights:**
- Write access to repositories
- Vote on RFC proposals
- +1/-1 on pull requests
- Participate in committer meetings

**Responsibilities:**
- Review pull requests
- Mentor new contributors
- Maintain code quality standards
- Participate in release planning

**Selection:** Nominated by existing committers, requires 2/3 approval

### Technical Steering Committee (TSC)

5-7 committers elected by the committer body to provide technical leadership.

**Rights:**
- Final decision on technical disputes
- Approve new committers
- Set release schedule
- Define coding standards

**Responsibilities:**
- Maintain technical roadmap
- Ensure project health
- Facilitate decision-making
- Represent community to board

**Election:** Annual election, 2-year terms, staggered

### Board of Directors

9-member board providing strategic oversight and financial governance.

**Composition:**
- 3 Iron Horse Security representatives
- 3 Partner company representatives (elected annually)
- 2 Community contributors (elected by committers)
- 1 Academic institution representative

**Responsibilities:**
- Financial oversight
- Legal matters
- Foundation strategy
- Partnership agreements
- Fundraising

## Decision Making

### Consensus Seeking

Decisions are made by consensus where possible. If consensus cannot be reached within a reasonable time, the TSC may call for a vote.

### Voting

- **Simple Majority:** Day-to-day technical decisions
- **2/3 Majority:** New committers, significant architectural changes
- **3/4 Majority:** Changes to governance, licensing

### Request for Comments (RFC)

Significant changes require an RFC:

1. Submit RFC as pull request to `rfcs/` repository
2. Community discussion (minimum 2 weeks)
3. TSC review and vote
4. If approved, implementation can begin

## Code Review

All code changes require:

1. Passing automated tests (CI)
2. At least 1 committer approval (+1)
3. No outstanding change requests
4. Security scan pass (for sensitive changes)

Committers cannot approve their own pull requests.

## Release Process

1. **Feature Freeze:** 2 weeks before release
2. **Release Candidate:** Testing period (1 week)
3. **Release:** TSC approval required
4. **Post-Release:** Bug fixes continue in maintenance branch

**Release Cadence:**
- Major releases: Twice yearly (March, September)
- Minor releases: Quarterly
- Patch releases: As needed

## Conflict Resolution

1. Attempt to resolve through discussion
2. Escalate to TSC if needed
3. TSC makes final decision
4. Serious disputes â†’ Board of Directors

## Code of Conduct

All community members must follow our [Code of Conduct](CODE_OF_CONDUCT.md).

Violations should be reported to conduct@ironhorsesecurity.org

## Amendments

This governance document can be amended by:
- 3/4 vote of TSC
- Board approval
- Community comment period (30 days)
```

---

# 4. Hardware Certification Program

## 4.1 Iron Horse Certified Hardware Initiative

### Program Overview

The **Iron Horse Certified Hardware** program establishes open standards for security IoT devices, ensuring:
- Interoperability across all platforms
- Security and privacy by design
- Open firmware (OpenIPC, ESP32, etc.)
- Local manufacturing support
- Long-term maintainability

### Certification Tiers

| Tier | Requirements | Support | Badge |
|------|-------------|---------|-------|
| **Bronze** | Basic interoperability, 1-year warranty | Community | ðŸ¥‰ |
| **Silver** | Security audit, 2-year warranty, firmware updates | Standard | ðŸ¥ˆ |
| **Gold** | Full compliance, 3-year warranty, priority support | Premium | ðŸ¥‡ |
| **Platinum** | Reference design, 5-year warranty, co-engineering | Enterprise | ðŸ’Ž |

## 4.2 Technical Standards

### Camera Certification Standard

**ironhorse-certified-camera-v1.0.yaml**
```yaml
# Iron Horse Certified Camera Standard v1.0
# Last Updated: 2024-02-15

specification_version: "1.0"
device_category: "IP Camera"

# Hardware Requirements
hardware:
  processor:
    minimum: "ARM Cortex-A7 @ 1GHz or equivalent"
    recommended: "ARM Cortex-A53 @ 1.5GHz or better"
  
  memory:
    minimum_ram: "256MB"
    recommended_ram: "512MB or more"
    minimum_flash: "16MB"
    recommended_flash: "32MB or more"
  
  image_sensor:
    minimum_resolution: "1920x1080 (1080p)"
    recommended_resolution: "2560x1440 (2K) or higher"
    minimum_fps: 15
    recommended_fps: 30
    sensor_types:
      - "CMOS"
      - "CCD"
    low_light:
      bronze: "5 lux"
      silver: "1 lux"
      gold: "0.1 lux"
  
  networking:
    required:
      - "10/100 Ethernet with PoE 802.3af"
    recommended:
      - "Gigabit Ethernet with PoE+ 802.3at"
      - "Wi-Fi 5 (802.11ac) or better"
  
  storage:
    required:
      - "microSD slot (up to 128GB)"
    recommended:
      - "microSD slot (up to 256GB)"
      - "NVMe SSD support"
  
  environmental:
    operating_temperature:
      indoor: "-10Â°C to 50Â°C"
      outdoor: "-30Â°C to 60Â°C"
    ingress_protection:
      indoor: "IP20 minimum"
      outdoor: "IP66 minimum"

# Firmware Requirements
firmware:
  base_system:
    approved:
      - name: "OpenIPC"
        version: "2.3 or later"
        url: "https://openipc.org"
      - name: "Custom Linux"
        requirements:
          - "Kernel 5.10 or later"
          - "Buildroot or Yocto-based"
    
    required_features:
      - "ONVIF Profile S compliance"
      - "RTSP/RTMP streaming"
      - "HTTP/HTTPS web interface"
      - "Time synchronization (NTP)"
      - "Secure boot support"
      - "OTA firmware updates"
      - "Factory reset capability"
  
  security:
    required:
      - "TLS 1.2 minimum for HTTPS"
      - "SSH with key authentication only (no password)"
      - "Unique default credentials per device"
      - "Certificate-based authentication support"
      - "Secure credential storage (encrypted)"
    recommended:
      - "TLS 1.3 support"
      - "Hardware cryptographic accelerator"
      - "Trusted Platform Module (TPM)"
      - "Verified boot"
  
  video_features:
    required:
      - "H.264 video compression"
      - "Multiple stream support (main + sub)"
      - "Configurable bitrate and resolution"
      - "Motion detection"
    recommended:
      - "H.265 (HEVC) support"
      - "Smart encoding (ROI)"
      - "Wide Dynamic Range (WDR)"
      - "3D noise reduction"
  
  integration:
    required_protocols:
      - "ONVIF Profile S"
      - "RTSP"
      - "HTTP REST API"
      - "MQTT publish/subscribe"
    recommended_protocols:
      - "ONVIF Profile T (H.265)"
      - "WebRTC"
      - "MQTT with QoS 2"
      - "Modbus TCP (for sensors)"
  
  ai_analytics:
    bronze: "None required"
    silver:
      - "Motion detection"
      - "Privacy masking"
    gold:
      - "Person detection"
      - "Vehicle detection"
      - "Line crossing"
    platinum:
      - "Face detection (privacy-preserving)"
      - "License plate recognition"
      - "Crowd detection"
      - "Loitering detection"

# API Requirements
api:
  rest_api:
    required_endpoints:
      - path: "/api/v1/device/info"
        method: "GET"
        description: "Device information and capabilities"
      - path: "/api/v1/stream/start"
        method: "POST"
        description: "Start video stream"
      - path: "/api/v1/stream/stop"
        method: "POST"
        description: "Stop video stream"
      - path: "/api/v1/settings"
        method: "GET"
        description: "Get device settings"
      - path: "/api/v1/settings"
        method: "PUT"
        description: "Update device settings"
      - path: "/api/v1/snapshot"
        method: "GET"
        description: "Capture snapshot image"
      - path: "/api/v1/events"
        method: "GET"
        description: "Get event history"
    
    authentication:
      required:
        - "Bearer token (JWT)"
        - "API key"
      recommended:
        - "OAuth 2.0"
        - "mTLS"
  
  mqtt_topics:
    required:
      - topic: "ironhorse/{device_id}/status"
        description: "Device health and status"
        qos: 1
        retain: true
      - topic: "ironhorse/{device_id}/events"
        description: "Motion and analytics events"
        qos: 1
        retain: false
      - topic: "ironhorse/{device_id}/commands"
        description: "Receive commands from platform"
        qos: 2
        retain: false

# Testing Requirements
testing:
  functional:
    - "Video stream quality at various bitrates"
    - "Network resilience (packet loss, latency)"
    - "Power failure recovery"
    - "Firmware upgrade/rollback"
    - "API endpoint validation"
  
  security:
    - "Vulnerability scanning (Nessus, OpenVAS)"
    - "Penetration testing"
    - "Fuzzing of network interfaces"
    - "Authentication bypass attempts"
    - "Default credential check"
  
  performance:
    - "Sustained streaming for 72 hours"
    - "CPU and memory usage monitoring"
    - "Thermal testing"
    - "Power consumption measurement"
  
  compliance:
    bronze:
      - "Basic functional testing"
      - "ONVIF conformance"
    silver:
      - "Full functional testing"
      - "Security vulnerability scan"
      - "Performance benchmarking"
    gold:
      - "Third-party security audit"
      - "Stress testing"
      - "Environmental testing"
    platinum:
      - "Full certification including EMC/FCC"
      - "Long-term reliability testing (1000+ hours)"

# Documentation Requirements
documentation:
  required:
    - "Quick start guide"
    - "Technical specifications"
    - "API documentation"
    - "Firmware update procedure"
    - "Troubleshooting guide"
    - "Open-source licenses disclosure"
  
  recommended:
    - "Integration examples"
    - "3D CAD models (STEP format)"
    - "PCB schematics"
    - "BOM (Bill of Materials)"

# Warranty & Support
warranty:
  bronze:
    duration: "1 year"
    coverage: "Hardware defects"
  silver:
    duration: "2 years"
    coverage: "Hardware defects + firmware updates"
  gold:
    duration: "3 years"
    coverage: "Hardware + firmware + security patches"
  platinum:
    duration: "5 years"
    coverage: "Full coverage + extended support"

# Manufacturing
manufacturing:
  required_certifications:
    - "ISO 9001 (Quality Management)"
    - "RoHS compliance"
  
  recommended_certifications:
    - "ISO 14001 (Environmental)"
    - "ISO 27001 (Information Security)"
  
  local_manufacturing:
    incentives:
      - "Priority listing in marketplace"
      - "\"Locally Made\" badge"
      - "Reduced certification fees"
```

### ESP32 Sensor Module Standard

**ironhorse-certified-esp32-sensor-v1.0.yaml**
```yaml
# Iron Horse Certified ESP32 Sensor Module Standard v1.0

specification_version: "1.0"
device_category: "IoT Sensor Module"

# Hardware Requirements
hardware:
  microcontroller:
    approved_models:
      - "ESP32"
      - "ESP32-S2"
      - "ESP32-S3"
      - "ESP32-C3"
      - "ESP32-C6"
    minimum_specifications:
      cpu: "240 MHz dual-core or equivalent"
      ram: "320 KB"
      flash: "4 MB"
      connectivity:
        - "Wi-Fi 802.11 b/g/n"
        - "Bluetooth 4.2 BLE or better"
  
  power:
    operating_voltage: "3.3V"
    power_modes:
      - "Active mode"
      - "Light sleep"
      - "Deep sleep (<10Î¼A)"
    battery_support:
      - "LiPo charging circuit"
      - "Low battery detection"
  
  sensors:
    supported_types:
      - "PIR motion (HC-SR501 or similar)"
      - "Door/window contact (magnetic reed)"
      - "Temperature/Humidity (DHT22, BME280)"
      - "Air quality (MQ sensors, SDS011)"
      - "Light level (LDR, BH1750)"
      - "Sound level (MAX4466)"
      - "Gas detection (MQ-2, MQ-7)"
    
    interface:
      required:
        - "GPIO pins"
        - "I2C"
      recommended:
        - "SPI"
        - "UART"
        - "Analog input"

# Firmware Requirements
firmware:
  framework:
    approved:
      - name: "ESP-IDF"
        version: "4.4 or later"
      - name: "Arduino ESP32"
        version: "2.0 or later"
      - name: "PlatformIO"
        version: "Any"
  
  required_features:
    - "Over-The-Air (OTA) updates"
    - "Wi-Fi provisioning (WPS or SmartConfig)"
    - "MQTT publish/subscribe"
    - "TLS 1.2 for MQTT"
    - "Certificate storage in flash"
    - "Watchdog timer"
    - "Factory reset (button press)"
  
  data_format:
    mqtt_payload: "JSON"
    example: |
      {
        "device_id": "sensor-12345",
        "type": "motion",
        "value": true,
        "timestamp": "2024-02-15T10:30:00Z",
        "battery": 87
      }

# Integration Requirements
integration:
  mqtt:
    required_topics:
      - "ironhorse/{device_id}/sensor/{sensor_type}"
      - "ironhorse/{device_id}/status"
      - "ironhorse/{device_id}/battery"
    qos: 1
    
  https_api:
    recommended: true
    endpoints:
      - "/api/v1/reading"
      - "/api/v1/status"

# Power Management
power_management:
  battery_life_targets:
    motion_sensor: "1 year (4 AA batteries, 1 event/hour)"
    environmental: "6 months (LiPo 3000mAh, 5 min interval)"
  
  strategies:
    - "Deep sleep between readings"
    - "Wi-Fi power save mode"
    - "Adaptive sampling rate"

# Testing & Certification
testing:
  functional:
    - "Sensor accuracy validation"
    - "Wi-Fi range test (minimum 30m clear line)"
    - "Power consumption measurement"
    - "OTA update success"
    - "Factory reset verification"
  
  reliability:
    - "Continuous operation (168 hours)"
    - "Temperature cycling (-10Â°C to 50Â°C)"
    - "Power cycle test (100 cycles)"

# Reference Designs
reference_designs:
  provided:
    - "KiCad PCB schematics"
    - "3D enclosure (STL files)"
    - "Sample firmware (ESP-IDF)"
    - "BOM with supplier links"
  
  licensing:
    hardware: "CERN-OHL-P v2"
    software: "MIT"
```

## 4.3 Certification Process

**certification_process.md**
```markdown
# Iron Horse Hardware Certification Process

## Step 1: Application

1. Submit application: https://certification.ironhorsesecurity.org
2. Provide:
   - Company information
   - Product details
   - Target certification tier
   - Technical documentation

**Fee:** $500 USD (refundable if certification passes)

## Step 2: Documentation Review

IHOTF reviews submitted documentation for:
- Compliance with technical standards
- Completeness of documentation
- Open-source licensing

**Timeline:** 2 weeks

## Step 3: Sample Submission

Send 3 sample units to IHOTF testing lab:
- Address: IHOTF Testing Lab, 123 Tech St, Waterloo, ON, Canada
- Include: Product manual, power supplies, cables

**Timeline:** 1 week shipping

## Step 4: Testing

IHOTF performs testing per standard:

### Bronze Certification
- Functional testing (3 days)
- ONVIF/Protocol compliance (2 days)
- Basic security scan (1 day)

### Silver Certification
- Bronze tests +
- Performance testing (2 days)
- Security vulnerability assessment (3 days)
- Environmental testing (optional)

### Gold Certification
- Silver tests +
- Third-party security audit (5 days)
- Stress testing (3 days)
- Full environmental testing (5 days)

### Platinum Certification
- Gold tests +
- EMC/FCC testing (external lab, 10+ days)
- Long-term reliability (1000 hours)
- Reference design validation

**Timeline:** 2-8 weeks depending on tier

## Step 5: Results & Certification

If passed:
1. Certificate issued (PDF + blockchain-verified)
2. Listed in marketplace: https://marketplace.ironhorsesecurity.org
3. Badge assets provided (SVG, PNG)
4. Press release drafted (optional)

If failed:
1. Detailed report of failures provided
2. Guidance on remediation
3. Re-test at reduced fee after fixes

## Certification Fees

| Tier | Testing Fee | Annual Renewal |
|------|-------------|----------------|
| Bronze | $1,500 | $500 |
| Silver | $5,000 | $1,500 |
| Gold | $15,000 | $3,000 |
| Platinum | $35,000 | $5,000 |

### Fee Waivers

50% discount for:
- Open hardware (full schematics public)
- Non-profit manufacturers
- First product from startup (<2 years)

75% discount for:
- Local North American manufacturing
- Reference design contributions

## Maintaining Certification

- Annual renewal required
- Random re-testing (1 in 10 units)
- Firmware updates must be reviewed
- Any critical security issues â†’ immediate re-certification

## Appeals Process

If certification denied:
1. Request detailed review from TSC
2. Present additional evidence
3. TSC makes final decision within 30 days
```

## 4.4 Reference Designs

**Reference designs will be published at:**
https://github.com/ironhorse-security/hardware-reference-designs

Including:
- ESP32 Motion Sensor PCB
- ESP32 Door/Window Sensor
- OpenIPC Camera (IMX307 + Hi3516EV200)
- LoRa Gateway for Remote Sites
- NFC/RFID Reader Module
- Access Control Board (Wiegand + MQTT)

---

# 5. Academic & Research Integration

## 5.1 University Partnership Framework

### Partnership Tiers

| Tier | Benefits | Requirements | Annual Fee |
|------|----------|--------------|------------|
| **Bronze** | Student accounts, Basic support | None | $0 |
| **Silver** | + Curriculum materials, Guest lectures | 50+ students/year | $1,000 |
| **Gold** | + Research data access, Co-op program | 100+ students, 1 research project | $2,500 |
| **Platinum** | + Joint R&D, Dedicated support, Revenue share | 200+ students, 3+ research projects, Published papers | Custom |

### Benefits Detail

**Student Access:**
- Free Iron Horse platform accounts (educational tier)
- Access to sandbox environments
- Mobile app test accounts
- Training certifications at 50% discount

**Curriculum Support:**
- Lecture slides and lab materials
- Sample projects and datasets
- Video tutorials
- Textbook chapter drafts

**Research Opportunities:**
- Access to anonymized operational data
- Beta features for testing
- Research grants ($5K-$50K per project)
- Co-authorship on publications

**Career Pipeline:**
- Student co-op placements (8-16 months)
- Internship opportunities
- New graduate hiring preference
- Alumni network

## 5.2 Joint R&D Programs

### Active Research Areas

1. **AI & Machine Learning**
   - Predictive incident modeling
   - Computer vision for security applications
   - Natural language processing for incident reports
   - Reinforcement learning for patrol optimization

2. **IoT & Edge Computing**
   - Low-power sensor networks
   - Edge AI inference
   - Mesh networking for disconnected sites
   - Energy harvesting for sensors

3. **Cybersecurity**
   - Zero-trust architecture
   - Blockchain for audit trails
   - Quantum-resistant encryption
   - Secure IoT firmware updates

4. **Human-Computer Interaction**
   - Guard interface usability
   - AR/VR training simulations
   - Voice-activated reporting
   - Accessibility features

### Research Grant Program

**Funding Levels:**
- Small Grants: $5,000 - $10,000 (undergraduate/masters projects)
- Medium Grants: $10,000 - $30,000 (PhD projects)
- Large Grants: $30,000 - $100,000 (multi-year research programs)

**Application Process:**
1. Submit proposal: research@ironhorsesecurity.org
2. Review by Technical Steering Committee (30 days)
3. If approved, execute research agreement
4. Quarterly progress reports required
5. Final paper due within 6 months of completion

**Requirements:**
- Open publication (pre-prints on arXiv)
- Open-source code release (if applicable)
- Acknowledgment of IHOTF funding
- Present findings at Iron Horse Annual Conference

## 5.3 Certification-to-Credit Mapping

### Academic Credit Equivalency

Iron Horse certifications can count toward academic credit at partner institutions:

| Iron Horse Certification | Academic Equivalent | Credits |
|--------------------------|---------------------|---------|
| **Security Guard Professional** | Introduction to Security Management | 3 |
| **Healthcare Security Specialist** | Healthcare Security Operations | 3 |
| **Cannabis Security Professional** | Cannabis Compliance & Security | 3 |
| **Cybersecurity for Physical Security** | Cybersecurity Fundamentals | 3 |
| **Security Operations Manager** | Security Management Capstone | 6 |

### Integration with LMS

**Moodle Plugin:** `moodle-local-ironhorse-credits`

Features:
- Automatic certification verification via API
- Grade book integration
- Completion tracking
- Badge display

**Installation:**
```bash
cd /var/www/moodle
git clone https://github.com/ironhorse-security/moodle-local-ironhorse-credits.git local/ironhorse_credits
php admin/cli/upgrade.php
```

**Configuration:**
```php
// config.php
$CFG->ironhorse_api_key = 'your-api-key';
$CFG->ironhorse_api_secret = 'your-api-secret';
$CFG->ironhorse_auto_credit = true; // Auto-grant credits
$CFG->ironhorse_notify_instructor = true; // Email instructor
```

## 5.4 Student Co-op Program

### Program Structure

**Duration:** 8-16 months (2-4 academic terms)

**Positions:**
- Software Developer (Full-Stack, Backend, Mobile)
- DevOps Engineer
- Data Scientist / ML Engineer
- Security Analyst
- UX/UI Designer
- Technical Writer

**Compensation:**
- $20-$30/hour (undergraduate)
- $25-$40/hour (graduate)
- Housing allowance (if relocation required)
- Transit pass
- Professional development budget ($1,000)

### Application Process

1. **University Coordinator** submits student roster
2. **Students Apply** via https://careers.ironhorsesecurity.org/coop
3. **Screening** by HR (resume + transcript review)
4. **Technical Interview** (coding challenge or case study)
5. **Manager Interview** (behavioral + technical)
6. **Offer** (2 weeks before term start)

### Learning Objectives

Each co-op includes:
- Onboarding (1 week): Platform overview, codebase tour
- Mentorship: Assigned senior engineer mentor
- Projects: 2-3 substantial projects per term
- Code Reviews: All code reviewed by senior staff
- Brown Bags: Weekly tech talks and learning sessions
- Final Presentation: Demo project to company

### Academic Integration

- **Work Reports:** Students write academic reports on work
- **Evaluation:** Manager completes evaluation form for university
- **Grading:** Pass/Fail based on performance
- **Credits:** Some programs grant academic credit for co-op

---

# 6. Implementation Roadmap

## Phase 1: Foundation (Months 1-3)

### Month 1: Legal & Organizational Setup
- **Week 1-2:** Register IHOTF as non-profit corporation
- **Week 3:** Draft founding documents, bylaws, CLA
- **Week 4:** Establish bank account, accounting system

### Month 2: Technical Infrastructure
- **Week 1:** Set up GitHub organization, CI/CD
- **Week 2:** Migrate repositories, update licenses
- **Week 3:** Deploy documentation site (docs.ironhorsesecurity.org)
- **Week 4:** Set up community infrastructure (Discord, mailing list)

### Month 3: Partner SDK Release
- **Week 1-2:** Finalize Partner SDK documentation
- **Week 3:** Release Python/JavaScript client libraries
- **Week 4:** Launch partner portal (partners.ironhorsesecurity.org)

**Deliverables:**
- âœ… IHOTF legally established
- âœ… All repos open-sourced
- âœ… Partner SDK v1.0 released
- âœ… Documentation site live

**Budget:** $50,000
- Legal: $15,000
- Infrastructure: $10,000
- Marketing: $10,000
- Staffing: $15,000

## Phase 2: Community Building (Months 4-6)

### Month 4: Onboard First Partners
- **Week 1:** Onboard 3 pilot partners
- **Week 2-3:** Gather feedback, iterate on SDK
- **Week 4:** Case studies and testimonials

### Month 5: Hardware Certification Launch
- **Week 1-2:** Publish hardware standards
- **Week 3-4:** Set up testing lab
- **Week 4:** Certify first 2 reference devices

### Month 6: Academic Partnerships
- **Week 1-2:** Sign first 3 university partnerships
- **Week 3:** Launch student accounts program
- **Week 4:** First research grant awarded

**Deliverables:**
- âœ… 5 federated partners live
- âœ… Hardware certification program operational
- âœ… 3 university partnerships signed
- âœ… 50+ students using platform

**Budget:** $75,000
- Partner support: $25,000
- Testing lab setup: $30,000
- Academic program: $20,000

## Phase 3: Ecosystem Growth (Months 7-12)

### Months 7-9: Scale Operations
- Onboard 10+ additional partners
- Certify 10+ hardware devices
- Launch marketplace (marketplace.ironhorsesecurity.org)
- First community conference (IronHorseCon)

### Months 10-12: Research & Innovation
- Fund 5 research grants
- Launch student co-op program (first cohort: 10 students)
- Release 3 major features from community contributions
- Publish first joint research papers

**Deliverables:**
- âœ… 20+ federated partners
- âœ… 20+ certified devices
- âœ… 500+ community contributors
- âœ… 10 students in co-op program
- âœ… First conference with 200+ attendees

**Budget:** $200,000
- Operations: $80,000
- Research grants: $50,000
- Marketing & events: $40,000
- Staffing: $30,000

## Total Year 1 Investment

**Budget:** $325,000

**Funding Sources:**
- Iron Horse Security: $150,000 (founding sponsor)
- Partner annual fees (15 partners Ã— $5K avg): $75,000
- Hardware certification fees (20 devices Ã— $3K avg): $60,000
- Research grants (external): $40,000

**ROI Metrics:**
- Partners: 20+
- Certified devices: 20+
- Community contributors: 500+
- Student participants: 100+
- Research grants: 5+

---

## Conclusion

The Iron Horse Federation & Ecosystem Framework creates a **sustainable, community-driven platform** that benefits all stakeholders:

- **Partners** get turnkey security operations infrastructure
- **Community** contributes to and benefits from open innovation
- **Manufacturers** access security market with certified devices
- **Universities** provide students with real-world experience
- **Iron Horse** builds network effects and accelerates innovation

By following this implementation roadmap, Iron Horse Security transforms from a single company into the **industry standard platform** for modern security operations worldwide.

---

**Next Steps:**
1. Review and approve this framework with stakeholders
2. Begin Phase 1: Foundation (Month 1 activities)
3. Recruit founding IHOTF board members
4. Launch community outreach campaign

**Contact:**
- Foundation: foundation@ironhorsesecurity.org
- Partners: partners@ironhorsesecurity.org
- Academic: research@ironhorsesecurity.org
- Hardware: certification@ironhorsesecurity.org

---

*This document is open for community feedback. Submit comments via GitHub Issues or email: community@ironhorsesecurity.org*
