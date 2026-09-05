---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: c0c9d243-223a-4860-81e6-15248ba5700b
original_filename: IHOSE_Digital_Twin_Knowledge_Graph_Architecture.md
created_at: 2025-11-10T23:32:36.535790+00:00
content_hash: fad80a041235
---

# Iron Horse Security - Digital Twin & Knowledge Graph Architecture

**Version 1.0 - Advanced AI & Simulation Framework**

*Extends: IHOSE Complete Technical Specification v3.0 - Layer 6 Enhancement*

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Digital Twin Architecture](#2-digital-twin-architecture)
3. [Knowledge Graph Design](#3-knowledge-graph-design)
4. [Data Synchronization Pipeline](#4-data-synchronization-pipeline)
5. [Simulation & Predictive Analytics](#5-simulation--predictive-analytics)
6. [LLM Integration & Reasoning](#6-llm-integration--reasoning)
7. [Implementation & Deployment](#7-implementation--deployment)
8. [Use Cases & Applications](#8-use-cases--applications)

---

# 1. Executive Summary

## 1.1 Strategic Vision

The Digital Twin and Knowledge Graph framework transforms Iron Horse Security from a reactive security operations company into a **predictive, intelligent, self-optimizing enterprise** where every physical entityâ€”guards, sites, devices, incidents, assetsâ€”exists as a real-time digital representation within an interconnected semantic network.

This enables:
- **Predictive Operations**: Simulate "what-if" scenarios before deploying guards or equipment
- **Contextual Intelligence**: LLM assistants answer complex queries like "Which guard with healthcare certification is closest to Hospital Site A and available in the next 2 hours?"
- **Continuous Optimization**: Digital twins run 24/7 simulations to optimize patrol routes, shift schedules, and resource allocation
- **Regulatory Compliance**: Automated compliance verification through knowledge graph reasoning
- **Incident Prevention**: Predict security incidents before they occur using pattern recognition across the entire enterprise graph

## 1.2 Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Digital Twin Platform** | Eclipse Ditto + Apache IoT | Device-level twins with state synchronization |
| **Simulation Engine** | Unity Simulation Pro (open framework) + AnyLogic PLE | 3D visualization and predictive modeling |
| **Knowledge Graph** | Neo4j 5.x Enterprise | Entity relationship modeling and graph queries |
| **Vector Database** | Weaviate / Qdrant | Semantic embeddings for LLM context |
| **Graph Analytics** | Neo4j Graph Data Science | Pattern detection, pathfinding, centrality analysis |
| **LLM Integration** | Llama 3.1 70B + LangChain | Contextual reasoning over graph |
| **Time-Series DB** | TimescaleDB | Historical twin state tracking |
| **Message Bus** | Apache Kafka | Real-time twin updates |

## 1.3 Architecture Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                        Physical World                                â”‚
â”‚  Guards â”‚ Sites â”‚ Cameras â”‚ Sensors â”‚ Access Points â”‚ Vehicles      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚ Real-time Data Streams
                         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   Data Ingestion Layer (Kafka)                       â”‚
â”‚  ERPNext Events â”‚ IoT MQTT â”‚ ZoneMinder â”‚ Keycloak â”‚ Traccar        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â–¼                                  â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Digital Twins   â”‚              â”‚ Knowledge Graph  â”‚
â”‚  (Eclipse Ditto) â”‚â—„â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–ºâ”‚    (Neo4j)       â”‚
â”‚                  â”‚  Sync State  â”‚                  â”‚
â”‚ â€¢ Guard Twins    â”‚              â”‚ â€¢ Entity Nodes   â”‚
â”‚ â€¢ Site Twins     â”‚              â”‚ â€¢ Relationships  â”‚
â”‚ â€¢ Device Twins   â”‚              â”‚ â€¢ Properties     â”‚
â”‚ â€¢ Asset Twins    â”‚              â”‚ â€¢ Constraints    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜              â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚                                 â”‚
         â”‚                                 â”‚
         â–¼                                 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Intelligence Layer                                â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”              â”‚
â”‚  â”‚ Simulation   â”‚  â”‚   Graph      â”‚  â”‚     LLM      â”‚              â”‚
â”‚  â”‚   Engine     â”‚  â”‚  Analytics   â”‚  â”‚   Reasoning  â”‚              â”‚
â”‚  â”‚  (Unity)     â”‚  â”‚   (Neo4j)    â”‚  â”‚  (Llama 3)   â”‚              â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                         â”‚
                         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      Application Layer                               â”‚
â”‚  Predictive Dashboard â”‚ Optimization API â”‚ AI Assistant â”‚ Alerts    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

# 2. Digital Twin Architecture

## 2.1 Digital Twin Definition Framework

### Core Principles

Every entity in the Iron Horse ecosystem exists in three states:

1. **Physical Entity** - The real-world object (guard, camera, door sensor)
2. **Digital Twin** - Real-time synchronized virtual representation
3. **Predictive Shadow** - Simulated future states based on current trajectory

### Twin Taxonomy

```yaml
twin_types:
  person_twins:
    - guard_twin
    - supervisor_twin
    - client_contact_twin
  
  location_twins:
    - site_twin
    - building_twin
    - zone_twin
    - checkpoint_twin
  
  device_twins:
    - camera_twin
    - sensor_twin
    - access_controller_twin
    - mobile_device_twin
    - vehicle_twin
  
  asset_twins:
    - equipment_twin
    - inventory_twin
  
  process_twins:
    - patrol_twin
    - shift_twin
    - incident_twin
  
  aggregate_twins:
    - fleet_twin (all vehicles)
    - workforce_twin (all guards)
    - security_posture_twin (site-wide)
```

## 2.2 Digital Twin Data Model

### Guard Digital Twin

**Schema: guard_twin.json**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "GuardDigitalTwin",
  "required": ["twin_id", "physical_id", "type", "state"],
  "properties": {
    "twin_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique digital twin identifier"
    },
    "physical_id": {
      "type": "string",
      "description": "ERPNext Guard ID"
    },
    "type": {
      "type": "string",
      "enum": ["guard_twin"],
      "const": "guard_twin"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "version": {"type": "integer"},
        "sync_status": {
          "type": "string",
          "enum": ["synced", "syncing", "out_of_sync", "error"]
        }
      }
    },
    "attributes": {
      "type": "object",
      "description": "Static properties from ERPNext",
      "properties": {
        "employee_id": {"type": "string"},
        "full_name": {"type": "string"},
        "certifications": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": {"type": "string"},
              "expiry_date": {"type": "string", "format": "date"},
              "status": {"type": "string", "enum": ["valid", "expiring_soon", "expired"]}
            }
          }
        },
        "skills": {
          "type": "array",
          "items": {"type": "string"}
        },
        "performance_metrics": {
          "type": "object",
          "properties": {
            "patrol_completion_rate": {"type": "number", "minimum": 0, "maximum": 100},
            "incident_report_quality": {"type": "number", "minimum": 0, "maximum": 100},
            "client_satisfaction": {"type": "number", "minimum": 0, "maximum": 5}
          }
        }
      }
    },
    "state": {
      "type": "object",
      "description": "Real-time dynamic state",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["available", "on_shift", "on_break", "off_duty", "sick_leave", "vacation"]
        },
        "location": {
          "type": "object",
          "properties": {
            "latitude": {"type": "number"},
            "longitude": {"type": "number"},
            "altitude": {"type": "number"},
            "accuracy": {"type": "number"},
            "timestamp": {"type": "string", "format": "date-time"}
          }
        },
        "current_site": {
          "type": ["string", "null"],
          "description": "Site ID if on duty"
        },
        "current_shift": {
          "type": ["string", "null"],
          "description": "Shift ID if on duty"
        },
        "current_patrol": {
          "type": ["string", "null"],
          "description": "Patrol ID if actively patrolling"
        },
        "device_health": {
          "type": "object",
          "properties": {
            "mobile_device_id": {"type": "string"},
            "battery_level": {"type": "integer", "minimum": 0, "maximum": 100},
            "signal_strength": {"type": "integer", "minimum": -120, "maximum": 0},
            "gps_accuracy": {"type": "number"},
            "app_version": {"type": "string"},
            "last_heartbeat": {"type": "string", "format": "date-time"}
          }
        },
        "vitals": {
          "type": "object",
          "description": "If wearable device integrated",
          "properties": {
            "heart_rate": {"type": "integer"},
            "stress_level": {"type": "string", "enum": ["low", "medium", "high"]},
            "fatigue_score": {"type": "number", "minimum": 0, "maximum": 100}
          }
        }
      }
    },
    "analytics": {
      "type": "object",
      "description": "Computed analytics from twin history",
      "properties": {
        "hours_worked_today": {"type": "number"},
        "hours_worked_week": {"type": "number"},
        "checkpoints_scanned_today": {"type": "integer"},
        "incidents_reported_week": {"type": "integer"},
        "average_response_time": {"type": "number", "description": "In seconds"},
        "patrol_efficiency_score": {"type": "number", "minimum": 0, "maximum": 100}
      }
    },
    "predictions": {
      "type": "object",
      "description": "ML-generated predictions",
      "properties": {
        "fatigue_risk": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Probability of fatigue in next 2 hours"
        },
        "incident_likelihood": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Probability of encountering incident this shift"
        },
        "schedule_adherence_forecast": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Likelihood of completing shift on time"
        },
        "recommended_break_time": {"type": "string", "format": "date-time"}
      }
    },
    "relationships": {
      "type": "object",
      "description": "Links to other twins",
      "properties": {
        "assigned_sites": {
          "type": "array",
          "items": {"type": "string", "description": "Site twin IDs"}
        },
        "supervisor": {
          "type": ["string", "null"],
          "description": "Supervisor twin ID"
        },
        "assigned_vehicle": {
          "type": ["string", "null"],
          "description": "Vehicle twin ID"
        },
        "issued_equipment": {
          "type": "array",
          "items": {"type": "string", "description": "Asset twin IDs"}
        }
      }
    }
  }
}
```

### Site Digital Twin

**Schema: site_twin.json**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "SiteDigitalTwin",
  "required": ["twin_id", "physical_id", "type", "state"],
  "properties": {
    "twin_id": {"type": "string", "format": "uuid"},
    "physical_id": {"type": "string", "description": "ERPNext Site ID"},
    "type": {"type": "string", "const": "site_twin"},
    "metadata": {
      "type": "object",
      "properties": {
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "sync_status": {"type": "string"}
      }
    },
    "attributes": {
      "type": "object",
      "properties": {
        "site_id": {"type": "string"},
        "name": {"type": "string"},
        "client": {"type": "string"},
        "site_type": {
          "type": "string",
          "enum": ["commercial_office", "healthcare", "government", "cannabis", "logistics", "retail", "residential"]
        },
        "address": {
          "type": "object",
          "properties": {
            "street": {"type": "string"},
            "city": {"type": "string"},
            "province": {"type": "string"},
            "postal_code": {"type": "string"},
            "coordinates": {
              "type": "object",
              "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
              }
            }
          }
        },
        "operating_hours": {
          "type": "object",
          "properties": {
            "monday": {"$ref": "#/definitions/day_hours"},
            "tuesday": {"$ref": "#/definitions/day_hours"},
            "wednesday": {"$ref": "#/definitions/day_hours"},
            "thursday": {"$ref": "#/definitions/day_hours"},
            "friday": {"$ref": "#/definitions/day_hours"},
            "saturday": {"$ref": "#/definitions/day_hours"},
            "sunday": {"$ref": "#/definitions/day_hours"}
          }
        },
        "floor_plan": {
          "type": "object",
          "properties": {
            "image_url": {"type": "string", "format": "uri"},
            "zones": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "zone_id": {"type": "string"},
                  "name": {"type": "string"},
                  "type": {"type": "string", "enum": ["public", "restricted", "secure", "emergency"]},
                  "polygon": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "lat": {"type": "number"},
                        "lng": {"type": "number"}
                      }
                    }
                  }
                }
              }
            },
            "checkpoints": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "checkpoint_id": {"type": "string"},
                  "name": {"type": "string"},
                  "location": {"type": "object"},
                  "nfc_tag_id": {"type": "string"}
                }
              }
            }
          }
        }
      }
    },
    "state": {
      "type": "object",
      "description": "Real-time site state",
      "properties": {
        "operational_status": {
          "type": "string",
          "enum": ["active", "inactive", "alarm", "lockdown", "maintenance"]
        },
        "guards_on_duty": {
          "type": "array",
          "items": {"type": "string", "description": "Guard twin IDs"}
        },
        "active_patrols": {
          "type": "array",
          "items": {"type": "string", "description": "Patrol twin IDs"}
        },
        "environmental_conditions": {
          "type": "object",
          "properties": {
            "temperature": {"type": "number", "description": "Celsius"},
            "humidity": {"type": "number", "description": "Percentage"},
            "light_level": {"type": "number", "description": "Lux"},
            "air_quality": {"type": "number", "description": "AQI"}
          }
        },
        "security_posture": {
          "type": "object",
          "properties": {
            "threat_level": {
              "type": "string",
              "enum": ["normal", "elevated", "high", "critical"]
            },
            "armed_status": {
              "type": "string",
              "enum": ["disarmed", "stay_armed", "away_armed"]
            },
            "all_zones_secured": {"type": "boolean"},
            "cameras_online": {"type": "integer"},
            "cameras_total": {"type": "integer"},
            "access_points_online": {"type": "integer"},
            "access_points_total": {"type": "integer"}
          }
        },
        "occupancy": {
          "type": "object",
          "properties": {
            "current_count": {"type": "integer"},
            "capacity": {"type": "integer"},
            "utilization_percentage": {"type": "number"}
          }
        }
      }
    },
    "analytics": {
      "type": "object",
      "properties": {
        "incidents_today": {"type": "integer"},
        "incidents_week": {"type": "integer"},
        "incidents_month": {"type": "integer"},
        "patrol_completion_rate_today": {"type": "number"},
        "average_response_time": {"type": "number", "description": "In seconds"},
        "compliance_score": {"type": "number", "minimum": 0, "maximum": 100}
      }
    },
    "predictions": {
      "type": "object",
      "properties": {
        "incident_risk_next_4h": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Probability of incident in next 4 hours"
        },
        "predicted_incident_types": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": {"type": "string"},
              "probability": {"type": "number"}
            }
          }
        },
        "optimal_guard_count": {
          "type": "integer",
          "description": "Recommended guards for next shift"
        },
        "high_risk_zones": {
          "type": "array",
          "items": {"type": "string", "description": "Zone IDs"}
        }
      }
    },
    "relationships": {
      "type": "object",
      "properties": {
        "cameras": {"type": "array", "items": {"type": "string"}},
        "sensors": {"type": "array", "items": {"type": "string"}},
        "access_controllers": {"type": "array", "items": {"type": "string"}},
        "assigned_guards": {"type": "array", "items": {"type": "string"}},
        "client_twin": {"type": "string"}
      }
    }
  },
  "definitions": {
    "day_hours": {
      "type": "object",
      "properties": {
        "open": {"type": "string", "pattern": "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"},
        "close": {"type": "string", "pattern": "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"},
        "is_24_hour": {"type": "boolean"}
      }
    }
  }
}
```

