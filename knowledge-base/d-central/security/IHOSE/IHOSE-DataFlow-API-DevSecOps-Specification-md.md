---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: b30cf260-aec8-4ca5-8f51-747573b82861
original_filename: IHOSE_DataFlow_API_DevSecOps_Specification.md
created_at: 2025-11-10T23:32:22.615832+00:00
content_hash: 586a40269f1f
topic: "ihose-openvision-documentation-package"
consolidated_into: docs/DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001.md
---

# Iron Horse Security - Data Flow & DevSecOps Pipeline Specification

**Version 1.0 - API Contracts & CI/CD Automation**

*Extends: IHOSE Complete Technical Specification v3.0*

---

# 2. Data Flow & API Contracts

## 2.1 OpenAPI 3.1 Specifications

### ERPNext Operations API

**openapi-erpnext-operations.yaml**
```yaml
openapi: 3.1.0
info:
  title: Iron Horse ERPNext Operations API
  description: |
    Unified API for Iron Horse Security field operations, patrol tracking,
    incident management, and client portal integration.
  version: 1.0.0
  contact:
    name: Iron Horse Security API Team
    email: api@ironhorsesecurity.com
  license:
    name: AGPL-3.0
    url: https://www.gnu.org/licenses/agpl-3.0.en.html

servers:
  - url: https://erp.ironhorsesecurity.com/api
    description: Production API
  - url: https://staging-erp.ironhorsesecurity.com/api
    description: Staging environment

security:
  - bearerAuth: []
  - apiKeyAuth: []
  - oauth2: [read, write]

tags:
  - name: Guards
    description: Security guard operations
  - name: Patrols
    description: Patrol tracking and checkpoints
  - name: Incidents
    description: Incident reporting and management
  - name: Sites
    description: Client site management
  - name: Schedules
    description: Shift scheduling
  - name: Assets
    description: Equipment and asset tracking

paths:
  /resource/Guard:
    get:
      tags: [Guards]
      summary: List all guards
      operationId: listGuards
      parameters:
        - name: fields
          in: query
          schema:
            type: array
            items:
              type: string
          description: Specific fields to return
        - name: filters
          in: query
          schema:
            type: object
          description: Filter criteria (JSON)
        - name: limit_start
          in: query
          schema:
            type: integer
            default: 0
        - name: limit_page_length
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Guard'
                  total:
                    type: integer
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
    
    post:
      tags: [Guards]
      summary: Create a new guard record
      operationId: createGuard
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GuardCreate'
      responses:
        '201':
          description: Guard created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Guard'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /resource/Guard/{guard_id}:
    get:
      tags: [Guards]
      summary: Get guard details
      operationId: getGuard
      parameters:
        - name: guard_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Guard details
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/Guard'
        '404':
          $ref: '#/components/responses/NotFound'
    
    put:
      tags: [Guards]
      summary: Update guard information
      operationId: updateGuard
      parameters:
        - name: guard_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GuardUpdate'
      responses:
        '200':
          description: Guard updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Guard'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'

  /method/ironhorse.api.patrol.submit_checkpoint:
    post:
      tags: [Patrols]
      summary: Submit patrol checkpoint scan
      description: |
        Records a guard's checkpoint scan during patrol.
        Publishes event to Kafka for real-time tracking.
      operationId: submitCheckpoint
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - guard_id
                - checkpoint_id
                - scan_time
                - location
              properties:
                guard_id:
                  type: string
                  description: Guard employee ID
                checkpoint_id:
                  type: string
                  description: NFC tag or QR code identifier
                scan_time:
                  type: string
                  format: date-time
                  description: Timestamp of scan (ISO 8601)
                location:
                  type: object
                  properties:
                    latitude:
                      type: number
                      format: double
                    longitude:
                      type: number
                      format: double
                    accuracy:
                      type: number
                      format: float
                      description: GPS accuracy in meters
                notes:
                  type: string
                  description: Optional guard notes
                  maxLength: 500
                attachments:
                  type: array
                  items:
                    type: object
                    properties:
                      type:
                        type: string
                        enum: [photo, video, audio]
                      file_url:
                        type: string
                        format: uri
                      file_size:
                        type: integer
                      mime_type:
                        type: string
      responses:
        '200':
          description: Checkpoint recorded successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: object
                    properties:
                      checkpoint_log_id:
                        type: string
                      status:
                        type: string
                        enum: [on_time, early, late]
                      next_checkpoint:
                        type: string
                      estimated_arrival:
                        type: string
                        format: date-time
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /method/ironhorse.api.incidents.create:
    post:
      tags: [Incidents]
      summary: Create incident report
      description: |
        Creates a new incident report. Automatically triggers:
        - Supervisor notification (Matrix)
        - Client portal update
        - Kafka event publication
        - Wazuh security log
      operationId: createIncident
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/IncidentCreate'
      responses:
        '201':
          description: Incident created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Incident'
        '400':
          $ref: '#/components/responses/BadRequest'

  /method/ironhorse.api.schedules.get_guard_shifts:
    get:
      tags: [Schedules]
      summary: Get guard shift schedule
      operationId: getGuardShifts
      parameters:
        - name: guard_id
          in: query
          required: true
          schema:
            type: string
        - name: start_date
          in: query
          required: true
          schema:
            type: string
            format: date
        - name: end_date
          in: query
          required: true
          schema:
            type: string
            format: date
      responses:
        '200':
          description: Guard shift schedule
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: array
                    items:
                      $ref: '#/components/schemas/Shift'

  /resource/Site:
    get:
      tags: [Sites]
      summary: List client sites
      operationId: listSites
      parameters:
        - name: filters
          in: query
          schema:
            type: object
          description: Filter criteria
      responses:
        '200':
          description: List of sites
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Site'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: Keycloak-issued JWT token
    
    apiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
      description: 'Format: token {api_key}:{api_secret}'
    
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.ironhorsesecurity.com/realms/ironhorse/protocol/openid-connect/auth
          tokenUrl: https://auth.ironhorsesecurity.com/realms/ironhorse/protocol/openid-connect/token
          scopes:
            read: Read access to resources
            write: Write access to resources
            admin: Administrative access

  schemas:
    Guard:
      type: object
      required:
        - name
        - employee_id
        - status
      properties:
        name:
          type: string
        employee_id:
          type: string
          description: Unique employee identifier
        email:
          type: string
          format: email
        phone:
          type: string
          pattern: '^\+?[1-9]\d{1,14}$'
        status:
          type: string
          enum: [Active, Inactive, On Leave, Terminated]
        certifications:
          type: array
          items:
            type: object
            properties:
              type:
                type: string
                enum: [Security Guard License, First Aid, CPR, CCTV Operations, Access Control]
              number:
                type: string
              issue_date:
                type: string
                format: date
              expiry_date:
                type: string
                format: date
              issuer:
                type: string
        performance_score:
          type: number
          format: float
          minimum: 0
          maximum: 100
        assigned_sites:
          type: array
          items:
            type: string
        keycloak_user_id:
          type: string
          description: Keycloak UUID
        created_at:
          type: string
          format: date-time
        modified_at:
          type: string
          format: date-time

    GuardCreate:
      type: object
      required:
        - first_name
        - last_name
        - email
        - employee_id
      properties:
        first_name:
          type: string
          minLength: 2
          maxLength: 50
        last_name:
          type: string
          minLength: 2
          maxLength: 50
        email:
          type: string
          format: email
        phone:
          type: string
        employee_id:
          type: string
          minLength: 4
          maxLength: 20
        hire_date:
          type: string
          format: date
        department:
          type: string
          default: Field Operations

    GuardUpdate:
      type: object
      properties:
        phone:
          type: string
        status:
          type: string
          enum: [Active, Inactive, On Leave, Terminated]
        assigned_sites:
          type: array
          items:
            type: string

    Incident:
      type: object
      required:
        - incident_id
        - site
        - reported_by
        - incident_time
        - severity
        - category
        - description
      properties:
        incident_id:
          type: string
          description: Unique incident identifier
        site:
          type: string
          description: Site where incident occurred
        reported_by:
          type: string
          description: Guard who reported incident
        incident_time:
          type: string
          format: date-time
        report_time:
          type: string
          format: date-time
        severity:
          type: string
          enum: [Critical, High, Medium, Low, Informational]
        category:
          type: string
          enum: [Theft, Vandalism, Trespassing, Medical, Fire, Hazard, Suspicious Activity, Other]
        description:
          type: string
          minLength: 20
        location_details:
          type: string
        witnesses:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              contact:
                type: string
              statement:
                type: string
        actions_taken:
          type: string
        police_notified:
          type: boolean
        police_report_number:
          type: string
        client_notified:
          type: boolean
        attachments:
          type: array
          items:
            type: object
            properties:
              file_name:
                type: string
              file_url:
                type: string
                format: uri
              file_type:
                type: string
              upload_time:
                type: string
                format: date-time
        status:
          type: string
          enum: [Open, Under Investigation, Resolved, Closed]
        supervisor_review:
          type: object
          properties:
            reviewed_by:
              type: string
            review_date:
              type: string
              format: date-time
            comments:
              type: string
            approved:
              type: boolean

    IncidentCreate:
      type: object
      required:
        - site
        - incident_time
        - severity
        - category
        - description
      properties:
        site:
          type: string
        incident_time:
          type: string
          format: date-time
        severity:
          type: string
          enum: [Critical, High, Medium, Low, Informational]
        category:
          type: string
          enum: [Theft, Vandalism, Trespassing, Medical, Fire, Hazard, Suspicious Activity, Other]
        description:
          type: string
          minLength: 20
        location_details:
          type: string
        actions_taken:
          type: string
        police_notified:
          type: boolean
        police_report_number:
          type: string
        client_notified:
          type: boolean

    Site:
      type: object
      properties:
        name:
          type: string
        site_id:
          type: string
        address:
          type: object
          properties:
            street:
              type: string
            city:
              type: string
            province:
              type: string
            postal_code:
              type: string
            country:
              type: string
        client:
          type: string
          description: Client company name
        site_type:
          type: string
          enum: [Commercial Office, Healthcare, Government, Cannabis, Logistics, Retail, Residential, Industrial]
        operational_status:
          type: string
          enum: [Active, Inactive, Setup, Terminated]
        guard_count:
          type: integer
          description: Number of guards assigned
        patrol_checkpoints:
          type: array
          items:
            type: object
            properties:
              checkpoint_id:
                type: string
              name:
                type: string
              location:
                type: string
              nfc_tag_id:
                type: string
              expected_frequency:
                type: string
                description: Expected visit frequency (e.g., "hourly")
        emergency_contacts:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              title:
                type: string
              phone:
                type: string
              email:
                type: string
              priority:
                type: integer

    Shift:
      type: object
      properties:
        shift_id:
          type: string
        guard:
          type: string
        site:
          type: string
        start_time:
          type: string
          format: date-time
        end_time:
          type: string
          format: date-time
        shift_type:
          type: string
          enum: [Regular, Overtime, On-Call, Training]
        status:
          type: string
          enum: [Scheduled, In Progress, Completed, Cancelled, No Show]
        patrol_route:
          type: string
          description: Assigned patrol route
        special_instructions:
          type: string

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            type: object
            properties:
              exception:
                type: string
              message:
                type: string
              _server_messages:
                type: string
    
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: Not authorized
    
    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: Insufficient permissions for this operation
    
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              message:
                type: string
                example: Resource not found
```

