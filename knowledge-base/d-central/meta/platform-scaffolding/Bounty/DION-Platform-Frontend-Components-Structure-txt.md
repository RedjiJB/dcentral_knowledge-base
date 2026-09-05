---
source_project: Bounty
source_project_uuid: 0198b52e-0516-768e-b6d4-182ebfca6ef0
doc_uuid: b56027f4-f252-4cb8-a01c-c14419f18bcd
original_filename: DION Platform - Frontend Components Structure.txt
created_at: 2025-08-23T16:09:37.011659+00:00
content_hash: c0de811992c7
---

// DION Platform - Key Frontend Components

// =============================================================================
// 1. MAIN DASHBOARD COMPONENT
// =============================================================================

// apps/web-dashboard/src/pages/Dashboard.tsx
import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Grid, Container, Paper, Typography, Box } from '@mui/material';
import { IntelligenceFeed } from '../features/intelligence/components/IntelligenceFeed';
import { OperatorMap } from '../features/operators/components/OperatorMap';
import { EmergencyAlerts } from '../features/emergency/components/EmergencyAlerts';
import { NetworkStatus } from '../components/common/NetworkStatus';
import { useRealTimeConnection } from '../hooks/useRealTimeConnection';
import { RootState } from '../store/store';

export const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { user, preferences } = useSelector((state: RootState) => state.auth);
  const { isConnected } = useRealTimeConnection();

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      <Grid container spacing={3}>
        
        {/* Network Status Header */}
        <Grid item xs={12}>
          <NetworkStatus isConnected={isConnected} />
        </Grid>

        {/* Emergency Alerts - High Priority */}
        <Grid item xs={12}>
          <EmergencyAlerts />
        </Grid>

        {/* Main Content Grid */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 2, height: '600px' }}>
            <Typography variant="h6" gutterBottom>
              Intelligence Feed
            </Typography>
            <IntelligenceFeed />
          </Paper>
        </Grid>

        {/* Operator Map Sidebar */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 2, height: '600px' }}>
            <Typography variant="h6" gutterBottom>
              Active Operators
            </Typography>
            <OperatorMap />
          </Paper>
        </Grid>

        {/* Analytics Row */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '300px' }}>
            <Typography variant="h6" gutterBottom>
              Platform Metrics
            </Typography>
            {/* Analytics component */}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '300px' }}>
            <Typography variant="h6" gutterBottom>
              Recent Activity
            </Typography>
            {/* Activity feed component */}
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '300px' }}>
            <Typography variant="h6" gutterBottom>
              Your Tasks
            </Typography>
            {/* User tasks component */}
          </Paper>
        </Grid>

      </Grid>
    </Container>
  );
};

// =============================================================================
// 2. INTELLIGENCE FEED COMPONENT
// =============================================================================

// apps/web-dashboard/src/features/intelligence/components/IntelligenceFeed.tsx
import React, { useState, useEffect, useMemo } from 'react';
import { 
  List, 
  ListItem, 
  Card, 
  CardContent, 
  Chip, 
  Typography, 
  Box, 
  IconButton,
  Tooltip,
  Menu,
  MenuItem,
  TextField,
  InputAdornment
} from '@mui/material';
import { 
  FilterList as FilterIcon, 
  Search as SearchIcon,
  Verified as VerifiedIcon,
  Warning as WarningIcon 
} from '@mui/icons-material';
import { useIntelligenceFeed } from '../hooks/useIntelligenceFeed';
import { useIntelligenceFilters } from '../hooks/useIntelligenceFilters';
import { IntelligenceCard } from './IntelligenceCard';
import { IntelligenceType, VerificationStatus } from '../types/intelligence.types';

