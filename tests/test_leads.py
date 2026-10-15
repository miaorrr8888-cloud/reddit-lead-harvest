from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review_leads',ROOT/'scripts/review_leads.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class LeadReview(unittest.TestCase):
    def good(self):
        return {'title':'Synthetic example, not a real buyer','evidence_url':'https://www.reddit.com/r/example/comments/demo123/example/',
                'evidence_quote':'Synthetic request for a service.','kind':'buyer_request','accepting_bids':True}
    def test_supplied_data_is_never_marked_verified_or_contacted(self):
        row=module.review({'leads':[self.good()]})['rows'][0]
        self.assertEqual(row['status'],'NEEDS_HUMAN_VERIFICATION'); self.assertFalse(row['content_verified']); self.assertFalse(row['contacted'])
    def test_promotion_excluded(self):
        lead=self.good(); lead['kind']='self_promotion'
        self.assertEqual(module.review({'leads':[lead]})['rows'][0]['status'],'EXCLUDED')
    def test_missing_quote_requires_information(self):
        lead=self.good(); lead.pop('evidence_quote')
        self.assertEqual(module.review({'leads':[lead]})['rows'][0]['status'],'NEEDS_INFORMATION')
    def test_duplicate_preserved_as_duplicate(self):
        self.assertEqual(module.review({'leads':[self.good(),self.good()]})['rows'][1]['status'],'DUPLICATE')
    def test_invalid_data_rejected(self):
        with self.assertRaises(ValueError): module.review({'leads':'wrong'})
    def test_upfront_payment_excluded(self):
        lead=self.good(); lead['requires_upfront_payment']=True
        self.assertEqual(module.review({'leads':[lead]})['rows'][0]['status'],'EXCLUDED')

if __name__=='__main__': unittest.main()
