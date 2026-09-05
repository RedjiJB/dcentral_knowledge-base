---
source_project: D Central Live Development
source_project_uuid: 01973716-9da5-7008-a549-0bc747dcf758
doc_uuid: a871cf9e-391c-4405-b769-40967a838959
original_filename: deployment_setup_guide.md
created_at: 2025-06-03T18:38:58.498304+00:00
content_hash: 0adc427b4112
---

# D Central Live Development - Complete Setup Guide

## Quick Start (15 Minutes to First Stream)

### 1. Repository Setup

```bash
# Clone the framework
git clone https://github.com/d-central/federated-dao-framework
cd federated-dao-framework

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
```

### 2. Environment Configuration

```bash
# .env file - fill in your actual values
# Twitch Integration
TWITCH_BOT_USERNAME=dcentral_bot
TWITCH_BOT_TOKEN=oauth:your_twitch_bot_token
TWITCH_CLIENT_ID=your_twitch_client_id
TWITCH_ACCESS_TOKEN=your_twitch_access_token

# GitHub Integration
GITHUB_TOKEN=ghp_your_github_personal_access_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret

# Blockchain RPCs
INFURA_KEY=your_infura_project_id
ALCHEMY_KEY=your_alchemy_api_key
ETHEREUM_RPC=https://mainnet.infura.io/v3/${INFURA_KEY}
POLYGON_RPC=https://polygon-mainnet.infura.io/v3/${INFURA_KEY}
ARBITRUM_RPC=https://arbitrum-mainnet.infura.io/v3/${INFURA_KEY}
BASE_RPC=https://base-mainnet.g.alchemy.com/v2/${ALCHEMY_KEY}

# Database
POSTGRES_PASSWORD=your_secure_password
GRAPH_NODE_DATABASE_URL=postgresql://graph-node:${POSTGRES_PASSWORD}@localhost:5432/graph-node

# Deployment
FLY_API_TOKEN=your_fly_io_token
OVERLAY_WEBHOOK_URL=https://your-overlay-app.fly.dev/webhook
```

### 3. Infrastructure Deployment

```bash
# Start Graph Node infrastructure
cd infrastructure
docker-compose up -d

# Wait for services to be ready
./scripts/wait-for-services.sh

# Deploy overlay system
cd ../overlay-system
npm run build
fly deploy

# Start chatbot
cd ../chatbot
npm run start

# Start WebSocket server
cd ../websocket-server
npm run start
```

## Detailed Component Setup

### Graph Node Infrastructure

```yaml
# infrastructure/docker-compose.yml
version: '3.8'
services:
  graph-node:
    image: graphprotocol/graph-node:v0.34.0
    ports:
      - '8000:8000'  # GraphQL HTTP
      - '8001:8001'  # GraphQL WebSocket  
      - '8020:8020'  # JSON-RPC
      - '8030:8030'  # Index node
      - '8040:8040'  # Metrics
    depends_on:
      - ipfs
      - postgres
    environment:
      postgres_host: postgres
      postgres_user: graph-node
      postgres_pass: ${POSTGRES_PASSWORD}
      postgres_db: graph-node
      ipfs: 'ipfs:5001'
      ethereum: 'mainnet:${ETHEREUM_RPC},polygon:${POLYGON_RPC},arbitrum:${ARBITRUM_RPC},base:${BASE_RPC}'
      GRAPH_LOG: info
      GRAPH_ALLOW_NON_DETERMINISTIC_FULLTEXT_SEARCH: true
      RUST_LOG: info
    volumes:
      - ./data/graph-node:/data
    restart: unless-stopped

  ipfs:
    image: ipfs/go-ipfs:v0.17.0
    ports:
      - '5001:5001'
      - '8080:8080'
    volumes:
      - ./data/ipfs:/data/ipfs
    restart: unless-stopped

  postgres:
    image: postgres:14
    ports:
      - '5432:5432'
    environment:
      POSTGRES_USER: graph-node
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: graph-node
      POSTGRES_INITDB_ARGS: "-E UTF8 --locale=C"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    restart: unless-stopped
```

### Subgraph Deployment

```bash
# Deploy the CredRank subgraph
cd subgraph

# Generate code
npm run codegen

# Build subgraph
npm run build

# Create subgraph on local node
npx graph create --node http://localhost:8020/ d-central/credrank

# Deploy subgraph
npx graph deploy --node http://localhost:8020/ --ipfs http://localhost:5001 d-central/credrank
```

