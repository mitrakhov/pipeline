#!/usr/bin/env python
import time

utc_offset = time.localtime()[3] - time.gmtime()[3]


fps = 25

media_pool = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()
clip_list = media_pool.GetCurrentFolder().GetClipList()


clip_dict = {}

for clip in clip_list:
    
    raw_clip_name = clip.GetName()

    # if clip belongs to Ochi

    if len(raw_clip_name.rsplit('.', 2)[-2]) == 3:

        raw_tc = raw_clip_name.rsplit('.', 2)[0].rsplit('_', 1)[-1].split('-')

        clip_name = raw_clip_name.rsplit('.', 2)[0]

        frame_tc = ( (int(raw_tc[0]) + utc_offset) * 3600 + int(raw_tc[1]) * 60 + int(raw_tc[2]) ) * fps

        duration = int(clip.GetClipProperty("frames"))

        clip_dict[clip_name] = [clip, duration, frame_tc]

    # if clip belongs to Vezha
    
    if len(raw_clip_name.rsplit('.', 2)[-2]) == 22:

        raw_tc = raw_clip_name.rsplit('.', 2)[-2].split('-')[0].split('_')[1:]

        clip_name = raw_clip_name.rsplit('.', 1)[0]

        frame_tc = (int(raw_tc[0]) * 3600 + int(raw_tc[1]) * 60 + int(raw_tc[2])) * fps

        duration = int(clip.GetClipProperty("frames"))

        clip_dict[clip_name] = [clip, duration, frame_tc]       

sc_dict = sorted(clip_dict.items(), key = lambda x: x[1][2])

sq_name = sc_dict[0][0]

min_frame_tc = sc_dict[0][1][2]

clip_timeline = media_pool.CreateEmptyTimeline(sq_name)

track_number = 1

for clip in sc_dict:

    timeline_clip = {

    "mediaPoolItem" : clip[1][0],
    "startFrame" : 0,
    "endFrame" : clip[1][1],
    "recordFrame" : clip[1][2] - min_frame_tc,
    "trackIndex" : track_number
    
    }   

    media_pool.AppendToTimeline([timeline_clip])
    
    clip_timeline.AddTrack("video")
    
    clip_timeline.AddTrack("audio")    
    
    track_number += 1


clip_timeline.DeleteTrack("video", track_number)

clip_timeline.DeleteTrack("audio", track_number)