### Camera Digital Twin

**Schema: camera_twin.json**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "title": "CameraDigitalTwin",
  "required": ["twin_id", "physical_id", "type", "state"],
  "properties": {
    "twin_id": {"type": "string", "format": "uuid"},
    "physical_id": {"type": "string", "description": "ZoneMinder Monitor ID"},
    "type": {"type": "string", "const": "camera_twin"},
    "attributes": {
      "type": "object",
      "properties": {
        "camera_id": {"type": "string"},
        "name": {"type": "string"},
        "site_id": {"type": "string"},
        "manufacturer": {"type": "string"},
        "model": {"type": "string"},
        "firmware_version": {"type": "string"},
        "resolution": {"type": "string", "example": "1920x1080"},
        "fps": {"type": "integer"},
        "location": {
          "type": "object",
          "properties": {
            "zone": {"type": "string"},
            "mounting": {"type": "string", "enum": ["ceiling", "wall", "pole"]},
            "height": {"type": "number", "description": "Meters"},
            "view_direction": {"type": "number", "description": "Degrees from north"}
          }
        },
        "capabilities": {
          "type": "object",
          "properties": {
            "ptz": {"type": "boolean"},
            "night_vision": {"type": "boolean"},
            "motion_detection": {"type": "boolean"},
            "audio": {"type": "boolean"},
            "ai_analytics": {"type": "boolean"}
          }
        }
      }
    },
    "state": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["online", "offline", "recording", "error", "maintenance"]
        },
        "streaming": {"type": "boolean"},
        "recording": {"type": "boolean"},
        "motion_detected": {"type": "boolean"},
        "last_motion_time": {"type": "string", "format": "date-time"},
        "health": {
          "type": "object",
          "properties": {
            "uptime_seconds": {"type": "integer"},
            "frame_rate_actual": {"type": "number"},
            "bitrate_kbps": {"type": "integer"},
            "storage_used_mb": {"type": "integer"},
            "errors_24h": {"type": "integer"}
          }
        },
        "current_view": {
          "type": "object",
          "properties": {
            "pan": {"type": "number", "description": "Degrees"},
            "tilt": {"type": "number", "description": "Degrees"},
            "zoom": {"type": "number", "description": "Zoom level"}
          }
        }
      }
    },
    "analytics": {
      "type": "object",
      "properties": {
        "events_today": {"type": "integer"},
        "motion_events_today": {"type": "integer"},
        "ai_detections_today": {
          "type": "object",
          "properties": {
            "person": {"type": "integer"},
            "vehicle": {"type": "integer"},
            "loitering": {"type": "integer"},
            "crowd_formation": {"type": "integer"}
          }
        },
        "recording_hours_today": {"type": "number"},
        "storage_growth_rate_mb_per_hour": {"type": "number"}
      }
    },
    "predictions": {
      "type": "object",
      "properties": {
        "failure_risk_30d": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Probability of camera failure in next 30 days"
        },
        "maintenance_recommended_date": {"type": "string", "format": "date"},
        "expected_lifespan_days": {"type": "integer"}
      }
    }
  }
}
```

## 2.3 Digital Twin Platform Implementation

### Eclipse Ditto Configuration

**docker-compose-ditto.yml**
```yaml
version: '3.8'

services:
  # MongoDB for Ditto persistence
  mongodb:
    image: mongo:6.0
    container_name: ditto-mongodb
    restart: unless-stopped
    environment:
      - MONGO_INITDB_ROOT_USERNAME=ditto
      - MONGO_INITDB_ROOT_PASSWORD=${DITTO_MONGO_PASSWORD}
    volumes:
      - ditto-mongo-data:/data/db
    networks:
      - ditto-network

  # Ditto Gateway
  ditto-gateway:
    image: eclipse/ditto-gateway:3.4.0
    container_name: ditto-gateway
    restart: unless-stopped
    environment:
      - DITTO_GATEWAY_MONGODB_URI=mongodb://ditto:${DITTO_MONGO_PASSWORD}@mongodb:27017/ditto
      - DITTO_GATEWAY_DEVOPS_PASSWORD=${DITTO_DEVOPS_PASSWORD}
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    ports:
      - "8080:8080"
    depends_on:
      - mongodb
      - kafka
    networks:
      - ditto-network
      - ironhorse-network

  # Ditto Things Service
  ditto-things:
    image: eclipse/ditto-things:3.4.0
    container_name: ditto-things
    restart: unless-stopped
    environment:
      - DITTO_THINGS_MONGODB_URI=mongodb://ditto:${DITTO_MONGO_PASSWORD}@mongodb:27017/ditto
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - mongodb
      - kafka
    networks:
      - ditto-network

  # Ditto Policies Service
  ditto-policies:
    image: eclipse/ditto-policies:3.4.0
    container_name: ditto-policies
    restart: unless-stopped
    environment:
      - DITTO_POLICIES_MONGODB_URI=mongodb://ditto:${DITTO_MONGO_PASSWORD}@mongodb:27017/ditto
    depends_on:
      - mongodb
    networks:
      - ditto-network

  # Ditto Connectivity Service (for Kafka integration)
  ditto-connectivity:
    image: eclipse/ditto-connectivity:3.4.0
    container_name: ditto-connectivity
    restart: unless-stopped
    environment:
      - DITTO_CONNECTIVITY_MONGODB_URI=mongodb://ditto:${DITTO_MONGO_PASSWORD}@mongodb:27017/ditto
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - mongodb
      - kafka
    networks:
      - ditto-network
      - ironhorse-network

  # Kafka (from existing IHOSE stack)
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
      - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
    networks:
      - ironhorse-network
      - ditto-network

  # Twin Sync Service (Custom)
  twin-sync:
    image: ironhorse/twin-sync:latest
    container_name: twin-sync
    restart: unless-stopped
    environment:
      - DITTO_URL=http://ditto-gateway:8080
      - DITTO_USERNAME=ditto
      - DITTO_PASSWORD=${DITTO_DEVOPS_PASSWORD}
      - ERPNEXT_URL=https://erp.ironhorsesecurity.com
      - ERPNEXT_API_KEY=${ERPNEXT_API_KEY}
      - ERPNEXT_API_SECRET=${ERPNEXT_API_SECRET}
      - KAFKA_BOOTSTRAP_SERVERS=kafka:9092
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
      - SYNC_INTERVAL_SECONDS=30
    depends_on:
      - ditto-gateway
      - kafka
      - neo4j
    networks:
      - ironhorse-network
      - ditto-network

volumes:
  ditto-mongo-data:

networks:
  ditto-network:
    driver: bridge
  ironhorse-network:
    external: true
```

### Twin Synchronization Service

**twin-sync/sync_service.py**
```python
"""
Digital Twin Synchronization Service
Syncs physical entities from ERPNext/IoT to Eclipse Ditto twins
"""

