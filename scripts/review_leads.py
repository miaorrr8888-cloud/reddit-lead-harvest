"""Review user-supplied leads offline. Never searches, contacts or verifies demand."""
import argparse
import json
from urllib.parse import urlsplit,urlunsplit

MODE='reddit'

def review(data):
    if not isinstance(data,dict) or not isinstance(data.get('leads'),list): raise ValueError('Expected an object with a leads array')
    rows=[]; seen=set()
    for index,lead in enumerate(data['leads'],1):
        if not isinstance(lead,dict): raise ValueError('Each lead must be an object')
        reasons=[]; excluded=False; canonical=None
        url=lead.get('evidence_url')
        try:
            p=urlsplit(url)
            if p.scheme!='https' or not p.hostname or p.username or p.password: raise ValueError()
            canonical=urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),p.query,''))
            if MODE=='reddit' and (p.hostname not in {'reddit.com','www.reddit.com','old.reddit.com'} or '/comments/' not in p.path):
                reasons.append('NOT_A_SUPPORTED_REDDIT_POST_URL')
        except (ValueError,TypeError,AttributeError): reasons.append('MISSING_OR_INVALID_EVIDENCE_URL')
        if not isinstance(lead.get('title'),str) or not lead['title'].strip(): reasons.append('MISSING_TITLE')
        if not isinstance(lead.get('evidence_quote'),str) or not lead['evidence_quote'].strip(): reasons.append('MISSING_QUOTED_EVIDENCE')
        kind=lead.get('kind','unknown')
        if kind in {'self_promotion','discussion','recruitment'}:
            excluded=True; reasons.append('NOT_A_PURCHASING_REQUEST')
        elif kind not in {'buyer_request','project_request'}: reasons.append('BUYER_INTENT_UNKNOWN')
        if MODE=='marketplace' and lead.get('accepting_bids') is not True: reasons.append('BIDDING_STATUS_NOT_CONFIRMED_BY_INPUT')
        if lead.get('requires_upfront_payment') is True:
            excluded=True; reasons.append('UPFRONT_PAYMENT_REQUEST')
        duplicate=canonical in seen if canonical else False
        if canonical: seen.add(canonical)
        status='DUPLICATE' if duplicate else ('EXCLUDED' if excluded else ('NEEDS_INFORMATION' if reasons else 'NEEDS_HUMAN_VERIFICATION'))
        rows.append({'row':index,'title':lead.get('title'),'evidence_url':canonical or url,
                     'evidence_quote':lead.get('evidence_quote'),'kind':kind,'budget':lead.get('budget'),
                     'status':status,'reasons':reasons,'content_verified':False,'contacted':False})
    return {'mode':MODE,'notice':'Offline review of supplied claims only. No live validation, contact, purchase or transaction occurred.',
            'rows':rows,'summary':{status:sum(r['status']==status for r in rows) for status in sorted({r['status'] for r in rows})}}

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('input'); args=parser.parse_args()
    try:
        with open(args.input,encoding='utf-8-sig') as f: report=review(json.load(f))
    except (OSError,ValueError,TypeError) as exc: parser.exit(2,'Input error: '+str(exc)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))

if __name__=='__main__': main()
