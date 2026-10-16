import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import {
  Activity,
  TrendingUp,
  TrendingDown,
  AlertCircle,
  Zap,
  BarChart2,
  ChevronRight,
  X,
  Gauge,
  Clock,
  Info,
  Maximize2,
} from 'lucide-react';
import {
  ASSET_SENTIMENT_DATA,
  AssetSentimentProfile,
  COMPOSITE_SENTIMENT,
  SentimentDataPoint,
} from '../data/marketSentimentData';

interface Props {
  selectedPair: string;
  onSelectPair?: (pair: string) => void;
  primaryColor?: string;
}

export const MarketSentimentIndicator: React.FC<Props> = ({
  selectedPair,
  onSelectPair,
  primaryColor = '#00FF66',
}) => {
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [activeAssetPair, setActiveAssetPair] = useState<string>(selectedPair || 'XAU/USD');
  const [hoveredPoint, setHoveredPoint] = useState<SentimentDataPoint | null>(null);
  const [hoveredPos, setHoveredPos] = useState<{ x: number; y: number } | null>(null);

  // Sync with selectedPair from outside
  useEffect(() => {
    if (selectedPair && ASSET_SENTIMENT_DATA[selectedPair]) {
      setActiveAssetPair(selectedPair);
    }
  }, [selectedPair]);

  const profile: AssetSentimentProfile =
    ASSET_SENTIMENT_DATA[activeAssetPair] || ASSET_SENTIMENT_DATA['XAU/USD'];

  // Refs for D3 SVG canvases
  const sparklineRef = useRef<SVGSVGElement | null>(null);
  const detailChartRef = useRef<SVGSVGElement | null>(null);
  const gaugeRef = useRef<SVGSVGElement | null>(null);

  // =========================================================================
  // 1. D3 SPARKLINE ON THE TICKER RIBBON (Compact View)
  // =========================================================================
  useEffect(() => {
    if (!sparklineRef.current) return;

    const svg = d3.select(sparklineRef.current);
    svg.selectAll('*').remove();

    const data = profile.historical24h;
    const width = 160;
    const height = 32;
    const margin = { top: 4, right: 6, bottom: 4, left: 4 };

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const g = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Color based on sentiment
    const isBullish = profile.currentSentiment >= 55;
    const isBearish = profile.currentSentiment <= 45;
    const strokeColor = isBullish ? '#10b981' : isBearish ? '#f43f5e' : '#f59e0b';
    const gradientId = `spark-grad-${activeAssetPair.replace(/[^a-zA-Z0-9]/g, '')}`;

    // Defs: Area gradient
    const defs = svg.append('defs');
    const grad = defs
      .append('linearGradient')
      .attr('id', gradientId)
      .attr('x1', '0%')
      .attr('y1', '0%')
      .attr('x2', '0%')
      .attr('y2', '100%');

    grad
      .append('stop')
      .attr('offset', '0%')
      .attr('stop-color', strokeColor)
      .attr('stop-opacity', 0.4);

    grad
      .append('stop')
      .attr('offset', '100%')
      .attr('stop-color', strokeColor)
      .attr('stop-opacity', 0.0);

    // Scales
    const xScale = d3
      .scaleLinear()
      .domain([0, data.length - 1])
      .range([0, innerWidth]);

    const yMin = d3.min(data, (d) => d.volatility) ?? 0;
    const yMax = d3.max(data, (d) => d.volatility) ?? 50;

    const yScale = d3
      .scaleLinear()
      .domain([yMin * 0.9, yMax * 1.1])
      .range([innerHeight, 0]);

    // Area generator
    const area = d3
      .area<SentimentDataPoint>()
      .x((_, i) => xScale(i))
      .y0(innerHeight)
      .y1((d) => yScale(d.volatility))
      .curve(d3.curveMonotoneX);

    // Line generator
    const line = d3
      .line<SentimentDataPoint>()
      .x((_, i) => xScale(i))
      .y((d) => yScale(d.volatility))
      .curve(d3.curveMonotoneX);

    // Render filled area
    g.append('path')
      .datum(data)
      .attr('fill', `url(#${gradientId})`)
      .attr('d', area);

    // Render path line
    g.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', strokeColor)
      .attr('stroke-width', 1.75)
      .attr('d', line);

    // Pulsing end circle
    const lastX = xScale(data.length - 1);
    const lastY = yScale(data[data.length - 1].volatility);

    g.append('circle')
      .attr('cx', lastX)
      .attr('cy', lastY)
      .attr('r', 3)
      .attr('fill', strokeColor);

    g.append('circle')
      .attr('cx', lastX)
      .attr('cy', lastY)
      .attr('r', 6)
      .attr('fill', strokeColor)
      .attr('opacity', 0.3)
      .attr('class', 'animate-ping');
  }, [profile, activeAssetPair]);

  // =========================================================================
  // 2. D3 DETAILED 24H VOLATILITY CHART (Expanded View)
  // =========================================================================
  useEffect(() => {
    if (!isExpanded || !detailChartRef.current) return;

    const svg = d3.select(detailChartRef.current);
    svg.selectAll('*').remove();

    const data = profile.historical24h;
    const container = detailChartRef.current.parentElement;
    const width = container ? container.clientWidth : 720;
    const height = 260;
    const margin = { top: 20, right: 35, bottom: 40, left: 45 };

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    svg.attr('width', width).attr('height', height);

    const g = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // X Scale (Index mapped to hours)
    const xScale = d3
      .scaleLinear()
      .domain([0, data.length - 1])
      .range([0, innerWidth]);

    // Y Scale (Volatility %)
    const yMin = d3.min(data, (d) => d.volatility) ?? 10;
    const yMax = d3.max(data, (d) => d.volatility) ?? 50;

    const yScale = d3
      .scaleLinear()
      .domain([Math.max(0, yMin - 4), yMax + 6])
      .range([innerHeight, 0]);

    // Color gradient
    const isBullish = profile.currentSentiment >= 55;
    const isBearish = profile.currentSentiment <= 45;
    const strokeColor = isBullish ? '#10b981' : isBearish ? '#f43f5e' : '#f59e0b';
    const detailGradId = 'detail-volatility-gradient';

    const defs = svg.append('defs');
    const grad = defs
      .append('linearGradient')
      .attr('id', detailGradId)
      .attr('x1', '0%')
      .attr('y1', '0%')
      .attr('x2', '0%')
      .attr('y2', '100%');

    grad.append('stop').attr('offset', '0%').attr('stop-color', strokeColor).attr('stop-opacity', 0.25);
    grad.append('stop').attr('offset', '70%').attr('stop-color', strokeColor).attr('stop-opacity', 0.05);
    grad.append('stop').attr('offset', '100%').attr('stop-color', strokeColor).attr('stop-opacity', 0.0);

    // Horizontal Grid Lines
    const yAxisTicks = yScale.ticks(5);
    g.append('g')
      .attr('class', 'grid')
      .selectAll('line')
      .data(yAxisTicks)
      .enter()
      .append('line')
      .attr('x1', 0)
      .attr('x2', innerWidth)
      .attr('y1', (d) => yScale(d))
      .attr('y2', (d) => yScale(d))
      .attr('stroke', 'rgba(255, 255, 255, 0.05)')
      .attr('stroke-dasharray', '2,2');

    // Axes Layout
    const xAxis = d3.axisBottom(xScale)
      .ticks(Math.min(data.length, 8))
      .tickFormat((d) => `${24 - Math.round(Number(d))}h ago`);
      
    const yAxis = d3.axisLeft(yScale).ticks(5).tickFormat((d) => `${d}%`);

    g.append('g')
      .attr('transform', `translate(0, ${innerHeight})`)
      .call(xAxis)
      .attr('color', 'rgba(255,255,255,0.3)')
      .selectAll('text')
      .attr('fill', '#8A99AD')
      .style('font-size', '10px');

    g.append('g')
      .call(yAxis)
      .attr('color', 'rgba(255,255,255,0.3)')
      .selectAll('text')
      .attr('fill', '#8A99AD')
      .style('font-size', '10px');

    // Volatility Area
    const area = d3
      .area<SentimentDataPoint>()
      .x((_, i) => xScale(i))
      .y0(innerHeight)
      .y1((d) => yScale(d.volatility))
      .curve(d3.curveMonotoneX);

    // Volatility Line
    const line = d3
      .line<SentimentDataPoint>()
      .x((_, i) => xScale(i))
      .y((d) => yScale(d.volatility))
      .curve(d3.curveMonotoneX);

    g.append('path')
      .datum(data)
      .attr('fill', `url(#${detailGradId})`)
      .attr('d', area);

    g.append('path')
      .datum(data)
      .attr('fill', 'none')
      .attr('stroke', strokeColor)
      .attr('stroke-width', 2.5)
      .attr('d', line);

    // Highlight Volatility Spike Annotations & Hover Listeners
    data.forEach((d, i) => {
      const cx = xScale(i);
      const cy = yScale(d.volatility);

      if (d.catalyst) {
        g.append('line')
          .attr('x1', cx)
          .attr('x2', cx)
          .attr('y1', cy)
          .attr('y2', innerHeight)
          .attr('stroke', 'rgba(255,255,255,0.15)')
          .attr('stroke-dasharray', '3,3');

        g.append('circle')
          .attr('cx', cx)
          .attr('cy', cy)
          .attr('r', 5)
          .attr('fill', '#f59e0b')
          .attr('stroke', '#06090F')
          .attr('stroke-width', 1.5)
          .style('cursor', 'pointer');
      }

      // Invisible tracking overlay rectangles for hover detection
      g.append('rect')
        .attr('x', cx - (innerWidth / data.length) / 2)
        .attr('y', 0)
        .attr('width', innerWidth / data.length)
        .attr('height', innerHeight)
        .attr('fill', 'transparent')
        .style('cursor', 'crosshair')
        .on('mousemove', (event) => {
          setHoveredPoint(d);
          setHoveredPos({ x: event.clientX, y: event.clientY });
        })
        .on('mouseleave', () => {
          setHoveredPoint(null);
          setHoveredPos(null);
        });
    });
  }, [isExpanded, profile]);

  // =========================================================================
  // 3. D3 SENTIMENT RADIAL GAUGE (Expanded View)
  // =========================================================================
  useEffect(() => {
