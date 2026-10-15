"""Normalize a lawfully obtained Reddit Listing JSON. No network calls or scraping."""
import argparse,json,re

def convert(data):
    children=data.get('data',{}).get('children') if isinstance(data,dict) else None
    if not isinstance(children,list):raise ValueError('Reddit Listing data.children required')
    rows=[]
    for child in children:
        post=child.get('data',{})
        permalink=post.get('permalink','')
        if child.get('kind')!='t3':continue
        if not re.fullmatch(r'/r/[A-Za-z0-9_]+/comments/[a-z0-9]+/[^\s?#]*/?',permalink):raise ValueError('unsupported post permalink')
        body=post.get('selftext','')
        if body in {'[removed]','[deleted]'}:continue
        if not isinstance(post.get('title'),str) or not isinstance(body,str):raise ValueError('post text invalid')
        rows.append({'title':post['title'],'evidence_url':'https://www.reddit.com'+permalink,
                     'evidence_quote':body[:1500],'quote_truncated':len(body)>1500,'kind':'unknown','budget':None,
                     'content_verified':False,'import_origin':'USER_SUPPLIED_REDDIT_LISTING'})
    return {'leads':rows}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    try:r=convert(json.load(open(a.input,encoding='utf-8-sig')))
    except (OSError,ValueError,TypeError) as e:p.exit(2,'Input error: '+str(e)+'\n')
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