import asyncio
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import aiohttp
from kafka import KafkaConsumer, KafkaProducer
from neo4j import AsyncGraphDatabase
import redis.asyncio as redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwinSyncService:
    """Synchronizes physical entities with digital twins"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ditto_url = config['ditto_url']
        self.ditto_auth = aiohttp.BasicAuth(
            config['ditto_username'],
            config['ditto_password']
        )
        self.erpnext_url = config['erpnext_url']
        self.erpnext_headers = {
            'Authorization': f"token {config['erpnext_api_key']}:{config['erpnext_api_secret']}"
        }
        
        # Kafka for real-time updates
        self.kafka_consumer = KafkaConsumer(
            'hr.attendance',
            'patrol.checkpoint',
            'camera.alert',
            'incident.created',
            bootstrap_servers=config['kafka_servers'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='twin-sync'
        )
        
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=config['kafka_servers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Neo4j for knowledge graph
        self.neo4j_driver = AsyncGraphDatabase.driver(
            config['neo4j_uri'],
            auth=(config['neo4j_user'], config['neo4j_password'])
        )
        
        # Redis for caching
        self.redis = redis.Redis(
            host=config.get('redis_host', 'localhost'),
            port=config.get('redis_port', 6379),
            decode_responses=True
        )
        
        self.session = None
    
    async def start(self):
        """Start the synchronization service"""
        self.session = aiohttp.ClientSession()
        logger.info("Twin Sync Service started")
        
        # Start background tasks
        await asyncio.gather(
            self.sync_guards_periodic(),
            self.sync_sites_periodic(),
            self.sync_cameras_periodic(),
            self.process_kafka_events(),
            self.update_predictions()
        )
    
    async def sync_guards_periodic(self):
        """Periodically sync all guard twins from ERPNext"""
        while True:
            try:
                logger.info("Starting periodic guard twin sync")
                
                # Fetch all active guards from ERPNext
                async with self.session.get(
                    f"{self.erpnext_url}/api/resource/Guard",
                    headers=self.erpnext_headers,
                    params={'filters': json.dumps([['status', '=', 'Active']])}
                ) as response:
                    data = await response.json()
                    guards = data.get('data', [])
                
                for guard in guards:
                    await self.sync_guard_twin(guard['name'])
                
                logger.info(f"Synced {len(guards)} guard twins")
                
            except Exception as e:
                logger.error(f"Error in periodic guard sync: {e}")
            
            await asyncio.sleep(self.config.get('sync_interval_seconds', 30))
    
    async def sync_guard_twin(self, guard_id: str):
        """Sync a single guard's digital twin"""
        try:
            # Fetch detailed guard data from ERPNext
            async with self.session.get(
                f"{self.erpnext_url}/api/resource/Guard/{guard_id}",
                headers=self.erpnext_headers
            ) as response:
                guard_data = await response.json()
                guard = guard_data['data']
            
            # Get real-time location from Redis (last GPS update)
            location_key = f"guard:{guard_id}:location"
            location_data = await self.redis.hgetall(location_key)
            
            # Construct digital twin
            twin = {
                "thingId": f"com.ironhorsesecurity:guard-{guard_id}",
                "policyId": "com.ironhorsesecurity:guard-policy",
                "attributes": {
                    "employee_id": guard.get('employee_id'),
                    "full_name": guard.get('full_name'),
                    "certifications": guard.get('certifications', []),
                    "skills": guard.get('skills', []),
                    "performance_metrics": {
                        "patrol_completion_rate": guard.get('patrol_completion_rate', 0),
                        "incident_report_quality": guard.get('incident_report_quality', 0),
                        "client_satisfaction": guard.get('client_satisfaction', 0)
                    }
                },
                "features": {
                    "state": {
                        "properties": {
                            "status": guard.get('status', 'off_duty'),
                            "location": {
                                "latitude": float(location_data.get('latitude', 0)) if location_data else None,
                                "longitude": float(location_data.get('longitude', 0)) if location_data else None,
                                "accuracy": float(location_data.get('accuracy', 0)) if location_data else None,
                                "timestamp": location_data.get('timestamp') if location_data else None
                            },
                            "current_site": guard.get('current_site'),
                            "current_shift": guard.get('current_shift'),
                            "device_health": await self._get_device_health(guard_id)
                        }
                    },
                    "analytics": {
                        "properties": await self._compute_guard_analytics(guard_id)
                    },
                    "predictions": {
                        "properties": await self._get_guard_predictions(guard_id)
                    }
                }
            }
            
            # Create or update twin in Ditto
            async with self.session.put(
                f"{self.ditto_url}/api/2/things/{twin['thingId']}",
                auth=self.ditto_auth,
                json=twin
            ) as response:
                if response.status in [201, 204]:
                    logger.info(f"Synced guard twin: {guard_id}")
                    
                    # Update knowledge graph
                    await self._update_guard_in_graph(guard_id, twin)
                else:
                    logger.error(f"Failed to sync guard twin {guard_id}: {response.status}")
        
        except Exception as e:
            logger.error(f"Error syncing guard twin {guard_id}: {e}")
    
    async def _get_device_health(self, guard_id: str) -> Dict[str, Any]:
        """Get mobile device health from Redis"""
        health_key = f"guard:{guard_id}:device_health"
        health_data = await self.redis.hgetall(health_key)
        
        if health_data:
            return {
                "mobile_device_id": health_data.get('device_id'),
                "battery_level": int(health_data.get('battery_level', 0)),
                "signal_strength": int(health_data.get('signal_strength', 0)),
                "app_version": health_data.get('app_version'),
                "last_heartbeat": health_data.get('last_heartbeat')
            }
        return {}
    
    async def _compute_guard_analytics(self, guard_id: str) -> Dict[str, Any]:
        """Compute real-time analytics for guard"""
        # Query TimescaleDB for today's metrics
        # This is a simplified version - actual implementation would query TimescaleDB
        
        analytics_key = f"guard:{guard_id}:analytics:today"
        analytics_data = await self.redis.hgetall(analytics_key)
        
        return {
            "hours_worked_today": float(analytics_data.get('hours_worked', 0)),
            "checkpoints_scanned_today": int(analytics_data.get('checkpoints_scanned', 0)),
            "incidents_reported_today": int(analytics_data.get('incidents_reported', 0)),
            "average_response_time": float(analytics_data.get('avg_response_time', 0)),
            "patrol_efficiency_score": float(analytics_data.get('patrol_efficiency', 0))
        }
    
    async def _get_guard_predictions(self, guard_id: str) -> Dict[str, Any]:
        """Get ML predictions for guard"""
        # In production, this would call a ML model inference service
        # For now, return cached predictions
        
        prediction_key = f"guard:{guard_id}:predictions"
        predictions = await self.redis.hgetall(prediction_key)
        
        return {
            "fatigue_risk": float(predictions.get('fatigue_risk', 0)),
            "incident_likelihood": float(predictions.get('incident_likelihood', 0)),
            "schedule_adherence_forecast": float(predictions.get('schedule_adherence', 0))
        }
    
    async def _update_guard_in_graph(self, guard_id: str, twin: Dict[str, Any]):
        """Update guard node in Neo4j knowledge graph"""
        async with self.neo4j_driver.session() as session:
            await session.run(
                """
                MERGE (g:Guard {id: $guard_id})
                SET g.twin_id = $twin_id,
                    g.name = $name,
                    g.status = $status,
                    g.updated_at = datetime()
                """,
                guard_id=guard_id,
                twin_id=twin['thingId'],
                name=twin['attributes']['full_name'],
                status=twin['features']['state']['properties']['status']
            )
    
    async def sync_sites_periodic(self):
        """Periodically sync all site twins"""
        while True:
            try:
                logger.info("Starting periodic site twin sync")
                
                async with self.session.get(
                    f"{self.erpnext_url}/api/resource/Site",
                    headers=self.erpnext_headers,
                    params={'filters': json.dumps([['status', '=', 'Active']])}
                ) as response:
                    data = await response.json()
                    sites = data.get('data', [])
                
                for site in sites:
                    await self.sync_site_twin(site['name'])
                
                logger.info(f"Synced {len(sites)} site twins")
                
            except Exception as e:
                logger.error(f"Error in periodic site sync: {e}")
            
            await asyncio.sleep(self.config.get('sync_interval_seconds', 30))
    
    async def sync_site_twin(self, site_id: str):
        """Sync a single site's digital twin"""
        try:
            # Fetch site data
            async with self.session.get(
                f"{self.erpnext_url}/api/resource/Site/{site_id}",
                headers=self.erpnext_headers
            ) as response:
                site_data = await response.json()
                site = site_data['data']
            
            # Get real-time site state
            state_key = f"site:{site_id}:state"
            state_data = await self.redis.hgetall(state_key)
            
            # Construct site twin
            twin = {
                "thingId": f"com.ironhorsesecurity:site-{site_id}",
                "policyId": "com.ironhorsesecurity:site-policy",
                "attributes": {
                    "site_id": site.get('site_id'),
                    "name": site.get('name'),
                    "client": site.get('client'),
                    "site_type": site.get('site_type'),
                    "address": site.get('address', {}),
                    "operating_hours": site.get('operating_hours', {}),
                    "floor_plan": site.get('floor_plan', {})
                },
                "features": {
                    "state": {
                        "properties": {
                            "operational_status": state_data.get('operational_status', 'active'),
                            "guards_on_duty": json.loads(state_data.get('guards_on_duty', '[]')),
                            "active_patrols": json.loads(state_data.get('active_patrols', '[]')),
                            "security_posture": json.loads(state_data.get('security_posture', '{}')),
                            "occupancy": json.loads(state_data.get('occupancy', '{}'))
                        }
                    },
                    "analytics": {
                        "properties": await self._compute_site_analytics(site_id)
                    },
                    "predictions": {
                        "properties": await self._get_site_predictions(site_id)
                    }
                }
            }
            
            # Update in Ditto
            async with self.session.put(
                f"{self.ditto_url}/api/2/things/{twin['thingId']}",
                auth=self.ditto_auth,
                json=twin
            ) as response:
                if response.status in [201, 204]:
                    logger.info(f"Synced site twin: {site_id}")
                    await self._update_site_in_graph(site_id, twin)
        
        except Exception as e:
            logger.error(f"Error syncing site twin {site_id}: {e}")
    
    async def _compute_site_analytics(self, site_id: str) -> Dict[str, Any]:
        """Compute real-time analytics for site"""
        analytics_key = f"site:{site_id}:analytics"
        analytics_data = await self.redis.hgetall(analytics_key)
        
        return {
            "incidents_today": int(analytics_data.get('incidents_today', 0)),
            "incidents_week": int(analytics_data.get('incidents_week', 0)),
            "patrol_completion_rate_today": float(analytics_data.get('patrol_completion_rate', 0)),
            "average_response_time": float(analytics_data.get('avg_response_time', 0)),
            "compliance_score": float(analytics_data.get('compliance_score', 0))
        }
    
    async def _get_site_predictions(self, site_id: str) -> Dict[str, Any]:
        """Get ML predictions for site"""
        prediction_key = f"site:{site_id}:predictions"
        predictions = await self.redis.hgetall(prediction_key)
        
        return {
            "incident_risk_next_4h": float(predictions.get('incident_risk_4h', 0)),
            "optimal_guard_count": int(predictions.get('optimal_guards', 2)),
            "high_risk_zones": json.loads(predictions.get('high_risk_zones', '[]'))
        }
    
    async def _update_site_in_graph(self, site_id: str, twin: Dict[str, Any]):
        """Update site node in Neo4j"""
        async with self.neo4j_driver.session() as session:
            await session.run(
                """
                MERGE (s:Site {id: $site_id})
                SET s.twin_id = $twin_id,
                    s.name = $name,
                    s.site_type = $site_type,
                    s.status = $status,
                    s.updated_at = datetime()
                """,
                site_id=site_id,
                twin_id=twin['thingId'],
                name=twin['attributes']['name'],
                site_type=twin['attributes']['site_type'],
                status=twin['features']['state']['properties']['operational_status']
            )
    
    async def sync_cameras_periodic(self):
        """Periodically sync all camera twins"""
        while True:
            try:
                logger.info("Starting periodic camera twin sync")
                
                # Fetch cameras from ZoneMinder API
                async with self.session.get(
                    f"{self.config['zoneminder_url']}/api/monitors.json",
                    params={'user': self.config['zm_user'], 'pass': self.config['zm_pass']}
                ) as response:
                    data = await response.json()
                    cameras = data.get('monitors', [])
                
                for camera in cameras:
                    await self.sync_camera_twin(camera['Monitor']['Id'])
                
                logger.info(f"Synced {len(cameras)} camera twins")
                
            except Exception as e:
                logger.error(f"Error in periodic camera sync: {e}")
            
            await asyncio.sleep(self.config.get('sync_interval_seconds', 30))
    
    async def sync_camera_twin(self, camera_id: str):
        """Sync a single camera's digital twin"""
        try:
            # Fetch camera data from ZoneMinder
            async with self.session.get(
                f"{self.config['zoneminder_url']}/api/monitors/{camera_id}.json",
                params={'user': self.config['zm_user'], 'pass': self.config['zm_pass']}
            ) as response:
                data = await response.json()
                camera = data['monitor']['Monitor']
            
            # Get real-time camera state
            state_key = f"camera:{camera_id}:state"
            state_data = await self.redis.hgetall(state_key)
            
            twin = {
                "thingId": f"com.ironhorsesecurity:camera-{camera_id}",
                "policyId": "com.ironhorsesecurity:camera-policy",
                "attributes": {
                    "camera_id": camera['Id'],
                    "name": camera['Name'],
                    "site_id": camera.get('Notes'),  # Site ID stored in Notes field
                    "manufacturer": camera.get('Manufacturer', 'Unknown'),
                    "model": camera.get('Model', 'Unknown'),
                    "resolution": f"{camera['Width']}x{camera['Height']}",
                    "fps": int(camera.get('MaxFPS', 15)),
                    "capabilities": {
                        "ptz": bool(camera.get('Controllable')),
                        "night_vision": True,  # Assumed
                        "motion_detection": bool(camera.get('Function') == 'Mocord'),
                        "audio": bool(camera.get('AudioChannels', 0) > 0),
                        "ai_analytics": True
                    }
                },
                "features": {
                    "state": {
                        "properties": {
                            "status": "online" if camera.get('Enabled') == '1' else "offline",
                            "streaming": state_data.get('streaming') == 'true',
                            "recording": camera.get('Function') in ['Record', 'Mocord', 'Nodect'],
                            "motion_detected": state_data.get('motion_detected') == 'true',
                            "last_motion_time": state_data.get('last_motion_time'),
                            "health": {
                                "uptime_seconds": int(state_data.get('uptime', 0)),
                                "frame_rate_actual": float(state_data.get('fps', 0)),
                                "errors_24h": int(state_data.get('errors_24h', 0))
                            }
                        }
                    },
                    "analytics": {
                        "properties": await self._compute_camera_analytics(camera_id)
                    },
                    "predictions": {
                        "properties": await self._get_camera_predictions(camera_id)
                    }
                }
            }
            
            async with self.session.put(
                f"{self.ditto_url}/api/2/things/{twin['thingId']}",
                auth=self.ditto_auth,
                json=twin
            ) as response:
                if response.status in [201, 204]:
                    logger.info(f"Synced camera twin: {camera_id}")
                    await self._update_camera_in_graph(camera_id, twin)
        
        except Exception as e:
            logger.error(f"Error syncing camera twin {camera_id}: {e}")
    
    async def _compute_camera_analytics(self, camera_id: str) -> Dict[str, Any]:
        """Compute analytics for camera"""
        analytics_key = f"camera:{camera_id}:analytics:today"
        analytics = await self.redis.hgetall(analytics_key)
        
        return {
            "events_today": int(analytics.get('events', 0)),
            "motion_events_today": int(analytics.get('motion_events', 0)),
            "ai_detections_today": json.loads(analytics.get('ai_detections', '{}')),
            "recording_hours_today": float(analytics.get('recording_hours', 0))
        }
    
    async def _get_camera_predictions(self, camera_id: str) -> Dict[str, Any]:
        """Get predictions for camera"""
        prediction_key = f"camera:{camera_id}:predictions"
        predictions = await self.redis.hgetall(prediction_key)
        
        return {
            "failure_risk_30d": float(predictions.get('failure_risk', 0)),
            "maintenance_recommended_date": predictions.get('maintenance_date')
        }
    
    async def _update_camera_in_graph(self, camera_id: str, twin: Dict[str, Any]):
        """Update camera node in Neo4j"""
        async with self.neo4j_driver.session() as session:
            await session.run(
                """
                MERGE (c:Camera {id: $camera_id})
                SET c.twin_id = $twin_id,
                    c.name = $name,
                    c.site_id = $site_id,
                    c.status = $status,
                    c.updated_at = datetime()
                WITH c
                MATCH (s:Site {id: $site_id})
                MERGE (c)-[:LOCATED_AT]->(s)
                """,
                camera_id=camera_id,
                twin_id=twin['thingId'],
                name=twin['attributes']['name'],
                site_id=twin['attributes']['site_id'],
                status=twin['features']['state']['properties']['status']
            )
    
    async def process_kafka_events(self):
        """Process real-time events from Kafka to update twins"""
        logger.info("Starting Kafka event processor")
        
        for message in self.kafka_consumer:
            try:
                topic = message.topic
                event = message.value
                
                if topic == 'patrol.checkpoint':
                    await self._handle_checkpoint_event(event)
                elif topic == 'hr.attendance':
                    await self._handle_attendance_event(event)
                elif topic == 'camera.alert':
                    await self._handle_camera_alert(event)
                elif topic == 'incident.created':
                    await self._handle_incident_event(event)
                
            except Exception as e:
                logger.error(f"Error processing Kafka event: {e}")
    
    async def _handle_checkpoint_event(self, event: Dict[str, Any]):
        """Update guard twin when checkpoint scanned"""
        guard_id = event['guard_id']
        
        # Update guard's location in Redis
        await self.redis.hset(
            f"guard:{guard_id}:location",
            mapping={
                'latitude': event['location']['latitude'],
                'longitude': event['location']['longitude'],
                'accuracy': event['location']['accuracy'],
                'timestamp': event['scan_time']
            }
        )
        
        # Increment checkpoint counter
        await self.redis.hincrby(
            f"guard:{guard_id}:analytics:today",
            'checkpoints_scanned',
            1
        )
        
        # Update twin in Ditto (partial update)
        twin_id = f"com.ironhorsesecurity:guard-{guard_id}"
        patch = {
            "features": {
                "state": {
                    "properties": {
                        "location": event['location'],
                        "last_checkpoint": event['checkpoint_id'],
                        "last_checkpoint_time": event['scan_time']
                    }
                }
            }
        }
        
        async with self.session.patch(
            f"{self.ditto_url}/api/2/things/{twin_id}",
            auth=self.ditto_auth,
            json=patch
        ) as response:
            if response.status == 204:
                logger.debug(f"Updated guard twin {guard_id} from checkpoint event")
    
    async def _handle_attendance_event(self, event: Dict[str, Any]):
        """Update guard twin when clocking in/out"""
        guard_id = event['guard_id']
        event_type = event['event_type']
        
        # Update guard status
        status_map = {
            'CLOCK_IN': 'on_shift',
            'CLOCK_OUT': 'off_duty',
            'BREAK_START': 'on_break',
            'BREAK_END': 'on_shift'
        }
        
        new_status = status_map.get(event_type, 'off_duty')
        
        twin_id = f"com.ironhorsesecurity:guard-{guard_id}"
        patch = {
            "features": {
                "state": {
                    "properties": {
                        "status": new_status,
                        "current_site": event.get('site_id'),
                        "current_shift": event.get('shift_id')
                    }
                }
            }
        }
        
        async with self.session.patch(
            f"{self.ditto_url}/api/2/things/{twin_id}",
            auth=self.ditto_auth,
            json=patch
        ) as response:
            if response.status == 204:
                logger.info(f"Updated guard twin {guard_id} status to {new_status}")
    
    async def _handle_camera_alert(self, event: Dict[str, Any]):
        """Update camera twin when AI alert triggered"""
        camera_id = event['camera_id']
        alert_type = event['alert_type']
        
        # Increment alert counter
        analytics_key = f"camera:{camera_id}:analytics:today"
        await self.redis.hincrby(analytics_key, 'events', 1)
        
        # Update AI detections
        ai_detections = json.loads(await self.redis.hget(analytics_key, 'ai_detections') or '{}')
        ai_detections[alert_type.lower()] = ai_detections.get(alert_type.lower(), 0) + 1
        await self.redis.hset(analytics_key, 'ai_detections', json.dumps(ai_detections))
        
        # Update twin
        twin_id = f"com.ironhorsesecurity:camera-{camera_id}"
        patch = {
            "features": {
                "state": {
                    "properties": {
                        "last_alert_type": alert_type,
                        "last_alert_time": event['timestamp']
                    }
                }
            }
        }
        
        async with self.session.patch(
            f"{self.ditto_url}/api/2/things/{twin_id}",
            auth=self.ditto_auth,
            json=patch
        ) as response:
            if response.status == 204:
                logger.debug(f"Updated camera twin {camera_id} from AI alert")
    
    async def _handle_incident_event(self, event: Dict[str, Any]):
        """Update site twin when incident created"""
        site_id = event['site_id']
        
        # Increment incident counter
        await self.redis.hincrby(
            f"site:{site_id}:analytics",
            'incidents_today',
            1
        )
        
        # If critical severity, update site threat level
        if event['severity'] == 'CRITICAL':
            twin_id = f"com.ironhorsesecurity:site-{site_id}"
            patch = {
                "features": {
                    "state": {
                        "properties": {
                            "security_posture": {
                                "threat_level": "critical",
                                "last_critical_incident": event['incident_id'],
                                "last_critical_time": event['incident_time']
                            }
                        }
                    }
                }
            }
            
            async with self.session.patch(
                f"{self.ditto_url}/api/2/things/{twin_id}",
                auth=self.ditto_auth,
                json=patch
            ) as response:
                if response.status == 204:
                    logger.warning(f"Updated site twin {site_id} to CRITICAL threat level")
    
    async def update_predictions(self):
        """Periodically run ML models to update predictions"""
        while True:
            try:
                logger.info("Updating predictions for all twins")
                
                # This would call ML inference services
                # For now, simulate with random predictions
                
                # Update guard fatigue predictions
                guards = await self._get_all_active_guards()
                for guard_id in guards:
                    # Call ML model (simplified)
                    fatigue_risk = await self._predict_guard_fatigue(guard_id)
                    
                    await self.redis.hset(
                        f"guard:{guard_id}:predictions",
                        'fatigue_risk',
                        str(fatigue_risk)
                    )
                
                # Update site incident predictions
                sites = await self._get_all_active_sites()
                for site_id in sites:
                    incident_risk = await self._predict_site_incident_risk(site_id)
                    
                    await self.redis.hset(
                        f"site:{site_id}:predictions",
                        'incident_risk_4h',
                        str(incident_risk)
                    )
                
                logger.info("Predictions updated")
                
            except Exception as e:
                logger.error(f"Error updating predictions: {e}")
            
            # Update predictions every 15 minutes
            await asyncio.sleep(900)
    
    async def _get_all_active_guards(self) -> List[str]:
        """Get list of all active guard IDs"""
        # Query ERPNext for active guards
        async with self.session.get(
            f"{self.erpnext_url}/api/resource/Guard",
            headers=self.erpnext_headers,
            params={'filters': json.dumps([['status', '=', 'Active']]), 'fields': '["name"]'}
        ) as response:
            data = await response.json()
            return [g['name'] for g in data.get('data', [])]
    
    async def _get_all_active_sites(self) -> List[str]:
        """Get list of all active site IDs"""
        async with self.session.get(
            f"{self.erpnext_url}/api/resource/Site",
            headers=self.erpnext_headers,
            params={'filters': json.dumps([['status', '=', 'Active']]), 'fields': '["name"]'}
        ) as response:
            data = await response.json()
            return [s['name'] for g in data.get('data', [])]
    
    async def _predict_guard_fatigue(self, guard_id: str) -> float:
        """Predict guard fatigue risk (ML model placeholder)"""
        # In production, this would call a TensorFlow/PyTorch model
        # Input features: hours_worked_today, hours_worked_week, time_since_last_break, etc.
        
        # For now, return mock prediction
        hours_today = float(await self.redis.hget(f"guard:{guard_id}:analytics:today", 'hours_worked') or 0)
        
        # Simple rule-based prediction (replace with ML model)
        if hours_today > 10:
            return 0.8
        elif hours_today > 8:
            return 0.5
        else:
            return 0.2
    
    async def _predict_site_incident_risk(self, site_id: str) -> float:
        """Predict site incident risk (ML model placeholder)"""
        # Input features: time_of_day, day_of_week, recent_incidents, guards_on_duty, etc.
        
        incidents_today = int(await self.redis.hget(f"site:{site_id}:analytics", 'incidents_today') or 0)
        
        # Simple rule-based prediction
        if incidents_today >= 3:
            return 0.9
        elif incidents_today >= 1:
            return 0.6
        else:
            return 0.3
    
    async def stop(self):
        """Gracefully stop the service"""
        logger.info("Stopping Twin Sync Service")
        
        if self.session:
            await self.session.close()
        
        await self.neo4j_driver.close()
        await self.redis.close()
        
        self.kafka_consumer.close()
        self.kafka_producer.close()


