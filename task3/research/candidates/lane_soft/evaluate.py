import importlib.util, json, os, sys, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'input/competition'
os.environ['POTATO_DATA_DIR']=str(DATA)

def loadmod(path):
 spec=importlib.util.spec_from_file_location('cand',path)
 m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def play(mod, judge_emb, secrets, public_emb=None, maxturns=30, noise=None, return_traces=False):
 words=json.loads((DATA/'vocabulary.json').read_text()); wi={w.casefold():i for i,w in enumerate(words)}
 if public_emb is None: public_emb=judge_emb
 p=mod.PotatoPlayer(words,public_emb)
 vals=[]; turns=[]; traces=[]
 for secret in secrets:
  p.new_game(); si=wi[secret.casefold()]; sv=judge_emb[si]; w1='lamp'; w2='potato'; tr=[]
  for t in range(1,maxturns+1):
   i1=wi[w1.casefold()]; i2=wi[w2.casefold()]
   d=float(sv@judge_emb[i1]-sv@judge_emb[i2])
   if noise is not None and noise>0:
    # logistic flip probability based on margin / noise
    prob=1/(1+np.exp(-d/noise))
    # deterministic RNG supplied externally? noise can tuple (scale,rng)
    rng=noise[1] if isinstance(noise,tuple) else np.random
    out=rng.random()<prob
   else: out=d>1e-12
   if abs(d)<=1e-12 and noise is None: verdict='same'; winner=w1
   elif out: verdict='first'; winner=w1
   else: verdict='second'; winner=w2
   prop=p.respond({'turn':t,'winner_word':winner,'verdict':verdict,'word1':w1,'word2':w2})
   tr.append((t,w1,w2,verdict,prop,d))
   if prop.casefold()==secret.casefold():
    score=1-.02*max(0,t-10); vals.append(score); turns.append(t); traces.append(tr); break
   w1,w2=winner,prop
  else: vals.append(0.); turns.append(None); traces.append(tr)
 return (100*np.mean(vals),vals,turns,traces) if return_traces else 100*np.mean(vals)

if __name__=='__main__':
 mod=loadmod(ROOT/'candidates/deployable_baseline/starter.py')
 words=json.loads((DATA/'vocabulary.json').read_text()); E=np.load(DATA/'public_embeddings.npy').astype('float32'); E/=np.linalg.norm(E,axis=1,keepdims=True)
 secrets=json.loads((DATA/'test_public.json').read_text())
 score,vals,turns,tr=play(mod,E,secrets,E,return_traces=True)
 from collections import Counter
 print('score',score,'solved',sum(v>0 for v in vals),'hist',Counter(turns),'unsolved',[s for s,t in zip(secrets,turns) if t is None])
 print('mean solved turn',np.mean([t for t in turns if t]))
