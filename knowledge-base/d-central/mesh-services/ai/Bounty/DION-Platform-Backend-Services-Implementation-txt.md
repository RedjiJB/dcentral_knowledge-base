---
source_project: Bounty
source_project_uuid: 0198b52e-0516-768e-b6d4-182ebfca6ef0
doc_uuid: 56342b0a-3482-40f1-9b52-681afcdc22ac
original_filename: DION Platform - Backend Services Implementation.txt
created_at: 2025-08-23T16:09:09.810257+00:00
content_hash: 977e73fab0ff
topic: "dion-platform-api-backend-architecture"
consolidated_into: docs/DC-DION-API-BACKEND-RECONCILED-001.md
---

// DION Platform - Backend Services Implementation

// =============================================================================
// 1. INTELLIGENCE SERVICE - MAIN CONTROLLER
// =============================================================================

// services/intelligence-service/src/controllers/intelligence.controller.ts
import { Request, Response, NextFunction } from 'express';
import { Body, Controller, Get, Post, Put, Query, Param, UseMiddleware } from 'routing-controllers';
import { Inject, Service } from 'typedi';
import { IntelligenceService } from '../services/intelligence.service';
import { VerificationService } from '../services/verification.service';
import { AuthMiddleware } from '../middlewares/auth.middleware';
import { RateLimitMiddleware } from '../middlewares/rate-limit.middleware';
import { IntelligenceSubmissionDto, IntelligenceSearchDto } from '../dto/intelligence.dto';
import { Logger } from '../utils/logger';

@Controller('/api/v1/intelligence')
@UseMiddleware(AuthMiddleware)
@Service()
export class IntelligenceController {
  
  constructor(
    @Inject() private intelligenceService: IntelligenceService,
    @Inject() private verificationService: VerificationService,
    @Inject() private logger: Logger
  ) {}

  @Post('/collect')
  @UseMiddleware(RateLimitMiddleware({ max: 1000, windowMs: 60000 })) // 1000 per minute
  async submitIntelligence(
    @Body() submission: IntelligenceSubmissionDto,
    req: Request
  ) {
    try {
      this.logger.info('Intelligence submission received', { 
        nodeId: req.user?.nodeId,
        type: submission.type,
        timestamp: submission.timestamp 
      });

      // Validate submission
      await this.intelligenceService.validateSubmission(submission);

      // Verify node attestation
      const nodeVerification = await this.verificationService.verifyNodeAttestation(
        req.user?.nodeId!,
        submission.attestation
      );

      if (!nodeVerification.valid) {
        throw new Error('Invalid node attestation');
      }

      // Process and store intelligence
      const intelligence = await this.intelligenceService.processIntelligence({
        ...submission,
        sourceNodeId: req.user?.nodeId!,
        sourceReputation: nodeVerification.reputation
      });

      // Trigger real-time analysis
      await this.intelligenceService.triggerAnalysis(intelligence.id);

      // Emit real-time update
      req.io?.emit('intelligence:new', {
        id: intelligence.id,
        type: intelligence.type,
        location: intelligence.location,
        confidence: intelligence.confidence,
        timestamp: intelligence.timestamp
      });

      return {
        id: intelligence.id,
        contentHash: intelligence.contentHash,
        status: 'accepted',
        confidence: intelligence.confidence,
        estimatedVerificationTime: '15-30 minutes'
      };

    } catch (error) {
      this.logger.error('Intelligence submission failed', error);
      throw error;
    }
  }

  @Get('/search')
  async searchIntelligence(@Query() searchParams: IntelligenceSearchDto, req: Request) {
    try {
      // Check user permissions for intelligence access
      await this.verificationService.checkIntelligenceAccess(
        req.user?.did!,
        searchParams.privacyLevel || 'public'
      );

      const results = await this.intelligenceService.searchIntelligence({
        ...searchParams,
        userDid: req.user?.did,
        accessLevel: req.user?.accessLevel
      });

      return {
        results: results.data,
        total: results.total,
        limit: searchParams.limit || 50,
        offset: searchParams.offset || 0,
        hasMore: results.hasMore,
        aggregations: results.aggregations
      };

    } catch (error) {
      this.logger.error('Intelligence search failed', error);
      throw error;
    }
  }