# Main entry point
if __name__ == "__main__":
    import os
    
    config = {
        'ditto_url': os.getenv('DITTO_URL', 'http://localhost:8080'),
        'ditto_username': os.getenv('DITTO_USERNAME', 'ditto'),
        'ditto_password': os.getenv('DITTO_PASSWORD'),
        'erpnext_url': os.getenv('ERPNEXT_URL'),
        'erpnext_api_key': os.getenv('ERPNEXT_API_KEY'),
        'erpnext_api_secret': os.getenv('ERPNEXT_API_SECRET'),
        'kafka_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(','),
        'neo4j_uri': os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
        'neo4j_user': os.getenv('NEO4J_USER', 'neo4j'),
        'neo4j_password': os.getenv('NEO4J_PASSWORD'),
        'zoneminder_url': os.getenv('ZONEMINDER_URL', 'http://localhost/zm'),
        'zm_user': os.getenv('ZM_USER'),
        'zm_pass': os.getenv('ZM_PASS'),
        'redis_host': os.getenv('REDIS_HOST', 'localhost'),
        'redis_port': int(os.getenv('REDIS_PORT', 6379)),
        'sync_interval_seconds': int(os.getenv('SYNC_INTERVAL_SECONDS', 30))
    }
    
    service = TwinSyncService(config)
    
    try:
        asyncio.run(service.start())
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        asyncio.run(service.stop())
```

---

# 3. Knowledge Graph Design

## 3.1 Neo4j Graph Schema

### Entity Model

The Iron Horse Knowledge Graph models the entire enterprise as an interconnected semantic network where every entity (people, places, assets, events, compliance requirements) exists as a node with typed relationships to other nodes.

**Core Node Types:**

```cypher
// People Nodes
CREATE CONSTRAINT guard_id IF NOT EXISTS FOR (g:Guard) REQUIRE g.id IS UNIQUE;
CREATE CONSTRAINT supervisor_id IF NOT EXISTS FOR (s:Supervisor) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT client_contact_id IF NOT EXISTS FOR (c:ClientContact) REQUIRE c.id IS UNIQUE;

