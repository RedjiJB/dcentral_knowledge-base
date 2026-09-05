---
source_project: D Central
source_project_uuid: 0197235f-e830-753a-966d-40f28b1d1fa2
doc_uuid: 246e0ca9-6b8d-41f8-b400-5d9afb3aa82d
original_filename: architecture_diagram.md
created_at: 2025-06-01T15:31:59.554169+00:00
content_hash: 43ab31edf7a3
---

# D Central Architecture Diagram

```mermaid
graph TB
    %% Main Containers
    subgraph "D Central Agent"
        Agent["Agent Process<br>(cmd/agent)"]
        Config["Configuration<br>(internal/config)"]
        Logging["Logging<br>(internal/logging)"]

        %% Core Modules
        subgraph "Core Modules (pkg)"
            MeshManager["Mesh Manager<br>(pkg/mesh)"]
            IdentityService["Identity Service<br>(pkg/identity)"]
            StorageManager["Storage Manager<br>(pkg/storage)"]
            ServiceRegistry["Service Registry<br>(pkg/services)"]
            TokenModule["Token Module<br>(pkg/token)"]
            AiModule["AI Module<br>(pkg/ai)"]
            DAOManager["DAO Manager<br>(pkg/dao)"]
            CommonLib["Common Utilities<br>(pkg/common)"]
        end
    end

    subgraph "Frontend"
        WebDashboard["Web Dashboard<br>(web/)"]
        ReactComponents["React Components<br>(web/src/components)"]
        Pages["Pages<br>(web/src/pages)"]
        Services["Frontend Services<br>(web/src/services)"]
        Hooks["Custom Hooks<br>(web/src/hooks)"]
    end

    subgraph "External Services"
        IPFS["IPFS Storage"]
        Blockchain["Blockchain<br>(Ethereum Compatible)"]
        SmartContracts["Smart Contracts"]
    end

    subgraph "CLI & Tooling"
        CLI["Command Line Interface<br>(cmd/cli)"]
        Scripts["Dev Scripts<br>(scripts/)"]
    end

    %% Connections within Agent
    Agent --> Config
    Agent --> Logging
    Agent --> MeshManager
    Agent --> IdentityService
    Agent --> StorageManager
    Agent --> ServiceRegistry
    Agent --> TokenModule

    %% Core Module Relationships
    MeshManager --> CommonLib
    IdentityService --> CommonLib
    StorageManager --> CommonLib
    ServiceRegistry --> CommonLib
    TokenModule --> CommonLib
    AiModule --> CommonLib
    DAOManager --> CommonLib

    %% External Connections
    StorageManager --> IPFS
    TokenModule --> Blockchain
    TokenModule --> SmartContracts
    DAOManager --> SmartContracts
    ServiceRegistry --> SmartContracts

    %% Frontend Connections
    WebDashboard --> ReactComponents
    WebDashboard --> Pages
    Pages --> Services
    Pages --> Hooks
    ReactComponents --> Services
    ReactComponents --> Hooks
    Services --> Agent
    
    %% CLI Connections
    CLI --> Config
    CLI --> Agent

    %% Deployment
    subgraph "Deployment"
        Docker["Docker<br>(docker/)"]
        DockerCompose["Docker Compose"]
    end
    
    Docker --> Agent
    Docker --> WebDashboard
    DockerCompose --> Docker

    %% Legend
    classDef core fill:#f9f,stroke:#333,stroke-width:2px
    classDef frontend fill:#bbf,stroke:#333,stroke-width:2px
    classDef external fill:#bfb,stroke:#333,stroke-width:2px
    classDef deployment fill:#fbb,stroke:#333,stroke-width:2px
    
    class Agent,Config,Logging,MeshManager,IdentityService,StorageManager,ServiceRegistry,TokenModule,AiModule,DAOManager,CommonLib core
    class WebDashboard,ReactComponents,Pages,Services,Hooks frontend
    class IPFS,Blockchain,SmartContracts external
    class Docker,DockerCompose deployment
```

## Component Descriptions

### D Central Agent
- **Agent Process**: The main entry point for the D Central node
- **Configuration**: Handles loading and managing application settings
- **Logging**: Provides structured logging capabilities

### Core Modules
- **Mesh Manager**: Handles peer-to-peer networking using libp2p
- **Identity Service**: Manages W3C DIDs for self-sovereign identity
- **Storage Manager**: Integrates with IPFS for decentralized storage
- **Service Registry**: Enables service discovery and provisioning
- **Token Module**: Manages blockchain interactions and token economics
- **AI Module**: Provides federated learning capabilities
- **DAO Manager**: Supports decentralized governance functionality
- **Common Utilities**: Shared utilities used across modules

### Frontend
- **Web Dashboard**: React-based user interface for interacting with the network
- **React Components**: Reusable UI components
- **Pages**: Application views and routes
- **Frontend Services**: API clients and data services
- **Custom Hooks**: React hooks for shared functionality

### External Services
- **IPFS Storage**: Decentralized content-addressed storage
- **Blockchain**: Ethereum-compatible chain for smart contracts
- **Smart Contracts**: Solidity contracts for governance and tokenomics

### CLI & Tooling
- **Command Line Interface**: Tools for interacting with the network
- **Dev Scripts**: Development and deployment utilities

### Deployment
- **Docker**: Containerization for the application components
- **Docker Compose**: Multi-container application orchestration