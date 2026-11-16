import React from 'react';
import {Composition} from 'remotion';
import {StoryMotionProof} from './StoryMotionProof';
export const Root: React.FC = () => <Composition id="StoryMotionProof" component={StoryMotionProof} width={1920} height={1080} fps={30} durationInFrames={180}/>;
