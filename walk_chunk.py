#!/usr/bin/env python3
"""Chunked tree walk: one foreground call = up to N pages or S seconds, cursor persisted."""
import json, urllib.request, urllib.error, re, os, sys, time
DS="agibot-world/AgiBotWorld2026"
MIRROR="https://hf-mirror.com"
W="/home/z/my-project/.state/agibot-evidence-work"
state_p=os.path.join(W,"walk-state.json")
entries_p=os.path.join(W,"entries.jsonl")
MAXPAGES=int(sys.argv[1]) if len(sys.argv)>1 else 30
MAXSEC=float(sys.argv[2]) if len(sys.argv)>2 else 50
if os.path.exists(state_p):
    st=json.load(open(state_p))
else:
    st={"url":f"{MIRROR}/api/datasets/{DS}/tree/main?recursive=true&limit=1000","pages":0,"entries":0,"done":False}
out=open(entries_p,"a")
t0=time.time(); url=st["url"]; added=0
for _ in range(MAXPAGES):
    if time.time()-t0>MAXSEC: break
    for attempt in range(4):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"correctover-evidence/1.0"}),timeout=30)
            break
        except urllib.error.HTTPError as e:
            if e.code==429 and attempt<3:
                time.sleep(25*(attempt+1)); continue
            raise
    items=json.load(r); nxt=r.headers.get("Link")
    m=re.search(r'<([^>]+)>;\s*rel="next"',nxt) if nxt else None
    for it in items: out.write(json.dumps(it)+"\n")
    added+=len(items); st["pages"]+=1; st["entries"]+=len(items)
    url=m.group(1) if m else None
    if not url: st["done"]=True; break
out.close()
st["url"]=url or ""
json.dump(st,open(state_p,"w"))
print(f"pages_total={st['pages']} entries_total={st['entries']} done={st['done']} this_chunk={added}")