// Location Nodes
CREATE CONSTRAINT site_id IF NOT EXISTS FOR (s:Site) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT zone_id IF NOT EXISTS FOR (z:Zone) REQUIRE z.id IS UNIQUE;
CREATE CONSTRAINT checkpoint_id IF NOT EXISTS FOR (cp:Checkpoint) REQUIRE cp.id IS UNIQUE;

// Asset Nodes
CREATE CONSTRAINT camera_id IF NOT EXISTS FOR (c:Camera) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT sensor_id IF NOT EXISTS FOR (s:Sensor) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT vehicle_id IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT equipment_id IF NOT EXISTS FOR (e:Equipment) REQUIRE e.id IS UNIQUE;

// Event Nodes
CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (i:Incident) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT patrol_id IF NOT EXISTS FOR (p:Patrol) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT shift_id IF NOT EXISTS FOR (s:Shift) REQUIRE s.id IS UNIQUE;

// Certification & Compliance Nodes
CREATE CONSTRAINT certification_id IF NOT EXISTS FOR (c:Certification) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT compliance_requirement_id IF NOT EXISTS FOR (cr:ComplianceRequirement) REQUIRE cr.id IS UNIQUE;
CREATE CONSTRAINT training_course_id IF NOT EXISTS FOR (tc:TrainingCourse) REQUIRE tc.id IS UNIQUE;

// Organization Nodes
CREATE CONSTRAINT client_id IF NOT EXISTS FOR (c:Client) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT department_id IF NOT EXISTS FOR (d:Department) REQUIRE d.id IS UNIQUE;
```

### Relationship Types

```cypher
// Employment Relationships
(:Guard)-[:EMPLOYED_BY]->(:Client)
(:Guard)-[:REPORTS_TO]->(:Supervisor)
(:Guard)-[:MEMBER_OF]->(:Department)

// Assignment Relationships
(:Guard)-[:ASSIGNED_TO {start_date, end_date}]->(:Site)
(:Guard)-[:SCHEDULED_FOR {date, start_time, end_time}]->(:Shift)
(:Guard)-[:CERTIFIED_IN {issue_date, expiry_date}]->(:Certification)
(:Guard)-[:COMPLETED {completion_date, score}]->(:TrainingCourse)

// Location Relationships
(:Site)-[:BELONGS_TO]->(:Client)
(:Site)-[:CONTAINS]->(:Zone)
(:Site)-[:REQUIRES_COMPLIANCE]->(:ComplianceRequirement)
(:Zone)-[:HAS_CHECKPOINT]->(:Checkpoint)
(:Camera)-[:LOCATED_AT]->(:Site)
(:Camera)-[:MONITORS]->(:Zone)
(:Sensor)-[:INSTALLED_IN]->(:Zone)

// Event Relationships
(:Patrol)-[:CONDUCTED_BY]->(:Guard)
(:Patrol)-[:OCCURRED_AT]->(:Site)
(:Patrol)-[:INCLUDES_CHECKPOINT {scan_time, status}]->(:Checkpoint)
(:Incident)-[:REPORTED_BY]->(:Guard)
(:Incident)-[:OCCURRED_AT]->(:Site)
(:Incident)-[:OCCURRED_IN]->(:Zone)
(:Incident)-[:CAPTURED_BY]->(:Camera)
(:Incident)-[:RELATED_TO]->(:Incident)

// Asset Relationships
(:Vehicle)-[:ASSIGNED_TO]->(:Guard)
(:Equipment)-[:ISSUED_TO {issue_date}]->(:Guard)
(:Camera)-[:FEEDS_INTO]->(:Site)

// Compliance Relationships
(:Site)-[:MUST_COMPLY_WITH]->(:ComplianceRequirement)
(:Guard)-[:SATISFIES]->(:ComplianceRequirement)
(:Certification)-[:FULFILLS]->(:ComplianceRequirement)
(:TrainingCourse)-[:ADDRESSES]->(:ComplianceRequirement)

// Hierarchical Relationships
(:Supervisor)-[:MANAGES]->(:Guard)
(:Client)-[:OWNS]->(:Site)
(:Department)-[:OPERATES_AT]->(:Site)
```

### Complete Graph Schema Implementation

**knowledge-graph/schema/init_graph.cypher**
```cypher
// Iron Horse Knowledge Graph - Schema Initialization
// Execute this in Neo4j Browser or via Python driver

// ============================================================================
// INDEXES AND CONSTRAINTS
// ============================================================================

// Guard Indexes
CREATE INDEX guard_name IF NOT EXISTS FOR (g:Guard) ON (g.name);
CREATE INDEX guard_status IF NOT EXISTS FOR (g:Guard) ON (g.status);
CREATE INDEX guard_employee_id IF NOT EXISTS FOR (g:Guard) ON (g.employee_id);
CREATE FULLTEXT INDEX guard_fulltext IF NOT EXISTS FOR (g:Guard) ON EACH [g.name, g.employee_id, g.email];

// Site Indexes
CREATE INDEX site_name IF NOT EXISTS FOR (s:Site) ON (s.name);
CREATE INDEX site_type IF NOT EXISTS FOR (s:Site) ON (s.site_type);
CREATE INDEX site_status IF NOT EXISTS FOR (s:Site) ON (s.status);

// Incident Indexes
CREATE INDEX incident_date IF NOT EXISTS FOR (i:Incident) ON (i.incident_time);
CREATE INDEX incident_severity IF NOT EXISTS FOR (i:Incident) ON (i.severity);
CREATE INDEX incident_category IF NOT EXISTS FOR (i:Incident) ON (i.category);

// Temporal Indexes
CREATE INDEX patrol_date IF NOT EXISTS FOR (p:Patrol) ON (p.start_time);
CREATE INDEX shift_date IF NOT EXISTS FOR (s:Shift) ON (s.start_time);

// ============================================================================
// SAMPLE DATA POPULATION
// ============================================================================

// Create Guards
CREATE (g1:Guard {
  id: 'GRD001',
  twin_id: 'com.ironhorsesecurity:guard-GRD001',
  employee_id: 'EMP12345',
  name: 'John Smith',
  email: 'john.smith@ironhorsesecurity.com',
  status: 'Active',
  hire_date: date('2023-01-15'),
  created_at: datetime(),
  updated_at: datetime()
})

CREATE (g2:Guard {
  id: 'GRD002',
  twin_id: 'com.ironhorsesecurity:guard-GRD002',
  employee_id: 'EMP12346',
  name: 'Sarah Johnson',
  email: 'sarah.johnson@ironhorsesecurity.com',
  status: 'Active',
  hire_date: date('2022-06-01'),
  created_at: datetime(),
  updated_at: datetime()
})

// Create Clients
CREATE (c1:Client {
  id: 'CLI001',
  name: 'General Hospital',
  industry: 'Healthcare',
  status: 'Active',
  created_at: datetime()
})

CREATE (c2:Client {
  id: 'CLI002',
  name: 'TechCorp Office Tower',
  industry: 'Commercial Office',
  status: 'Active',
  created_at: datetime()
})

// Create Sites
CREATE (s1:Site {
  id: 'SITE001',
  twin_id: 'com.ironhorsesecurity:site-SITE001',
  site_id: 'GH-MAIN',
  name: 'General Hospital - Main Campus',
  site_type: 'Healthcare',
  status: 'Active',
  address: '123 Medical Drive, Ottawa, ON',
  coordinates: point({latitude: 45.4215, longitude: -75.6972}),
  created_at: datetime()
})

CREATE (s2:Site {
  id: 'SITE002',
  twin_id: 'com.ironhorsesecurity:site-SITE002',
  site_id: 'TC-TOWER',
  name: 'TechCorp Office Tower',
  site_type: 'Commercial Office',
  status: 'Active',
  address: '456 Business Blvd, Toronto, ON',
  coordinates: point({latitude: 43.6532, longitude: -79.3832}),
  created_at: datetime()
})

// Create Zones
CREATE (z1:Zone {
  id: 'ZONE001',
  name: 'Emergency Department',
  type: 'restricted',
  site_id: 'SITE001',
  created_at: datetime()
})

CREATE (z2:Zone {
  id: 'ZONE002',
  name: 'Main Lobby',
  type: 'public',
  site_id: 'SITE001',
  created_at: datetime()
})

