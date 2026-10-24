import React from 'react';
import { DataComponent, DataTable, EvidenceChart, ReportSection, RichNarrative, useDataApp } from '../../data-app-public.jsx';
import copy from './report-copy.json';

const tierLabels = { meaningful_request: 'Meaningful request', partial: 'Partial', opaque_to_narrative: 'Opaque to narrative' };
const querySets = {
  overview: ['summary','coverage'], opening: ['anchors'], fire: ['anchors'],
  push: ['anchors','push_window'], late: ['anchors','shoot_types'],
  coverage: ['coverage','summary','slots','opaque_breakdown','phases'],
  methods: ['summary','anchors','coverage'],
};

export function ReportContent() {
  const { reviewedRows, visible } = useDataApp();
  const rows = (id) => reviewedRows(id);
  const anchorRows = rows('anchors');
  function sourceRows(id, query) {
    if (query !== 'anchors') return rows(query);
    if (id === 'opening') return anchorRows.filter(r => r.frame <= 1499);
    if (id === 'fire') return anchorRows.filter(r => r.frame >= 1500 && r.frame <= 5826);
    if (id === 'push') return anchorRows.filter(r => r.frame >= 6125 && r.frame <= 6999);
    if (id === 'late') return anchorRows.filter(r => r.frame >= 9000);
    return anchorRows;
  }
  const coverageRows = rows('coverage').map(r => ({ ...r, label: tierLabels[r.tier] }));
  return <article className="report-content">
    {copy.map(section => {
      const id = `sample1-${section.id}`;
      if (!visible(id)) return null;
      const queryIds = querySets[section.id];
      const sources = Object.fromEntries(queryIds.map(q => [q, sourceRows(section.id, q)]));
      return <React.Fragment key={id}>
        <ReportSection id={id} queryId={queryIds[0]} queryIds={queryIds}
          sourceRows={sources[queryIds[0]]} sourceRowsByQuery={sources}
          title={section.title} showHeading={false}>
          <RichNarrative id={`${id}-body`} value={section.markdown} label={`Edit ${section.title}`} />
        </ReportSection>
        {section.id === 'coverage' && <>
          <EvidenceChart id="sample1-readability-chart" queryId="coverage"
            title="Only one in eight commands has a readable action request"
            description="All4162 commands. These tiers measure requests, not executed battle outcomes."
            rows={coverageRows} sourceRows={rows('coverage')} height={260}
            spec={{type:'horizontalBar',x:'label',y:'commands',xLabel:'Command records',valueDecimals:0}} />
          <DataComponent id="sample1-readability-table" queryId="coverage" title="Readability rubric and full-file coverage"
            sourceRows={rows('coverage')} displayRows={coverageRows}>
            <DataTable searchable={false} caption="Coverage of all4162 command events"
              rows={coverageRows.map(r => ({Tier:r.label,Commands:r.commands,'Share (%)':Number(r.percent.toFixed(1))}))}/>
          </DataComponent>
          <DataComponent id="sample1-slot-table" queryId="slots" title="The readable fraction varies by slot"
            sourceRows={rows('slots')} displayRows={rows('slots')}>
            <DataTable searchable={false} caption="Explicit requested verbs within each slot's standard orders"
              rows={rows('slots').map(r => ({Slot:`S${r.slot}`,'Standard orders':r.standard_orders,
                'Explicit verbs':r.explicit_orders,'Contextual39':r.contextual_orders,'Explicit (%)':Number(r.explicit_percent.toFixed(1))}))}/>
          </DataComponent>
          <DataComponent id="sample1-order-table" queryId="order_counts" title="The476 explicit standard-order requests"
            sourceRows={rows('order_counts')} displayRows={rows('order_counts')}>
            <DataTable searchable={false} caption="Explicit order classification; commands, not physical-unit counts"
              rows={rows('order_counts').map(r => ({'Requested order':r.requested_order,Commands:r.commands}))}/>
          </DataComponent>
          <DataComponent id="sample1-phase-table" queryId="phases" title="Coverage gaps continue throughout the replay"
            sourceRows={rows('phases')} displayRows={rows('phases')}>
            <DataTable searchable={false} caption="Frame windows; variable duration, no conversion to seconds"
              rows={rows('phases').map(r => ({Frames:r.frame_range,Commands:r.events,'Meaningful request':r.meaningful_request,
                Partial:r.partial,'Opaque to narrative':r.opaque_to_narrative}))}/>
          </DataComponent>
        </>}
      </React.Fragment>;
    })}
    <DataComponent id="sample1-selected-ledger" queryId="anchors" title="Inspect the selected report evidence"
      description="45 selected examples:39 meaningful requests,4 partial,2 opaque. Selection favors readable moments; full-file coverage uses all4162 events."
      sourceRows={anchorRows} displayRows={anchorRows}>
      <DataTable caption="Selected zero-based command-order anchors; complete4162-event audit supplied separately"
        rows={anchorRows.map(r => ({Event:r.command_order,Frame:r.frame,Slot:`S${r.slot}`,
          Request:r.requested_action || r.class,'Configured types':r.actors.join('; ') || 'Not recovered',
          'Marker text':r.marker_text || '',Tier:tierLabels[r.tier]}))}/>
    </DataComponent>
  </article>;
}
