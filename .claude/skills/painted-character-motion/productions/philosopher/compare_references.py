"""Measure equal moving-image windows; these are diagnostics, never creative scores."""
import argparse, json, subprocess
from pathlib import Path
import numpy as np

def measure(path,seconds=60,start=0):
    cmd=['ffmpeg','-v','error','-ss',str(start),'-i',str(path),'-t',str(seconds),'-vf','fps=10,scale=160:90','-pix_fmt','rgb24','-f','rawvideo','-']
    deltas=[];previous=None;count=0
    with subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE) as proc:
        try:
            while True:
                raw=proc.stdout.read(160*90*3)
                if not raw:break
                if len(raw)!=160*90*3:raise RuntimeError('Incomplete decoded frame')
                frame=np.frombuffer(raw,dtype=np.uint8).astype(np.int16)
                if previous is not None:deltas.append(float(np.abs(frame-previous).mean()/255))
                previous=frame;count+=1
            error=proc.stderr.read().decode(errors='replace')
            if proc.wait():raise RuntimeError(error)
        except BaseException:
            proc.kill();raise
    if count<round(seconds*10)-1 or not deltas:raise ValueError('Not enough decoded frames for the requested window')
    a=np.asarray(deltas)
    return {'path':str(path),'start_seconds':start,'duration_seconds':seconds,'sampled_frames':count,
            'fast_fraction':float((a>.025).mean()),'median_pixel_delta':float(np.median(a)),
            'large_image_change_times':[round(start+(i+1)/10,1) for i in np.where(a>.12)[0]]}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot',type=Path,required=True)
    parser.add_argument('--reference',type=Path,action='append',required=True)
    parser.add_argument('--baseline',type=Path)
    parser.add_argument('--seconds',type=float,default=60)
    parser.add_argument('--start',type=float,default=0)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.seconds<=0 or args.start<0:parser.error('Use a positive duration and nonnegative start')
    paths=[args.pilot]+([args.baseline] if args.baseline else [])+args.reference
    if not all(p.is_file() for p in paths):parser.error('Every input must be a real local video file')
    result={'scope':'Equal windows, 10 fps, 160x90 RGB, mean absolute pixel delta /255',
            'limits':['Includes cuts and camera motion; does not measure character acting or audience response',
                      'Large image changes are not a complete shot count',
                      'A motion threshold cannot establish creative quality or reference parity'],
            'clips':[measure(p,args.seconds,args.start) for p in paths]}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