## 2.2 GraphQL Federation Schemas

### Unified GraphQL Gateway Schema

**schema.graphql**
```graphql
"""
Iron Horse Security - Unified GraphQL Schema
Federation gateway combining ERPNext, Keycloak, ZoneMinder, and custom services
"""

schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

# Root Query Type
type Query {
  # Guard operations
  guard(id: ID!): Guard
  guards(
    filter: GuardFilter
    limit: Int = 20
    offset: Int = 0
    sort: GuardSort
  ): GuardConnection!
  
  # Patrol operations
  patrol(id: ID!): Patrol
  currentPatrols(siteId: ID): [Patrol!]!
  patrolHistory(
    guardId: ID
    siteId: ID
    startDate: DateTime!
    endDate: DateTime!
  ): [Patrol!]!
  
  # Incident operations
  incident(id: ID!): Incident
  incidents(
    filter: IncidentFilter
    limit: Int = 20
    offset: Int = 0
    sort: IncidentSort
  ): IncidentConnection!
  
  # Site operations
  site(id: ID!): Site
  sites(clientId: ID): [Site!]!
  
  # Schedule operations
  shift(id: ID!): Shift
  myShifts(startDate: DateTime!, endDate: DateTime!): [Shift!]!
  siteSchedule(siteId: ID!, date: Date!): [Shift!]!
  
  # Video surveillance
  camera(id: ID!): Camera
  cameras(siteId: ID!): [Camera!]!
  liveStream(cameraId: ID!): StreamURL!
  recordedVideo(
    cameraId: ID!
    startTime: DateTime!
    endTime: DateTime!
  ): [VideoClip!]!
  
  # Analytics
  siteAnalytics(siteId: ID!, period: Period!): SiteAnalytics!
  guardPerformance(guardId: ID!, period: Period!): GuardPerformance!
  incidentTrends(period: Period!): IncidentTrends!
  
  # Client portal
  clientDashboard(clientId: ID!): ClientDashboard!
  clientReports(clientId: ID!, reportType: ReportType!): [Report!]!
  
  # Current user context
  me: User!
}

# Root Mutation Type
type Mutation {
  # Guard operations
  createGuard(input: CreateGuardInput!): Guard!
  updateGuard(id: ID!, input: UpdateGuardInput!): Guard!
  deactivateGuard(id: ID!): Guard!
  
  # Patrol operations
  startPatrol(input: StartPatrolInput!): Patrol!
  submitCheckpoint(input: CheckpointInput!): CheckpointLog!
  endPatrol(patrolId: ID!): Patrol!
  
  # Incident operations
  createIncident(input: CreateIncidentInput!): Incident!
  updateIncident(id: ID!, input: UpdateIncidentInput!): Incident!
  reviewIncident(id: ID!, input: IncidentReviewInput!): Incident!
  
  # Schedule operations
  createShift(input: CreateShiftInput!): Shift!
  updateShift(id: ID!, input: UpdateShiftInput!): Shift!
  cancelShift(id: ID!, reason: String!): Shift!
  
  # Camera operations
  startRecording(cameraId: ID!): Camera!
  stopRecording(cameraId: ID!): Camera!
  archiveVideo(videoId: ID!): VideoClip!
  
  # Authentication
  login(username: String!, password: String!): AuthPayload!
  refreshToken(token: String!): AuthPayload!
  logout: Boolean!
}

# Root Subscription Type
type Subscription {
  # Real-time patrol updates
  patrolUpdated(siteId: ID): Patrol!
  checkpointScanned(siteId: ID): CheckpointLog!
  
  # Real-time incident alerts
  incidentCreated(siteId: ID, severity: IncidentSeverity): Incident!
  incidentUpdated(incidentId: ID!): Incident!
  
  # Live camera feeds
  cameraFeed(cameraId: ID!): CameraFrame!
  cameraAlert(siteId: ID, alertType: AlertType): CameraAlert!
  
  # System notifications
  notification(userId: ID!): Notification!
  
  # Schedule changes
  shiftChanged(guardId: ID): Shift!
}

# Core Types

type Guard implements Node {
  id: ID!
  employeeId: String!
  firstName: String!
  lastName: String!
  fullName: String!
  email: String!
  phone: String
  status: GuardStatus!
  hireDate: Date!
  
  # Certifications
  certifications: [Certification!]!
  certificationsExpiringSoon: [Certification!]!
  
  # Performance metrics
  performanceScore: Float
  patrolCompletionRate: Float
  incidentReportQuality: Float
  clientSatisfactionScore: Float
  
  # Assignments
  assignedSites: [Site!]!
  currentShift: Shift
  upcomingShifts(limit: Int = 5): [Shift!]!
  
  # Training
  completedCourses: [Course!]!
  requiredCourses: [Course!]!
  trainingHours: Int!
  
  # Relations
  incidents(limit: Int = 10): [Incident!]!
  patrols(
    startDate: DateTime
    endDate: DateTime
    limit: Int = 20
  ): [Patrol!]!
  
  # Keycloak integration
  keycloakUserId: String
  roles: [String!]!
  groups: [String!]!
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
  createdBy: User
  modifiedBy: User
}

type Site implements Node {
  id: ID!
  siteId: String!
  name: String!
  client: Client!
  siteType: SiteType!
  status: SiteStatus!
  
  # Location
  address: Address!
  coordinates: Coordinates
  timezone: String!
  
  # Operations
  guardsOnDuty: [Guard!]!
  activePatrols: [Patrol!]!
  currentShifts: [Shift!]!
  
  # Infrastructure
  cameras: [Camera!]!
  accessPoints: [AccessPoint!]!
  checkpoints: [Checkpoint!]!
  
  # Analytics
  incidentCount(period: Period!): Int!
  patrolCompletionRate(period: Period!): Float!
  responseTime(period: Period!): Duration!
  
  # Edge infrastructure
  edgeClusterId: String
  edgeClusterStatus: EdgeClusterStatus
  
  # Configuration
  operatingHours: OperatingHours!
  emergencyContacts: [EmergencyContact!]!
  specialInstructions: String
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Patrol implements Node {
  id: ID!
  guard: Guard!
  site: Site!
  shift: Shift
  
  # Timing
  startTime: DateTime!
  endTime: DateTime
  duration: Duration
  
  # Status
  status: PatrolStatus!
  completionPercentage: Float!
  
  # Route
  route: PatrolRoute!
  checkpoints: [CheckpointLog!]!
  missedCheckpoints: [Checkpoint!]!
  
  # Location tracking
  gpsTrack: [GPSPoint!]!
  currentLocation: GPSPoint
  
  # Observations
  observations: String
  incidents: [Incident!]!
  photos: [Attachment!]!
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
}

type CheckpointLog implements Node {
  id: ID!
  patrol: Patrol!
  checkpoint: Checkpoint!
  guard: Guard!
  
  # Timing
  scanTime: DateTime!
  expectedTime: DateTime
  status: CheckpointStatus!
  
  # Location
  location: GPSPoint
  accuracy: Float
  
  # Data
  notes: String
  attachments: [Attachment!]!
  
  # Verification
  nfcTagId: String
  qrCodeData: String
  verificationMethod: VerificationMethod!
  
  # Metadata
  createdAt: DateTime!
}

type Incident implements Node {
  id: ID!
  incidentId: String!
  site: Site!
  reportedBy: Guard!
  
  # Classification
  severity: IncidentSeverity!
  category: IncidentCategory!
  title: String!
  description: String!
  
  # Timing
  incidentTime: DateTime!
  reportTime: DateTime!
  responseTime: Duration
  resolutionTime: Duration
  
  # Location
  locationDetails: String!
  coordinates: GPSPoint
  
  # People involved
  witnesses: [Witness!]!
  involvedParties: [InvolvedParty!]!
  
  # Actions
  actionsTaken: String!
  policeNotified: Boolean!
  policeReportNumber: String
  clientNotified: Boolean!
  
  # Evidence
  attachments: [Attachment!]!
  relatedVideos: [VideoClip!]!
  
  # Workflow
  status: IncidentStatus!
  supervisorReview: SupervisorReview
  clientFeedback: ClientFeedback
  
  # Related
  relatedIncidents: [Incident!]!
  followUpActions: [FollowUpAction!]!
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
  closedAt: DateTime
}

type Shift implements Node {
  id: ID!
  guard: Guard!
  site: Site!
  
  # Timing
  startTime: DateTime!
  endTime: DateTime!
  duration: Duration!
  
  # Type
  shiftType: ShiftType!
  status: ShiftStatus!
  
  # Assignment
  patrolRoute: PatrolRoute
  specialInstructions: String
  
  # Execution
  actualStartTime: DateTime
  actualEndTime: DateTime
  patrol: Patrol
  
  # Incidents during shift
  incidents: [Incident!]!
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
  createdBy: User!
}

type Camera implements Node {
  id: ID!
  cameraId: String!
  name: String!
  site: Site!
  
  # Configuration
  type: CameraType!
  manufacturer: String
  model: String
  firmware: String
  
  # Location
  location: String!
  coordinates: GPSPoint
  viewDirection: Float
  coverageArea: Polygon
  
  # Streaming
  status: CameraStatus!
  streamUrl: StreamURL
  liveViewUrl: String
  
  # Recording
  recordingEnabled: Boolean!
  retentionDays: Int!
  storageUsed: Int!
  
  # Analytics
  aiEnabled: Boolean!
  motionDetection: Boolean!
  faceDetection: Boolean!
  licenseP lateRecognition: Boolean!
  
  # Events
  recentEvents(limit: Int = 10): [CameraEvent!]!
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
  lastOnline: DateTime
}

type Client implements Node {
  id: ID!
  name: String!
  industry: Industry!
  status: ClientStatus!
  
  # Contact
  primaryContact: Contact!
  billingContact: Contact
  
  # Sites
  sites: [Site!]!
  totalSites: Int!
  
  # Contracts
  activeContracts: [Contract!]!
  billingInfo: BillingInfo!
  
  # Portal access
  portalUsers: [User!]!
  portalEnabled: Boolean!
  
  # Analytics
  totalGuards: Int!
  totalIncidents(period: Period!): Int!
  satisfaction Score: Float
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Supporting Types

type Certification {
  type: CertificationType!
  number: String!
  issueDate: Date!
  expiryDate: Date!
  issuer: String!
  status: CertificationStatus!
  daysUntilExpiry: Int!
  documentUrl: String
}

type Address {
  street: String!
  city: String!
  province: String!
  postalCode: String!
  country: String!
}

type Coordinates {
  latitude: Float!
  longitude: Float!
}

type GPSPoint {
  latitude: Float!
  longitude: Float!
  altitude: Float
  accuracy: Float
  timestamp: DateTime!
}

type OperatingHours {
  monday: DayHours
  tuesday: DayHours
  wednesday: DayHours
  thursday: DayHours
  friday: DayHours
  saturday: DayHours
  sunday: DayHours
  holidays: [Holiday!]
}

type DayHours {
  open: Time!
  close: Time!
  is24Hour: Boolean!
}

type EmergencyContact {
  name: String!
  title: String!
  phone: String!
  email: String
  priority: Int!
}

type PatrolRoute {
  name: String!
  checkpoints: [Checkpoint!]!
  estimatedDuration: Duration!
  instructions: String
}

type Checkpoint {
  id: ID!
  name: String!
  location: String!
  coordinates: GPSPoint
  nfcTagId: String
  qrCode: String
  expectedFrequency: Duration!
}

type Attachment {
  id: ID!
  fileName: String!
  fileType: AttachmentType!
  fileSize: Int!
  url: String!
  thumbnail: String
  uploadedAt: DateTime!
  uploadedBy: User!
}

type VideoClip {
  id: ID!
  camera: Camera!
  startTime: DateTime!
  endTime: DateTime!
  duration: Duration!
  fileSize: Int!
  url: String!
  thumbnailUrl: String
  status: VideoStatus!
}

type SupervisorReview {
  reviewedBy: User!
  reviewDate: DateTime!
  comments: String
  approved: Boolean!
  recommendations: String
}

type ClientFeedback {
  providedBy: User!
  date: DateTime!
  rating: Int!
  comments: String
}

type User implements Node {
  id: ID!
  username: String!
  email: String!
  firstName: String
  lastName: String
  fullName: String!
  
  # Authentication
  keycloakId: String!
  roles: [String!]!
  groups: [String!]!
  permissions: [String!]!
  
  # Profile
  phone: String
  timezone: String
  language: String
  
  # Relations
  guard: Guard
  clientOrganization: Client
  
  # Activity
  lastLogin: DateTime
  lastActivity: DateTime
  
  # Metadata
  createdAt: DateTime!
  updatedAt: DateTime!
}

type AuthPayload {
  token: String!
  refreshToken: String!
  expiresIn: Int!
  user: User!
}

# Enums

enum GuardStatus {
  ACTIVE
  INACTIVE
  ON_LEAVE
  PROBATION
  TERMINATED
}

enum CertificationType {
  SECURITY_LICENSE
  FIRST_AID
  CPR
  CCTV_OPERATIONS
  ACCESS_CONTROL
  FIRE_SAFETY
  EMERGENCY_RESPONSE
  HEALTHCARE_SECURITY
  CANNABIS_SECURITY
}

enum CertificationStatus {
  VALID
  EXPIRING_SOON
  EXPIRED
  PENDING_RENEWAL
}

enum SiteType {
  COMMERCIAL_OFFICE
  HEALTHCARE
  GOVERNMENT
  CANNABIS
  LOGISTICS
  RETAIL
  RESIDENTIAL
  INDUSTRIAL
  EDUCATIONAL
}

enum SiteStatus {
  ACTIVE
  INACTIVE
  SETUP
  SUSPENDED
  TERMINATED
}

enum PatrolStatus {
  SCHEDULED
  IN_PROGRESS
  COMPLETED
  ABANDONED
  INTERRUPTED
}

enum CheckpointStatus {
  ON_TIME
  EARLY
  LATE
  MISSED
}

enum VerificationMethod {
  NFC
  QR_CODE
  GPS
  MANUAL
}

enum IncidentSeverity {
  CRITICAL
  HIGH
  MEDIUM
  LOW
  INFORMATIONAL
}

enum IncidentCategory {
  THEFT
  VANDALISM
  TRESPASSING
  MEDICAL_EMERGENCY
  FIRE
  HAZARD
  SUSPICIOUS_ACTIVITY
  WORKPLACE_VIOLENCE
  PROPERTY_DAMAGE
  OTHER
}

enum IncidentStatus {
  OPEN
  UNDER_INVESTIGATION
  AWAITING_CLIENT_RESPONSE
  RESOLVED
  CLOSED
}

enum ShiftType {
  REGULAR
  OVERTIME
  ON_CALL
  TRAINING
  EMERGENCY
}

enum ShiftStatus {
  SCHEDULED
  IN_PROGRESS
  COMPLETED
  CANCELLED
  NO_SHOW
}

enum CameraType {
  FIXED
  PTZ
  DOME
  BULLET
  FISHEYE
}

enum CameraStatus {
  ONLINE
  OFFLINE
  RECORDING
  ERROR
  MAINTENANCE
}

enum Period {
  TODAY
  WEEK
  MONTH
  QUARTER
  YEAR
  CUSTOM
}

# Input Types

input CreateGuardInput {
  firstName: String!
  lastName: String!
  email: String!
  phone: String
  employeeId: String!
  hireDate: Date!
}

input UpdateGuardInput {
  phone: String
  status: GuardStatus
  assignedSites: [ID!]
}

input StartPatrolInput {
  guardId: ID!
  siteId: ID!
  routeId: ID!
  shiftId: ID
}

input CheckpointInput {
  patrolId: ID!
  checkpointId: ID!
  scanTime: DateTime!
  location: GPSPointInput!
  notes: String
  attachments: [AttachmentUpload!]
}

input GPSPointInput {
  latitude: Float!
  longitude: Float!
  accuracy: Float
}

input CreateIncidentInput {
  siteId: ID!
  incidentTime: DateTime!
  severity: IncidentSeverity!
  category: IncidentCategory!
  title: String!
  description: String!
  locationDetails: String!
  actionsTaken: String!
  policeNotified: Boolean
  policeReportNumber: String
}

input UpdateIncidentInput {
  severity: IncidentSeverity
  description: String
  actionsTaken: String
  status: IncidentStatus
}

input IncidentReviewInput {
  comments: String!
  approved: Boolean!
  recommendations: String
}

input CreateShiftInput {
  guardId: ID!
  siteId: ID!
  startTime: DateTime!
  endTime: DateTime!
  shiftType: ShiftType!
  routeId: ID
  specialInstructions: String
}

input UpdateShiftInput {
  startTime: DateTime
  endTime: DateTime
  guardId: ID
  specialInstructions: String
}

# Pagination

type GuardConnection {
  edges: [GuardEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type GuardEdge {
  cursor: String!
  node: Guard!
}

type IncidentConnection {
  edges: [IncidentEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type IncidentEdge {
  cursor: String!
  node: Incident!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Interfaces

interface Node {
  id: ID!
}

# Scalars

scalar DateTime
scalar Date
scalar Time
scalar Duration
scalar JSON
```