export const IntelligenceFeed: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAnchor, setFilterAnchor] = useState<null | HTMLElement>(null);
  
  const {
    filters,
    updateFilters,
    clearFilters,
    activeFiltersCount
  } = useIntelligenceFilters();

  const {
    intelligence,
    loading,
    error,
    hasMore,
    loadMore,
    refetch
  } = useIntelligenceFeed({
    filters: {
      ...filters,
      search: searchQuery
    },
    realTime: true
  });

  const filteredIntelligence = useMemo(() => {
    if (!searchQuery) return intelligence;
    
    return intelligence.filter(intel => 
      intel.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      intel.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  }, [intelligence, searchQuery]);

  const handleFilterClick = (event: React.MouseEvent<HTMLElement>) => {
    setFilterAnchor(event.currentTarget);
  };

  const handleFilterClose = () => {
    setFilterAnchor(null);
  };

  const handleTypeFilter = (type: IntelligenceType) => {
    updateFilters({
      types: filters.types?.includes(type) 
        ? filters.types.filter(t => t !== type)
        : [...(filters.types || []), type]
    });
  };

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="400px">
        <Typography color="error">Error loading intelligence feed</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      
      {/* Search and Filter Bar */}
      <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
        <TextField
          fullWidth
          size="small"
          placeholder="Search intelligence..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            )
          }}
        />
        
        <Tooltip title="Filter">
          <IconButton onClick={handleFilterClick} color={activeFiltersCount > 0 ? 'primary' : 'default'}>
            <FilterIcon />
            {activeFiltersCount > 0 && (
              <Chip 
                size="small" 
                label={activeFiltersCount} 
                sx={{ position: 'absolute', top: -8, right: -8 }}
              />
            )}
          </IconButton>
        </Tooltip>
      </Box>

      {/* Active Filters */}
      {activeFiltersCount > 0 && (
        <Box sx={{ mb: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {filters.types?.map(type => (
            <Chip
              key={type}
              label={type}
              onDelete={() => handleTypeFilter(type)}
              size="small"
              color="primary"
              variant="outlined"
            />
          ))}
        </Box>
      )}

      {/* Intelligence List */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <List sx={{ p: 0 }}>
          {filteredIntelligence.map((intel) => (
            <ListItem key={intel.id} sx={{ p: 0, mb: 1 }}>
              <IntelligenceCard intelligence={intel} />
            </ListItem>
          ))}
        </List>

        {/* Load More */}
        {hasMore && (
          <Box textAlign="center" sx={{ mt: 2 }}>
            <IconButton onClick={loadMore} disabled={loading}>
              Load More
            </IconButton>
          </Box>
        )}
      </Box>

      {/* Filter Menu */}
      <Menu
        anchorEl={filterAnchor}
        open={Boolean(filterAnchor)}
        onClose={handleFilterClose}
      >
        <MenuItem onClick={() => handleTypeFilter('OSINT')}>
          OSINT
        </MenuItem>
        <MenuItem onClick={() => handleTypeFilter('IMINT')}>
          IMINT
        </MenuItem>
        <MenuItem onClick={() => handleTypeFilter('SIGINT')}>
          SIGINT
        </MenuItem>
        {/* Add more filter options */}
      </Menu>
    </Box>
  );
};

// =============================================================================
// 3. INTELLIGENCE CARD COMPONENT
// =============================================================================

// apps/web-dashboard/src/features/intelligence/components/IntelligenceCard.tsx
import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Box,
  IconButton,
  Avatar,
  Tooltip,
  Button,
  Collapse,
  LinearProgress
} from '@mui/material';
import {
  ExpandMore as ExpandIcon,
  Verified as VerifiedIcon,
  Warning as WarningIcon,
  LocationOn as LocationIcon,
  Share as ShareIcon,
  Flag as FlagIcon
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { Intelligence } from '../types/intelligence.types';
import { useIntelligenceActions } from '../hooks/useIntelligenceActions';

interface IntelligenceCardProps {
  intelligence: Intelligence;
}

export const IntelligenceCard: React.FC<IntelligenceCardProps> = ({ intelligence }) => {
  const [expanded, setExpanded] = useState(false);
  
  const {
    verify,
    flag,
    share,
    loading
  } = useIntelligenceActions();

  const getVerificationIcon = () => {
    switch (intelligence.verificationStatus) {
      case 'verified':
        return <VerifiedIcon color="success" />;
      case 'disputed':
        return <WarningIcon color="warning" />;
      default:
        return null;
    }
  };

  const getTypeColor = (type: string) => {
    const colors = {
      'OSINT': 'primary',
      'IMINT': 'secondary',
      'SIGINT': 'info',
      'HUMINT': 'success',
      'MASINT': 'warning',
      'GEOINT': 'error'
    } as const;
    
    return colors[type as keyof typeof colors] || 'default';
  };

  return (
    <Card sx={{ width: '100%', mb: 1 }}>
      <CardContent sx={{ pb: 1 }}>
        
        {/* Header */}
        <Box display="flex" alignItems="center" justifyContent="between" mb={1}>
          <Box display="flex" alignItems="center" gap={1}>
            <Chip 
              label={intelligence.type} 
              size="small" 
              color={getTypeColor(intelligence.type)}
            />
            {getVerificationIcon()}
            <Typography variant="caption" color="text.secondary">
              {formatDistanceToNow(new Date(intelligence.timestamp), { addSuffix: true })}
            </Typography>
          </Box>
          
          <Tooltip title="Confidence Score">
            <Box display="flex" alignItems="center" gap={1}>
              <Typography variant="caption">
                {Math.round(intelligence.confidence * 100)}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={intelligence.confidence * 100}
                sx={{ width: 50, height: 4 }}
              />
            </Box>
          </Tooltip>
        </Box>

        {/* Content Preview */}
        <Typography variant="body2" sx={{ mb: 1 }}>
          {intelligence.description}
        </Typography>

        {/* Location */}
        {intelligence.location && (
          <Box display="flex" alignItems="center" gap={0.5} mb={1}>
            <LocationIcon fontSize="small" color="action" />
            <Typography variant="caption" color="text.secondary">
              {intelligence.location.latitude.toFixed(4)}, {intelligence.location.longitude.toFixed(4)}
            </Typography>
          </Box>
        )}

        {/* Tags */}
        <Box display="flex" flexWrap="wrap" gap={0.5}>
          {intelligence.tags.map((tag, index) => (
            <Chip key={index} label={tag} size="small" variant="outlined" />
          ))}
        </Box>

      </CardContent>

      {/* Actions */}
      <CardActions sx={{ pt: 0, justifyContent: 'space-between' }}>
        <Box>
          <Tooltip title="Verify">
            <IconButton 
              size="small" 
              onClick={() => verify(intelligence.id)}
              disabled={loading}
            >
              <VerifiedIcon />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Flag">
            <IconButton 
              size="small"
              onClick={() => flag(intelligence.id)}
              disabled={loading}
            >
              <FlagIcon />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Share">
            <IconButton 
              size="small"
              onClick={() => share(intelligence.id)}
              disabled={loading}
            >
              <ShareIcon />
            </IconButton>
          </Tooltip>
        </Box>

        <IconButton 
          size="small"
          onClick={() => setExpanded(!expanded)}
          sx={{
            transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)',
            transition: 'transform 0.2s'
          }}
        >
          <ExpandIcon />
        </IconButton>
      </CardActions>

      {/* Expanded Content */}
      <Collapse in={expanded}>
        <CardContent sx={{ pt: 0 }}>
          <Typography variant="body2" paragraph>
            <strong>Source:</strong> {intelligence.sources?.[0]?.nodeDID || 'Unknown'}
          </Typography>
          
          {intelligence.metadata && (
            <Box>
              <Typography variant="body2" paragraph>
                <strong>Additional Details:</strong>
              </Typography>
              <pre style={{ fontSize: '12px', overflow: 'auto' }}>
                {JSON.stringify(intelligence.metadata, null, 2)}
              </pre>
            </Box>
          )}
        </CardContent>
      </Collapse>
    </Card>
  );
};

