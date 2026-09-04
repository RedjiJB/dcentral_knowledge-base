---
source_project: D Central Live Development
source_project_uuid: 01973716-9da5-7008-a549-0bc747dcf758
doc_uuid: e65b997b-47c7-4475-bc99-e6e2c1d29006
original_filename: chatbot_integration_system.ts
created_at: 2025-06-03T18:38:57.484379+00:00
content_hash: 87a11c58dea9topic: 'amplifier-default-steward'
topic: livestream-overlay-chatbot-system
---

// D Central Interactive Development Chatbot
// Handles Twitch chat commands and integrates with GitHub, deployments, and overlay

import tmi from 'tmi.js';
import { Octokit } from '@octokit/rest';
import axios from 'axios';
import WebSocket from 'ws';
import { EventEmitter } from 'events';

interface ChatCommand {
  command: string;
  args: string[];
  user: string;
  userInfo: {
    username: string;
    displayName: string;
    userId: string;
    isMod: boolean;
    isSubscriber: boolean;
    badges: Record<string, string>;
  };
}

interface StreamEvent {
  type: string;
  data: any;
  timestamp: number;
  user?: string;
}

class DCentralChatBot extends EventEmitter {
  private twitchClient: tmi.Client;
  private github: Octokit;
  private overlayWs: WebSocket | null = null;
  private contributors: Map<string, ContributorData> = new Map();
  private activePolls: Map<string, PollData> = new Map();
  private deploymentStatus: DeploymentStatus = { status: 'idle', progress: 0 };

  constructor() {
    super();
    this.initializeTwitchClient();
    this.initializeGitHub();
    this.initializeOverlayConnection();
    this.setupCommandHandlers();
  }

  private initializeTwitchClient() {
    this.twitchClient = new tmi.Client({
      options: { debug: true },
      connection: {
        reconnect: true,
        secure: true
      },
      identity: {
        username: process.env.TWITCH_BOT_USERNAME,
        password: process.env.TWITCH_BOT_TOKEN
      },
      channels: ['dcentral_build']
    });

    this.twitchClient.connect();

    this.twitchClient.on('message', (channel, tags, message, self) => {
      if (self) return;

      const command = this.parseCommand(message, tags);
      if (command) {
        this.handleCommand(command);
      }
    });
  }

  private initializeGitHub() {
    this.github = new Octokit({
      auth: process.env.GITHUB_TOKEN
    });
  }

  private initializeOverlayConnection() {
    // Connect to overlay WebSocket for real-time updates
    try {
      this.overlayWs = new WebSocket('ws://localhost:3001');
      
      this.overlayWs.on('open', () => {
        console.log('Connected to overlay system');
      });

      this.overlayWs.on('error', (error) => {
        console.error('Overlay connection error:', error);
      });
    } catch (error) {
      console.error('Failed to connect to overlay:', error);
    }
  }

  private parseCommand(message: string, tags: any): ChatCommand | null {
    if (!message.startsWith('!')) return null;

    const parts = message.slice(1).split(' ');
    const command = parts[0].toLowerCase();
    const args = parts.slice(1);

    return {
      command,
      args,
      user: tags.username,
      userInfo: {
        username: tags.username,
        displayName: tags['display-name'],
        userId: tags['user-id'],
        isMod: tags.mod,
        isSubscriber: tags.subscriber,
        badges: tags.badges || {}
      }
    };
  }

  private setupCommandHandlers() {
    // Core development commands
    this.on('command:vote', this.handleVote.bind(this));
    this.on('command:issue', this.handleCreateIssue.bind(this));
    this.on('command:deploy', this.handleDeploy.bind(this));
    this.on('command:test', this.handleTest.bind(this));
    this.on('command:gist', this.handleGist.bind(this));
    this.on('command:cred', this.handleCredCheck.bind(this));
    this.on('command:passport', this.handlePassportCheck.bind(this));
    this.on('command:chapter', this.handleChapterInfo.bind(this));
    this.on('command:debug', this.handleDebug.bind(this));
    this.on('command:poll', this.handleCreatePoll.bind(this));
    this.on('command:suggest', this.handleSuggestion.bind(this));
    
    // Infrastructure commands
    this.on('command:ping-node', this.handlePingNode.bind(this));
    this.on('command:query', this.handleGraphQLQuery.bind(this));
    this.on('command:cross-chain', this.handleCrossChain.bind(this));
    this.on('command:stats', this.handleStats.bind(this));
  }

