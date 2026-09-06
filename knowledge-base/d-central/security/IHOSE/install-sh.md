---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 0da36558-6813-46fd-9d0e-4d62e11c59b8
original_filename: install.sh
created_at: 2025-12-02T00:47:55.067525+00:00
content_hash: a0c26462eb3e
topic: ihose-quickstart-install
topic: "ihose-openvision-documentation-package"
consolidated_into: [docs/DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001.md, docs/DC-IHOSE-QUICKSTART-RECONCILED-001.md]
---

#!/bin/bash
# OpenVision Platform - Quick Installation Script
# This script automates the installation of OpenVision Platform

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Display banner
display_banner() {
    echo -e "${BLUE}"
    cat << "EOF"
   ___                  __     ___     _           
  / _ \ _ __   ___ _ _ \ \   / (_)___(_) ___  _ __  
 | | | | '_ \ / _ \ '_ \ \ \ / /| / __| |/ _ \| '_ \ 
 | |_| | |_) |  __/ | | \ V / | \__ \ | (_) | | | |
  \___/| .__/ \___|_| |_|\_/  |_|___/_|\___/|_| |_|
       |_|                                           
EOF
    echo -e "${NC}"
    echo "OpenVision Platform - Installation Script"
    echo "Version 1.0.0"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    local missing_deps=()
    
    # Check for required commands
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if ! command_exists git; then
        missing_deps+=("git")
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_info "Please install them and run this script again."
        exit 1
    fi
    
    # Check Docker daemon
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_success "All prerequisites satisfied"
}

# Detect deployment type
select_deployment_type() {
    echo ""
    print_info "Select deployment type:"
    echo "1) Household (1-5 cameras, single device)"
    echo "2) Small Business (10-50 cameras, single server)"
    echo "3) Enterprise (100+ cameras, distributed)"
    echo ""
    read -p "Enter choice [1-3]: " deployment_choice
    
    case $deployment_choice in
        1)
            DEPLOYMENT_TYPE="household"
            COMPOSE_FILE="deployment/docker/household-stack.yml"
            ;;
        2)
            DEPLOYMENT_TYPE="smb"
            COMPOSE_FILE="deployment/docker/core-stack.yml"
            ;;
        3)
            DEPLOYMENT_TYPE="enterprise"
            print_warning "Enterprise deployment requires Kubernetes"
            print_info "Please refer to docs/deployment/enterprise.md"
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
    
    print_success "Deployment type: $DEPLOYMENT_TYPE"
}

# Generate configuration
generate_config() {
    print_info "Generating configuration..."
    
    cd "$PROJECT_ROOT"
    
    # Copy example config
    if [ ! -f configs/.env ]; then
        cp configs/env.example configs/.env
        
        # Generate secure passwords
        print_info "Generating secure passwords..."
        
        POSTGRES_PASSWORD=$(openssl rand -base64 32)
        REDIS_PASSWORD=$(openssl rand -base64 32)
        MINIO_PASSWORD=$(openssl rand -base64 32)
        JWT_SECRET=$(openssl rand -base64 64)
        KEYCLOAK_PASSWORD=$(openssl rand -base64 24)
        GRAFANA_PASSWORD=$(openssl rand -base64 24)
        
        # Replace placeholders
        sed -i "s/POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD_HERE/POSTGRES_PASSWORD=$POSTGRES_PASSWORD/" configs/.env
        sed -i "s/REDIS_PASSWORD=CHANGE_ME_STRONG_PASSWORD_HERE/REDIS_PASSWORD=$REDIS_PASSWORD/" configs/.env
        sed -i "s/S3_SECRET_KEY=CHANGE_ME_SECRET_KEY/S3_SECRET_KEY=$MINIO_PASSWORD/" configs/.env
        sed -i "s/JWT_SECRET=CHANGE_ME_JWT_SECRET/JWT_SECRET=$JWT_SECRET/" configs/.env
        sed -i "s/KEYCLOAK_ADMIN_PASSWORD=CHANGE_ME_KEYCLOAK_ADMIN_PASSWORD/KEYCLOAK_ADMIN_PASSWORD=$KEYCLOAK_PASSWORD/" configs/.env
        sed -i "s/GRAFANA_ADMIN_PASSWORD=CHANGE_ME_GRAFANA_PASSWORD/GRAFANA_ADMIN_PASSWORD=$GRAFANA_PASSWORD/" configs/.env
        
        sed -i "s/SCALE=enterprise/SCALE=$DEPLOYMENT_TYPE/" configs/.env
        
        print_success "Configuration generated at configs/.env"
        print_warning "IMPORTANT: Save these credentials securely!"
        echo ""
        echo "Grafana Admin Password: $GRAFANA_PASSWORD"
        echo "Keycloak Admin Password: $KEYCLOAK_PASSWORD"
        echo ""
    else
        print_info "Configuration already exists at configs/.env"
        read -p "Overwrite? (y/N): " overwrite
        if [[ $overwrite =~ ^[Yy]$ ]]; then
            mv configs/.env configs/.env.backup
            print_info "Backed up existing config to configs/.env.backup"
            generate_config
            return
        fi
    fi
}

# Create required directories
create_directories() {
    print_info "Creating required directories..."
    
    cd "$PROJECT_ROOT"
    
    mkdir -p data/{frigate,postgres,redis,minio,grafana,prometheus,loki}
    mkdir -p logs
    mkdir -p models
    mkdir -p configs/{frigate,mosquitto,prometheus,grafana}
    
    # Set permissions
    chmod 755 data
    chmod 755 logs
    
    print_success "Directories created"
}