  @Get('/:id')
  async getIntelligence(@Param('id') id: string, req: Request) {
    try {
      const intelligence = await this.intelligenceService.getById(id);
      
      if (!intelligence) {
        throw new Error('Intelligence not found');
      }

      // Check access permissions
      await this.verificationService.checkIntelligenceAccess(
        req.user?.did!,
        intelligence.privacyLevel
      );

      return intelligence;

    } catch (error) {
      this.logger.error('Failed to get intelligence', { id, error });
      throw error;
    }
  }

  @Post('/:id/verify')
  async verifyIntelligence(
    @Param('id') id: string,
    @Body() verification: { status: 'verified' | 'disputed'; evidence?: string; confidence?: number },
    req: Request
  ) {
    try {
      const result = await this.verificationService.verifyIntelligence({
        intelligenceId: id,
        verifierDid: req.user?.did!,
        verificationStatus: verification.status,
        evidence: verification.evidence,
        confidence: verification.confidence
      });

      // Emit real-time verification update
      req.io?.emit('intelligence:verified', {
        id,
        verificationStatus: result.status,
        confidence: result.confidence,
        verifierReputation: result.verifierReputation
      });

      return result;

    } catch (error) {
      this.logger.error('Intelligence verification failed', { id, error });
      throw error;
    }
  }
}

// =============================================================================
// 2. INTELLIGENCE SERVICE - BUSINESS LOGIC
// =============================================================================

// services/intelligence-service/src/services/intelligence.service.ts
import { Service, Inject } from 'typedi';
import { Repository } from 'typeorm';
import { Intelligence } from '../entities/intelligence.entity';
import { IntelligenceSource } from '../entities/intelligence-source.entity';
import { DatabaseService } from '../services/database.service';
import { ContentHashingService } from '../services/content-hashing.service';
import { LocationService } from '../services/location.service';
import { CorrelationService } from '../services/correlation.service';
import { QualityAssessmentService } from '../services/quality-assessment.service';
import { NotificationService } from '../services/notification.service';
import { IntelligenceSubmissionDto, IntelligenceSearchParams } from '../dto/intelligence.dto';
import { Logger } from '../utils/logger';

@Service()
export class IntelligenceService {
  private intelligenceRepository: Repository<Intelligence>;
  private sourceRepository: Repository<IntelligenceSource>;

  constructor(
    @Inject() private databaseService: DatabaseService,
    @Inject() private contentHashing: ContentHashingService,
    @Inject() private locationService: LocationService,
    @Inject() private correlationService: CorrelationService,
    @Inject() private qualityAssessment: QualityAssessmentService,
    @Inject() private notificationService: NotificationService,
    @Inject() private logger: Logger
  ) {
    this.intelligenceRepository = this.databaseService.getRepository(Intelligence);
    this.sourceRepository = this.databaseService.getRepository(IntelligenceSource);
  }

