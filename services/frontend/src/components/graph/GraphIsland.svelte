<script lang="ts">
  import { onMount } from 'svelte';
  import type { GraphLink, GraphNode, WisdomEntry } from '../../types/domain';
  import { joinTags, radialLayout, type PositionedNode } from './layout';

  let allNodes = $state<Array<GraphNode & { tags: string[] }>>([]);
  let allEdges = $state<GraphLink[]>([]);
  let selected = $state<PositionedNode | null>(null);
  let loading = $state(true);
  let error = $state('');

  const nodes = $derived(radialLayout(allNodes));
  const positioned = $derived(new Map(nodes.map((node) => [node.id, node])));
  const edges = $derived(allEdges.filter((edge) => positioned.has(edge.source) && positioned.has(edge.target)));

  function selectNode(node: PositionedNode) {
    selected = node;
  }

  function handleNodeKeydown(event: KeyboardEvent, node: PositionedNode) {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    selectNode(node);
  }

  onMount(() => {
    void (async () => {
      try {
        // Data flow: API response -> joinTags -> radialLayout -> SVG render -> selectNode -> <aside>.
        const [graphResponse, wisdomResponse] = await Promise.all([
          fetch('/api/v1/graph', { cache: 'no-store' }),
          fetch('/api/v1/wisdom/sample', { cache: 'no-store' })
        ]);
        if (!graphResponse.ok || !wisdomResponse.ok) throw new Error('The live graph is unavailable.');
        const graph: { nodes: GraphNode[]; edges: GraphLink[] } = await graphResponse.json();
        const wisdom: WisdomEntry[] = await wisdomResponse.json();
        allNodes = joinTags(graph.nodes, wisdom);
        allEdges = graph.edges;
      } catch (reason) {
        error = reason instanceof Error ? reason.message : 'The live graph is unavailable.';
      } finally {
        loading = false;
      }
    })();
  });
</script>

<section class="graph-island" aria-labelledby="graph-title">
  <header>
    <h1 id="graph-title">TTOD knowledge graph</h1>
    <p>{nodes.length} nodes · {edges.length} edges</p>
  </header>
  <div class="legend" aria-label="Origin legend">
    <span class="human">Human</span><span class="studio">Studio</span><span class="blackbox">AI proposal</span><span class="mixed">Mixed</span><span class="legacy-unknown">Legacy</span>
  </div>
  {#if loading}<p>Loading live graph…</p>{:else if error}<p role="alert">{error}</p>{:else if nodes.length === 0}<p>No graph nodes are available.</p>{:else}
    <svg viewBox="0 0 960 620" role="group" aria-label={`Knowledge graph with ${nodes.length} nodes and ${edges.length} edges`}>
      <g class="edges">{#each edges as edge}<line x1={positioned.get(edge.source)?.x} y1={positioned.get(edge.source)?.y} x2={positioned.get(edge.target)?.x} y2={positioned.get(edge.target)?.y}><title>{edge.rel}</title></line>{/each}</g>
      <g>{#each nodes as node (node.id)}<circle class:deprecated={node.status === 'deprecated'} class={`node ${node.origin}`} cx={node.x} cy={node.y} r="5" tabindex="0" role="button" aria-label={`${node.id}: ${node.text}`} onclick={() => selectNode(node)} onkeydown={(event) => handleNodeKeydown(event, node)}><title>{node.id} · {node.origin} · {node.text}</title></circle>{/each}</g>
    </svg>
  {/if}
  <aside aria-labelledby="graph-node-details-title" aria-live="polite" aria-atomic="true">
    <h2 id="graph-node-details-title">Selected node</h2>
    {#if selected}
      <strong>{selected.id}</strong>
      <p>{selected.text}</p>
      <small>{selected.section} · {selected.origin}</small>
    {:else}
      <p>Select a node to view its details.</p>
    {/if}
  </aside>
</section>

<style>
  .graph-island { font-family: ui-sans-serif, system-ui, sans-serif; }
  header { align-items: end; display: flex; justify-content: space-between; gap: 1rem; }
  h1 { margin-bottom: 0; } header p { margin-top: .25rem; opacity: .7; }
  svg { background: color-mix(in srgb, Canvas 96%, #9c7a31); border: 1px solid #7775; border-radius: 1rem; width: 100%; }
  line { stroke: #7776; stroke-width: .65; }
  circle { cursor: pointer; fill: #678; stroke: Canvas; stroke-width: 1.5; }
  circle.human { fill: #208a58; } circle.studio { fill: #3178c6; } circle.blackbox { fill: #d33; stroke: #ffda00; stroke-width: 2.5; } circle.mixed { fill: #d3a11f; } circle.legacy-unknown { fill: #777; }
  circle.deprecated { opacity: .35; stroke-dasharray: 2 2; }
  .legend { display: flex; flex-wrap: wrap; gap: 1rem; margin-block: 1rem; }
  .legend span::before { background: #678; border-radius: 50%; content: ''; display: inline-block; height: .7rem; margin-right: .35rem; width: .7rem; }
  .legend .human::before { background: #208a58; } .legend .studio::before { background: #3178c6; } .legend .blackbox::before { background: #d33; outline: 2px solid #ffda00; } .legend .mixed::before { background: #d3a11f; } .legend .legacy-unknown::before { background: #777; }
  aside { margin-block: 1rem; border-inline-start: .25rem solid #9c7a31; padding: .75rem 1rem; }
</style>
