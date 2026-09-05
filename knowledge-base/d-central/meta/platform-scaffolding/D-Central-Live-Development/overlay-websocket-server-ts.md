---
source_project: D Central Live Development
source_project_uuid: 01973716-9da5-7008-a549-0bc747dcf758
doc_uuid: 6e618f04-f48c-403a-852e-83a032460129
original_filename: overlay_websocket_server.ts
created_at: 2025-06-03T18:39:01.481541+00:00
content_hash: 5ae458aad686
topic: livestream-overlay-chatbot-system
---

// Overlay WebSocket Server
// Handles real-time communication between chatbot, GitHub, deployments and overlay

import WebSocket from 'ws';
import { Server } from 'http';
import express from 'express';
import cors from 'cors';
import { Octokit } from '@octokit/rest';
import axios from 'axios';

interface StreamMetrics {
  liveViewers: number;
  totalCommits: number;
  linesOfCode: number;
  testCoverage: number;
  deploymentStatus: string;
  buildStatus: string;
  contributors: ContributorMetric[];
  chapters: ChapterMetric[];
  credLeaderboard: CredLeaderboardEntry[];
  crossChainStatus: CrossChainMetric[];
  chatIssues: ChatIssue[];
  currentStats: CurrentStats;
}

interface ContributorMetric {
  name: string;
  action: string;
  cred: number;
  timestamp: string;
  level: string;
}

interface ChapterMetric {
  name: string;
  members: number;
  budget: string;
  status: string;
  location: string;
}

interface CredLeaderboardEntry {
  name: string;
  cred: number;
  level: string;
  sessionContributions: number;
}

interface CrossChainMetric {
  chain: string;
  status: 'connected' | 'syncing' | 'disconnected';
  blockHeight: string;
  latency: string;
}

interface ChatIssue {
  user: string;
  issue: string;
  votes: number;
  githubIssueNumber?: number;
}

interface CurrentStats {
  totalCommits: number;
  linesOfCode: number;
  testCoverage: number;
  passportVerifications: number;
  activeChapters: number;
  totalCred: number;
}

class OverlayWebSocketServer {
  private wss: WebSocket.Server;
  private app: express.Application;
  private server: Server;
  private github: Octokit;
  private streamMetrics: StreamMetrics;
  private connectedClients: Set<WebSocket> = new Set();
  private metricsUpdateInterval: NodeJS.Timeout | null = null;

  constructor() {
    this.app = express();
    this.setupExpress();
    this.server = this.app.listen(3001);
    this.wss = new WebSocket.Server({ server: this.server });
    this.github = new Octokit({ auth: process.env.GITHUB_TOKEN });
    this.initializeMetrics();
    this.setupWebSocket();
    this.startMetricsUpdates();
  }