### Twitch Bot Setup

```javascript
// chatbot/config.js
export const CHAT_COMMANDS = {
  // Development Commands
  vote: {
    description: 'Vote on issues or polls',
    usage: '!vote <issue#|poll> <option>',
    cooldown: 5000,
    requiredLevel: 'observer'
  },
  issue: {
    description: 'Create GitHub issue',
    usage: '!issue "title" "description"',
    cooldown: 30000,
    requiredLevel: 'amplifier_l1'
  },
  deploy: {
    description: 'Trigger deployment',
    usage: '!deploy <environment>',
    cooldown: 60000,
    requiredLevel: 'chapter_steward'
  },
  test: {
    description: 'Run test suite',
    usage: '!test <suite>',
    cooldown: 15000,
    requiredLevel: 'amplifier_l1'
  },
  gist: {
    description: 'Submit code via gist',
    usage: '!gist <gist-url>',
    cooldown: 120000,
    requiredLevel: 'amplifier_l2'
  },

  // Information Commands  
  cred: {
    description: 'Check cred score',
    usage: '!cred [username]',
    cooldown: 10000,
    requiredLevel: 'observer'
  },
  passport: {
    description: 'Check Gitcoin Passport',
    usage: '!passport <address>',
    cooldown: 30000,
    requiredLevel: 'amplifier_l1'
  },
  chapter: {
    description: 'Get chapter info',
    usage: '!chapter <name|number>',
    cooldown: 5000,
    requiredLevel: 'observer'
  },

  // Technical Commands
  'ping-node': {
    description: 'Check Graph Node health',
    usage: '!ping-node',
    cooldown: 10000,
    requiredLevel: 'observer'
  },
  query: {
    description: 'Execute GraphQL query',
    usage: '!query <graphql>',
    cooldown: 15000,
    requiredLevel: 'amplifier_l2'
  },
  'cross-chain': {
    description: 'Test cross-chain messaging',
    usage: '!cross-chain <message>',
    cooldown: 30000,
    requiredLevel: 'chapter_steward'
  }
};

// Rate limiting and permissions
export const RATE_LIMITS = {
  global: { requests: 100, window: 60000 }, // 100 requests per minute globally
  perUser: { requests: 10, window: 60000 }, // 10 requests per minute per user
  perCommand: { requests: 5, window: 30000 } // 5 of same command per 30 seconds
};
```

### GitHub Actions Integration

```yaml
# .github/workflows/stream-deploy.yml
name: Stream Development Deploy

on:
  push:
    branches: [main, development]
  repository_dispatch:
    types: [deploy_command, test_command]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production
      triggered_by:
        description: 'Who triggered this deployment'
        required: false

jobs:
  test:
    runs-on: ubuntu-latest
    outputs:
      test-results: ${{ steps.test.outputs.results }}
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        id: test
        run: |
          npm run test:coverage
          echo "results=$(cat coverage/coverage-summary.json)" >> $GITHUB_OUTPUT
      
      - name: Update overlay with test results
        run: |
          curl -X POST ${{ secrets.OVERLAY_WEBHOOK_URL }}/test-results \
            -H "Content-Type: application/json" \
            -d '{"status": "completed", "results": ${{ steps.test.outputs.results }}}'

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          docker build -t dcentral/framework:${{ github.sha }} .
          docker tag dcentral/framework:${{ github.sha }} dcentral/framework:latest
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_HUB_TOKEN }} | docker login -u ${{ secrets.DOCKER_HUB_USERNAME }} --password-stdin
          docker push dcentral/framework:${{ github.sha }}
          docker push dcentral/framework:latest

  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || 'staging' }}
    steps:
      - name: Update overlay with deployment start
        run: |
          curl -X POST ${{ secrets.OVERLAY_WEBHOOK_URL }}/deployment \
            -H "Content-Type: application/json" \
            -d '{"status": "started", "environment": "${{ github.event.inputs.environment }}", "commit": "${{ github.sha }}"}'
      
      - name: Deploy to Fly.io
        uses: superfly/flyctl-actions/setup-flyctl@master
      
      - run: |
          flyctl deploy --remote-only --app dcentral-${{ github.event.inputs.environment }}
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
      
      - name: Update overlay with deployment success
        if: success()
        run: |
          curl -X POST ${{ secrets.OVERLAY_WEBHOOK_URL }}/deployment \
            -H "Content-Type: application/json" \
            -d '{"status": "success", "environment": "${{ github.event.inputs.environment }}", "url": "https://dcentral-${{ github.event.inputs.environment }}.fly.dev"}'
      
      - name: Update overlay with deployment failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.OVERLAY_WEBHOOK_URL }}/deployment \
            -H "Content-Type: application/json" \
            -d '{"status": "failed", "environment": "${{ github.event.inputs.environment }}"}'
      
      - name: Notify Twitch chat
        if: always()
        run: |
          STATUS="${{ job.status }}"
          MESSAGE="🚀 Deployment to ${{ github.event.inputs.environment }}: $STATUS"
          if [ "${{ github.event.inputs.triggered_by }}" != "" ]; then
            MESSAGE="@${{ github.event.inputs.triggered_by }} $MESSAGE"
          fi
          
          curl -X POST "https://api.twitch.tv/helix/chat/messages" \
            -H "Authorization: Bearer ${{ secrets.TWITCH_BOT_TOKEN }}" \
            -H "Client-Id: ${{ secrets.TWITCH_CLIENT_ID }}" \
            -H "Content-Type: application/json" \
            -d "{\"broadcaster_id\": \"${{ secrets.TWITCH_CHANNEL_ID }}\", \"sender_id\": \"${{ secrets.TWITCH_BOT_ID }}\", \"message\": \"$MESSAGE\"}"
```

