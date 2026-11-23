# Estimate qc_video's fast-motion ratio without rendering: bash estall.sh /abs/path/film/stick.html [duration]
F=$1; DUR=${2:-$(python3 -c "import re;print(re.search(r'DUR=([\\d.]+)',open('$(dirname $1)/timing.js').read()).group(1))")}; S=$(mktemp -d); cp "$(dirname "$0")/est.mjs" $S/; cd $S; rm -f est*.txt; for i in 0 1 2 3 4 5; do A=$(python3 -c "print($i*$DUR/6)"); B=$(python3 -c "print(($i+1)*$DUR/6)"); node est.mjs $F $A $B > est$i.txt 2>&1 & done; wait; python3 -c "
import json,glob;n=f=0
for x in sorted(glob.glob('est*.txt')):
  a,b=json.loads(open(x).read().strip().splitlines()[-1]);n+=a;f+=b;print(x,b/a)
print('RATIO',f/n)"
