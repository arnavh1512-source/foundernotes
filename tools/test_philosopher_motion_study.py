import unittest
from PIL import Image, ImageDraw
from philosopher_motion_study import frame, map_sheet, arm_joint
import math

class MotionStudyTests(unittest.TestCase):
    def test_all_shots_and_scaled_limb_widths_render_deterministically(self):
        for cut in (1,2,3):
            for t in (0,2.5,4.8,7.6,9.6,12.0,14.4,17.0,19.2,23.9):
                with self.subTest(cut=cut,t=t):
                    a=frame(t,cut)
                    self.assertEqual(a.size,(960,540))
                    self.assertEqual(a.tobytes(),frame(t,cut).tobytes())
                    if t in (0,12.0,17.0):
                        self.assertNotEqual(a.tobytes(),frame(t+.025,cut).tobytes())

    def test_route_draw_does_not_reveal_later_segment_early(self):
        im=Image.new('RGB',(800,500))
        map_sheet(ImageDraw.Draw(im),(180,55,600,370),.3,continuous=True)
        self.assertNotEqual(im.getpixel((550,113)),(71,120,118))
        map_sheet(ImageDraw.Draw(im),(180,55,600,370),1,continuous=True)
        self.assertEqual(im.getpixel((550,113)),(71,120,118))

    def test_pointing_arm_preserves_bone_lengths_for_entire_reach(self):
        for i in range(101):
            q=i/100
            hand=(613-50*q,343+26*q)
            elbow=arm_joint((683,296),hand)
            self.assertAlmostEqual(math.dist((683,296),elbow),70)
            self.assertAlmostEqual(math.dist(elbow,hand),75)
        with self.assertRaises(ValueError):
            arm_joint((0,0),(1000,0))

if __name__=='__main__': unittest.main()
