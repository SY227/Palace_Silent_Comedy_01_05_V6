#!/usr/bin/env python3
"""Build a local Grok JSON request. Does not contact an API or spend credits."""
from pathlib import Path
import argparse,base64,json

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--episode',required=True,choices=['EP01','EP02','EP03','EP04','EP05'])
 p.add_argument('--language',choices=['EN','TC'],default='EN')
 p.add_argument('--mode',choices=['references','anchors'],default='anchors')
 p.add_argument('--out',required=True,help='Output JSON file; can be large because PNGs are embedded')
 a=p.parse_args();root=Path(__file__).resolve().parents[1]
 series=json.loads((root/'series.json').read_text(encoding='utf-8'))
 ep=next((e for e in series['episodes'] if e['id']==a.episode),None)
 if ep is None:p.error('That episode is not included in this extracted kit.')
 frame_dir=root/ep['folder']/'01_Reference_Images'
 def asset(i):
  data=(frame_dir/f"{ep['prefix']}_F{i:02d}.png").read_bytes()
  return {'url':'data:image/png;base64,'+base64.b64encode(data).decode('ascii')}
 body={'model':'grok-imagine-video-1.5','duration':15,'resolution':'720p','aspect_ratio':'9:16'}
 story=ep['prompt_en' if a.language=='EN' else 'prompt_tc']
 if a.mode=='references':
  body['reference_images']=[asset(i) for i in range(1,9)]
  mapping='Input mapping: '+', '.join(f'Image{i:02d}/F{i:02d} = <IMAGE_{i-1}>' for i in range(1,9))+'. These are chronological story-state references, not eight timed pins. Preserve F01 as the intended opening state.'
 else:
  body['image']=asset(1);body['last_frame']=asset(8)
  body['keyframes']=[{'image':asset(i),'timestamp_s':t} for i,t in [(3,3.0),(4,5.0),(5,7.0),(7,11.5)]]
  body['reference_images']=[asset(2),asset(6)]
  mapping='All eight story assets are supplied in separate roles. F01 is the first-frame pin (<IMAGE_0>); F08 is the last-frame pin. F03,F04,F05,F07 are the timed keyframe images at3,5,7,11.5 seconds. Supplementary reference <IMAGE_1> is F02 (failed attempt), and <IMAGE_2> is F06 (confirmed result). Interpret Image01-Image08 in the following story as these named story states, not as the reference_images array indexes. Synthesize continuous plausible action between the pins.'
 body['prompt']=mapping+'\n\n'+story
 out=Path(a.out).expanduser().resolve();out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(body,ensure_ascii=False),encoding='utf-8')
 print(json.dumps({'output':str(out),'episode':a.episode,'mode':a.mode,'duration':15,'assets':8,'network_requests':0}))
if __name__=='__main__':main()