  private setupExpress() {
    this.app.use(cors());
    this.app.use(express.json());

    // Health check endpoint
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        connectedClients: this.connectedClients.size,
        lastUpdate: Date.now()
      });
    });

    // Manual metrics endpoint for debugging
    this.app.get('/metrics', (req, res) => {
      res.json(this.streamMetrics);
    });

    // Webhook endpoint for GitHub Actions
    this.app.post('/webhook/deployment', (req, res) => {
      this.handleDeploymentWebhook(req.body);
      res.status(200).send('OK');
    });

    // Webhook endpoint for GitHub issues
    this.app.post('/webhook/github', (req, res) => {
      this.handleGitHubWebhook(req.body);
      res.status(200).send('OK');
    });

    // Twitch EventSub webhook
    this.app.post('/webhook/twitch', (req, res) => {
      this.handleTwitchWebhook(req.body);
      res.status(200).send('OK');
    });
  }

  private setupWebSocket() {
    this.wss.on('connection', (ws: WebSocket) => {
      console.log('New overlay client connected');
      this.connectedClients.add(ws);

      // Send current metrics immediately
      ws.send(JSON.stringify({
        type: 'INITIAL_METRICS',
        data: this.streamMetrics,
        timestamp: Date.now()
      }));

      ws.on('close', () => {
        console.log('Overlay client disconnected');
        this.connectedClients.delete(ws);
      });

      ws.on('error', (error) => {
        console.error('WebSocket error:', error);
        this.connectedClients.delete(ws);
      });

      // Handle messages from overlay (for interactive features)
      ws.on('message', (message: string) => {
        try {
          const data = JSON.parse(message);
          this.handleOverlayMessage(data, ws);
        } catch (error) {
          console.error('Error parsing overlay message:', error);
        }
      });
    });
  }

  private initializeMetrics() {
    this.streamMetrics = {
      liveViewers: 0,
      totalCommits: 0,
      linesOfCode: 0,
      testCoverage: 0,
      deploymentStatus: 'idle',
      buildStatus: 'unknown',
      contributors: [],
      chapters: [],
      credLeaderboard: [],
      crossChainStatus: [
        { chain: 'Ethereum', status: 'disconnected', blockHeight: '0', latency: '0ms' },
        { chain: 'Polygon', status: 'disconnected', blockHeight: '0', latency: '0ms' },
        { chain: 'Arbitrum', status: 'disconnected', blockHeight: '0', latency: '0ms' },
        { chain: 'Base', status: 'disconnected', blockHeight: '0', latency: '0ms' }
      ],
      chatIssues: [],
      currentStats: {
        totalCommits: 0,
        linesOfCode: 0,
        testCoverage: 0,
        passportVerifications: 0,
        activeChapters: 0,
        totalCred: 0
      }
    };
  }

  private startMetricsUpdates() {
    // Update metrics every 30 seconds
    this.metricsUpdateInterval = setInterval(async () => {
      await this.updateMetrics();
      this.broadcastToClients({
        type: 'METRICS_UPDATE',
        data: this.streamMetrics,
        timestamp: Date.now()
      });
    }, 30000);

    // Update viewer count every 10 seconds
    setInterval(async () => {
      await this.updateViewerCount();
    }, 10000);

    // Update cross-chain status every 15 seconds
    setInterval(async () => {
      await this.updateCrossChainStatus();
    }, 15000);
  }

  private async updateMetrics() {
    try {
      // Update GitHub metrics
      await this.updateGitHubMetrics();
      
      // Update build status
      await this.updateBuildStatus();
      
      // Update chapter metrics
      await this.updateChapterMetrics();
      
      // Update contributor stats
      await this.updateContributorStats();

    } catch (error) {
      console.error('Error updating metrics:', error);
    }
  }

  private async updateGitHubMetrics() {
    try {
      // Get repository stats
      const repo = await this.github.rest.repos.get({
        owner: 'd-central',
        repo: 'federated-dao-framework'
      });

      // Get recent commits
      const commits = await this.github.rest.repos.listCommits({
        owner: 'd-central',
        repo: 'federated-dao-framework',
        since: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString() // Last 24 hours
      });

      // Get code frequency
      const codeFreq = await this.github.rest.repos.getCodeFrequencyStats({
        owner: 'd-central',
        repo: 'federated-dao-framework'
      });

      this.streamMetrics.totalCommits = commits.data.length;
      this.streamMetrics.currentStats.totalCommits = commits.data.length;

      // Calculate lines of code (approximation)
      const latestWeek = codeFreq.data[codeFreq.data.length - 1];
      if (latestWeek) {
        this.streamMetrics.linesOfCode = latestWeek[1] - latestWeek[2]; // additions - deletions
        this.streamMetrics.currentStats.linesOfCode = this.streamMetrics.linesOfCode;
      }

    } catch (error) {
      console.error('Error updating GitHub metrics:', error);
    }
  }

  private async updateBuildStatus() {
    try {
      const runs = await this.github.rest.actions.listWorkflowRuns({
        owner: 'd-central',
        repo: 'federated-dao-framework',
        per_page: 1
      });

      if (runs.data.workflow_runs.length > 0) {
        const latestRun = runs.data.workflow_runs[0];
        
        if (latestRun.status === 'in_progress') {
          this.streamMetrics.buildStatus = 'building';
        } else if (latestRun.conclusion === 'success') {
          this.streamMetrics.buildStatus = 'success';
        } else if (latestRun.conclusion === 'failure') {
          this.streamMetrics.buildStatus = 'failed';
        }
      }

    } catch (error) {
      console.error('Error updating build status:', error);
    }
  }

  private async updateViewerCount() {
    try {
      // Mock Twitch API call - replace with actual Twitch API
      const response = await axios.get('https://api.twitch.tv/helix/streams', {
        headers: {
          'Client-ID': process.env.TWITCH_CLIENT_ID,
          'Authorization': `Bearer ${process.env.TWITCH_ACCESS_TOKEN}`
        },
        params: {
          user_login: 'dcentral_build'
        }
      });

      if (response.data.data.length > 0) {
        this.streamMetrics.liveViewers = response.data.data[0].viewer_count;
      }

    } catch (error) {
      // Fallback to mock data if Twitch API fails
      this.streamMetrics.liveViewers = Math.floor(Math.random() * 1000) + 500;
    }
  }

  private async updateCrossChainStatus() {
    const chains = [
      { name: 'Ethereum', rpc: 'https://mainnet.infura.io/v3/' + process.env.INFURA_KEY },
      { name: 'Polygon', rpc: 'https://polygon-mainnet.infura.io/v3/' + process.env.INFURA_KEY },
      { name: 'Arbitrum', rpc: 'https://arbitrum-mainnet.infura.io/v3/' + process.env.INFURA_KEY },
      { name: 'Base', rpc: 'https://base-mainnet.g.alchemy.com/v2/' + process.env.ALCHEMY_KEY }
    ];

    for (const chain of chains) {
      try {
        const start = Date.now();
        const response = await axios.post(chain.rpc, {
          jsonrpc: '2.0',
          method: 'eth_blockNumber',
          params: [],
          id: 1
        }, { timeout: 5000 });

        const latency = Date.now() - start;
        const blockHeight = parseInt(response.data.result, 16);

        const chainMetric = this.streamMetrics.crossChainStatus.find(c => c.chain === chain.name);
        if (chainMetric) {
          chainMetric.status = 'connected';
          chainMetric.blockHeight = blockHeight.toLocaleString();
          chainMetric.latency = `${latency}ms`;
        }

      } catch (error) {
        const chainMetric = this.streamMetrics.crossChainStatus.find(c => c.chain === chain.name);
        if (chainMetric) {
          chainMetric.status = 'disconnected';
          chainMetric.latency = 'timeout';
        }
      }
    }
  }

  private async updateChapterMetrics() {
    // Mock chapter data - replace with actual chapter contract calls
    this.streamMetrics.chapters = [
      { name: 'Toronto', members: 23, budget: '1.2K DCT', status: 'active', location: 'CA' },
      { name: 'Bangalore', members: 18, budget: '800 DCT', status: 'active', location: 'IN' },
      { name: 'Berlin', members: 31, budget: '1.5K DCT', status: 'active', location: 'DE' },
      { name: 'São Paulo', members: 15, budget: '600 DCT', status: 'active', location: 'BR' }
    ];

    this.streamMetrics.currentStats.activeChapters = this.streamMetrics.chapters.length;
  }

  private async updateContributorStats() {
    // This would be populated by the chatbot
    // For now, using mock data
    this.streamMetrics.credLeaderboard = [
      { name: 'alice_dev', cred: 2840, level: 'Core Contributor', sessionContributions: 5 },
      { name: 'bob_builder', cred: 1920, level: 'Chapter Steward', sessionContributions: 3 },
      { name: 'charlie_code', cred: 1340, level: 'Amplifier L2', sessionContributions: 7 },
      { name: 'diana_dao', cred: 890, level: 'Amplifier L1', sessionContributions: 2 },
      { name: 'eve_engineer', cred: 720, level: 'Amplifier L1', sessionContributions: 4 }
    ];

    this.streamMetrics.currentStats.totalCred = this.streamMetrics.credLeaderboard.reduce(
      (total, contributor) => total + contributor.cred, 0
    );
  }

  // Webhook handlers
  private handleDeploymentWebhook(data: any) {
    console.log('Deployment webhook received:', data);
    
    if (data.action === 'completed') {
      this.streamMetrics.deploymentStatus = data.conclusion === 'success' ? 'success' : 'failed';
      
      this.broadcastToClients({
        type: 'DEPLOYMENT_COMPLETE',
        data: {
          status: this.streamMetrics.deploymentStatus,
          environment: data.environment,
          duration: data.duration
        },
        timestamp: Date.now()
      });
    }
  }

  private handleGitHubWebhook(data: any) {
    console.log('GitHub webhook received:', data);
    
    if (data.action === 'opened' && data.issue) {
      // New issue created
      const chatIssue: ChatIssue = {
        user: data.issue.user.login,
        issue: data.issue.title,
        votes: 0,
        githubIssueNumber: data.issue.number
      };
      
      this.streamMetrics.chatIssues.unshift(chatIssue);
      if (this.streamMetrics.chatIssues.length > 10) {
        this.streamMetrics.chatIssues.pop();
      }
      
      this.broadcastToClients({
        type: 'NEW_ISSUE',
        data: chatIssue,
        timestamp: Date.now()
      });
    }
  }

  private handleTwitchWebhook(data: any) {
    console.log('Twitch webhook received:', data);
    
    if (data.subscription?.type === 'stream.online') {
      this.broadcastToClients({
        type: 'STREAM_ONLINE',
        data: { streamer: data.event.broadcaster_user_name },
        timestamp: Date.now()
      });
    }
  }

  private handleOverlayMessage(data: any, ws: WebSocket) {
    switch (data.type) {
      case 'REQUEST_METRICS':
        ws.send(JSON.stringify({
          type: 'METRICS_RESPONSE',
          data: this.streamMetrics,
          timestamp: Date.now()
        }));
        break;
        
      case 'TRIGGER_ANIMATION':
        this.broadcastToClients({
          type: 'ANIMATION_TRIGGER',
          data: data.animation,
          timestamp: Date.now()
        });
        break;
    }
  }

  // Public methods for chatbot integration
  public updateContributor(contributorData: ContributorMetric) {
    // Add or update contributor in the feed
    this.streamMetrics.contributors.unshift(contributorData);
    
    // Keep only last 10 contributions
    if (this.streamMetrics.contributors.length > 10) {
      this.streamMetrics.contributors.pop();
    }
    
    // Update leaderboard
    const existingContributor = this.streamMetrics.credLeaderboard.find(
      c => c.name === contributorData.name
    );
    
    if (existingContributor) {
      existingContributor.cred += contributorData.cred;
      existingContributor.sessionContributions++;
    } else {
      this.streamMetrics.credLeaderboard.push({
        name: contributorData.name,
        cred: contributorData.cred,
        level: contributorData.level,
        sessionContributions: 1
      });
    }
    
    // Sort leaderboard by cred
    this.streamMetrics.credLeaderboard.sort((a, b) => b.cred - a.cred);
    
    // Keep top 10
    this.streamMetrics.credLeaderboard = this.streamMetrics.credLeaderboard.slice(0, 10);
    
    this.broadcastToClients({
      type: 'CONTRIBUTOR_UPDATE',
      data: contributorData,
      timestamp: Date.now()
    });
  }

  public updateChatIssue(issueData: ChatIssue) {
    this.streamMetrics.chatIssues.unshift(issueData);
    if (this.streamMetrics.chatIssues.length > 10) {
      this.streamMetrics.chatIssues.pop();
    }
    
    this.broadcastToClients({
      type: 'CHAT_ISSUE_UPDATE',
      data: issueData,
      timestamp: Date.now()
    });
  }

  public updateDeploymentProgress(progress: number, status: string) {
    this.streamMetrics.deploymentStatus = status;
    
    this.broadcastToClients({
      type: 'DEPLOYMENT_PROGRESS',
      data: { progress, status },
      timestamp: Date.now()
    });
  }

  private broadcastToClients(message: any) {
    const messageString = JSON.stringify(message);
    
    this.connectedClients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(messageString);
      }
    });
  }

  public stop() {
    if (this.metricsUpdateInterval) {
      clearInterval(this.metricsUpdateInterval);
    }
    
    this.wss.close();
    this.server.close();
    console.log('Overlay WebSocket server stopped');
  }
}

// Start the server
const overlayServer = new OverlayWebSocketServer();
console.log('🔴 Overlay WebSocket Server running on port 3001');

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down overlay server...');
  overlayServer.stop();
  process.exit(0);
});

export default OverlayWebSocketServer;