### OBS Studio Overlay Integration

```html
<!-- obs-overlay.html - Browser source for OBS -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>D Central Stream Overlay</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: 'Roboto Mono', monospace;
            overflow: hidden;
        }
        
        .overlay-container {
            position: relative;
            width: 1920px;
            height: 1080px;
        }
        
        .build-status {
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        }
        
        .build-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }
        
        .build-building {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            animation: pulse 2s infinite;
        }
        
        .build-failed {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .contributor-feed {
            position: absolute;
            bottom: 100px;
            left: 20px;
            width: 400px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 12px;
            padding: 15px;
            color: white;
        }
        
        .viewer-count {
            position: absolute;
            top: 20px;
            left: 20px;
            background: linear-gradient(135deg, #dc2626, #991b1b);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
        }
        
        .deployment-progress {
            position: absolute;
            top: 80px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            min-width: 200px;
        }
        
        .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 3px;
            margin-top: 8px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            transition: width 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="overlay-container">
        <div id="buildStatus" class="build-status build-success">BUILD PASSING</div>
        <div id="viewerCount" class="viewer-count">🔴 LIVE: 0 viewers</div>
        <div id="deploymentProgress" class="deployment-progress" style="display: none;">
            <div>Deploying: <span id="deploymentName">graph-node</span></div>
            <div class="progress-bar">
                <div id="progressFill" class="progress-fill" style="width: 0%"></div>
            </div>
            <div><span id="deploymentPercent">0</span>% complete</div>
        </div>
        <div id="contributorFeed" class="contributor-feed">
            <div style="font-weight: bold; margin-bottom: 10px;">🚀 LIVE CONTRIBUTIONS</div>
            <div id="contributions"></div>
        </div>
    </div>

    <script>
        // Connect to WebSocket for real-time updates
        const ws = new WebSocket('ws://localhost:3001');
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleOverlayUpdate(data);
        };
        
        function handleOverlayUpdate(data) {
            switch(data.type) {
                case 'METRICS_UPDATE':
                    updateMetrics(data.data);
                    break;
                case 'CONTRIBUTOR_UPDATE':
                    addContribution(data.data);
                    break;
                case 'DEPLOYMENT_PROGRESS':
                    updateDeploymentProgress(data.data);
                    break;
                case 'BUILD_STATUS_CHANGE':
                    updateBuildStatus(data.data.status);
                    break;
            }
        }
        
        function updateMetrics(metrics) {
            // Update viewer count
            document.getElementById('viewerCount').textContent = `🔴 LIVE: ${metrics.liveViewers.toLocaleString()} viewers`;
            
            // Update build status
            updateBuildStatus(metrics.buildStatus);
        }
        
        function updateBuildStatus(status) {
            const buildStatus = document.getElementById('buildStatus');
            buildStatus.className = `build-status build-${status}`;
            
            const statusText = {
                'success': 'BUILD PASSING',
                'building': 'BUILDING...',
                'failed': 'BUILD FAILED'
            };
            
            buildStatus.textContent = statusText[status] || 'BUILD UNKNOWN';
        }
        
        function addContribution(contribution) {
            const contributionsDiv = document.getElementById('contributions');
            
            const contributionEl = document.createElement('div');
            contributionEl.style.cssText = 'display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px;';
            contributionEl.innerHTML = `
                <div>
                    <span style="color: #10b981; font-weight: bold;">${contribution.name}</span>
                    <span style="color: #d1d5db;">${contribution.action}</span>
                </div>
                <div style="color: #fbbf24; font-weight: bold;">+${contribution.cred}</div>
            `;
            
            contributionsDiv.insertBefore(contributionEl, contributionsDiv.firstChild);
            
            // Keep only last 5 contributions visible
            while (contributionsDiv.children.length > 5) {
                contributionsDiv.removeChild(contributionsDiv.lastChild);
            }
            
            // Animate new contribution
            contributionEl.style.opacity = '0';
            contributionEl.style.transform = 'translateX(-20px)';
            setTimeout(() => {
                contributionEl.style.transition = 'all 0.3s ease';
                contributionEl.style.opacity = '1';
                contributionEl.style.transform = 'translateX(0)';
            }, 100);
        }
        
        function updateDeploymentProgress(data) {
            const progressDiv = document.getElementById('deploymentProgress');
            
            if (data.status === 'deploying') {
                progressDiv.style.display = 'block';
                document.getElementById('deploymentName').textContent = data.environment || 'staging';
                document.getElementById('progressFill').style.width = `${data.progress || 0}%`;
                document.getElementById('deploymentPercent').textContent = data.progress || 0;
            } else if (data.status === 'success' || data.status === 'failed') {
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                }, 3000);
            }
        }
        
        // Initialize connection
        ws.onopen = function() {
            console.log('Connected to overlay WebSocket');
            ws.send(JSON.stringify({ type: 'REQUEST_METRICS' }));
        };
        
        ws.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    </script>
</body>
</html>
```

