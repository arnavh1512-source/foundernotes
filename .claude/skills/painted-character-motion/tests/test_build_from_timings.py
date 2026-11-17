import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_from_timings import DEFAULT_SCENES,collect,build

class TimingsTests(unittest.TestCase):
    def test_timeline_preserves_lead_pause_tail(self):
        src={'duration':8.5,'segments':[
          {'start':0.3,'end':2.7,'scene_id':'hook','text':'First'},
          {'start':3.6,'end':7.3,'scene_id':'study','text':'Second'}]}
        shots,total=collect(src,DEFAULT_SCENES)
        self.assertEqual(total,8.5)
        self.assertAlmostEqual(sum(x['duration'] for x in shots),8.5)
        self.assertEqual([s['id'] for s in shots],['gate','study'])
        self.assertEqual([s['duration'] for s in shots],[3.6,4.9])
    def test_overlap_fails(self):
        with self.assertRaises(ValueError):
            collect({'duration':5,'segments':[{'start':0.3,'end':3,'scene_id':'hook'},
                     {'start':2.6,'end':4,'scene_id':'study'}]},DEFAULT_SCENES)
    def test_unsupported_scene_fails(self):
        with self.assertRaises(ValueError):
            collect({'duration':3,'segments':[{'start':0,'end':1,'scene_id':'venus'}]},DEFAULT_SCENES)
    def test_build_writes_single_page_and_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            input=root/'timings.json'
            input.write_text(json.dumps({'duration':6,'segments':[
                {'start':.2,'end':2,'scene_id':'hook','speaker':'youth','text':'Hi'},
                {'start':2.5,'end':5,'scene_id':'close','speaker':'philosopher','text':'There'}]}))
            shots,duration=build(input,root/'visual',DEFAULT_SCENES)
            self.assertEqual(len(shots),2)
            self.assertIn('window.MOTION',(root/'visual/index.html').read_text())
            self.assertEqual(json.loads((root/'visual/shot-timeline.json').read_text())['format'],'16:9')



class BuilderSafetyTests(unittest.TestCase):
    def test_malformed_segment_is_rejected_before_lookahead(self):
        with self.assertRaises(ValueError):
            collect({'duration':3,'segments':[{'start':0,'end':1,'scene_id':'hook'},None]},DEFAULT_SCENES)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary); source=root/'timings.json'; output=root/'visual';output.mkdir()
            source.write_text(json.dumps({'duration':2,'segments':[{'start':0,'end':1,'scene_id':'study'}]}))
            (output/'index.html').write_text('previous approved cut')
            with self.assertRaises(ValueError): build(source,output,DEFAULT_SCENES)
            self.assertEqual((output/'index.html').read_text(),'previous approved cut')

if __name__=='__main__':unittest.main()