  async processIntelligence(submission: IntelligenceSubmissionDto & { 
    sourceNodeId: string; 
    sourceReputation: number; 
  }): Promise<Intelligence> {
    
    // Generate content hash for deduplication
    const contentHash = await this.contentHashing.generateHash(submission.content);
    
    // Check for duplicates
    const existingIntelligence = await this.intelligenceRepository.findOne({
      where: { contentHash }
    });

    if (existingIntelligence) {
      // Update source information for existing intelligence
      await this.addIntelligenceSource(existingIntelligence.id, submission);
      return existingIntelligence;
    }

    // Process location data
    let processedLocation = null;
    if (submission.location) {
      processedLocation = await this.locationService.processLocation(submission.location);
    }

    // Assess initial quality and confidence
    const qualityAssessment = await this.qualityAssessment.assessSubmission({
      type: submission.type,
      content: submission.content,
      sourceReputation: submission.sourceReputation,
      location: processedLocation,
      metadata: submission.metadata
    });

    // Create intelligence record
    const intelligence = this.intelligenceRepository.create({
      contentHash,
      type: submission.type,
      location: processedLocation,
      timestamp: submission.timestamp,
      confidence: qualityAssessment.confidence,
      verificationStatus: 'unverified',
      privacyLevel: submission.privacyLevel || 'public',
      metadata: {
        ...submission.metadata,
        originalSubmission: {
          timestamp: new Date().toISOString(),
          nodeId: submission.sourceNodeId
        },
        qualityMetrics: qualityAssessment.metrics
      },
      tags: submission.tags || []
    });

    await this.intelligenceRepository.save(intelligence);

    // Create source record
    await this.addIntelligenceSource(intelligence.id, submission);

    this.logger.info('Intelligence processed successfully', {
      id: intelligence.id,
      type: intelligence.type,
      confidence: intelligence.confidence
    });

    return intelligence;
  }

  async searchIntelligence(params: IntelligenceSearchParams): Promise<{
    data: Intelligence[];
    total: number;
    hasMore: boolean;
    aggregations?: any;
  }> {
    
    const queryBuilder = this.intelligenceRepository
      .createQueryBuilder('intelligence')
      .leftJoinAndSelect('intelligence.sources', 'sources');

    // Apply filters
    if (params.types && params.types.length > 0) {
      queryBuilder.andWhere('intelligence.type IN (:...types)', { types: params.types });
    }

    if (params.location && params.radius) {
      queryBuilder.andWhere(
        'ST_DWithin(intelligence.location, ST_Point(:lng, :lat)::geography, :radius)',
        {
          lng: params.location.longitude,
          lat: params.location.latitude,
          radius: params.radius
        }
      );
    }

    if (params.timeRange) {
      queryBuilder.andWhere(
        'intelligence.timestamp BETWEEN :start AND :end',
        {
          start: params.timeRange.start,
          end: params.timeRange.end
        }
      );
    }

    if (params.confidenceThreshold) {
      queryBuilder.andWhere('intelligence.confidence >= :threshold', {
        threshold: params.confidenceThreshold
      });
    }

    if (params.verificationRequired) {
      queryBuilder.andWhere('intelligence.verificationStatus != :status', {
        status: 'unverified'
      });
    }

    // Apply privacy filters based on user access
    queryBuilder.andWhere('intelligence.privacyLevel = :level', {
      level: params.accessLevel || 'public'
    });

    // Apply search text if provided
    if (params.search) {
      queryBuilder.andWhere(
        'intelligence.description ILIKE :search OR :search = ANY(intelligence.tags)',
        { search: `%${params.search}%` }
      );
    }

    // Count total results
    const total = await queryBuilder.getCount();

    // Apply pagination
    queryBuilder
      .orderBy('intelligence.timestamp', 'DESC')
      .limit(params.limit || 50)
      .offset(params.offset || 0);

    const data = await queryBuilder.getMany();
    const hasMore = (params.offset || 0) + data.length < total;

    return { data, total, hasMore };
  }

  async triggerAnalysis(intelligenceId: string): Promise<void> {
    // Find correlations with existing intelligence
    const correlations = await this.correlationService.findCorrelations(intelligenceId);
    
    if (correlations.length > 0) {
      await this.notificationService.sendCorrelationNotification({
        intelligenceId,
        correlations
      });
    }

    // Trigger AI analysis pipeline
    await this.correlationService.triggerAIAnalysis(intelligenceId);
  }

  private async addIntelligenceSource(
    intelligenceId: string, 
    submission: IntelligenceSubmissionDto & { sourceNodeId: string; sourceReputation: number }
  ): Promise<void> {
    
    const source = this.sourceRepository.create({
      intelligenceId,
      nodeId: submission.sourceNodeId,
      sensorType: submission.metadata?.sensorType || 'unknown',
      reputation: submission.sourceReputation,
      attestation: submission.attestation,
      collectionTimestamp: submission.timestamp
    });

    await this.sourceRepository.save(source);
  }

