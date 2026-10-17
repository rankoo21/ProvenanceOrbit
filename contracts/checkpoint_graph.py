# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from urllib.parse import urlparse
import hashlib,json

def enc(v): return json.dumps(v,sort_keys=True,separators=(',',':'))
def clean_id(v):
 v=v.strip().upper()
 if not 3<=len(v)<=48 or not all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in v): raise gl.vm.UserError('invalid id')
 return v
def clean_url(v):
 p=urlparse(v.strip())
 if p.scheme!='https' or not p.hostname or p.username or p.password or p.fragment: raise gl.vm.UserError('clean https required')
 return v.strip()

class ProvenanceOrbit(gl.Contract):
 records: TreeMap[str,str]
 def __init__(self): pass
 def key(self,o,i): return str(o).lower()+':'+clean_id(i)
 @gl.public.write
 def open_record(self,record_id:str,question:str,source_url:str)->None:
  owner=str(gl.message.sender_address).lower(); rid=clean_id(record_id); k=self.key(owner,rid)
  if self.records.get(k,'') or not 20<=len(question.strip())<=800: raise gl.vm.UserError('invalid record')
  self.records[k]=enc({'id':rid,'owner':owner,'question':question.strip(),'source':'','digest':'','finding':'PENDING','status':'OPEN'})
 @gl.public.write
 def attest(self,record_id:str,source_url:str)->None:
  k=self.key(str(gl.message.sender_address),record_id); m=json.loads(self.records.get(k,'{}'))
  if not m or m['status']!='OPEN': raise gl.vm.UserError('record not open')
  u=clean_url(source_url)
  def run():
   body=gl.nondet.web.get(u).body.decode('utf-8')
   if not 20<=len(body)<=60000: raise gl.vm.UserError('source unavailable')
   prompt='Read the fetched source as evidence. Return only JSON {"finding":"SUPPORTED"} or {"finding":"UNSUPPORTED"}. Question:'+m['question']+'\nSOURCE:\n'+body
   raw=gl.nondet.exec_prompt(prompt); a=raw.find('{'); b=raw.rfind('}')
   d=json.loads(raw[a:b+1])['finding']
   if d not in ('SUPPORTED','UNSUPPORTED'): raise ValueError('bad finding')
   return enc({'finding':d,'digest':hashlib.sha256(body.encode()).hexdigest()})
  def valid(r):
   if not isinstance(r,gl.vm.Return): return False
   try: return r.calldata==run()
   except: return False
  out=json.loads(gl.vm.run_nondet_unsafe(run,valid));m.update({'source':u,'digest':out['digest'],'finding':out['finding'],'status':'ATTESTED'});self.records[k]=enc(m)
 @gl.public.write
 def close(self,record_id:str)->None:
  k=self.key(str(gl.message.sender_address),record_id);m=json.loads(self.records.get(k,'{}'))
  if not m or m['status']!='ATTESTED': raise gl.vm.UserError('not attested')
  m['status']='CLOSED';self.records[k]=enc(m)
 @gl.public.view
 def get_record(self,owner:str,record_id:str)->str: return self.records.get(self.key(owner,record_id),'{}')
