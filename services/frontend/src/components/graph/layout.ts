import type { GraphLink, GraphNode, WisdomEntry } from '../../types/domain';

export const SECTION_COLORS = {
  images: '#8b5cf6',
  css: '#06b6d4',
  html: '#f59e0b',
  javascript: '#eab308',
  accessibility: '#3b82f6',
  performance: '#10b981',
  git: '#a16207',
  debugging: '#a855f7',
  'qa-tooling': '#f97316',
  operations: '#ef4444',
  networking: '#0ea5e9',
  ux: '#ec4899',
  'code-craft': '#14b8a6',
  wisdom: '#d946ef',
  devops: '#22c55e',
  general: '#6366f1',
  architecture: '#0d9488',
  'remote-repo': '#84cc16'
} as const;

export const SECTION_LABELS = {
  images: 'Web Images',
  css: 'CSS & Styling',
  html: 'HTML & Semantics',
  javascript: 'JavaScript',
  accessibility: 'Accessibility',
  performance: 'Performance',
  git: 'Version Control',
  debugging: 'Debugging',
  'qa-tooling': 'Quality Assurance & Tooling',
  operations: 'Operations & Reliability',
  networking: 'Networking',
  ux: 'User Experience',
  'code-craft': 'Code Craft',
  wisdom: 'Wisdom',
  devops: 'DevOps',
  general: 'General Wisdom',
  architecture: 'Architecture & Modularization',
  'remote-repo': 'Remote Repository Processing'
} as const;

export type SectionColorKey = keyof typeof SECTION_COLORS | 'fallback';

export function sectionColorKey(section: string): SectionColorKey {
  return section in SECTION_COLORS ? section as keyof typeof SECTION_COLORS : 'fallback';
}

export function sectionColor(section: string): string {
  const colorKey = sectionColorKey(section);
  return colorKey === 'fallback' ? '#777' : SECTION_COLORS[colorKey];
}

export function sectionLabel(section: string): string {
  return section in SECTION_LABELS
    ? SECTION_LABELS[section as keyof typeof SECTION_LABELS]
    : section;
}

export interface PositionedNode extends GraphNode {
  x: number;
  y: number;
  tags: string[];
}

export function joinTags(nodes: GraphNode[], wisdom: WisdomEntry[]): Array<GraphNode & { tags: string[] }> {
  const tagsById = new Map(wisdom.map((entry) => [entry.id, entry.tags]));
  return nodes.map((node) => ({ ...node, tags: tagsById.get(node.id) ?? [] }));
}

export function filterGraph(
  nodes: Array<GraphNode & { tags: string[] }>,
  edges: GraphLink[],
  tag: string
): { nodes: Array<GraphNode & { tags: string[] }>; edges: GraphLink[] } {
  const visible = tag ? nodes.filter((node) => node.tags.includes(tag)) : nodes;
  const ids = new Set(visible.map((node) => node.id));
  return { nodes: visible, edges: edges.filter((edge) => ids.has(edge.source) && ids.has(edge.target)) };
}

export function radialLayout(
  nodes: Array<GraphNode & { tags: string[] }>,
  width = 960,
  height = 620
): PositionedNode[] {
  const groups = new Map<string, Array<GraphNode & { tags: string[] }>>();
  for (const node of nodes) {
    const sectionNodes = groups.get(node.section);
    if (sectionNodes) sectionNodes.push(node);
    else groups.set(node.section, [node]);
  }
  const sections = [...groups.keys()].sort();
  const centerX = width / 2;
  const centerY = height / 2;
  const sectionRadius = Math.min(width, height) * 0.31;
  const clusterRadius = Math.max(24, Math.min(90, sectionRadius * 0.34));
  return sections.flatMap((section, sectionIndex) => {
    const angle = (sectionIndex / Math.max(sections.length, 1)) * Math.PI * 2 - Math.PI / 2;
    const clusterX = centerX + Math.cos(angle) * sectionRadius;
    const clusterY = centerY + Math.sin(angle) * sectionRadius;
    const group = groups.get(section)!.slice().sort((a, b) => a.id.localeCompare(b.id));
    return group.map((node, index) => {
      const nodeAngle = (index / Math.max(group.length, 1)) * Math.PI * 2;
      const ring = clusterRadius * (0.35 + 0.65 * ((index % 4) + 1) / 4);
      return { ...node, x: clusterX + Math.cos(nodeAngle) * ring, y: clusterY + Math.sin(nodeAngle) * ring };
    });
  });
}

export function selectedTag(search: string): string {
  return new URLSearchParams(search).get('tag') ?? '';
}