  private async handleCommand(command: ChatCommand) {
    try {
      console.log(`Processing command: ${command.command} from ${command.user}`);
      
      // Emit command event for handlers
      this.emit(`command:${command.command}`, command);
      
      // Update contributor activity
      await this.updateContributorActivity(command.user, command.command);
      
      // Send activity to overlay
      this.sendToOverlay({
        type: 'COMMAND_EXECUTED',
        data: {
          command: command.command,
          user: command.user,
          args: command.args
        },
        timestamp: Date.now()
      });

    } catch (error) {
      console.error(`Error handling command ${command.command}:`, error);
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Command failed: ${error.message}`);
    }
  }

  // Command Handlers

  private async handleVote(command: ChatCommand) {
    const [target, option] = command.args;
    
    if (!target || !option) {
      this.twitchClient.say('dcentral_build', `@${command.user} Usage: !vote <issue#|poll> <option>`);
      return;
    }

    if (target.startsWith('#')) {
      // GitHub issue vote
      const issueNumber = parseInt(target.slice(1));
      await this.voteOnGitHubIssue(issueNumber, command.user, option);
    } else {
      // Poll vote
      await this.voteOnPoll(target, option, command.user);
    }
  }

  private async handleCreateIssue(command: ChatCommand) {
    const title = command.args.find(arg => arg.startsWith('"') && arg.endsWith('"'))?.slice(1, -1);
    const bodyStart = command.args.findIndex(arg => arg.startsWith('"')) + 1;
    const body = command.args.slice(bodyStart).join(' ').replace(/"/g, '');

    if (!title) {
      this.twitchClient.say('dcentral_build', `@${command.user} Usage: !issue "title" "description"`);
      return;
    }

    try {
      const issue = await this.github.rest.issues.create({
        owner: 'd-central',
        repo: 'federated-dao-framework',
        title: `[Stream] ${title}`,
        body: `**Created by:** @${command.user} during live stream\n\n${body || 'No description provided'}`,
        labels: ['viewer-suggestion', 'stream-generated']
      });

      this.twitchClient.say('dcentral_build', 
        `@${command.user} ✅ Issue #${issue.data.number} created! github.com/d-central/federated-dao-framework/issues/${issue.data.number}`
      );

      await this.awardCred(command.user, 'ISSUE_CREATION', 25);

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Failed to create issue: ${error.message}`);
    }
  }

  private async handleDeploy(command: ChatCommand) {
    const environment = command.args[0] || 'staging';
    
    // Check if user has deployment permissions
    if (!this.canDeploy(command.userInfo)) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Insufficient permissions for deployment`);
      return;
    }

    try {
      this.deploymentStatus = { status: 'deploying', progress: 0, environment };
      
      this.twitchClient.say('dcentral_build', `🚀 Deployment to ${environment} started by @${command.user}`);
      
      // Trigger GitHub Actions deployment
      await this.triggerDeployment(environment, command.user);
      
      await this.awardCred(command.user, 'DEPLOYMENT_TRIGGER', 50);

    } catch (error) {
      this.deploymentStatus = { status: 'failed', progress: 0, error: error.message };
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Deployment failed: ${error.message}`);
    }
  }

  private async handleTest(command: ChatCommand) {
    const testSuite = command.args[0] || 'all';
    
    try {
      this.twitchClient.say('dcentral_build', `🧪 Running tests: ${testSuite}`);
      
      // Trigger test run via GitHub Actions
      const testResult = await this.runTests(testSuite, command.user);
      
      if (testResult.success) {
        this.twitchClient.say('dcentral_build', 
          `@${command.user} ✅ Tests passed! ${testResult.passed}/${testResult.total} • Coverage: ${testResult.coverage}%`
        );
        await this.awardCred(command.user, 'TEST_RUN', 15);
      } else {
        this.twitchClient.say('dcentral_build', 
          `@${command.user} ❌ Tests failed! ${testResult.failed} failures • Check logs for details`
        );
      }

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Test run failed: ${error.message}`);
    }
  }

  private async handleGist(command: ChatCommand) {
    const gistUrl = command.args[0];
    
    if (!gistUrl || !gistUrl.includes('gist.github.com')) {
      this.twitchClient.say('dcentral_build', `@${command.user} Usage: !gist <gist-url>`);
      return;
    }

    try {
      // Create draft PR from gist
      const gistId = gistUrl.split('/').pop();
      const gistData = await this.github.rest.gists.get({ gist_id: gistId });
      
      // Create branch and PR
      const prResult = await this.createPRFromGist(gistData.data, command.user);
      
      this.twitchClient.say('dcentral_build', 
        `@${command.user} ✅ Draft PR created from gist! #${prResult.number} - Ready for review`
      );

      await this.awardCred(command.user, 'CODE_CONTRIBUTION', 40);

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Failed to process gist: ${error.message}`);
    }
  }

  private async handleCredCheck(command: ChatCommand) {
    const targetUser = command.args[0] || command.user;
    const contributor = this.contributors.get(targetUser);
    
    if (!contributor) {
      this.twitchClient.say('dcentral_build', `@${command.user} No cred data for ${targetUser}`);
      return;
    }

    this.twitchClient.say('dcentral_build', 
      `@${command.user} 🏆 ${targetUser}: ${contributor.totalCred} cred • Level: ${contributor.level} • This session: +${contributor.sessionCred}`
    );
  }

  private async handlePassportCheck(command: ChatCommand) {
    const address = command.args[0];
    
    if (!address) {
      this.twitchClient.say('dcentral_build', `@${command.user} Usage: !passport <ethereum-address>`);
      return;
    }

    try {
      const passportData = await this.checkGitcoinPassport(address);
      
      this.twitchClient.say('dcentral_build', 
        `@${command.user} 🛂 ${address}: Score ${passportData.score} • Stamps: ${passportData.stampCount} • Eligible: ${passportData.eligibleRoles.join(', ')}`
      );

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Passport check failed: ${error.message}`);
    }
  }

  private async handlePingNode(command: ChatCommand) {
    try {
      const nodeStatus = await this.checkGraphNodeHealth();
      
      if (nodeStatus.healthy) {
        this.twitchClient.say('dcentral_build', 
          `@${command.user} ✅ Graph Node: Healthy • Synced: ${nodeStatus.syncStatus} • Latency: ${nodeStatus.latency}ms`
        );
      } else {
        this.twitchClient.say('dcentral_build', 
          `@${command.user} ❌ Graph Node: Unhealthy • Status: ${nodeStatus.error}`
        );
      }

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Node check failed: ${error.message}`);
    }
  }

  private async handleGraphQLQuery(command: ChatCommand) {
    const query = command.args.join(' ');
    
    if (!query) {
      this.twitchClient.say('dcentral_build', `@${command.user} Usage: !query <graphql-query>`);
      return;
    }

    try {
      const result = await this.executeGraphQLQuery(query);
      
      this.twitchClient.say('dcentral_build', 
        `@${command.user} ✅ Query executed • Results: ${JSON.stringify(result).slice(0, 100)}...`
      );

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${command.user} ❌ Query failed: ${error.message}`);
    }
  }

  // Utility Methods

  private async voteOnGitHubIssue(issueNumber: number, user: string, reaction: string) {
    try {
      const reactionMap = {
        'yes': '+1',
        'no': '-1',
        'confused': 'confused',
        'heart': 'heart',
        'hooray': 'hooray',
        'laugh': 'laugh',
        'rocket': 'rocket',
        'eyes': 'eyes'
      };

      const reactionType = reactionMap[reaction.toLowerCase()] || '+1';

      await this.github.rest.reactions.createForIssue({
        owner: 'd-central',
        repo: 'federated-dao-framework',
        issue_number: issueNumber,
        content: reactionType as any
      });

      this.twitchClient.say('dcentral_build', `@${user} ✅ Voted ${reaction} on issue #${issueNumber}`);
      await this.awardCred(user, 'ISSUE_VOTE', 5);

    } catch (error) {
      this.twitchClient.say('dcentral_build', `@${user} ❌ Vote failed: ${error.message}`);
    }
  }

  private async triggerDeployment(environment: string, triggeredBy: string) {
    try {
      await this.github.rest.actions.createWorkflowDispatch({
        owner: 'd-central',
        repo: 'federated-dao-framework',
        workflow_id: 'deploy.yml',
        ref: 'main',
        inputs: {
          environment,
          triggered_by: triggeredBy
        }
      });

      // Monitor deployment progress
      this.monitorDeployment(environment);

    } catch (error) {
      throw new Error(`Deployment trigger failed: ${error.message}`);
    }
  }

  private async monitorDeployment(environment: string) {
    const checkInterval = setInterval(async () => {
      try {
        const runs = await this.github.rest.actions.listWorkflowRuns({
          owner: 'd-central',
          repo: 'federated-dao-framework',
          workflow_id: 'deploy.yml',
          per_page: 1
        });

        const latestRun = runs.data.workflow_runs[0];
        
        if (latestRun) {
          this.deploymentStatus.progress = this.calculateDeploymentProgress(latestRun.status);
          
          if (latestRun.conclusion) {
            clearInterval(checkInterval);
            
            if (latestRun.conclusion === 'success') {
              this.deploymentStatus = { status: 'success', progress: 100 };
              this.twitchClient.say('dcentral_build', `✅ Deployment to ${environment} completed successfully!`);
            } else {
              this.deploymentStatus = { status: 'failed', progress: 0, error: latestRun.conclusion };
              this.twitchClient.say('dcentral_build', `❌ Deployment to ${environment} failed: ${latestRun.conclusion}`);
            }
          }
        }

      } catch (error) {
        console.error('Deployment monitoring error:', error);
        clearInterval(checkInterval);
      }
    }, 10000);
  }

  private calculateDeploymentProgress(status: string): number {
    const progressMap = {
      'queued': 10,
      'in_progress': 50,
      'completed': 100
    };
    return progressMap[status] || 0;
  }

  private async awardCred(user: string, action: string, amount: number) {
    const contributor = this.contributors.get(user) || {
      username: user,
      totalCred: 0,
      sessionCred: 0,
      level: 'Observer',
      contributions: []
    };

    contributor.totalCred += amount;
    contributor.sessionCred += amount;
    contributor.contributions.push({
      action,
      amount,
      timestamp: Date.now()
    });

    // Update level based on total cred
    contributor.level = this.calculateLevel(contributor.totalCred);

    this.contributors.set(user, contributor);

    // Send to overlay
    this.sendToOverlay({
      type: 'CRED_AWARDED',
      data: { user, action, amount, newTotal: contributor.totalCred },
      timestamp: Date.now()
    });
  }

  private calculateLevel(totalCred: number): string {
    if (totalCred >= 5000) return 'Core Contributor';
    if (totalCred >= 2000) return 'Chapter Steward';
    if (totalCred >= 500) return 'Amplifier L2';
    if (totalCred >= 100) return 'Amplifier L1';
    return 'Observer';
  }

  private canDeploy(userInfo: any): boolean {
    return userInfo.isMod || 
           userInfo.isSubscriber || 
           userInfo.badges.vip ||
           this.contributors.get(userInfo.username)?.level === 'Core Contributor';
  }

  private sendToOverlay(event: StreamEvent) {
    if (this.overlayWs && this.overlayWs.readyState === WebSocket.OPEN) {
      this.overlayWs.send(JSON.stringify(event));
    }
  }

  private async checkGraphNodeHealth() {
    try {
      const response = await axios.get('http://localhost:8000/graphql', {
        timeout: 5000
      });
      
      return {
        healthy: response.status === 200,
        syncStatus: 'synced',
        latency: response.responseTime || 0
      };
    } catch (error) {
      return {
        healthy: false,
        error: error.message
      };
    }
  }

  private async checkGitcoinPassport(address: string) {
    try {
      const response = await axios.get(`https://api.passport.gitcoin.co/registry/score/${address}`);
      
      return {
        score: response.data.score || 0,
        stampCount: response.data.evidence?.length || 0,
        eligibleRoles: this.determineEligibleRoles(response.data.score || 0)
      };
    } catch (error) {
      throw new Error(`Passport API error: ${error.message}`);
    }
  }

  private determineEligibleRoles(score: number): string[] {
    const roles = [];
    if (score >= 1) roles.push('Amplifier L1');
    if (score >= 10) roles.push('Amplifier L2');
    if (score >= 25) roles.push('Chapter Steward');
    if (score >= 40) roles.push('Mod Guardian');
    if (score >= 60) roles.push('Core Contributor');
    return roles;
  }

  // Start the bot
  public async start() {
    console.log('🤖 D Central Chat Bot starting...');
    
    try {
      await this.twitchClient.connect();
      console.log('✅ Connected to Twitch');
      
      this.twitchClient.say('dcentral_build', 
        '🚀 D Central Development Bot online! Use !help for commands • Building the future of federated DAOs live!'
      );

    } catch (error) {
      console.error('❌ Failed to start bot:', error);
    }
  }
}

// Types
interface ContributorData {
  username: string;
  totalCred: number;
  sessionCred: number;
  level: string;
  contributions: Array<{
    action: string;
    amount: number;
    timestamp: number;
  }>;
}

interface PollData {
  id: string;
  question: string;
  options: string[];
  votes: Map<string, string>;
  endTime: number;
  creator: string;
}

interface DeploymentStatus {
  status: 'idle' | 'deploying' | 'success' | 'failed';
  progress: number;
  environment?: string;
  error?: string;
}

// Initialize and start the bot
const bot = new DCentralChatBot();
bot.start();

export default DCentralChatBot;