import Live 

app = Live.Application.get_application()
IS_LIVE_10 = app.get_major_version() == 10
IS_LIVE_9 = app.get_major_version() >= 9
IS_LIVE_9_1 = IS_LIVE_10 or (IS_LIVE_9 and app.get_minor_version() >= 1)
IS_LIVE_9_5 = IS_LIVE_10 or (IS_LIVE_9 and app.get_minor_version() >= 5)


KEYWORDS = {'ON' : 1, 'OFF' : 0} 

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVE_NAMES = ['-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7', '8']

GQ_STATES = {'NONE' : 0, '8 BARS' : 1, '4 BARS' : 2, '2 BARS' : 3, '1 BAR' : 4, '1/2' : 5, '1/2T' : 6, '1/4' : 7, '1/4T' : 8, '1/8' : 9, '1/8T' : 10, '1/16' : 11, '1/16T' : 12, '1/32' : 13}
RQ_STATES = {'NONE' : 0, '1/4' : 1, '1/8' : 2, '1/8T' : 3, '1/8 + 1/8T' : 4, '1/16' : 5, '1/16T' : 6, '1/16 + 1/16T' : 7, '1/32' : 8}

XFADE_STATES = {'A': 0, 'OFF' : 1, 'B' : 2}
MON_STATES = {'IN' : 0, 'AUTO' : 1, 'OFF' : 2}

LOOPER_STATES = {'STOP': 0.0, 'REC' : 1.0, 'PLAY' : 2.0, 'OVER' : 3.0}

if IS_LIVE_9:
    R_QNTZ_STATES = {'1/4' : Live.Song.RecordingQuantization.rec_q_quarter, '1/8' : Live.Song.RecordingQuantization.rec_q_eight, 
                   '1/8T' : Live.Song.RecordingQuantization.rec_q_eight_triplet, '1/8 + 1/8T' : Live.Song.RecordingQuantization.rec_q_eight_eight_triplet, '1/16' : Live.Song.RecordingQuantization.rec_q_sixtenth, 
                   '1/16T' : Live.Song.RecordingQuantization.rec_q_sixtenth_triplet, '1/16 + 1/16T' : Live.Song.RecordingQuantization.rec_q_sixtenth_sixtenth_triplet, 
                   '1/32' : Live.Song.RecordingQuantization.rec_q_thirtysecond}
    
    CLIP_GRID_STATES = {'OFF' : Live.Clip.GridQuantization.no_grid, '8 BARS' : Live.Clip.GridQuantization.g_8_bars, 
                        '4 BARS' : Live.Clip.GridQuantization.g_4_bars, '2 BARS' : Live.Clip.GridQuantization.g_2_bars,
                        '1 BAR' : Live.Clip.GridQuantization.g_bar, '1/2' : Live.Clip.GridQuantization.g_half,
                        '1/4' : Live.Clip.GridQuantization.g_quarter, '1/8' : Live.Clip.GridQuantization.g_eighth, 
                        '1/16' : Live.Clip.GridQuantization.g_sixteenth, '1/32' : Live.Clip.GridQuantization.g_thirtysecond}
    
    REPEAT_STATES = {'OFF' : 1.0, '1/4' : 1.0, '1/4T' : 0.666666666667, '1/8' : 0.5, '1/8T' : 0.333333333333, '1/16' : 0.25, '1/16T' : 0.166666666667, '1/32' : 0.125, '1/32T' : 0.0833333333333}
    
    WARP_MODES = {'BEATS': 0, 'TONES': 1, 'TEXTURE': 2, 'RE-PITCH': 3, 'COMPLEX': 4, 'COMPLEX PRO': 6}
    
    AUDIO_DEVS = {u'SIMPLE DELAY': u'Simple Delay', u'OVERDRIVE': u'Overdrive', u'LOOPER': u'Looper', u'AUTO FILTER': u'Auto Filter', u'EXTERNAL AUDIO EFFECT': u'External Audio Effect', u'SATURATOR': u'Saturator', u'PHASER': u'Phaser', u'VINYL DISTORTION': u'Vinyl Distortion', u'DYNAMIC TUBE': u'Dynamic Tube', u'BEAT REPEAT': u'Beat Repeat', u'MULTIBAND DYNAMICS': u'Multiband Dynamics', u'CABINET': u'Cabinet', u'AUDIO EFFECT RACK': u'Audio Effect Rack', u'FLANGER': u'Flanger', u'GATE': u'Gate', u'REVERB': u'Reverb', u'GRAIN DELAY': u'Grain Delay', u'REDUX': u'Redux', u'PING PONG DELAY': u'Ping Pong Delay', u'SPECTRUM': u'Spectrum', u'COMPRESSOR': u'Compressor', u'VOCODER': u'Vocoder', u'AMP': u'Amp', u'GLUE COMPRESSOR': u'Glue Compressor', u'EROSION': u'Erosion', u'EQ THREE': u'EQ Three', u'EQ EIGHT': u'EQ Eight', u'RESONATORS': u'Resonators', u'FREQUENCY SHIFTER': u'Frequency Shifter', u'AUTO PAN': u'Auto Pan', u'CHORUS': u'Chorus', u'LIMITER': u'Limiter', u'CORPUS': u'Corpus', u'FILTER DELAY': u'Filter Delay', u'UTILITY': u'Utility'}
    
    INS_DEVS = {u'TENSION': u'Tension', u'EXTERNAL INSTRUMENT': u'External Instrument', u'ELECTRIC': u'Electric', u'INSTRUMENT RACK': u'Instrument Rack', u'DRUM RACK': u'Drum Rack', u'COLLISION': u'Collision', u'IMPULSE': u'Impulse', u'SAMPLER': u'Sampler', u'OPERATOR': u'Operator', u'ANALOG': u'Analog', u'SIMPLER': u'Simpler'}
    
    MIDI_DEVS = {u'NOTE LENGTH': u'Note Length', u'CHORD': u'Chord', u'RANDOM': u'Random', u'MIDI EFFECT RACK': u'MIDI Effect Rack', u'SCALE': u'Scale', u'PITCH': u'Pitch', u'ARPEGGIATOR': u'Arpeggiator', u'VELOCITY': u'Velocity'}
