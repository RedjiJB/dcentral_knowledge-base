---
source_project: Bounty
source_project_uuid: 0198b52e-0516-768e-b6d4-182ebfca6ef0
doc_uuid: f29d8edd-1684-4b80-abb1-fa5b762f4a73
original_filename: DION Platform API - Completion of OpenAPI Specification.md
created_at: 2025-08-23T15:56:37.850493+00:00
content_hash: 3602b9784e86
topic: "dion-platform-api-backend-architecture"
consolidated_into: docs/DC-DION-API-BACKEND-RECONCILED-001.md
---

# DION Platform API - Completion of OpenAPI Specification

## Continuing from EmergencyAlertCreation schema:

```yaml
    EmergencyAlertCreation:
      type: object
      properties:
        type:
          type: string
        severity:
          type: string
          enum: [low, medium, high, critical]
        title:
          type: string
        description:
          type: string
        location:
          $ref: '#/components/schemas/Location'
        radius:
          type: number
          description: Alert radius in meters
        priority:
          type: integer
          minimum: 1
          maximum: 10
          default: 5
        metadata:
          type: object
          additionalProperties: true
      required: [type, severity, title, location, radius]

    Location:
      type: object
      properties:
        latitude:
          type: number
          format: double
          minimum: -90
          maximum: 90
        longitude:
          type: number
          format: double
          minimum: -180
          maximum: 180
        altitude:
          type: number
          format: double
        accuracy:
          type: number
          description: GPS accuracy in meters
      required: [latitude, longitude]

    LocationQuery:
      type: object
      properties:
        latitude:
          type: number
          format: double
        longitude:
          type: number
          format: double
        radius:
          type: number
          description: Search radius in meters
          default: 1000
      required: [latitude, longitude]

    Node:
      type: object
      properties:
        id:
          type: string
          format: uuid
        did:
          type: string
        type:
          type: string
          enum: [community, professional, command]
        capabilities:
          type: array
          items:
            type: string
        hardwareSpec:
          type: object
          properties:
            cpu:
              type: string
            memory:
              type: string
            storage:
              type: string
            sensors:
              type: array
              items:
                type: string
        location:
          $ref: '#/components/schemas/Location'
        status:
          type: string
          enum: [online, offline, maintenance, error]
        reputation:
          type: number
        stakeAmount:
          type: number
        lastHeartbeat:
          type: string
          format: date-time
        createdAt:
          type: string
          format: date-time

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object
        timestamp:
          type: string
          format: date-time
        traceId:
          type: string
      required: [code, message]

    PaginatedResponse:
      type: object
      properties:
        data:
          type: array
          items:
            type: object
        total:
          type: integer
        page:
          type: integer
        limit:
          type: integer
        hasNext:
          type: boolean
        hasPrev:
          type: boolean

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: BAD_REQUEST
            message: Invalid request parameters
            details:
              field: location.latitude
              reason: Value must be between -90 and 90

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

    Forbidden:
      description: Access denied
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: FORBIDDEN
            message: Insufficient permissions

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: Resource not found

    RateLimit:
      description: Too many requests
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: RATE_LIMITED
            message: Request rate limit exceeded
            details:
              limit: 100
              window: 3600
              reset: 1640995200

    ServerError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: INTERNAL_ERROR
            message: An unexpected error occurred
```

## Additional API Endpoints

