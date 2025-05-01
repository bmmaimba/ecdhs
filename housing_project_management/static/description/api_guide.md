# Housing Project Management API Guide

## Authentication
All API endpoints require user authentication. Use the following headers:
```
Content-Type: application/json
X-Openerp-Session-Id: your_session_id
```

## Available Endpoints

### 1. Projects

#### Get All Projects
```
GET /api/housing/projects
```
Response:
```json
[
    {
        "id": 1,
        "name": "Project Name",
        "type": "irdp",
        "state": "draft",
        "budget": 1000000
    }
]
```

#### Get Single Project
```
GET /api/housing/projects/<project_id>
```

#### Create Project
```
POST /api/housing/projects
```
Request Body:
```json
{
    "name": "New Project",
    "project_type": "irdp",
    "municipality_id": 1,
    "budget_allocation": 1000000
}
```

### 2. Beneficiaries

#### Get Project Beneficiaries
```
GET /api/housing/beneficiaries
```

#### Add Beneficiary
```
POST /api/housing/beneficiaries
```
Request Body:
```json
{
    "name": "John Doe",
    "id_number": "8001015009087",
    "project_id": 1,
    "monthly_income": 3500
}
```

### 3. Services

#### Get Project Services
```
GET /api/housing/services
```

## Error Handling
The API returns standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Rate Limiting
API calls are limited to 1000 requests per hour per user.