// =============================================================================
// 4. EMERGENCY ALERTS COMPONENT
// =============================================================================

// apps/web-dashboard/src/features/emergency/components/EmergencyAlerts.tsx
import React, { useState } from 'react';
import {
  Alert,
  AlertTitle,
  Box,
  Button,
  Collapse,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Typography,
  Chip,
  Snackbar
} from '@mui/material';
import {
  Close as CloseIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { useEmergencyAlerts } from '../hooks/useEmergencyAlerts';
import { useEmergencyActions } from '../hooks/useEmergencyActions';
import { EmergencyAlert, SeverityLevel } from '../types/emergency.types';

export const EmergencyAlerts: React.FC = () => {
  const [dismissedAlerts, setDismissedAlerts] = useState<Set<string>>(new Set());
  const [selectedAlert, setSelectedAlert] = useState<EmergencyAlert | null>(null);
  
  const { alerts, loading } = useEmergencyAlerts();
  const { respondToAlert, dismissAlert } = useEmergencyActions();

  const activeAlerts = alerts.filter(alert => 
    alert.status === 'active' && !dismissedAlerts.has(alert.id)
  );

  const getSeverityIcon = (severity: SeverityLevel) => {
    switch (severity) {
      case 'critical':
        return <ErrorIcon />;
      case 'high':
        return <WarningIcon />;
      default:
        return <InfoIcon />;
    }
  };

  const getSeverityColor = (severity: SeverityLevel) => {
    switch (severity) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      default:
        return 'success';
    }
  };

  const handleDismiss = (alertId: string) => {
    setDismissedAlerts(prev => new Set(prev.add(alertId)));
  };

  const handleRespond = async (alert: EmergencyAlert) => {
    try {
      await respondToAlert(alert.id);
      setSelectedAlert(null);
    } catch (error) {
      console.error('Failed to respond to alert:', error);
    }
  };

  if (loading || activeAlerts.length === 0) {
    return null;
  }

  return (
    <>
      <Box sx={{ mb: 2 }}>
        {activeAlerts.map((alert) => (
          <Alert
            key={alert.id}
            severity={getSeverityColor(alert.severity)}
            icon={getSeverityIcon(alert.severity)}
            action={
              <Box>
                <Button
                  color="inherit"
                  size="small"
                  onClick={() => setSelectedAlert(alert)}
                  sx={{ mr: 1 }}
                >
                  RESPOND
                </Button>
                <IconButton
                  size="small"
                  color="inherit"
                  onClick={() => handleDismiss(alert.id)}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </Box>
            }
            sx={{ mb: 1 }}
          >
            <AlertTitle>
              {alert.title} - {alert.type}
              <Chip 
                label={alert.severity.toUpperCase()} 
                size="small" 
                sx={{ ml: 1 }}
                color={getSeverityColor(alert.severity)}
              />
            </AlertTitle>
            <Typography variant="body2">
              {alert.description}
            </Typography>
            {alert.location && (
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                Location: {alert.location.latitude.toFixed(4)}, {alert.location.longitude.toFixed(4)}
                {alert.radius && ` (${alert.radius}m radius)`}
              </Typography>
            )}
          </Alert>
        ))}
      </Box>

      {/* Emergency Response Dialog */}
      <Dialog
        open={selectedAlert !== null}
        onClose={() => setSelectedAlert(null)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Emergency Response - {selectedAlert?.title}
        </DialogTitle>
        <DialogContent>
          {selectedAlert && (
            <Box>
              <Typography variant="body1" paragraph>
                {selectedAlert.description}
              </Typography>
              
              <Typography variant="body2" color="text.secondary" paragraph>
                <strong>Type:</strong> {selectedAlert.type}<br/>
                <strong>Severity:</strong> {selectedAlert.severity}<br/>
                <strong>Priority:</strong> {selectedAlert.priority}<br/>
                <strong>Time:</strong> {new Date(selectedAlert.createdAt).toLocaleString()}
              </Typography>

              {selectedAlert.location && (
                <Typography variant="body2" color="text.secondary">
                  <strong>Location:</strong> {selectedAlert.location.latitude.toFixed(4)}, {selectedAlert.location.longitude.toFixed(4)}
                  {selectedAlert.radius && ` (${selectedAlert.radius}m radius)`}
                </Typography>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelectedAlert(null)}>
            Cancel
          </Button>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => selectedAlert && handleRespond(selectedAlert)}
          >
            Respond to Emergency
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

// =============================================================================
// 5. CUSTOM HOOKS
// =============================================================================

// apps/web-dashboard/src/features/intelligence/hooks/useIntelligenceFeed.ts
import { useState, useEffect, useCallback } from 'react';
import { useWebSocket } from '../../../hooks/useWebSocket';
import { intelligenceAPI } from '../services/intelligenceAPI';
import { Intelligence, IntelligenceFilters } from '../types/intelligence.types';

interface UseIntelligenceFeedOptions {
  filters?: IntelligenceFilters;
  realTime?: boolean;
  limit?: number;
}

export const useIntelligenceFeed = ({
  filters = {},
  realTime = false,
  limit = 50
}: UseIntelligenceFeedOptions = {}) => {
  const [intelligence, setIntelligence] = useState<Intelligence[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);

  const { isConnected, subscribe, unsubscribe } = useWebSocket();

  // Load initial data
  const loadIntelligence = useCallback(async (reset = false) => {
    setLoading(true);
    setError(null);

    try {
      const currentOffset = reset ? 0 : offset;
      const response = await intelligenceAPI.search({
        ...filters,
        limit,
        offset: currentOffset
      });

      if (reset) {
        setIntelligence(response.results);
        setOffset(response.results.length);
      } else {
        setIntelligence(prev => [...prev, ...response.results]);
        setOffset(prev => prev + response.results.length);
      }

      setHasMore(response.hasMore);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load intelligence');
    } finally {
      setLoading(false);
    }
  }, [filters, limit, offset]);

  // Load more data
  const loadMore = useCallback(() => {
    if (!loading && hasMore) {
      loadIntelligence();
    }
  }, [loadIntelligence, loading, hasMore]);

  // Refetch data
  const refetch = useCallback(() => {
    setOffset(0);
    loadIntelligence(true);
  }, [loadIntelligence]);

  // Handle real-time updates
  useEffect(() => {
    if (!realTime || !isConnected) return;

    const handleNewIntelligence = (newIntelligence: Intelligence) => {
      // Check if it matches current filters
      if (filters.types && !filters.types.includes(newIntelligence.type)) {
        return;
      }

      setIntelligence(prev => [newIntelligence, ...prev]);
    };

    const handleIntelligenceUpdate = (updatedIntelligence: Intelligence) => {
      setIntelligence(prev => 
        prev.map(intel => 
          intel.id === updatedIntelligence.id ? updatedIntelligence : intel
        )
      );
    };

    subscribe('intelligence:new', handleNewIntelligence);
    subscribe('intelligence:updated', handleIntelligenceUpdate);

    return () => {
      unsubscribe('intelligence:new', handleNewIntelligence);
      unsubscribe('intelligence:updated', handleIntelligenceUpdate);
    };
  }, [realTime, isConnected, filters, subscribe, unsubscribe]);

  // Initial load
  useEffect(() => {
    loadIntelligence(true);
  }, [filters]);

  return {
    intelligence,
    loading,
    error,
    hasMore,
    loadMore,
    refetch
  };
};