## Stream Setup Checklist

### Before Going Live

- [ ] Graph Node running and synced
- [ ] Subgraph deployed and indexing
- [ ] Chatbot connected to Twitch IRC
- [ ] WebSocket server running
- [ ] Overlay displaying in OBS
- [ ] GitHub webhooks configured
- [ ] Deployment pipeline tested
- [ ] Core contributors in Discord
- [ ] Social media cross-posting ready

### OBS Studio Configuration

1. **Scene Setup**:
   - Main Scene: VS Code (fullscreen)
   - Secondary Scene: Terminal + browser
   - Overlay Scene: Browser source pointing to `http://localhost:3000/obs-overlay.html`

2. **Audio Sources**:
   - Desktop Audio (for notifications)
   - Microphone (your voice)
   - Discord Audio (for core contributor calls)

3. **Streaming Settings**:
   - Resolution: 1920x1080
   - FPS: 30
   - Bitrate: 6000 kbps
   - Encoder: x264 (software) or NVENC (hardware)

### Go-Live Protocol

1. **15 minutes before**:
   ```bash
   # Start all services
   docker-compose up -d
   npm run start:chatbot
   npm run start:websocket
   npm run start:overlay
   
   # Test all integrations
   npm run test:integration
   ```

2. **5 minutes before**:
   - Post to Discord: "Going live in 5 minutes!"
   - Test chat commands
   - Verify overlay is updating
   - Check audio levels

3. **Stream start**:
   - "Hello D Central community! Today we're building..."
   - Quick overview of chat commands
   - First interactive poll to engage audience

## Monitoring & Analytics

### Real-Time Metrics Dashboard

Access at `http://localhost:3001/metrics` to see:
- Active viewers
- Chat command usage
- GitHub activity
- Deployment status
- Contributor engagement
- Cross-chain health

### Post-Stream Analytics

```bash
# Generate stream report
npm run generate-report --date=2024-05-26

# Outputs:
# - viewer-engagement.json
# - contributor-stats.json
# - code-changes.json
# - community-decisions.json
```

This setup creates a professional, interactive development environment where the community genuinely participates in building D Central's infrastructure while maintaining code quality and security.