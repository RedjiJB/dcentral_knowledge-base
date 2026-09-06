---
source_project: D Central Live Development
source_project_uuid: 01973716-9da5-7008-a549-0bc747dcf758
doc_uuid: 1d0c454c-5dc9-438c-a4e5-892074dacfee
original_filename: streaming_overlay_system.tsx
created_at: 2025-06-03T18:39:02.334655+00:00
content_hash: 1f0962aed602
topic: livestream-overlay-chatbot-system
consolidated_into: docs/DC-LIVESTREAM-OVERLAY-RECONCILED-001.md
---

import React, { useState, useEffect } from 'react';
import { Activity, GitBranch, Users, MapPin, Trophy, Zap, ExternalLink, CheckCircle, XCircle } from 'lucide-react';

// Mock data - in real implementation, this would come from WebSocket connections
const mockData = {
  buildStatus: 'success',
  currentDeployment: 'graph-node-setup',
  deploymentProgress: 75,
  liveViewers: 847,
  contributors: [
    { name: 'alice_dev', action: 'merged PR #142', cred: 50, timestamp: '2 min ago' },
    { name: 'bob_builder', action: 'fixed docker issue', cred: 30, timestamp: '5 min ago' },
    { name: 'charlie_code', action: 'suggested optimization', cred: 15, timestamp: '8 min ago' },
    { name: 'diana_dao', action: 'voted on architecture', cred: 10, timestamp: '12 min ago' }
  ],
  chapters: [
    { name: 'Toronto', members: 23, budget: '1.2K DCT', status: 'active' },
    { name: 'Bangalore', members: 18, budget: '800 DCT', status: 'active' },
    { name: 'Berlin', members: 31, budget: '1.5K DCT', status: 'active' }
  ],
  credLeaderboard: [
    { name: 'alice_dev', cred: 2840, level: 'Core Contributor' },
    { name: 'bob_builder', cred: 1920, level: 'Chapter Steward' },
    { name: 'charlie_code', cred: 1340, level: 'Amplifier L2' },
    { name: 'diana_dao', cred: 890, level: 'Amplifier L1' },
    { name: 'eve_engineer', cred: 720, level: 'Amplifier L1' }
  ],
  crossChainStatus: [
    { chain: 'Ethereum', status: 'connected', blockHeight: '19,234,567', latency: '12ms' },
    { chain: 'Polygon', status: 'connected', blockHeight: '54,123,890', latency: '8ms' },
    { chain: 'Arbitrum', status: 'syncing', blockHeight: '187,654,321', latency: '15ms' },
    { chain: 'Base', status: 'connected', blockHeight: '12,456,789', latency: '6ms' }
  ],
  latestChatIssues: [
    { user: 'stream_user_1', issue: 'Add mobile responsive design to dashboard', votes: 23 },
    { user: 'stream_user_2', issue: 'Optimize graph node indexing speed', votes: 18 },
    { user: 'stream_user_3', issue: 'Add chapter budget visualization', votes: 15 }
  ],
  currentStats: {
    totalCommits: 142,
    linesOfCode: 12847,
    testCoverage: 84,
    passportVerifications: 67
  }
};