```yaml
  # Node Management endpoints
  /nodes:
    get:
      summary: List nodes
      tags: [Nodes]
      parameters:
        - name: type
          in: query
          schema:
            type: string
            enum: [community, professional, command]
        - name: status
          in: query
          schema:
            type: string
            enum: [online, offline, maintenance, error]
        - name: location
          in: query
          schema:
            $ref: '#/components/schemas/LocationQuery'
        - name: capabilities
          in: query
          schema:
            type: array
            items:
              type: string
      responses:
        '200':
          description: List of nodes
          content:
            application/json:
              schema:
                type: object
                properties:
                  nodes:
                    type: array
                    items:
                      $ref: '#/components/schemas/Node'

    post:
      summary: Register new node
      tags: [Nodes]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                did:
                  type: string
                type:
                  type: string
                  enum: [community, professional, command]
                capabilities:
                  type: array
                  items:
                    type: string
                hardwareSpec:
                  type: object
                location:
                  $ref: '#/components/schemas/Location'
                stakeAmount:
                  type: number
                attestation:
                  type: string
                  description: Hardware attestation proof
              required: [did, type, capabilities, hardwareSpec, attestation]
      responses:
        '201':
          description: Node registered successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Node'

  /nodes/{id}/heartbeat:
    post:
      summary: Send node heartbeat
      tags: [Nodes]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  enum: [online, offline, maintenance, error]
                metrics:
                  type: object
                  properties:
                    cpuUsage:
                      type: number
                      minimum: 0
                      maximum: 100
                    memoryUsage:
                      type: number
                      minimum: 0
                      maximum: 100
                    diskUsage:
                      type: number
                      minimum: 0
                      maximum: 100
                    networkLatency:
                      type: number
                signature:
                  type: string
              required: [status, signature]
      responses:
        '200':
          description: Heartbeat accepted
        '404':
          $ref: '#/components/responses/NotFound'

  # GraphQL endpoint
  /graphql:
    post:
      summary: GraphQL endpoint
      tags: [GraphQL]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                variables:
                  type: object
                operationName:
                  type: string
      responses:
        '200':
          description: GraphQL response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                  errors:
                    type: array
                    items:
                      type: object

  # WebSocket endpoints
  /ws/notifications:
    get:
      summary: WebSocket for real-time notifications
      tags: [WebSocket]
      responses:
        '101':
          description: Switching Protocols

  /ws/emergency/{alertId}:
    get:
      summary: WebSocket for emergency coordination
      tags: [WebSocket]
      parameters:
        - name: alertId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '101':
          description: Switching Protocols

  # Blockchain integration endpoints
  /blockchain/transactions:
    get:
      summary: Get blockchain transactions
      tags: [Blockchain]
      parameters:
        - name: address
          in: query
          schema:
            type: string
        - name: type
          in: query
          schema:
            type: string
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, confirmed, failed]
      responses:
        '200':
          description: Transaction history
          content:
            application/json:
              schema:
                type: object
                properties:
                  transactions:
                    type: array
                    items:
                      type: object
                      properties:
                        hash:
                          type: string
                        type:
                          type: string
                        status:
                          type: string
                        timestamp:
                          type: string
                          format: date-time
                        value:
                          type: string
                        gasUsed:
                          type: string

  # Training and certification endpoints
  /training/modules:
    get:
      summary: Get training modules
      tags: [Training]
      responses:
        '200':
          description: Available training modules
          content:
            application/json:
              schema:
                type: object
                properties:
                  modules:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                        title:
                          type: string
                        description:
                          type: string
                        level:
                          type: integer
                        duration:
                          type: integer
                          description: Duration in minutes
                        prerequisites:
                          type: array
                          items:
                            type: string

  /training/certifications:
    post:
      summary: Submit certification exam
      tags: [Training]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                moduleId:
                  type: string
                answers:
                  type: object
                proctorSignature:
                  type: string
              required: [moduleId, answers, proctorSignature]
      responses:
        '201':
          description: Certification submitted
          content:
            application/json:
              schema:
                type: object
                properties:
                  certificationId:
                    type: string
                  status:
                    type: string
                    enum: [pending, passed, failed]
                  score:
                    type: number
                  issuedAt:
                    type: string
                    format: date-time
```

## Rate Limiting and Security

```yaml
# Rate limiting configuration
x-rate-limits:
  intelligence-submission:
    rate: 100
    per: hour
    burst: 10
  
  task-creation:
    rate: 50
    per: hour
    burst: 5
  
  emergency-alerts:
    rate: 10
    per: hour
    burst: 2
  
  api-general:
    rate: 1000
    per: hour
    burst: 100

# Security requirements
security:
  - BearerAuth: []
  - DIDAuth: []

# API versioning
x-api-version:
  current: "1.0.0"
  supported: ["1.0.0"]
  deprecated: []
```

## Error Codes Reference

```yaml
x-error-codes:
  # Authentication & Authorization
  UNAUTHORIZED: "Authentication required"
  FORBIDDEN: "Access denied"
  INVALID_TOKEN: "Invalid or expired token"
  INSUFFICIENT_PERMISSIONS: "Insufficient permissions"
  
  # Validation
  BAD_REQUEST: "Invalid request parameters"
  VALIDATION_ERROR: "Request validation failed"
  MISSING_REQUIRED_FIELD: "Required field missing"
  INVALID_FORMAT: "Invalid data format"
  
  # Resource Management
  NOT_FOUND: "Resource not found"
  ALREADY_EXISTS: "Resource already exists"
  CONFLICT: "Resource conflict"
  GONE: "Resource no longer available"
  
  # Rate Limiting
  RATE_LIMITED: "Request rate limit exceeded"
  QUOTA_EXCEEDED: "API quota exceeded"
  
  # Business Logic
  INSUFFICIENT_FUNDS: "Insufficient funds for operation"
  TASK_ALREADY_ASSIGNED: "Task already assigned"
  OPERATOR_UNAVAILABLE: "Operator not available"
  NODE_OFFLINE: "Node is offline"
  VERIFICATION_FAILED: "Data verification failed"
  
  # System
  INTERNAL_ERROR: "Internal server error"
  SERVICE_UNAVAILABLE: "Service temporarily unavailable"
  MAINTENANCE_MODE: "System in maintenance mode"
  
  # Blockchain
  TRANSACTION_FAILED: "Blockchain transaction failed"
  INSUFFICIENT_GAS: "Insufficient gas for transaction"
  CONTRACT_ERROR: "Smart contract execution error"
```

This completes the OpenAPI specification for the DION Platform API, providing comprehensive documentation for all endpoints, schemas, error handling, and security requirements.

<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/dion-platform-api-backend-architecture|dion-platform-api-backend-architecture]]

**Consolidated into:**
- [[docs/DC-DION-API-BACKEND-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
