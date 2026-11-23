"""Per-line facial expressions: speaker expression, listener reaction. Writes film/expr.js (keyed by line start time)."""
import json,re
M={'n02b_m':('shouting','worried'),'n02d_m':('happy','worried'),'d01':('angry',None),'n06b_y':('angry','calm'),'d02':('smug','shocked'),
'd03':('shouting','calm'),'n07b_p':('calm','thinking'),'n08a_p':('calm','worried'),'d04':('angry','calm'),'n09b_p':('calm','thinking'),
'd05':('shouting','calm'),'n11b_y':('angry','calm'),'d06':('calm','thinking'),'n12b_p':('smug','shocked'),'n14b_p':('calm','thinking'),
'n15a_p':('calm','thinking'),'d07':('thinking','happy'),'d08':('happy','thinking'),'n16a_p':('calm','thinking'),'n18b_y':('smug','calm'),
'd09':('calm','smug'),'d10':('smug','calm'),'n19a_p':('calm','angry'),'n19c_p':('calm','thinking'),'n20b_p':('calm','worried'),
'n21b_p':('sad','sad'),'d11':('sad','calm'),'n22b_p':('calm','sad'),'n22c_y':('thinking','calm'),'n22d_p':('happy','thinking'),
'n23b_p':('calm','thinking'),'d12':('calm','thinking'),'d13':('angry','calm'),'n25b_p':('calm','angry'),'d14':('calm','shocked'),
'd15':('shocked','calm'),'n26b_p':('calm','thinking'),'n27a_p':('calm','worried'),'n27b_y':('angry','calm'),'n27c_p':('smug','angry'),
'd16':('calm','angry'),'n29a_p':('calm','thinking'),'n30b_p':('calm','thinking'),'n31b_p':('calm','thinking'),'d17':('shouting','calm'),
'n32a_p':('calm','shocked'),'n33b_p':('calm','thinking'),'n34a_p':('calm','worried'),'n34c_p':('calm','sad'),'n35b_p':('calm','worried'),
'n36a_p':('calm','thinking'),'n37a_p':('calm','worried'),'d18':('worried','calm'),'d19':('calm','thinking'),'n38a_p':('calm','thinking'),
'd20':('angry','calm'),'d21':('smug','worried'),'n39b_p':('calm','thinking'),'d22':('shouting','calm'),'n40a_p':('calm','worried'),
'n43b_y':('worried','happy'),'n43d_p':('happy','happy')}
t={s['id']:s['start'] for s in json.load(open('mix/timings.json'))['segments']}
X={f"{t[k]:.3f}":v for k,v in M.items() if k in t}
open('film/expr.js','w').write('window.LEXPR='+json.dumps(X)+';'); print(len(X),'lines mapped')