## 2.3 Event Stream Definitions (Kafka / MQTT)

### Kafka Topic Schema Registry

**kafka-topics.yaml**
```yaml
topics:
  - name: patrol.checkpoint
    description: Real-time patrol checkpoint scans
    partitions: 6
    replication_factor: 3
    retention_ms: 2592000000  # 30 days
    schema:
      type: avro
      definition: |
        {
          "type": "record",
          "name": "CheckpointScan",
          "namespace": "com.ironhorsesecurity.patrol",
          "fields": [
            {"name": "patrol_id", "type": "string"},
            {"name": "checkpoint_id", "type": "string"},
            {"name": "guard_id", "type": "string"},
            {"name": "site_id", "type": "string"},
            {"name": "scan_time", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "location", "type": {
              "type": "record",
              "name": "Location",
              "fields": [
                {"name": "latitude", "type": "double"},
                {"name": "longitude", "type": "double"},
                {"name": "accuracy", "type": "float"}
              ]
            }},
            {"name": "status", "type": {"type": "enum", "name": "CheckpointStatus", "symbols": ["ON_TIME", "EARLY", "LATE", "MISSED"]}},
            {"name": "notes", "type": ["null", "string"], "default": null},
            {"name": "attachment_urls", "type": {"type": "array", "items": "string"}, "default": []},
            {"name": "device_id", "type": "string"},
            {"name": "event_timestamp", "type": "long", "logicalType": "timestamp-millis"}
          ]
        }

  - name: training.completion
    description: Training course completion events
    partitions: 3
    replication_factor: 3
    retention_ms: 7776000000  # 90 days
    schema:
      type: avro
      definition: |
        {
          "type": "record",
          "name": "TrainingCompletion",
          "namespace": "com.ironhorsesecurity.training",
          "fields": [
            {"name": "guard_id", "type": "string"},
            {"name": "course_id", "type": "string"},
            {"name": "course_name", "type": "string"},
            {"name": "completion_date", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "score", "type": "int"},
            {"name": "passed", "type": "boolean"},
            {"name": "certificate_id", "type": ["null", "string"], "default": null},
            {"name": "expiry_date", "type": ["null", "long"], "logicalType": "timestamp-millis", "default": null},
            {"name": "certification_type", "type": ["null", "string"], "default": null},
            {"name": "event_timestamp", "type": "long", "logicalType": "timestamp-millis"}
          ]
        }

  - name: incident.created
    description: New incident reports
    partitions: 6
    replication_factor: 3
    retention_ms: 31536000000  # 365 days
    schema:
      type: avro
      definition: |
        {
          "type": "record",
          "name": "IncidentCreated",
          "namespace": "com.ironhorsesecurity.incident",
          "fields": [
            {"name": "incident_id", "type": "string"},
            {"name": "site_id", "type": "string"},
            {"name": "site_name", "type": "string"},
            {"name": "client_id", "type": "string"},
            {"name": "reported_by", "type": "string"},
            {"name": "incident_time", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "report_time", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "severity", "type": {"type": "enum", "name": "Severity", "symbols": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"]}},
            {"name": "category", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "description", "type": "string"},
            {"name": "location_details", "type": "string"},
            {"name": "police_notified", "type": "boolean"},
            {"name": "client_notified", "type": "boolean"},
            {"name": "attachment_count", "type": "int"},
            {"name": "event_timestamp", "type": "long", "logicalType": "timestamp-millis"}
          ]
        }

  - name: hr.attendance
    description: Guard clock in/out events
    partitions: 6
    replication_factor: 3
    retention_ms: 7776000000  # 90 days
    schema:
      type: avro
      definition: |
        {
          "type": "record",
          "name": "AttendanceEvent",
          "namespace": "com.ironhorsesecurity.hr",
          "fields": [
            {"name": "guard_id", "type": "string"},
            {"name": "site_id", "type": "string"},
            {"name": "shift_id", "type": "string"},
            {"name": "event_type", "type": {"type": "enum", "name": "EventType", "symbols": ["CLOCK_IN", "CLOCK_OUT", "BREAK_START", "BREAK_END"]}},
            {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "location", "type": {
              "type": "record",
              "name": "Location",
              "fields": [
                {"name": "latitude", "type": "double"},
                {"name": "longitude", "type": "double"}
              ]
            }},
            {"name": "verification_method", "type": {"type": "enum", "name": "VerificationMethod", "symbols": ["NFC", "QR", "BIOMETRIC", "MANUAL"]}},
            {"name": "device_id", "type": "string"},
            {"name": "event_timestamp", "type": "long", "logicalType": "timestamp-millis"}
          ]
        }

  - name: camera.alert
    description: AI-generated camera alerts
    partitions: 12
    replication_factor: 3
    retention_ms: 2592000000  # 30 days
    schema:
      type: avro
      definition: |
        {
          "type": "record",
          "name": "CameraAlert",
          "namespace": "com.ironhorsesecurity.camera",
          "fields": [
            {"name": "alert_id", "type": "string"},
            {"name": "camera_id", "type": "string"},
            {"name": "site_id", "type": "string"},
            {"name": "alert_type", "type": {"type": "enum", "name": "AlertType", "symbols": ["MOTION", "PERSON_DETECTED", "LOITERING", "CROWD_FORMATION", "VEHICLE_DETECTED", "LICENSE_PLATE", "OBJECT_LEFT", "PERIMETER_BREACH"]}},
            {"name": "confidence", "type": "float"},
            {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
            {"name": "snapshot_url", "type": "string"},
            {"name": "video_clip_url", "type": ["null", "string"], "default": null},
            {"name": "metadata", "type": "string"},  # JSON-encoded additional data
            {"name": "event_timestamp", "type": "long", "logicalType": "timestamp-millis"}
          ]
        }

  - name: system.audit
    description: Audit trail for all system actions
    partitions: 12
    replication_factor: 3
    retention_ms: 31536000000  # 365 days
    cleanup_policy: compact
    schema:
      type: avro
      definition: |
        {
          "type": "record",
          "name": "AuditEvent",
          "namespace": "com.ironhorsesecurity.audit",
          "fields": [
            {"name": "event_id", "type": "string"},
            {"name": "user_id", "type": "string"},
            {"name": "user_email", "type": "string"},
            {"name": "action", "type": "string"},
            {"name": "resource_type", "type": "string"},
            {"name": "resource_id", "type": "string"},
            {"name": "changes", "type": "string"},  # JSON-encoded before/after
            {"name": "ip_address", "type": "string"},
            {"name": "user_agent", "type": "string"},
            {"name": "session_id", "type": "string"},
            {"name": "success", "type": "boolean"},
            {"name": "error_message", "type": ["null", "string"], "default": null},
            {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"}
          ]
        }
```