  async getById(id: string): Promise<Intelligence | null> {
    return this.intelligenceRepository.findOne({
      where: { id },
      relations: ['sources']
    });
  }
}

// =============================================================================
// 3. EMERGENCY RESPONSE SERVICE
// =============================================================================

// services/emergency-service/src/controllers/emergency.controller.ts
import { Controller, Get, Post, Put, Body, Query, Param, UseMiddleware } from 'routing-controllers';
import { Inject, Service } from 'typedi';
import { EmergencyService } from '../services/emergency.service';
import { MobilizationService } from '../services/mobilization.service';
import { AuthMiddleware } from '../middlewares/auth.middleware';
import { EmergencyAlertDto, MobilizationRequestDto } from '../dto/emergency.dto';
import { Logger } from '../utils/logger';

@Controller('/api/v1/emergency')
@UseMiddleware(AuthMiddleware)
@Service()
export class EmergencyController {

  constructor(
    @Inject() private emergencyService: EmergencyService,
    @Inject() private mobilizationService: MobilizationService,
    @Inject() private logger: Logger
  ) {}

  @Get('/alerts')
  async getEmergencyAlerts(@Query() params: {
    location?: { latitude: number; longitude: number };
    radius?: number;
    severity?: string;
    status?: string;
  }, req: any) {
    
    try {
      const alerts = await this.emergencyService.getActiveAlerts({
        location: params.location,
        radius: params.radius || 50000, // 50km default
        severity: params.severity,
        status: params.status || 'active',
        userAccessLevel: req.user?.accessLevel
      });

      return { alerts };

    } catch (error) {
      this.logger.error('Failed to get emergency alerts', error);
      throw error;
    }
  }

  @Post('/alerts')
  async createEmergencyAlert(@Body() alertData: EmergencyAlertDto, req: any) {
    
    try {
      // Verify user has permission to create alerts
      if (!req.user?.permissions.includes('create:emergency_alert')) {
        throw new Error('Insufficient permissions');
      }

      const alert = await this.emergencyService.createAlert({
        ...alertData,
        createdBy: req.user.did,
        createdAt: new Date()
      });

      // Immediately trigger cascade notifications
      await this.emergencyService.triggerAlertCascade(alert.id);

      // Emit real-time alert to all connected clients in area
      req.io?.to(`location:${alert.location.latitude}:${alert.location.longitude}`)
          .emit('emergency:alert', {
            id: alert.id,
            type: alert.type,
            severity: alert.severity,
            location: alert.location,
            description: alert.description,
            radius: alert.radius
          });

      this.logger.info('Emergency alert created', {
        id: alert.id,
        type: alert.type,
        severity: alert.severity,
        location: alert.location
      });

      return alert;

    } catch (error) {
      this.logger.error('Failed to create emergency alert', error);
      throw error;
    }
  }

  @Post('/mobilize')
  async mobilizeEmergencyResponse(@Body() mobilization: MobilizationRequestDto, req: any) {
    
    try {
      // Verify emergency services credentials
      if (!req.user?.roles.includes('emergency_services')) {
        throw new Error('Emergency services credentials required');
      }

      const mobilizationPlan = await this.mobilizationService.createMobilizationPlan({
        ...mobilization,
        coordinatorId: req.user.did,
        timestamp: new Date()
      });

      // Deploy operators and resources
      const deployment = await this.mobilizationService.executeDeployment(mobilizationPlan.id);

      // Set up real-time coordination hub
      const coordinationHub = await this.mobilizationService.setupCoordinationHub({
        mobilizationId: mobilizationPlan.id,
        alertId: mobilization.alertId,
        coordinatorId: req.user.did
      });

      // Notify all assigned operators
      await this.mobilizationService.notifyAssignedOperators(deployment.assignments);

      this.logger.info('Emergency mobilization initiated', {
        mobilizationId: mobilizationPlan.id,
        operatorsDeployed: deployment.assignments.length,
        estimatedResponseTime: deployment.estimatedResponseTime
      });

      return {
        mobilizationId: mobilizationPlan.id,
        status: 'initiated',
        operatorsAssigned: deployment.assignments.length,
        estimatedResponseTime: deployment.estimatedResponseTime,
        coordinationHub: coordinationHub.url
      };

    } catch (error) {
      this.logger.error('Emergency mobilization failed', error);
      throw error;
    }
  }
}