# Download ML models
download_models() {
    print_info "Downloading AI models..."
    
    cd "$PROJECT_ROOT/models"
    
    # Download YOLOv8 model
    if [ ! -f yolov8n.pt ]; then
        print_info "Downloading YOLOv8n model..."
        wget -q https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
        print_success "YOLOv8n downloaded"
    else
        print_info "YOLOv8n model already exists"
    fi
    
    cd "$PROJECT_ROOT"
}

# Generate default configs
generate_default_configs() {
    print_info "Generating default configurations..."
    
    cd "$PROJECT_ROOT"
    
    # Frigate config
    if [ ! -f configs/frigate.yml ]; then
        cat > configs/frigate.yml << 'EOF'
mqtt:
  host: mosquitto
  port: 1883
  user: openvision
  password: "{FRIGATE_MQTT_PASSWORD}"

database:
  path: /media/frigate/frigate.db

detectors:
  coral:
    type: cpu

cameras:
  # Add your cameras here
  # Example:
  # front_door:
  #   ffmpeg:
  #     inputs:
  #       - path: rtsp://username:password@192.168.1.100:554/stream1
  #         roles:
  #           - detect
  #           - record
  #   detect:
  #     enabled: true
  #     width: 1920
  #     height: 1080
  #   record:
  #     enabled: true
  #     retain:
  #       days: 30
  #       mode: motion
EOF
        print_success "Default Frigate config created"
    fi
    
    # Mosquitto config
    if [ ! -f configs/mosquitto.conf ]; then
        cat > configs/mosquitto.conf << 'EOF'
listener 1883
listener 9883
protocol websockets

allow_anonymous false
password_file /mosquitto/config/passwd

persistence true
persistence_location /mosquitto/data/
EOF
        print_success "Mosquitto config created"
    fi
    
    # Create mosquitto password file
    if [ ! -f configs/mosquitto-passwd ]; then
        touch configs/mosquitto-passwd
        # Note: Run mosquitto_passwd manually to add users
        print_info "Run: docker run --rm -v $(pwd)/configs:/config eclipse-mosquitto mosquitto_passwd -b /config/mosquitto-passwd openvision YOUR_PASSWORD"
    fi
}

# Pull Docker images
pull_images() {
    print_info "Pulling Docker images (this may take a while)..."
    
    cd "$PROJECT_ROOT"
    
    docker-compose -f "$COMPOSE_FILE" pull
    
    print_success "Docker images pulled"
}

# Start services
start_services() {
    print_info "Starting OpenVision Platform..."
    
    cd "$PROJECT_ROOT"
    
    docker-compose -f "$COMPOSE_FILE" up -d
    
    print_success "Services started"
    
    # Wait for services to be ready
    print_info "Waiting for services to initialize (30 seconds)..."
    sleep 30
}

# Check service health
check_health() {
    print_info "Checking service health..."
    
    cd "$PROJECT_ROOT"
    
    # Check running containers
    local running_containers=$(docker-compose -f "$COMPOSE_FILE" ps --services --filter "status=running" | wc -l)
    local total_containers=$(docker-compose -f "$COMPOSE_FILE" ps --services | wc -l)
    
    print_info "Running containers: $running_containers/$total_containers"
    
    if [ "$running_containers" -eq "$total_containers" ]; then
        print_success "All services are running"
    else
        print_warning "Some services are not running"
        docker-compose -f "$COMPOSE_FILE" ps
    fi
}

# Display access information
display_access_info() {
    echo ""
    print_success "Installation complete!"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Access Information${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "Web Interface: http://localhost"
    echo "Grafana Dashboard: http://localhost:3000"
    echo "Frigate: http://localhost:5000"
    echo "Node-RED: http://localhost:1880"
    echo "MinIO Console: http://localhost:9001"
    echo ""
    echo -e "${YELLOW}Default Credentials:${NC}"
    echo "  Grafana: admin / (see configs/.env)"
    echo "  Keycloak: admin / (see configs/.env)"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Configure your cameras in configs/frigate.yml"
    echo "2. Add camera credentials"
    echo "3. Restart Frigate: docker-compose restart frigate"
    echo "4. Check logs: docker-compose logs -f"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  Getting Started: docs/quickstart-camera.md"
    echo "  Configuration: docs/configuration.md"
    echo "  Troubleshooting: docs/troubleshooting.md"
    echo ""
    print_info "Configuration file: configs/.env"
    print_warning "IMPORTANT: Save your credentials securely!"
    echo ""
}

# Cleanup function
cleanup() {
    print_info "Cleaning up..."
    cd "$PROJECT_ROOT"
}

# Main installation flow
main() {
    display_banner
    check_prerequisites
    select_deployment_type
    generate_config
    create_directories
    generate_default_configs
    download_models
    pull_images
    start_services
    check_health
    display_access_info
    
    cleanup
}

# Trap errors
trap 'print_error "Installation failed at line $LINENO"; cleanup; exit 1' ERR

# Run main installation
main

exit 0


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/ihose-openvision-documentation-package|ihose-openvision-documentation-package]]
- [[knowledge-base/_topics/ihose-quickstart-install|ihose-quickstart-install]]

**Consolidated into:**
- [[docs/DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001]]
- [[docs/DC-IHOSE-QUICKSTART-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