const StreamOverlay = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [activeTab, setActiveTab] = useState(0);
  
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const tabTimer = setInterval(() => {
      setActiveTab(prev => (prev + 1) % 4);
    }, 8000);
    return () => clearInterval(tabTimer);
  }, []);

  const BuildStatusIndicator = () => (
    <div className="flex items-center space-x-2 bg-gradient-to-r from-gray-900 to-gray-800 px-4 py-2 rounded-lg border border-gray-700">
      {mockData.buildStatus === 'success' ? (
        <CheckCircle className="w-4 h-4 text-green-400" />
      ) : mockData.buildStatus === 'building' ? (
        <Activity className="w-4 h-4 text-yellow-400 animate-pulse" />
      ) : (
        <XCircle className="w-4 h-4 text-red-400" />
      )}
      <span className="text-sm font-medium text-white">
        {mockData.buildStatus === 'success' ? 'BUILD PASSING' : 
         mockData.buildStatus === 'building' ? 'BUILDING...' : 'BUILD FAILED'}
      </span>
    </div>
  );

  const DeploymentProgress = () => (
    <div className="bg-gradient-to-r from-blue-900 to-purple-900 px-4 py-2 rounded-lg border border-blue-700">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-medium text-blue-200">DEPLOYING: {mockData.currentDeployment}</span>
        <span className="text-xs text-blue-300">{mockData.deploymentProgress}%</span>
      </div>
      <div className="w-32 bg-blue-800 rounded-full h-1.5">
        <div 
          className="bg-gradient-to-r from-blue-400 to-purple-400 h-1.5 rounded-full transition-all duration-300"
          style={{ width: `${mockData.deploymentProgress}%` }}
        />
      </div>
    </div>
  );

  const LiveViewers = () => (
    <div className="flex items-center space-x-2 bg-gradient-to-r from-red-900 to-pink-900 px-4 py-2 rounded-lg border border-red-700">
      <Users className="w-4 h-4 text-red-300" />
      <span className="text-sm font-bold text-white">{mockData.liveViewers.toLocaleString()}</span>
      <span className="text-xs text-red-200">LIVE</span>
    </div>
  );

  const ContributorFeed = () => (
    <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-lg border border-gray-700 p-3 w-80">
      <div className="flex items-center space-x-2 mb-2">
        <GitBranch className="w-4 h-4 text-green-400" />
        <span className="text-sm font-bold text-white">LIVE CONTRIBUTIONS</span>
      </div>
      <div className="space-y-2 max-h-24 overflow-hidden">
        {mockData.contributors.slice(0, 3).map((contributor, idx) => (
          <div key={idx} className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              <span className="text-green-300 font-medium">{contributor.name}</span>
              <span className="text-gray-300">{contributor.action}</span>
            </div>
            <div className="flex items-center space-x-1">
              <span className="text-yellow-400 font-bold">+{contributor.cred}</span>
              <span className="text-gray-400">{contributor.timestamp}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const ChapterMap = () => (
    <div className="bg-gradient-to-r from-green-900 to-emerald-900 rounded-lg border border-green-700 p-3 w-64">
      <div className="flex items-center space-x-2 mb-2">
        <MapPin className="w-4 h-4 text-green-400" />
        <span className="text-sm font-bold text-white">ACTIVE CHAPTERS</span>
      </div>
      <div className="space-y-1">
        {mockData.chapters.map((chapter, idx) => (
          <div key={idx} className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full" />
              <span className="text-green-300 font-medium">{chapter.name}</span>
            </div>
            <div className="text-right">
              <div className="text-white">{chapter.members} members</div>
              <div className="text-green-400">{chapter.budget}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const CredLeaderboard = () => (
    <div className="bg-gradient-to-r from-purple-900 to-pink-900 rounded-lg border border-purple-700 p-3 w-72">
      <div className="flex items-center space-x-2 mb-2">
        <Trophy className="w-4 h-4 text-yellow-400" />
        <span className="text-sm font-bold text-white">CRED LEADERBOARD</span>
      </div>
      <div className="space-y-1">
        {mockData.credLeaderboard.slice(0, 4).map((contributor, idx) => (
          <div key={idx} className="flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2">
              <span className="text-yellow-400 font-bold">#{idx + 1}</span>
              <span className="text-purple-200 font-medium">{contributor.name}</span>
            </div>
            <div className="text-right">
              <div className="text-yellow-400 font-bold">{contributor.cred.toLocaleString()}</div>
              <div className="text-purple-300 text-xs">{contributor.level}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const CrossChainStatus = () => (
    <div className="bg-gradient-to-r from-blue-900 to-cyan-900 rounded-lg border border-blue-700 p-3 w-80">
      <div className="flex items-center space-x-2 mb-2">
        <Zap className="w-4 h-4 text-blue-400" />
        <span className="text-sm font-bold text-white">CROSS-CHAIN STATUS</span>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {mockData.crossChainStatus.map((chain, idx) => (
          <div key={idx} className="text-xs">
            <div className="flex items-center space-x-1">
              <div className={`w-2 h-2 rounded-full ${
                chain.status === 'connected' ? 'bg-green-400' :
                chain.status === 'syncing' ? 'bg-yellow-400 animate-pulse' :
                'bg-red-400'
              }`} />
              <span className="text-blue-200 font-medium">{chain.chain}</span>
            </div>
            <div className="text-gray-400 ml-3">
              <div>Block: {chain.blockHeight}</div>
              <div>Latency: {chain.latency}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const ChatIssues = () => (
    <div className="bg-gradient-to-r from-orange-900 to-red-900 rounded-lg border border-orange-700 p-3 w-80">
      <div className="flex items-center space-x-2 mb-2">
        <ExternalLink className="w-4 h-4 text-orange-400" />
        <span className="text-sm font-bold text-white">CHAT → GITHUB ISSUES</span>
      </div>
      <div className="space-y-1">
        {mockData.latestChatIssues.map((issue, idx) => (
          <div key={idx} className="text-xs">
            <div className="flex items-center justify-between">
              <span className="text-orange-300 font-medium">{issue.user}</span>
              <span className="text-orange-400">👍 {issue.votes}</span>
            </div>
            <div className="text-gray-300 truncate">{issue.issue}</div>
          </div>
        ))}
      </div>
    </div>
  );

  const CurrentStats = () => (
    <div className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-lg border border-gray-700 p-3 w-64">
      <div className="text-sm font-bold text-white mb-2">DEVELOPMENT STATS</div>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div>
          <div className="text-gray-400">Commits</div>
          <div className="text-white font-bold">{mockData.currentStats.totalCommits}</div>
        </div>
        <div>
          <div className="text-gray-400">Lines of Code</div>
          <div className="text-white font-bold">{mockData.currentStats.linesOfCode.toLocaleString()}</div>
        </div>
        <div>
          <div className="text-gray-400">Test Coverage</div>
          <div className="text-green-400 font-bold">{mockData.currentStats.testCoverage}%</div>
        </div>
        <div>
          <div className="text-gray-400">Verified Users</div>
          <div className="text-blue-400 font-bold">{mockData.currentStats.passportVerifications}</div>
        </div>
      </div>
    </div>
  );

  const RotatingSection = () => {
    const sections = [
      <CredLeaderboard key="leaderboard" />,
      <ChapterMap key="chapters" />,
      <CrossChainStatus key="crosschain" />,
      <ChatIssues key="issues" />
    ];
    
    return (
      <div className="transition-all duration-500">
        {sections[activeTab]}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-black text-white p-4 font-mono">
      {/* Top Bar */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <div className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            D CENTRAL
          </div>
          <div className="text-sm text-gray-400">
            LIVE BUILD SESSION • {currentTime.toLocaleTimeString()}
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <BuildStatusIndicator />
          <DeploymentProgress />
          <LiveViewers />
        </div>
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-12 gap-4">
        {/* Left Column - Always Visible */}
        <div className="col-span-4 space-y-4">
          <ContributorFeed />
          <CurrentStats />
        </div>

        {/* Center Column - Rotating Content */}
        <div className="col-span-4 flex justify-center">
          <RotatingSection />
        </div>

        {/* Right Column - Session Info */}
        <div className="col-span-4 space-y-4">
          <div className="bg-gradient-to-r from-indigo-900 to-purple-900 rounded-lg border border-indigo-700 p-4">
            <div className="text-sm font-bold text-white mb-2">TODAY'S FOCUS</div>
            <div className="text-indigo-200 text-sm mb-3">
              Building self-hosted Graph Node infrastructure with community debugging
            </div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-indigo-300">Stream Duration:</span>
                <span className="text-white">2h 15m</span>
              </div>
              <div className="flex justify-between">
                <span className="text-indigo-300">Next Milestone:</span>
                <span className="text-white">First Subgraph Deploy</span>
              </div>
              <div className="flex justify-between">
                <span className="text-indigo-300">Community Votes:</span>
                <span className="text-white">23 active polls</span>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-900 to-teal-900 rounded-lg border border-green-700 p-4">
            <div className="text-sm font-bold text-white mb-2">CHAT COMMANDS</div>
            <div className="space-y-1 text-xs text-green-200">
              <div><span className="text-green-400">!vote</span> - Influence decisions</div>
              <div><span className="text-green-400">!issue</span> - Create GitHub issue</div>
              <div><span className="text-green-400">!deploy</span> - Trigger deployment</div>
              <div><span className="text-green-400">!test</span> - Run specific tests</div>
              <div><span className="text-green-400">!cred</span> - Check your score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Ticker */}
      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-gray-900 to-gray-800 border-t border-gray-700 py-2">
        <div className="flex items-center space-x-8 animate-marquee">
          <span className="text-green-400">🚀 Graph Node: SYNCING</span>
          <span className="text-blue-400">📊 Subgraph: INDEXING</span>
          <span className="text-purple-400">⚡ Cross-chain: ACTIVE</span>
          <span className="text-yellow-400">👥 Contributors: +{mockData.contributors.length} this session</span>
          <span className="text-pink-400">🏆 Top contributor: alice_dev (+{mockData.contributors[0]?.cred} cred)</span>
          <span className="text-cyan-400">🌐 Chapters: {mockData.chapters.length} active worldwide</span>
        </div>
      </div>

      <style jsx>{`
        @keyframes marquee {
          0% { transform: translateX(100vw); }
          100% { transform: translateX(-100%); }
        }
        .animate-marquee {
          animation: marquee 60s linear infinite;
        }
      `}</style>
    </div>
  );
};

export default StreamOverlay;

<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/livestream-overlay-chatbot-system|livestream-overlay-chatbot-system]]

**Consolidated into:**
- [[docs/DC-LIVESTREAM-OVERLAY-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
