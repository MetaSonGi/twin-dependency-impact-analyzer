"""장비·센서·서비스 의존 그래프에서 장애의 downstream 영향 범위, 순환 참조, 핵심 단절 지점을 계산합니다."""
import argparse,html,json,math
from pathlib import Path
def finite(v,n,minimum=None):
 if type(v) not in (int,float) or not math.isfinite(v):raise ValueError(n+": finite number required")
 if minimum is not None and v<minimum:raise ValueError(n+": below minimum")
 return v
def report(x,t):
 p=html.escape(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
 return '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(t)+'</title><style>body{font:16px/1.6 system-ui;max-width:1000px;margin:30px auto;padding:20px;background:#101b2b;color:#eef7ff}pre{background:#192b40;padding:22px;border-radius:12px;white-space:pre-wrap}h1{color:#79e3c2}</style><h1>'+html.escape(t)+'</h1><p>오프라인 합성 예제 · 실물 장비 연결 없음</p><pre>'+p+'</pre>'
def cli(fn,title):
 p=argparse.ArgumentParser();p.add_argument("--input",default=str(Path(__file__).with_name("sample-input.json")));p.add_argument("--html");a=p.parse_args()
 try:
  x=fn(json.loads(Path(a.input).read_text(encoding="utf-8")))
  if a.html:Path(a.html).write_text(report(x,title),encoding="utf-8")
  print(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False))
 except (ValueError,KeyError,TypeError) as e:p.exit(2,"input error: "+str(e)+"\n")

def path(edges,start,target):
 q=[start];seen={start}
 while q:
  n=q.pop(0)
  for m in edges[n]:
   if m==target:return True
   if m not in seen:seen.add(m);q.append(m)
 return False
def run(d):
 nodes={n["id"]:n for n in d["nodes"]}
 if len(nodes)!=len(d["nodes"]):raise ValueError("duplicate node ID")
 edges={n:[] for n in nodes};issues=[]
 for e in d["edges"]:
  a,b=e["from"],e["to"]
  if a not in nodes or b not in nodes:issues.append({"edge":e,"reason":"dangling_edge"});continue
  edges[a].append(b)
 color={n:0 for n in nodes};cycles=[]
 def dfs(n,p):
  color[n]=1
  for m in edges[n]:
   if color[m]==0:dfs(m,p+[m])
   elif color[m]==1:cycles.append(p[p.index(m):]+[m] if m in p else p+[m])
  color[n]=2
 for n in nodes:
  if color[n]==0:dfs(n,[n])
 impacts=[]
 for f in d["failures"]:
  if f not in nodes:issues.append({"node":f,"reason":"unknown_failure"});continue
  q=[f];dist={f:0}
  while q:
   n=q.pop(0)
   for m in edges[n]:
    if m not in dist:dist[m]=dist[n]+1;q.append(m)
  impacts.append({"failure":f,"affected":[{"id":n,"distance":v,"kind":nodes[n]["kind"]} for n,v in sorted(dist.items(),key=lambda x:(x[1],x[0]))]})
 critical=sorted(({"id":n,"downstream_count":sum(path(edges,n,m) for m in nodes if m!=n)} for n in nodes),key=lambda x:(-x["downstream_count"],x["id"]))
 return {"impacts":impacts,"critical_nodes":critical,"cycles":cycles,"issues":issues,"direction":"provider_to_consumer"}

if __name__=="__main__":cli(run,'트윈 의존성 영향 분석기')