// =============================================================================
// 4. WEBSOCKET GATEWAY FOR REAL-TIME COMMUNICATION
// =============================================================================

// services/api-gateway/src/websocket/websocket-gateway.ts
import { Server, Socket } from 'socket.io';
import { Service, Inject } from 'typedi';
import { AuthService } from '../services/auth.service';
import { LocationService } from '../services/location.service';
import { Logger } from '../utils/logger';

interface AuthenticatedSocket extends Socket {
  user?: {
    did: string;
    roles: string[];
    location?: { latitude: number; longitude: number };
  };
}

@Service()
export class WebSocketGateway {
  private io: Server;

  constructor(
    @Inject() private authService: AuthService,
    @Inject() private locationService: LocationService,
    @Inject() private logger: Logger
  ) {}

  initializeGateway(io: Server): void {
    this.io = io;

    // Authentication middleware
    io.use(async (socket: AuthenticatedSocket, next) => {
      try {
        const token = socket.handshake.auth.token;
        const user = await this.authService.verifyToken(token);
        
        socket.user = user;
        next();
      } catch (error) {
        next(new Error('Authentication failed'));
      }
    });

    io.on('connection', (socket: AuthenticatedSocket) => {
      this.handleConnection(socket);
    });
  }

  private handleConnection(socket: AuthenticatedSocket): void {
    this.logger.info('WebSocket connection established', {
      socketId: socket.id,
      userDid: socket.user?.did
    });

    // Subscribe to location-based updates
    socket.on('subscribe:location', async (data: { 
      latitude: number; 
      longitude: number; 
      radius: number; 
    }) => {
      const locationRoom = `location:${data.latitude.toFixed(3)}:${data.longitude.toFixed(3)}`;
      socket.join(locationRoom);
      
      this.logger.debug('User subscribed to location updates', {
        userDid: socket.user?.did,
        location: data,
        room: locationRoom
      });
    });

    // Subscribe to intelligence updates
    socket.on('subscribe:intelligence', (filters: {
      types?: string[];
      location?: { latitude: number; longitude: number; radius: number };
    }) => {
      // Join intelligence type rooms
      filters.types?.forEach(type => {
        socket.join(`intelligence:${type}`);
      });

      // Join location-based intelligence room
      if (filters.location) {
        const locationRoom = `intelligence:location:${filters.location.latitude.toFixed(3)}:${filters.location.longitude.toFixed(3)}`;
        socket.join(locationRoom);
      }
    });

    // Subscribe to emergency alerts
    socket.on('subscribe:emergency', (data: {
      location: { latitude: number; longitude: number };
      radius: number;
      minSeverity?: string;
    }) => {
      const emergencyRoom = `emergency:${data.location.latitude.toFixed(3)}:${data.location.longitude.toFixed(3)}`;
      socket.join(emergencyRoom);
    });

    // Handle operator status updates
    socket.on('operator:status_update', async (status: {
      availability: 'available' | 'busy' | 'offline';
      location?: { latitude: number; longitude: number };
    }) => {
      if (socket.user?.roles.includes('operator')) {
        await this.updateOperatorStatus(socket.user.did, status);
        
        // Broadcast to coordination rooms
        socket.broadcast.emit('operator:status_changed', {
          operatorDid: socket.user.did,
          status: status.availability,
          location: status.location
        });
      }
    });

    // Handle coordination messages
    socket.on('coordination:message', (data: {
      room: string;
      message: string;
      type: 'text' | 'location' | 'status';
    }) => {
      socket.to(data.room).emit('coordination:message', {
        from: socket.user?.did,
        message: data.message,
        type: data.type,
        timestamp: new Date().toISOString()
      });
    });

    // Handle disconnection
    socket.on('disconnect', () => {
      this.logger.info('WebSocket connection closed', {
        socketId: socket.id,
        userDid: socket.user?.did
      });
    });
  }