### MQTT Topic Structure

**mqtt-topics.yaml**
```yaml
mqtt:
  broker: mosquitto
  port: 8883  # TLS
  auth: username_password
  
  topics:
    # IoT Sensor Data
    - topic: ironhorse/{site_id}/sensors/{sensor_id}/temperature
      qos: 1
      retain: true
      description: Temperature sensor readings
      payload_format: JSON
      example: |
        {
          "sensor_id": "temp_001",
          "value": 22.5,
          "unit": "celsius",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    - topic: ironhorse/{site_id}/sensors/{sensor_id}/motion
      qos: 1
      retain: false
      description: Motion sensor triggers
      payload_format: JSON
      example: |
        {
          "sensor_id": "pir_002",
          "motion_detected": true,
          "zone": "loading_dock",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    - topic: ironhorse/{site_id}/sensors/{sensor_id}/door
      qos: 1
      retain: true
      description: Door/window sensor status
      payload_format: JSON
      example: |
        {
          "sensor_id": "door_003",
          "state": "open",
          "door_name": "Main Entrance",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    # Access Control Events
    - topic: ironhorse/{site_id}/access/{reader_id}/event
      qos: 2
      retain: false
      description: Access control reader events
      payload_format: JSON
      example: |
        {
          "reader_id": "reader_main_door",
          "event_type": "access_granted",
          "credential_id": "badge_1234",
          "user_id": "guard_567",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    # Camera Events
    - topic: ironhorse/{site_id}/camera/{camera_id}/motion
      qos: 1
      retain: false
      description: Camera motion detection
      payload_format: JSON
      example: |
        {
          "camera_id": "cam_parking_01",
          "motion_detected": true,
          "zone": "parking_lot",
          "snapshot_url": "https://...",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    # NFC Checkpoint Scans
    - topic: ironhorse/{site_id}/checkpoint/{checkpoint_id}/scan
      qos: 2
      retain: false
      description: Guard checkpoint NFC scans
      payload_format: JSON
      example: |
        {
          "checkpoint_id": "nfc_lobby_01",
          "guard_id": "guard_567",
          "scan_time": "2024-01-15T10:30:00Z",
          "tag_id": "04:5E:3A:12:34:80"
        }
    
    # Guard Device Heartbeat
    - topic: ironhorse/guards/{guard_id}/heartbeat
      qos: 1
      retain: true
      description: Guard mobile device heartbeat
      payload_format: JSON
      example: |
        {
          "guard_id": "guard_567",
          "device_id": "mobile_android_123",
          "location": {
            "latitude": 45.4215,
            "longitude": -75.6972,
            "accuracy": 10.5
          },
          "battery_level": 75,
          "network_type": "4G",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    # System Commands (Edge Ã¢â€ ' Devices)
    - topic: ironhorse/{site_id}/commands/{device_id}
      qos: 2
      retain: false
      description: Commands sent to IoT devices
      payload_format: JSON
      example: |
        {
          "command": "unlock_door",
          "target_device": "lock_main_entrance",
          "duration_seconds": 10,
          "issued_by": "guard_567",
          "timestamp": "2024-01-15T10:30:00Z"
        }
    
    # System Status
    - topic: ironhorse/{site_id}/system/status
      qos: 1
      retain: true
      description: Edge system health status
      payload_format: JSON
      example: |
        {
          "site_id": "site_001",
          "services": {
            "zoneminder": "running",
            "openhab": "running",
            "nodered": "running",
            "mqtt": "running"
          },
          "cpu_usage": 45.2,
          "memory_usage": 62.8,
          "disk_usage": 71.5,
          "uptime_seconds": 1234567,
          "timestamp": "2024-01-15T10:30:00Z"
        }
```