CREATE (z3:Zone {
  id: 'ZONE003',
  name: 'Executive Floor',
  type: 'secure',
  site_id: 'SITE002',
  created_at: datetime()
})

// Create Checkpoints
CREATE (cp1:Checkpoint {
  id: 'CP001',
  name: 'ER Entrance Checkpoint',
  location: 'Emergency Department Main Entrance',
  nfc_tag_id: '04:5E:3A:12:34:80',
  expected_frequency: duration('PT1H'),
  site_id: 'SITE001',
  zone_id: 'ZONE001',
  created_at: datetime()
})

CREATE (cp2:Checkpoint {
  id: 'CP002',
  name: 'Lobby Security Desk',
  location: 'Main Lobby Security Station',
  nfc_tag_id: '04:5E:3A:12:34:81',
  expected_frequency: duration('PT30M'),
  site_id: 'SITE001',
  zone_id: 'ZONE002',
  created_at: datetime()
})

// Create Cameras
CREATE (cam1:Camera {
  id: 'CAM001',
  twin_id: 'com.ironhorsesecurity:camera-CAM001',
  name: 'ER Parking Lot Camera 1',
  manufacturer: 'Hikvision',
  model: 'DS-2CD2043G2-I',
  site_id: 'SITE001',
  status: 'Online',
  created_at: datetime()
})

CREATE (cam2:Camera {
  id: 'CAM002',
  twin_id: 'com.ironhorsesecurity:camera-CAM002',
  name: 'Main Lobby PTZ',
  manufacturer: 'Dahua',
  model: 'SD59432XA-HNR',
  site_id: 'SITE001',
  status: 'Online',
  created_at: datetime()
})

// Create Certifications
CREATE (cert1:Certification {
  id: 'CERT001',
  type: 'Security Guard License',
  name: 'Ontario Security Guard License',
  issuer: 'Ministry of Community Safety',
  jurisdiction: 'Ontario',
  created_at: datetime()
})

CREATE (cert2:Certification {
  id: 'CERT002',
  type: 'Healthcare Security',
  name: 'Healthcare Security Specialist',
  issuer: 'Iron Horse Security',
  created_at: datetime()
})

CREATE (cert3:Certification {
  id: 'CERT003',
  type: 'First Aid',
  name: 'Standard First Aid & CPR Level C',
  issuer: 'Red Cross Canada',
  created_at: datetime()
})

// Create Training Courses
CREATE (tc1:TrainingCourse {
  id: 'COURSE001',
  name: 'Healthcare Security Fundamentals',
  duration: duration('PT16H'),
  created_at: datetime()
})

CREATE (tc2:TrainingCourse {
  id: 'COURSE002',
  name: 'HIPAA Privacy & Security',
  duration: duration('PT4H'),
  created_at: datetime()
})

// Create Compliance Requirements
CREATE (cr1:ComplianceRequirement {
  id: 'COMP001',
  name: 'HIPAA Physical Safeguards',
  framework: 'HIPAA',
  description: 'Physical access controls for healthcare facilities',
  severity: 'Critical',
  created_at: datetime()
})

CREATE (cr2:ComplianceRequirement {
  id: 'COMP002',
  name: 'Healthcare Worker Background Check',
  framework: 'Joint Commission',
  description: 'All personnel must undergo criminal background check',
  severity: 'High',
  created_at: datetime()
})

// Create Incidents
CREATE (inc1:Incident {
  id: 'INC001',
  incident_id: 'INC-2024-001',
  title: 'Unauthorized Access Attempt',
  description: 'Individual attempted to access restricted area without badge',
  severity: 'High',
  category: 'Trespassing',
  incident_time: datetime('2024-01-15T14:30:00Z'),
  report_time: datetime('2024-01-15T14:35:00Z'),
  status: 'Resolved',
  created_at: datetime()
})

// Create Patrols
CREATE (pat1:Patrol {
  id: 'PAT001',
  start_time: datetime('2024-01-15T08:00:00Z'),
  end_time: datetime('2024-01-15T12:00:00Z'),
  status: 'Completed',
  completion_percentage: 100.0,
  created_at: datetime()
})

// ============================================================================
// CREATE RELATIONSHIPS
// ============================================================================

// Client â†’ Site Relationships
MATCH (c:Client {id: 'CLI001'}), (s:Site {id: 'SITE001'})
CREATE (c)-[:OWNS {since: date('2020-01-01')}]->(s)

MATCH (c:Client {id: 'CLI002'}), (s:Site {id: 'SITE002'})
CREATE (c)-[:OWNS {since: date('2021-06-01')}]->(s)

// Site â†’ Zone Relationships
MATCH (s:Site {id: 'SITE001'}), (z:Zone {id: 'ZONE001'})
CREATE (s)-[:CONTAINS]->(z)

MATCH (s:Site {id: 'SITE001'}), (z:Zone {id: 'ZONE002'})
CREATE (s)-[:CONTAINS]->(z)

MATCH (s:Site {id: 'SITE002'}), (z:Zone {id: 'ZONE003'})
CREATE (s)-[:CONTAINS]->(z)

// Zone â†’ Checkpoint Relationships
MATCH (z:Zone {id: 'ZONE001'}), (cp:Checkpoint {id: 'CP001'})
CREATE (z)-[:HAS_CHECKPOINT]->(cp)

MATCH (z:Zone {id: 'ZONE002'}), (cp:Checkpoint {id: 'CP002'})
CREATE (z)-[:HAS_CHECKPOINT]->(cp)

// Camera â†’ Site/Zone Relationships
MATCH (cam:Camera {id: 'CAM001'}), (s:Site {id: 'SITE001'})
CREATE (cam)-[:LOCATED_AT]->(s)

MATCH (cam:Camera {id: 'CAM002'}), (s:Site {id: 'SITE001'})
CREATE (cam)-[:LOCATED_AT]->(s)

MATCH (cam:Camera {id: 'CAM002'}), (z:Zone {id: 'ZONE002'})
CREATE (cam)-[:MONITORS]->(z)

// Guard â†’ Site Assignment
MATCH (g:Guard {id: 'GRD001'}), (s:Site {id: 'SITE001'})
CREATE (g)-[:ASSIGNED_TO {
  start_date: date('2023-02-01'),
  primary: true
}]->(s)

MATCH (g:Guard {id: 'GRD002'}), (s:Site {id: 'SITE002'})
CREATE (g)-[:ASSIGNED_TO {
  start_date: date('2022-07-01'),
  primary: true
}]->(s)

// Guard â†’ Certification Relationships
MATCH (g:Guard {id: 'GRD001'}), (c:Certification {id: 'CERT001'})
CREATE (g)-[:CERTIFIED_IN {
  issue_date: date('2023-01-10'),
  expiry_date: date('2026-01-10'),
  certificate_number: 'SGL-2023-12345',
  status: 'Valid'
}]->(c)

MATCH (g:Guard {id: 'GRD001'}), (c:Certification {id: 'CERT002'})
CREATE (g)-[:CERTIFIED_IN {
  issue_date: date('2023-03-15'),
  expiry_date: date('2025-03-15'),
  certificate_number: 'HCS-2023-001',
  status: 'Valid'
}]->(c)

MATCH (g:Guard {id: 'GRD001'}), (c:Certification {id: 'CERT003'})
CREATE (g)-[:CERTIFIED_IN {
  issue_date: date('2023-02-01'),
  expiry_date: date('2026-02-01'),
  certificate_number: 'FA-2023-567',
  status: 'Valid'
}]->(c)

// Guard â†’ Training Course Completion
MATCH (g:Guard {id: 'GRD001'}), (tc:TrainingCourse {id: 'COURSE001'})
CREATE (g)-[:COMPLETED {
  completion_date: date('2023-03-10'),
  score: 92,
  passed: true
}]->(tc)

MATCH (g:Guard {id: 'GRD001'}), (tc:TrainingCourse {id: 'COURSE002'})
CREATE (g)-[:COMPLETED {
  completion_date: date('2023-03-12'),
  score: 88,
  passed: true
}]->(tc)

// Site â†’ Compliance Requirements
MATCH (s:Site {id: 'SITE001'}), (cr:ComplianceRequirement {id: 'COMP001'})
CREATE (s)-[:MUST_COMPLY_WITH {
  effective_date: date('2020-01-01'),
  audit_frequency: duration('P1Y')
}]->(cr)

MATCH (s:Site {id: 'SITE001'}), (cr:ComplianceRequirement {id: 'COMP002'})
CREATE (s)-[:MUST_COMPLY_WITH {
  effective_date: date('2020-01-01'),
  audit_frequency: duration('P1Y')
}]->(cr)

// Guard Satisfies Compliance (through certifications)
MATCH (g:Guard {id: 'GRD001'}), (cr:ComplianceRequirement {id: 'COMP002'})
CREATE (g)-[:SATISFIES {
  verified_date: date('2023-01-15'),
  verification_method: 'Background Check',
  next_verification: date('2024-01-15')
}]->(cr)

// Incident Relationships
MATCH (inc:Incident {id: 'INC001'}), (g:Guard {id: 'GRD001'})
CREATE (inc)-[:REPORTED_BY]->(g)

MATCH (inc:Incident {id: 'INC001'}), (s:Site {id: 'SITE001'})
CREATE (inc)-[:OCCURRED_AT]->(s)

MATCH (inc:Incident {id: 'INC001'}), (z:Zone {id: 'ZONE001'})
CREATE (inc)-[:OCCURRED_IN]->(z)

MATCH (inc:Incident {id: 'INC001'}), (cam:Camera {id: 'CAM001'})
CREATE (inc)-[:CAPTURED_BY]->(cam)

// Patrol Relationships
MATCH (pat:Patrol {id: 'PAT001'}), (g:Guard {id: 'GRD001'})
CREATE (pat)-[:CONDUCTED_BY]->(g)

MATCH (pat:Patrol {id: 'PAT001'}), (s:Site {id: 'SITE001'})
CREATE (pat)-[:OCCURRED_AT]->(s)

MATCH (pat:Patrol {id: 'PAT001'}), (cp:Checkpoint {id: 'CP001'})
CREATE (pat)-[:INCLUDES_CHECKPOINT {
  scan_time: datetime('2024-01-15T08:30:00Z'),
  status: 'On Time'
}]->(cp)

MATCH (pat:Patrol {id: 'PAT001'}), (cp:Checkpoint {id: 'CP002'})
CREATE (pat)-[:INCLUDES_CHECKPOINT {
  scan_time: datetime('2024-01-15T09:00:00Z'),
  status: 'On Time'
}]->(cp);
```

## 3.2 Knowledge Graph Query Examples

### Complex Reasoning Queries

**1. Find Guards Qualified for Healthcare Emergency**

```cypher
// Find all active guards with valid healthcare certifications,
// first aid, and within 30km of the incident site
MATCH (incident_site:Site {id: 'SITE001'})
MATCH (g:Guard {status: 'Active'})-[assigned:ASSIGNED_TO]->(site:Site)
MATCH (g)-[cert:CERTIFIED_IN]->(c:Certification)
WHERE c.type IN ['Healthcare Security', 'First Aid']
  AND cert.status = 'Valid'
  AND cert.expiry_date > date()
WITH g, incident_site, 
     point.distance(site.coordinates, incident_site.coordinates) AS distance
WHERE distance < 30000  // 30km
WITH g, distance, 
     collect(DISTINCT c.type) AS certifications
WHERE size(certifications) >= 2  // Must have both certifications
MATCH (g)-[:COMPLETED]->(tc:TrainingCourse)
WHERE tc.name CONTAINS 'Healthcare'
RETURN g.name AS guard_name,
       g.employee_id,
       distance / 1000.0 AS distance_km,
       certifications,
       g.status AS current_status