  // Broadcast intelligence updates to subscribed users
  async broadcastIntelligenceUpdate(intelligence: {
    id: string;
    type: string;
    location?: { latitude: number; longitude: number };
    confidence: number;
  }): Promise<void> {
    
    // Broadcast to type-specific rooms
    this.io.to(`intelligence:${intelligence.type}`).emit('intelligence:new', intelligence);

    // Broadcast to location-specific rooms
    if (intelligence.location) {
      const locationRoom = `intelligence:location:${intelligence.location.latitude.toFixed(3)}:${intelligence.location.longitude.toFixed(3)}`;
      this.io.to(locationRoom).emit('intelligence:new', intelligence);
    }
  }

  // Broadcast emergency alerts
  async broadcastEmergencyAlert(alert: {
    id: string;
    type: string;
    severity: string;
    location: { latitude: number; longitude: number };
    radius: number;
    description: string;
  }): Promise<void> {
    
    const alertRoom = `emergency:${alert.location.latitude.toFixed(3)}:${alert.location.longitude.toFixed(3)}`;
    this.io.to(alertRoom).emit('emergency:alert', alert);

    // Also broadcast to wider area based on severity
    if (alert.severity === 'critical') {
      this.io.emit('emergency:critical_alert', alert);
    }
  }

  private async updateOperatorStatus(operatorDid: string, status: any): Promise<void> {
    // Update operator status in database
    // This would integrate with the operator service
  }
}

// =============================================================================
// 5. DATABASE ENTITIES
// =============================================================================

// services/intelligence-service/src/entities/intelligence.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, OneToMany, Index } from 'typeorm';
import { IntelligenceSource } from './intelligence-source.entity';

@Entity('intelligence')
@Index(['type'])
@Index(['timestamp'])
@Index(['location'], { spatial: true })
@Index(['verificationStatus'])
export class Intelligence {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  contentHash: string;

  @Column({
    type: 'enum',
    enum: ['OSINT', 'IMINT', 'SIGINT', 'HUMINT', 'MASINT', 'GEOINT', 'CYBINT', 'FININT', 'TECHINT', 'MEDINT']
  })
  type: string;

  @Column('geometry', { nullable: true, spatialFeatureType: 'Point', srid: 4326 })
  location: object | null;

  @Column('timestamp with time zone')
  timestamp: Date;

  @Column('decimal', { precision: 3, scale: 2 })
  confidence: number;

  @Column({
    type: 'enum',
    enum: ['unverified', 'single_source', 'multi_source', 'expert_verified', 'disputed'],
    default: 'unverified'
  })
  verificationStatus: string;

  @Column({
    type: 'enum',
    enum: ['public', 'restricted', 'confidential', 'secret'],
    default: 'public'
  })
  privacyLevel: string;

  @Column('jsonb', { default: '{}' })
  metadata: object;

  @Column('text', { array: true, default: '{}' })
  tags: string[];

  @Column('text', { nullable: true })
  description: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @OneToMany(() => IntelligenceSource, source => source.intelligence)
  sources: IntelligenceSource[];
}

@Entity('intelligence_sources')
export class IntelligenceSource {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column('uuid')
  intelligenceId: string;

  @Column()
  nodeId: string;

  @Column()
  sensorType: string;

  @Column('decimal', { precision: 10, scale: 2 })
  reputation: number;

  @Column('text')
  attestation: string;

  @Column('timestamp with time zone')
  collectionTimestamp: Date;

  @CreateDateColumn()
  createdAt: Date;
}