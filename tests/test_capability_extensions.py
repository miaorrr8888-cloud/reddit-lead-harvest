from pathlib import Path
import importlib.util,unittest,tempfile,json,sys,subprocess,os
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('extension',ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class SnapshotEvidence(unittest.TestCase):
    def review(self,d,quote='Need cleanup',captured='2026-10-15T00:00:00Z'):
        from datetime import datetime,timezone
        p=Path(d);(p/'page.txt').write_text('Need cleanup service')
        return load('scripts/review_snapshot.py').review({'snapshot':'page.txt','quote':quote,'captured_at':captured,'source_url':'https://example.com/post'},p,datetime(2026,10,15,1,tzinfo=timezone.utc))
    def test_quote_present_is_not_buyer_verification(self):
        with tempfile.TemporaryDirectory() as d:
            r=self.review(d);self.assertEqual(r['status'],'READY_FOR_HUMAN_REVIEW');self.assertFalse(r['buyer_verified'])
    def test_absent_and_stale_hold(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.review(d,'Unknown quote')['status'],'HOLD');self.assertEqual(self.review(d,captured='2026-01-01T00:00:00Z')['status'],'HOLD')

class ExportImport(unittest.TestCase):
    def test_preserve_unknown_intent(self):
        data={'data':{'children':[{'kind':'t3','data':{'title':'Demo','selftext':'Need help','permalink':'/r/demo/comments/abc123/demo/'}}]}}
        row=load('scripts/import_reddit_export.py').convert(data)['leads'][0];self.assertEqual(row['kind'],'unknown');self.assertFalse(row['content_verified'])
    def test_bad_export_rejected(self):
        with self.assertRaises(ValueError):load('scripts/import_reddit_export.py').convert({'data':{}})