ORDER BY distance ASC
LIMIT 5;
```

**2. Compliance Gap Analysis**

```cypher
// Identify sites with compliance gaps
MATCH (s:Site)-[:MUST_COMPLY_WITH]->(cr:ComplianceRequirement)
OPTIONAL MATCH (s)<-[:ASSIGNED_TO]-(g:Guard)-[:SATISFIES]->(cr)
WITH s, cr, count(DISTINCT g) AS compliant_guards
MATCH (s)<-[:ASSIGNED_TO]-(all_guards:Guard)
WITH s, cr, 
     compliant_guards,
     count(DISTINCT all_guards) AS total_guards,
     (toFloat(compliant_guards) / count(DISTINCT all_guards) * 100) AS compliance_percentage
WHERE compliance_percentage < 100
RETURN s.name AS site_name,
       cr.name AS requirement,
       cr.framework,
       cr.severity,
       total_guards,
       compliant_guards,
       round(compliance_percentage, 2) AS compliance_pct,
       (total_guards - compliant_guards) AS guards_needing_certification
ORDER BY cr.severity DESC, compliance_percentage ASC;
```

**3. Incident Pattern Detection**

```cypher
// Find incident patterns: same zone, similar time of day, similar category
MATCH (i1:Incident)-[:OCCURRED_IN]->(z:Zone)<-[:OCCURRED_IN]-(i2:Incident)
WHERE i1.id <> i2.id
  AND i1.category = i2.category
  AND abs(duration.between(i1.incident_time, i2.incident_time).hours % 24 - 
          duration.between(i1.incident_time, datetime()).hours % 24) < 2
  AND i1.incident_time > datetime() - duration('P30D')
WITH z, i1.category AS category, 
     collect(DISTINCT i1) + collect(DISTINCT i2) AS incidents
WHERE size(incidents) >= 3
MATCH (z)<-[:CONTAINS]-(s:Site)
RETURN s.name AS site_name,
       z.name AS zone_name,
       category,
       size(incidents) AS incident_count,
       [i IN incidents | i.incident_time][0..3] AS sample_times,
       'High risk zone - consider increased patrols' AS recommendation
ORDER BY incident_count DESC;
```

**4. Optimal Guard Assignment (Graph Algorithm)**

```cypher
// Use Cypher projection and pathfinding to find optimal assignments
// considering distance, certifications, and workload

// Step 1: Create graph projection
CALL gds.graph.project(
  'guard-site-network',
  ['Guard', 'Site', 'Certification'],
  {
    ASSIGNED_TO: {
      properties: 'distance'
    },
    CERTIFIED_IN: {
      orientation: 'UNDIRECTED'
    }
  }
);

// Step 2: Run PageRank to find most qualified guards
CALL gds.pageRank.stream('guard-site-network', {
  nodeLabels: ['Guard'],
  relationshipTypes: ['CERTIFIED_IN', 'COMPLETED'],
  dampingFactor: 0.85
})
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS guard, score AS qualification_score
WHERE guard:Guard AND guard.status = 'Active'

// Step 3: Calculate workload
MATCH (guard)-[shifts:SCHEDULED_FOR]->(shift:Shift)
WHERE shift.start_time > datetime() - duration('P7D')
WITH guard, qualification_score, count(shifts) AS weekly_shifts

// Step 4: Find optimal assignments for undermanned sites
MATCH (site:Site)-[:REQUIRES_GUARDS]->(requirement)
WHERE requirement.current < requirement.minimum
MATCH (guard)-[assigned:ASSIGNED_TO]->(current_site:Site)
WITH site, requirement, guard, qualification_score, weekly_shifts,
     point.distance(current_site.coordinates, site.coordinates) AS distance
WHERE distance < 50000  // 50km max travel distance
  AND weekly_shifts < 40  // Not overloaded
RETURN site.name,
       collect({
         guard: guard.name,
         qualification_score: round(qualification_score, 3),
         weekly_shifts: weekly_shifts,
         distance_km: round(distance / 1000.0, 1)
       })[0..3] AS recommended_guards
ORDER BY qualification_score DESC;
```

**5. Predictive Risk Scoring**

```cypher
// Calculate risk score for each site based on multiple factors
MATCH (s:Site)
OPTIONAL MATCH (s)<-[:OCCURRED_AT]-(recent_incidents:Incident)
WHERE recent_incidents.incident_time > datetime() - duration('P30D')

OPTIONAL MATCH (s)<-[:ASSIGNED_TO]-(guards:Guard)-[cert:CERTIFIED_IN]->(c:Certification)
WHERE cert.expiry_date < datetime() + duration('P30D')  // Expiring soon

OPTIONAL MATCH (s)-[:CONTAINS]->(z:Zone)<-[:MONITORS]-(cameras:Camera)
WHERE cameras.status <> 'Online'

WITH s,
     count(DISTINCT recent_incidents) AS incident_count_30d,
     count(DISTINCT guards) AS guards_with_expiring_certs,
     count(DISTINCT cameras) AS offline_cameras,
     count(DISTINCT z) AS total_zones

// Calculate weighted risk score
WITH s,
     incident_count_30d,
     guards_with_expiring_certs,
     offline_cameras,
     total_zones,
     (incident_count_30d * 3.0 +  // Incidents weighted 3x
      guards_with_expiring_certs * 2.0 +  // Expiring certs 2x
      offline_cameras * 1.5) AS raw_risk_score  // Offline cameras 1.5x

// Normalize to 0-100 scale
WITH s,
     incident_count_30d,
     guards_with_expiring_certs,
     offline_cameras,
     total_zones,
     CASE 
       WHEN raw_risk_score > 20 THEN 100
       ELSE (raw_risk_score / 20.0) * 100
     END AS risk_score

RETURN s.name AS site_name,
       s.site_type,
       round(risk_score, 1) AS risk_score,
       incident_count_30d,
       guards_with_expiring_certs,
       offline_cameras,
       CASE
         WHEN risk_score >= 75 THEN 'Critical'
         WHEN risk_score >= 50 THEN 'High'
         WHEN risk_score >= 25 THEN 'Medium'
         ELSE 'Low'
       END AS risk_level
ORDER BY risk_score DESC;
```

## 3.3 Knowledge Graph Integration Service

**knowledge-graph/graph_service.py**
```python
"""
Knowledge Graph Service
Manages Neo4j graph database and provides reasoning capabilities
"""