---

# 3. DevSecOps Pipeline

## 3.1 GitLab CI/CD Configuration

**.gitlab-ci.yml** (Root Pipeline)
```yaml
# Iron Horse Security - Master CI/CD Pipeline
# Supports multi-project deployments with security scanning

stages:
  - validate
  - test
  - security
  - build
  - deploy_staging
  - integration_test
  - deploy_production
  - monitoring

variables:
  # Docker registry
  DOCKER_REGISTRY: registry.ironhorsesecurity.com
  DOCKER_DRIVER: overlay2
  
  # Kubernetes
  KUBE_NAMESPACE_STAGING: ironhorse-staging
  KUBE_NAMESPACE_PRODUCTION: ironhorse-platform
  
  # SonarQube
  SONAR_HOST_URL: https://sonar.ironhorsesecurity.com
  SONAR_PROJECT_KEY: ironhorse-platform
  
  # Trivy
  TRIVY_SEVERITY: CRITICAL,HIGH
  TRIVY_NO_PROGRESS: "true"
  
  # Vault
  VAULT_ADDR: https://vault.ironhorsesecurity.com
  
  # Feature flags
  ENABLE_SAST: "true"
  ENABLE_DAST: "true"
  ENABLE_CONTAINER_SCANNING: "true"
  ENABLE_IaC_SCANNING: "true"
  
  # Slack notifications
  SLACK_WEBHOOK_URL: $CI_SLACK_WEBHOOK

# Templates
.docker_login: &docker_login
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin $DOCKER_REGISTRY

.kubectl_config: &kubectl_config
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_URL"
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab --namespace=$KUBE_NAMESPACE
    - kubectl config use-context default

# Validation Stage
validate:yaml:
  stage: validate
  image: cytopia/yamllint:latest
  script:
    - yamllint -c .yamllint.yml .
  only:
    changes:
      - "**/*.yaml"
      - "**/*.yml"

validate:helm:
  stage: validate
  image: alpine/helm:latest
  script:
    - helm lint charts/*
    - helm template charts/* --validate
  only:
    changes:
      - "charts/**/*"

validate:terraform:
  stage: validate
  image: hashicorp/terraform:latest
  script:
    - cd terraform
    - terraform init -backend=false
    - terraform validate
    - terraform fmt -check -recursive
  only:
    changes:
      - "terraform/**/*"

validate:ansible:
  stage: validate
  image: cytopia/ansible-lint:latest
  script:
    - ansible-lint playbooks/
  only:
    changes:
      - "ansible/**/*"

# Test Stage
test:python:
  stage: test
  image: python:3.11
  before_script:
    - pip install -r requirements-test.txt
  script:
    - pytest --cov=src --cov-report=xml --cov-report=term
    - coverage xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  only:
    changes:
      - "src/**/*.py"
      - "tests/**/*.py"

test:nodejs:
  stage: test
  image: node:20-alpine
  before_script:
    - npm ci
  script:
    - npm run lint
    - npm run test:unit
    - npm run test:integration
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  only:
    changes:
      - "frontend/**/*.js"
      - "frontend/**/*.ts"

# Security Scanning Stage
sast:sonarqube:
  stage: security
  image: sonarsource/sonar-scanner-cli:latest
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
    GIT_DEPTH: "0"
  cache:
    key: "${CI_JOB_NAME}"
    paths:
      - .sonar/cache
  script:
    - sonar-scanner
        -Dsonar.projectKey=$SONAR_PROJECT_KEY
        -Dsonar.sources=.
        -Dsonar.host.url=$SONAR_HOST_URL
        -Dsonar.token=$SONAR_TOKEN
        -Dsonar.python.coverage.reportPaths=coverage.xml
        -Dsonar.javascript.lcov.reportPaths=coverage/lcov.info
  allow_failure: false
  only:
    - main
    - develop
    - merge_requests

sast:semgrep:
  stage: security
  image: returntocorp/semgrep:latest
  script:
    - semgrep --config=auto --json --output=semgrep-results.json .
    - semgrep --config=auto --sarif --output=semgrep-results.sarif .
  artifacts:
    reports:
      sast: semgrep-results.sarif
    paths:
      - semgrep-results.json
    expire_in: 1 week
  allow_failure: true

secret_detection:
  stage: security
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog filesystem . --json --fail > trufflehog-results.json || true
    - |
      if [ -s trufflehog-results.json ]; then
        echo "âš ï¸  Secrets detected in code!"
        cat trufflehog-results.json
        exit 1
      fi
  artifacts:
    paths:
      - trufflehog-results.json
    expire_in: 1 week
  allow_failure: false

iac_scanning:checkov:
  stage: security
  image: bridgecrew/checkov:latest
  script:
    - checkov --directory . --output junitxml --output-file-path checkov-results.xml
    - checkov --directory . --framework terraform --soft-fail
    - checkov --directory . --framework kubernetes --soft-fail
    - checkov --directory . --framework dockerfile --soft-fail
  artifacts:
    reports:
      junit: checkov-results.xml
    paths:
      - checkov-results.xml
    expire_in: 1 week
  allow_failure: true
  only:
    changes:
      - "terraform/**/*"
      - "**/*.dockerfile"
      - "**/Dockerfile"
      - "charts/**/*"

# Build Stage
build:docker:backend:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  <<: *docker_login
  script:
    - |
      docker build \
        --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
        --build-arg VCS_REF=$CI_COMMIT_SHORT_SHA \
        --build-arg VERSION=$CI_COMMIT_TAG \
        --tag $DOCKER_REGISTRY/ironhorse-backend:$CI_COMMIT_SHORT_SHA \
        --tag $DOCKER_REGISTRY/ironhorse-backend:latest \
        -f docker/Dockerfile.backend .
    - docker push $DOCKER_REGISTRY/ironhorse-backend:$CI_COMMIT_SHORT_SHA
    - docker push $DOCKER_REGISTRY/ironhorse-backend:latest
  only:
    changes:
      - "backend/**/*"
      - "docker/Dockerfile.backend"

build:docker:frontend:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  <<: *docker_login
  script:
    - |
      docker build \
        --build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
        --build-arg VCS_REF=$CI_COMMIT_SHORT_SHA \
        --build-arg VERSION=$CI_COMMIT_TAG \
        --tag $DOCKER_REGISTRY/ironhorse-frontend:$CI_COMMIT_SHORT_SHA \
        --tag $DOCKER_REGISTRY/ironhorse-frontend:latest \
        -f docker/Dockerfile.frontend .
    - docker push $DOCKER_REGISTRY/ironhorse-frontend:$CI_COMMIT_SHORT_SHA
    - docker push $DOCKER_REGISTRY/ironhorse-frontend:latest
  only:
    changes:
      - "frontend/**/*"
      - "docker/Dockerfile.frontend"

container_scanning:trivy:
  stage: security
  image: aquasec/trivy:latest
  dependencies:
    - build:docker:backend
    - build:docker:frontend
  script:
    - trivy image --severity $TRIVY_SEVERITY --exit-code 1 --no-progress $DOCKER_REGISTRY/ironhorse-backend:$CI_COMMIT_SHORT_SHA
    - trivy image --severity $TRIVY_SEVERITY --exit-code 1 --no-progress $DOCKER_REGISTRY/ironhorse-frontend:$CI_COMMIT_SHORT_SHA
    - trivy image --format template --template "@contrib/gitlab.tpl" -o trivy-container-scanning.json $DOCKER_REGISTRY/ironhorse-backend:$CI_COMMIT_SHORT_SHA
  artifacts:
    reports:
      container_scanning: trivy-container-scanning.json
  allow_failure: false

# Deploy Staging
deploy:staging:
  stage: deploy_staging
  image: alpine/helm:latest
  <<: *kubectl_config
  environment:
    name: staging
    url: https://staging.ironhorsesecurity.com
    on_stop: cleanup:staging
  script:
    - |
      helm upgrade --install ironhorse-platform ./charts/ironhorse-platform \
        --namespace $KUBE_NAMESPACE_STAGING \
        --create-namespace \
        --set image.tag=$CI_COMMIT_SHORT_SHA \
        --set ingress.host=staging.ironhorsesecurity.com \
        --set replicas=2 \
        --values charts/ironhorse-platform/values-staging.yaml \
        --wait \
        --timeout 10m
    - kubectl rollout status deployment/ironhorse-backend -n $KUBE_NAMESPACE_STAGING
    - kubectl rollout status deployment/ironhorse-frontend -n $KUBE_NAMESPACE_STAGING
  only:
    - develop
  when: manual

# Integration Tests
integration_test:api:
  stage: integration_test
  image: postman/newman:alpine
  dependencies:
    - deploy:staging
  script:
    - newman run tests/postman/api-tests.json \
        --environment tests/postman/staging-env.json \
        --reporters cli,json \
        --reporter-json-export newman-results.json
  artifacts:
    reports:
      junit: newman-results.xml
    paths:
      - newman-results.json
    expire_in: 1 week
  only:
    - develop

dast:zap:
  stage: integration_test
  image: owasp/zap2docker-stable:latest
  dependencies:
    - deploy:staging
  script:
    - mkdir -p /zap/wrk
    - zap-baseline.py -t https://staging.ironhorsesecurity.com -r zap-baseline-report.html -J zap-baseline-report.json || true
  artifacts:
    paths:
      - zap-baseline-report.html
      - zap-baseline-report.json
    expire_in: 1 week
  allow_failure: true
  only:
    - develop

# Deploy Production
deploy:production:
  stage: deploy_production
  image: alpine/helm:latest
  <<: *kubectl_config
  environment:
    name: production
    url: https://erp.ironhorsesecurity.com
  script:
    - |
      helm upgrade --install ironhorse-platform ./charts/ironhorse-platform \
        --namespace $KUBE_NAMESPACE_PRODUCTION \
        --create-namespace \
        --set image.tag=$CI_COMMIT_TAG \
        --set ingress.host=erp.ironhorsesecurity.com \
        --set replicas=5 \
        --values charts/ironhorse-platform/values-production.yaml \
        --wait \
        --timeout 15m
    - kubectl rollout status deployment/ironhorse-backend -n $KUBE_NAMESPACE_PRODUCTION
    - kubectl rollout status deployment/ironhorse-frontend -n $KUBE_NAMESPACE_PRODUCTION
  only:
    - tags
  when: manual
  allow_failure: false

# Monitoring
deploy:grafana_dashboards:
  stage: monitoring
  image: alpine/helm:latest
  <<: *kubectl_config
  script:
    - kubectl apply -f monitoring/dashboards/ -n monitoring
  only:
    changes:
      - "monitoring/dashboards/**/*"

notify:slack:success:
  stage: .post
  image: curlimages/curl:latest
  script:
    - |
      curl -X POST $SLACK_WEBHOOK_URL \
        -H 'Content-Type: application/json' \
        -d "{
          \"text\": \"Ã¢Å“â€¦ Pipeline Success: $CI_PROJECT_NAME\",
          \"attachments\": [{
            \"color\": \"good\",
            \"fields\": [
              {\"title\": \"Branch\", \"value\": \"$CI_COMMIT_REF_NAME\", \"short\": true},
              {\"title\": \"Commit\", \"value\": \"$CI_COMMIT_SHORT_SHA\", \"short\": true},
              {\"title\": \"Author\", \"value\": \"$GITLAB_USER_NAME\", \"short\": true},
              {\"title\": \"Pipeline\", \"value\": \"<$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \"short\": true}
            ]
          }]
        }"
  when: on_success

notify:slack:failure:
  stage: .post
  image: curlimages/curl:latest
  script:
    - |
      curl -X POST $SLACK_WEBHOOK_URL \
        -H 'Content-Type: application/json' \
        -d "{
          \"text\": \"âŒ Pipeline Failed: $CI_PROJECT_NAME\",
          \"attachments\": [{
            \"color\": \"danger\",
            \"fields\": [
              {\"title\": \"Branch\", \"value\": \"$CI_COMMIT_REF_NAME\", \"short\": true},
              {\"title\": \"Commit\", \"value\": \"$CI_COMMIT_SHORT_SHA\", \"short\": true},
              {\"title\": \"Failed Job\", \"value\": \"$CI_JOB_NAME\", \"short\": true},
              {\"title\": \"Pipeline\", \"value\": \"<$CI_PIPELINE_URL|#$CI_PIPELINE_ID>\", \"short\": true}
            ]
          }]
        }"
  when: on_failure
```

## 3.2 ArgoCD Application Definitions

**argocd/ironhorse-platform.yaml**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ironhorse-platform
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: ironhorse
  
  source:
    repoURL: https://gitlab.ironhorsesecurity.com/platform/infrastructure.git
    targetRevision: HEAD
    path: charts/ironhorse-platform
    helm:
      valueFiles:
        - values-production.yaml
      parameters:
        - name: image.tag
          value: $ARGOCD_APP_REVISION
  
  destination:
    server: https://kubernetes.default.svc
    namespace: ironhorse-platform
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
  
  revisionHistoryLimit: 10
  
  info:
    - name: 'Documentation'
      value: 'https://docs.ironhorsesecurity.com/platform'
    - name: 'Grafana'
      value: 'https://metrics.ironhorsesecurity.com'
```

---

[View Full DevOps Implementation Guide](computer:///mnt/user-data/outputs/IHOSE_DevOps_Infrastructure_Implementation_Guide.md)

This completes the Data Flow, API Contracts, and DevSecOps Pipeline specifications for the Iron Horse Security IHOSE platform.


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/ihose-openvision-documentation-package|ihose-openvision-documentation-package]]

**Consolidated into:**
- [[docs/DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
