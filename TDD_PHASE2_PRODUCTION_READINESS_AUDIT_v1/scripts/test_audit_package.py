#!/usr/bin/env python3
"""Bookkeeping/integrity tests, NOT visual or semantic source inspection."""
import unittest,json,csv,re,hashlib,subprocess
from pathlib import Path
B=Path(__file__).resolve().parents[1];R=B.parent;V=B/'verification'
def load(p):return json.loads(p.read_text())
class AuditPackageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=load(V/'AUDIT_COVERAGE_STATUS.json');cls.data=load(B/'inventory/CATALOGUE_DATA.json');cls.n=load(V/'remote_nodes.json');cls.arc=load(V/'ARCHIVE_MEMBERS.json');cls.ledger=load(V/'CONTENT_INSPECTION_LEDGER.json');cls.ph=load(V/'PHASE1_STATUS_CROSSWALK.json');cls.am=load(V/'CONTENT_INSPECTION_AMENDMENTS.json')
 def test_explicit_incompletion(self):
  self.assertFalse(self.c['all_actual_files_inspected']);self.assertFalse(self.c['final_distinct_logical_asset_denominator_established']);self.assertFalse(self.c['all_corpus_native_asset_absence_asserted']);self.assertGreater(self.c['all_catalogue_uninspected_record_count_not_distinct_assets'],0)
 def test_complete_known_folder_listing(self):
  self.assertEqual([],self.c['known_folders_without_complete_final_page']);self.assertTrue(self.c['all_known_folders_enumerated']);self.assertEqual(144,self.c['saved_normalized_listing_pages'])
 def test_physical_identity_enumeration(self):
  expected={i for i,n in self.n.items() if not n.get('is_folder')};actual={x['source_id'] for x in self.data['physical']};self.assertEqual(expected,actual);self.assertEqual(len(actual),self.c['physical_files']);self.assertEqual(len(actual),len(self.data['physical']))
 def test_archive_member_identity(self):
  expected={(x['archive_id'],x['member_path']) for x in self.arc};actual={(x['archive_id'],x['member_path']) for x in self.data['archives']};self.assertEqual(expected,actual);self.assertEqual(len(actual),len(self.arc));self.assertTrue(all(x['crc_pass'] for x in self.arc))
 def test_inspection_hash_joins(self):
  for r in self.data['physical']:
   for index in r['inspection_ledger_rows_1based']:
    ob=self.ledger[index-1];self.assertEqual(ob['sha256'],r['verified_representation_sha256']);self.assertEqual('visual' if r['mime_at_listing'].startswith('image/') else 'semantic',ob['inspection_kind'])
  self.assertEqual(len(self.ledger),self.c['inspection_ledger_observations']);self.assertEqual(sum(r['inspection_kind']=='visual' for r in self.ledger),self.c['visual_observations'])
 def test_no_duplicate_inspection_key(self):
  keys=[(x['source_id'],x['inspection_kind'],x['inspection_scope']) for x in self.ledger];self.assertEqual(len(keys),len(set(keys)))
 def test_no_approval_inheritance(self):
  self.assertTrue(all(x['approval_inherited_from_matching_bytes'] is False for x in self.data['physical']));self.assertTrue(all(x['shared_content_inspection_only_never_shared_approval'] for x in self.data['duplicates']))
 def test_exact_phase1_scope_and_source_statuses(self):
  self.assertEqual(193,len(self.ph));self.assertEqual(193,len({x['source_id'] for x in self.ph}));ph={x['source_id']:x for x in self.ph}
  for x in self.data['physical']:
   if x['source_id'] in ph:self.assertEqual(ph[x['source_id']]['final_verdict'],x['exact_source_phase1_disposition'])
  self.assertEqual('REPLACED / SUPERSEDED',ph['1IhgfuIFZ5wOj4Wb0KpTrYQcyj57nT9Pz']['final_verdict']);self.assertEqual('APPROVED WITH DEFINED CONDITIONS',ph['1npYn0kJB2FFjTxPyGdACAsCqKk8ZbDPq']['final_verdict'])
 def test_controlling_recording_error_amendments(self):
  observed={x['source_id_actually_read']:x for x in self.data['observations']};k=observed['1b2vTn10kpAsmmMaN53yzQ8G4pJZc1wR0'];self.assertIn('COMPLETED AND VISUALLY ACCEPTED',k['limitations_and_unknowns']);self.assertNotIn('FAILED',k['limitations_and_unknowns'])
  states=load(V/'STATE_SOURCE_AUTHORITY_RECONCILIATION.json')
  for x in states:
   ob=observed[x['predecessor']['source_id']];self.assertTrue(ob['limitations_and_unknowns'].startswith('REPLACED / SUPERSEDED'));self.assertIn(x['later_distinct_source']['source_id'],ob['limitations_and_unknowns'])
 def test_every_gap_has_required_fields_and_real_sources(self):
  g=load(B/'production_gap_register.json');known=set(self.n)|{x['archive_id']+'::'+x['member_path'] for x in self.arc};keys=['gap_id','asset_scene','affected_sources','current_material','deficiency','production_impact','priority','required_solution','production_instructions','acceptance_criteria','dependency','owner_expertise'];seen=set()
  for r in g['gaps']:
   self.assertNotIn(r['gap_id'],seen);seen.add(r['gap_id'])
   for key in keys:self.assertTrue(r.get(key),(r['gap_id'],key))
   self.assertIn(r['priority'],['critical blocker','high','medium','low'])
   for src in r['affected_sources']:self.assertTrue(src in known or (B/src).is_file(),(r['gap_id'],src))
 def test_briefs_and_decisions_join_gaps(self):
  gaps={x['gap_id'] for x in load(B/'production_gap_register.json')['gaps']}
  for r in load(B/'artist_ready_briefs.json')['briefs']:
   for key in ['specialist','inputs','start_condition','instructions','deliverables','acceptance_tests','do_not','dependencies']:self.assertTrue(r.get(key),(r['brief_id'],key))
   self.assertLessEqual(set(r['related_gaps']),gaps)
  for r in load(B/'cd_decision_register.json')['decisions']:self.assertLessEqual(set(r['related_gaps']),gaps)
 def test_native_recovery_not_old_hash_restoration(self):
  old=load(V/'NATIVE_EXPORT_SNAPSHOTS.json')[0];new=load(V/'NATIVE_EXPORT_ADDITIONAL_SNAPSHOTS.json')[0];self.assertNotEqual(old['sha256'],new['sha256']);self.assertEqual(old['export_returned_bytes'],new['export_returned_bytes']);comp=load(V/'NATIVE_RECOVERY_COMPARISON.json');self.assertTrue(comp['same_word_document_xml']);self.assertEqual(['word/styles.xml'],comp['different_parts'])
 def test_history_readpack_only_actual_prefix_counted(self):
  manifest=load(V/'HISTORY_LOSSLESS_READPACK_MANIFEST.json');reads=load(V/'HISTORY_READPACK_READS.json');covered=set()
  for x in reads:
   self.assertEqual(manifest['pack_sha256'],x['pack_sha256']);covered.update(range(x['start'],x['end']+1))
  self.assertTrue(set(range(1,1046))<=covered);self.assertNotIn(manifest['pack_lines'],covered)
  for x in self.ledger:
   rr=x.get('read_ranges') or {}
   if isinstance(rr,dict) and rr.get('readpack_sha256')==manifest['pack_sha256']:
    lo,hi=rr['document_pack_range_inclusive'];self.assertTrue(set(range(lo,hi+1))<=covered)
 def test_rendered_report_contains_a_to_j_and_qualification(self):
  s=(B/'TDD_PHASE2_A_TO_J_WORKING_AUDIT.md').read_text()
  self.assertNotRegex(s,r'\{\{[A-Z_]+\}\}')
  for letter in 'ABCDEFGHIJ':self.assertRegex(s,r'(?m)^# '+letter+r'\. ')
  self.assertIn('Phase 2 is not complete',s);self.assertIn('does not complete the user',s);self.assertIn('no downloaded',s.lower())
  h=(B/'TDD_PHASE2_A_TO_J_WORKING_AUDIT.html').read_text();self.assertNotIn('<script',h.lower());self.assertIn('Coverage qualified',h)
 def test_completed_batch20_exact_content_coverage(self):
  cp=load(V/'BATCH_20_CHECKPOINT.json');self.assertFalse(cp['all_phase2_complete']);self.assertEqual(79,cp['new_distinct_payloads_inspected']);self.assertEqual(62,cp['new_visual_observations']);self.assertEqual(17,cp['new_semantic_observations'])
  visual={x['sha256'] for x in self.ledger if x['inspection_kind']=='visual'};semantic={x['sha256'] for x in self.ledger if x['inspection_kind']=='semantic'}
  for x in self.arc:
   if x['archive_id'] in cp['selected_archives']:self.assertIn(x['sha256'],visual if x.get('width') else semantic)
  self.assertEqual(394,cp['ending_uninspected_archive_raster_hashes'])
 def test_batch20_delta_complete_read_not_preparation(self):
  m=load(V/'BATCH_20_DOCUMENT_DELTA_MANIFEST.json');r=load(V/'BATCH_20_DOCUMENT_DELTA_READS.json');self.assertEqual(m['pack_sha256'],r['pack_sha256']);self.assertEqual([[1,645]],r['actual_read_ranges_inclusive']);self.assertTrue(r['all_source_documents_complete']);self.assertEqual(8,len(m['documents']))
  for d in m['documents']:self.assertTrue(d['independent_roundtrip_equal'])
 def test_historical_measured_dimensions_not_erased(self):
  dims={x['sha256']:(x['width'],x['height']) for x in load(V/'DOWNLOAD_HASH_CHECKS.json')+self.arc if x.get('width') and x.get('height')}
  for x in self.data['physical']:
   h=x.get('verified_representation_sha256')
   if h in dims:self.assertEqual(dims[h],(x.get('width_px'),x.get('height_px')))
 def test_catalogue_counts_not_asset_denominator(self):
  self.assertEqual(self.c['all_catalogue_records'],sum(len(self.data[k]) for k in ['physical','archives','local']));self.assertEqual(self.c['all_catalogue_uninspected_record_count_not_distinct_assets'],sum(x['content_inspection_state']!='ACTUALLY_INSPECTED_EXACT_PAYLOAD' for k in ['physical','archives','local'] for x in self.data[k]))
 def test_phase1_read_only_seal_recheck(self):
  x=load(V/'PHASE1_READ_ONLY_SEAL_RECHECK.json');self.assertEqual([],x['errors']);self.assertEqual(504,x['good'])
 def test_protected_tracked_sources_unchanged(self):
  p=subprocess.run(['git','diff','--exit-code','--'],cwd=R,capture_output=True,text=True);self.assertEqual(0,p.returncode,p.stdout+p.stderr)
if __name__=='__main__':unittest.main(verbosity=2)