from neo4j import AsyncGraphDatabase, AsyncDriver
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeGraphService:
    """Service for interacting with Neo4j knowledge graph"""
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver: AsyncDriver = AsyncGraphDatabase.driver(
            uri, auth=(user, password)
        )
    
    async def close(self):
        """Close the driver connection"""
        await self.driver.close()
    
    async def create_guard_node(self, guard_data: Dict[str, Any]) -> str:
        """Create or update a Guard node in the graph"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (g:Guard {id: $guard_id})
                SET g.twin_id = $twin_id,
                    g.employee_id = $employee_id,
                    g.name = $name,
                    g.email = $email,
                    g.status = $status,
                    g.hire_date = date($hire_date),
                    g.updated_at = datetime()
                RETURN g.id AS guard_id
                """,
                guard_id=guard_data['id'],
                twin_id=guard_data.get('twin_id'),
                employee_id=guard_data['employee_id'],
                name=guard_data['name'],
                email=guard_data['email'],
                status=guard_data['status'],
                hire_date=guard_data['hire_date']
            )
            record = await result.single()
            return record['guard_id']
    
    async def create_site_node(self, site_data: Dict[str, Any]) -> str:
        """Create or update a Site node"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MERGE (s:Site {id: $site_id})
                SET s.twin_id = $twin_id,
                    s.name = $name,
                    s.site_type = $site_type,
                    s.status = $status,
                    s.address = $address,
                    s.coordinates = point({latitude: $latitude, longitude: $longitude}),
                    s.updated_at = datetime()
                RETURN s.id AS site_id
                """,
                site_id=site_data['id'],
                twin_id=site_data.get('twin_id'),
                name=site_data['name'],
                site_type=site_data['site_type'],
                status=site_data['status'],
                address=site_data.get('address'),
                latitude=site_data.get('latitude'),
                longitude=site_data.get('longitude')
            )
            record = await result.single()
            return record['site_id']
    
    async def assign_guard_to_site(
        self,
        guard_id: str,
        site_id: str,
        start_date: str,
        primary: bool = True
    ) -> bool:
        """Create ASSIGNED_TO relationship between Guard and Site"""
        async with self.driver.session() as session:
            await session.run(
                """
                MATCH (g:Guard {id: $guard_id})
                MATCH (s:Site {id: $site_id})
                MERGE (g)-[r:ASSIGNED_TO]->(s)
                SET r.start_date = date($start_date),
                    r.primary = $primary,
                    r.updated_at = datetime()
                """,
                guard_id=guard_id,
                site_id=site_id,
                start_date=start_date,
                primary=primary
            )
            return True
    
    async def record_incident(self, incident_data: Dict[str, Any]) -> str:
        """Record an incident in the knowledge graph"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                CREATE (i:Incident {
                    id: $incident_id,
                    title: $title,
                    description: $description,
                    severity: $severity,
                    category: $category,
                    incident_time: datetime($incident_time),
                    report_time: datetime($report_time),
                    status: $status,
                    created_at: datetime()
                })
                
                WITH i
                MATCH (g:Guard {id: $reported_by})
                CREATE (i)-[:REPORTED_BY]->(g)
                
                WITH i
                MATCH (s:Site {id: $site_id})
                CREATE (i)-[:OCCURRED_AT]->(s)
                
                WITH i
                OPTIONAL MATCH (z:Zone {id: $zone_id})
                FOREACH (_ IN CASE WHEN z IS NOT NULL THEN [1] ELSE [] END |
                    CREATE (i)-[:OCCURRED_IN]->(z)
                )
                
                RETURN i.id AS incident_id
                """,
                incident_id=incident_data['id'],
                title=incident_data['title'],
                description=incident_data['description'],
                severity=incident_data['severity'],
                category=incident_data['category'],
                incident_time=incident_data['incident_time'],
                report_time=incident_data['report_time'],
                status=incident_data['status'],
                reported_by=incident_data['reported_by'],
                site_id=incident_data['site_id'],
                zone_id=incident_data.get('zone_id')
            )
            record = await result.single()
            return record['incident_id']
    
    async def find_qualified_guards_for_site(
        self,
        site_id: str,
        required_certifications: List[str],
        max_distance_km: float = 50.0
    ) -> List[Dict[str, Any]]:
        """Find guards qualified for a specific site"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (target_site:Site {id: $site_id})
                MATCH (g:Guard {status: 'Active'})-[:ASSIGNED_TO]->(current_site:Site)
                
                // Check certifications
                MATCH (g)-[cert:CERTIFIED_IN]->(c:Certification)
                WHERE c.type IN $required_certs
                  AND cert.status = 'Valid'
                  AND cert.expiry_date > date()
                
                // Calculate distance
                WITH g, target_site, current_site,
                     point.distance(current_site.coordinates, target_site.coordinates) AS distance,
                     collect(DISTINCT c.type) AS certifications
                WHERE distance < ($max_distance * 1000)
                  AND size(certifications) = size($required_certs)
                
                // Get recent performance metrics
                OPTIONAL MATCH (g)-[:COMPLETED_SHIFT]->(recent_shift:Shift)
                WHERE recent_shift.end_time > datetime() - duration('P30D')
                
                WITH g, distance, certifications,
                     count(recent_shift) AS shifts_last_30d,
                     avg(recent_shift.performance_score) AS avg_performance
                
                RETURN g.id AS guard_id,
                       g.name AS guard_name,
                       g.employee_id,
                       round(distance / 1000.0, 1) AS distance_km,
                       certifications,
                       shifts_last_30d,
                       round(coalesce(avg_performance, 0), 1) AS avg_performance_score
                ORDER BY distance ASC, avg_performance DESC
                LIMIT 10
                """,
                site_id=site_id,
                required_certs=required_certifications,
                max_distance=max_distance_km
            )
            
            guards = []
            async for record in result:
                guards.append({
                    'guard_id': record['guard_id'],
                    'guard_name': record['guard_name'],
                    'employee_id': record['employee_id'],
                    'distance_km': record['distance_km'],
                    'certifications': record['certifications'],
                    'shifts_last_30d': record['shifts_last_30d'],
                    'avg_performance_score': record['avg_performance_score']
                })
            
            return guards
    
    async def get_site_risk_score(self, site_id: str) -> Dict[str, Any]:
        """Calculate comprehensive risk score for a site"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (s:Site {id: $site_id})
                
                // Recent incidents
                OPTIONAL MATCH (s)<-[:OCCURRED_AT]-(recent_incidents:Incident)
                WHERE recent_incidents.incident_time > datetime() - duration('P30D')
                
                // Guards with expiring certifications
                OPTIONAL MATCH (s)<-[:ASSIGNED_TO]-(guards:Guard)-[cert:CERTIFIED_IN]->(c:Certification)
                WHERE cert.expiry_date < datetime() + duration('P30D')
                
                // Offline cameras
                OPTIONAL MATCH (s)<-[:LOCATED_AT]-(cameras:Camera)
                WHERE cameras.status = 'Offline'
                
                // Missed patrols
                OPTIONAL MATCH (s)<-[:SCHEDULED_AT]-(patrols:Patrol)
                WHERE patrols.status = 'Missed'
                  AND patrols.scheduled_time > datetime() - duration('P7D')
                
                WITH s,
                     count(DISTINCT recent_incidents) AS incident_count,
                     count(DISTINCT guards) AS guards_with_expiring_certs,
                     count(DISTINCT cameras) AS offline_cameras,
                     count(DISTINCT patrols) AS missed_patrols_week
                
                // Calculate weighted risk score
                WITH s,
                     incident_count,
                     guards_with_expiring_certs,
                     offline_cameras,
                     missed_patrols_week,
                     (incident_count * 3.0 +
                      guards_with_expiring_certs * 2.0 +
                      offline_cameras * 1.5 +
                      missed_patrols_week * 2.5) AS raw_score
                
                WITH s,
                     incident_count,
                     guards_with_expiring_certs,
                     offline_cameras,
                     missed_patrols_week,
                     CASE
                       WHEN raw_score > 20 THEN 100
                       ELSE (raw_score / 20.0) * 100
                     END AS risk_score
                
                RETURN s.name AS site_name,
                       round(risk_score, 1) AS risk_score,
                       incident_count,
                       guards_with_expiring_certs,
                       offline_cameras,
                       missed_patrols_week,
                       CASE
                         WHEN risk_score >= 75 THEN 'Critical'
                         WHEN risk_score >= 50 THEN 'High'
                         WHEN risk_score >= 25 THEN 'Medium'
                         ELSE 'Low'
                       END AS risk_level
                """,
                site_id=site_id
            )
            
            record = await result.single()
            if record:
                return {
                    'site_name': record['site_name'],
                    'risk_score': record['risk_score'],
                    'risk_level': record['risk_level'],
                    'contributing_factors': {
                        'incident_count_30d': record['incident_count'],
                        'guards_with_expiring_certs': record['guards_with_expiring_certs'],
                        'offline_cameras': record['offline_cameras'],
                        'missed_patrols_week': record['missed_patrols_week']
                    }
                }
            return None
    
    async def detect_incident_patterns(
        self,
        lookback_days: int = 30,
        min_incidents: int = 3
    ) -> List[Dict[str, Any]]:
        """Detect patterns in incidents for predictive analysis"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (i1:Incident)-[:OCCURRED_IN]->(z:Zone)<-[:OCCURRED_IN]-(i2:Incident)
                WHERE i1.id <> i2.id
                  AND i1.category = i2.category
                  AND i1.incident_time > datetime() - duration({days: $lookback_days})
                  AND abs(duration.between(i1.incident_time, i2.incident_time).hours % 24 - 
                          duration.between(i1.incident_time, datetime()).hours % 24) < 2
                
                WITH z, i1.category AS category,
                     collect(DISTINCT i1) + collect(DISTINCT i2) AS incidents
                WHERE size(incidents) >= $min_incidents
                
                MATCH (z)<-[:CONTAINS]-(s:Site)
                
                WITH s, z, category, incidents
                UNWIND incidents AS incident
                WITH s, z, category, incidents,
                     extract(hour FROM incident.incident_time) AS hour
                
                RETURN s.name AS site_name,
                       s.id AS site_id,
                       z.name AS zone_name,
                       z.id AS zone_id,
                       category,
                       size(incidents) AS incident_count,
                       collect(DISTINCT hour) AS frequent_hours,
                       [i IN incidents | i.incident_time][0..3] AS sample_times
                ORDER BY incident_count DESC
                """,
                lookback_days=lookback_days,
                min_incidents=min_incidents
            )
            
            patterns = []
            async for record in result:
                patterns.append({
                    'site_name': record['site_name'],
                    'site_id': record['site_id'],
                    'zone_name': record['zone_name'],
                    'zone_id': record['zone_id'],
                    'category': record['category'],
                    'incident_count': record['incident_count'],
                    'frequent_hours': record['frequent_hours'],
                    'sample_times': [str(t) for t in record['sample_times']],
                    'recommendation': f"Increase patrols in {record['zone_name']} during hours {record['frequent_hours']}"
                })
            
            return patterns
    
    async def get_guard_context_for_llm(self, guard_id: str) -> Dict[str, Any]:
        """Get comprehensive context about a guard for LLM reasoning"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (g:Guard {id: $guard_id})
                
                // Get certifications
                OPTIONAL MATCH (g)-[cert:CERTIFIED_IN]->(c:Certification)
                
                // Get assigned sites
                OPTIONAL MATCH (g)-[assigned:ASSIGNED_TO]->(s:Site)
                
                // Get recent shifts
                OPTIONAL MATCH (g)-[:WORKED_SHIFT]->(recent_shift:Shift)
                WHERE recent_shift.end_time > datetime() - duration('P30D')
                
                // Get recent incidents reported
                OPTIONAL MATCH (inc:Incident)-[:REPORTED_BY]->(g)
                WHERE inc.incident_time > datetime() - duration('P30D')
                
                // Get completed training
                OPTIONAL MATCH (g)-[completed:COMPLETED]->(tc:TrainingCourse)
                
                RETURN g.id AS guard_id,
                       g.name AS name,
                       g.employee_id,
                       g.status,
                       g.hire_date,
                       collect(DISTINCT {
                         type: c.type,
                         name: c.name,
                         expiry_date: cert.expiry_date,
                         status: cert.status
                       }) AS certifications,
                       collect(DISTINCT {
                         site_id: s.id,
                         site_name: s.name,
                         primary: assigned.primary
                       }) AS assigned_sites,
                       count(DISTINCT recent_shift) AS shifts_last_30d,
                       count(DISTINCT inc) AS incidents_reported_30d,
                       collect(DISTINCT {
                         course: tc.name,
                         completion_date: completed.completion_date,
                         score: completed.score
                       }) AS training_completed
                """,
                guard_id=guard_id
            )
            
            record = await result.single()
            if record:
                return {
                    'guard_id': record['guard_id'],
                    'name': record['name'],
                    'employee_id': record['employee_id'],
                    'status': record['status'],
                    'hire_date': str(record['hire_date']),
                    'certifications': [c for c in record['certifications'] if c['type']],
                    'assigned_sites': [s for s in record['assigned_sites'] if s['site_id']],
                    'shifts_last_30d': record['shifts_last_30d'],
                    'incidents_reported_30d': record['incidents_reported_30d'],
                    'training_completed': [t for t in record['training_completed'] if t['course']]
                }
            return None
    
    async def get_site_context_for_llm(self, site_id: str) -> Dict[str, Any]:
        """Get comprehensive context about a site for LLM reasoning"""
        async with self.driver.session() as session:
            result = await session.run(
                """
                MATCH (s:Site {id: $site_id})
                
                // Get client
                OPTIONAL MATCH (c:Client)-[:OWNS]->(s)
                
                // Get assigned guards
                OPTIONAL MATCH (g:Guard)-[:ASSIGNED_TO]->(s)
                WHERE g.status = 'Active'
                
                // Get zones and checkpoints
                OPTIONAL MATCH (s)-[:CONTAINS]->(z:Zone)
                OPTIONAL MATCH (z)-[:HAS_CHECKPOINT]->(cp:Checkpoint)
                
                // Get cameras
                OPTIONAL MATCH (cam:Camera)-[:LOCATED_AT]->(s)
                
                // Get recent incidents
                OPTIONAL MATCH (inc:Incident)-[:OCCURRED_AT]->(s)
                WHERE inc.incident_time > datetime() - duration('P30D')
                
                // Get compliance requirements
                OPTIONAL MATCH (s)-[:MUST_COMPLY_WITH]->(cr:ComplianceRequirement)
                
                RETURN s.id AS site_id,
                       s.name AS name,
                       s.site_type,
                       s.status,
                       s.address,
                       s.coordinates,
                       c.name AS client_name,
                       count(DISTINCT g) AS guards_assigned,
                       count(DISTINCT z) AS zone_count,
                       count(DISTINCT cp) AS checkpoint_count,
                       count(DISTINCT cam) AS camera_count,
                       count(DISTINCT inc) AS incidents_30d,
                       collect(DISTINCT {
                         requirement: cr.name,
                         framework: cr.framework,
                         severity: cr.severity
                       }) AS compliance_requirements
                """,
                site_id=site_id
            )
            
            record = await result.single()
            if record:
                return {
                    'site_id': record['site_id'],
                    'name': record['name'],
                    'site_type': record['site_type'],
                    'status': record['status'],
                    'address': record['address'],
                    'client_name': record['client_name'],
                    'guards_assigned': record['guards_assigned'],
                    'zone_count': record['zone_count'],
                    'checkpoint_count': record['checkpoint_count'],
                    'camera_count': record['camera_count'],
                    'incidents_30d': record['incidents_30d'],
                    'compliance_requirements': [r for r in record['compliance_requirements'] if r['requirement']]
                }
            return None


# Example usage
async def main():
    kg = KnowledgeGraphService(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="your-password"
    )
    
    try:
        # Find qualified guards for emergency
        qualified = await kg.find_qualified_guards_for_site(
            site_id='SITE001',
            required_certifications=['Healthcare Security', 'First Aid'],
            max_distance_km=30.0
        )
        
        print("Qualified Guards:")
        for guard in qualified:
            print(f"  {guard['guard_name']} - {guard['distance_km']}km away")
        
        # Get site risk score
        risk = await kg.get_site_risk_score('SITE001')
        print(f"\nSite Risk: {risk['risk_score']} ({risk['risk_level']})")
        
        # Detect incident patterns
        patterns = await kg.detect_incident_patterns(lookback_days=30, min_incidents=3)
        print(f"\nDetected {len(patterns)} incident patterns")
        
    finally:
        await kg.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

# 4. Data Synchronization Pipeline

[Continuing with remaining sections...]
