from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip,concatenate,VideoClip
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip,ImageClip,AudioFileClip,CompositeAudioClip
from PIL import Image
# Function to create a crossfade transition
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip,concatenate_audioclips
import numpy as np
from lib.openai import tts
from moviepy.audio.fx.all import volumex

def wipe_effect(get_frame, t, transition_duration):
    """ Generates a frame for a wipe effect mask using NumPy for efficiency """
    frame = get_frame(t)
    frame_width = frame.shape[1]
    wipe_width = int(frame_width * (t / transition_duration))
    # Use numpy to create the mask efficiently
    mask = np.zeros((frame.shape[0], frame.shape[1]))
    mask[:, :wipe_width] = 1
    return mask
    
def add_premier_league_style_banner(clip, text):
    # Banner settings
    banner_duration = 6
    banner_image_path = "assets/banner.png"
    banner_height = int(clip.h / 5)
    banner_width = clip.w
    banner_pos = (5, clip.h - banner_height - 30)
    
    # Determine banner duration
    banner_clip_duration = min(banner_duration, clip.duration)
    
    # Create banner image clip
    banner_image = ImageClip(banner_image_path, duration=banner_clip_duration)

    # Create text clip
    txt_clip = TextClip(text, fontsize=90, color='white', font='Montserrat-Regular')
    
    # Calculate vertical position for the text
    vertical_center = (banner_height - txt_clip.h) / 2
    text_position = (200, vertical_center)

    # Set position and duration of text clip
    txt_clip = txt_clip.set_position(text_position).set_duration(banner_clip_duration)

    # Overlay text on the banner
    banner_clip = CompositeVideoClip([banner_image, txt_clip], size=(banner_width, banner_height))

    # Apply fade in and fade out to the banner
    banner_clip = banner_clip.fadein(0.5).fadeout(2)

    # Set the banner position and duration
    banner_clip = banner_clip.set_position(banner_pos)

    mask_clip = banner_clip.mask

    # Apply fade in and fade out to both the image and the mask
    banner_clip = banner_clip.fadein(0.5).fadeout(2)
    mask_clip = mask_clip.fadein(0.5).fadeout(2)

    # Reattach the mask to the image
    banner_clip = banner_clip.set_mask(mask_clip)

    # Overlay the banner clip on the original clip
    final_clip = CompositeVideoClip([clip, banner_clip])

    # Save a preview frame
    frame = final_clip.get_frame(1)
    Image.fromarray(frame).save("preview.jpg")

    # Set the duration for the final clip
    return final_clip.set_duration(clip.duration)

def make_highlights_reel(highlights):
    file_name = input("Finished highlights video name?\n")
    source_file_name =  "source-video.mp4" #input("Source file name") # 
    # Load your video
    video = VideoFileClip(f"./source/{source_file_name}")

    # List of highlights
    # Duration of each clip in seconds
    duration_before = 4  # 5 seconds before the timestamp
    duration_after = 10  # 12 seconds after the timestamp

    # Duration of the transition (in seconds)
    transition_duration = 0.5

    # List to hold all the clips
    clips = []

    for index, highlight in enumerate(highlights):
        text_commentary = highlight["commentary"]
        timestamp = highlight['timestamp']
        name = highlight["name"]

        audio_file_name = f"highlight_{index}"
        tts(text_commentary, audio_file_name)  # Assuming
        commentary_audio = AudioFileClip(f"highlights/commentary/{audio_file_name}.mp3")
        start = max(0, timestamp - duration_before)
        end = min(timestamp + duration_after, video.duration)
        clip = video.subclip(start, end)
        overlay_text = name  # Customize your text
        clip_with_banner = add_premier_league_style_banner(clip, overlay_text)

        # Combine the video clip with the audio commentary
        clip_with_audio = clip_with_banner.set_audio(commentary_audio)
        clips.append(clip_with_audio)
    # Adding transitions between clips
    print(f"There are total of {len(clips)} clips")

    custom_padding = 2
    final_clips = [clips[0]]
    for clip in clips[1:]:
        final_clips.append(clip.crossfadein(3))
    final_video = concatenate_videoclips(final_clips, padding=-custom_padding, method="chain")

    final_video_duration = final_video.duration

    background_audio = AudioFileClip("assets/stadion-sound.mp3")
    loop_count = int(final_video_duration / background_audio.duration) + 1
    
    background_audio = background_audio.fx(volumex, 0.15)
    
    extended_background_audio = concatenate_audioclips([background_audio] * loop_count)
    extended_background_audio = extended_background_audio.set_duration(final_video_duration)

    final_audio = CompositeAudioClip([final_video.audio, extended_background_audio])
    final_video = final_video.set_audio(final_audio)

    # Write the result to a file
    final_video.write_videofile(
    f"highlights/{file_name}.mp4", 
        codec="libx265", 
        fps=24, 
        ffmpeg_params=['-vcodec', 'hevc_videotoolbox', '-tag:v', 'hvc1', '-quality', '54', 
                    '-acodec', 'aac', '-b:a', '128k']
    )

timestamps = [
    {'timestamp': 318, 'name': 'Tekma I', 'commentary': "Welcome to today's match between Team A and Team B! The atmosphere is electric as we kick off this exciting encounter."},
    {'timestamp': 615, 'name': 'PRILOŽNOST', 'commentary': "Here comes Žan, with a spectacular dribble across the entire court! Just couldn't find the finish."},
    {'timestamp': 775, 'name': 'GOL', 'commentary': "Goal in the dying moments for Team B! Hamzo finds the net, securing a win in a dramatic fashion. What a climax to this game!"},
    {'timestamp': 860, 'name': 'Tekma II', 'commentary': "And we're onto the next game, with Team B carrying their momentum against Team C. Let's see how this unfolds."},
    {'timestamp': 1365, 'name': 'Tekma III', 'commentary': "The third game begins with Team A looking to bounce back against Team C. The stakes are high!"},
    {'timestamp': 1583, 'name': 'PRILOŽNOST', 'commentary': "Matija makes a daring dribble into the corner. He passes to Aleksander... Oh, but the finish is just not there!"},
    {'timestamp': 1665, 'name': 'GOL', 'commentary': "Team C scores a beautifully worked goal! Tazzo with the finish and Nick with the assist. That's textbook teamwork!"},
    {'timestamp': 1788, 'name': 'GOL', 'commentary': "Mark for Team A responds with a goal after incredible dribbling by Matija. This match is full of twists!"},
    {'timestamp': 1880, 'name': 'Tekma IV', 'commentary': "The second encounter between Team A and Team B begins. The rivalry intensifies!"},
    {'timestamp': 2265, 'name': 'GOL', 'commentary': "Tim scores for Team A after a deflection. Sometimes, luck is all you need!"},
    {'timestamp': 2325, 'name': 'GOL', 'commentary': "Aleksander with a cool finish for Team A, following a splitting pass from Matija. These guys are on fire!"},
    {'timestamp': 2350, 'name': 'PRILOŽNOST', 'commentary': "A 4v1 chance for Team A, but they can't capitalize! Such moments can turn games, and they've missed it."},
    {'timestamp': 2414, 'name': 'Tekma V', 'commentary': "We're now into the second encounter between Team B and Team C. The competition is heating up!"},
    {'timestamp': 2503, 'name': 'Izbijanje NM', 'commentary': "A crucial clearance by Nick, denying Argentim a scoring opportunity. That was close!"},
    {'timestamp': 2780, 'name': 'GREAT GOL', 'commentary': "What a phenomenal volley by Matic for Team B! Žetko had no chance. The crowd goes wild!"},
    {'timestamp': 2930, 'name': 'Tekma VI', 'commentary': "Team A faces off against Team C in the next match. The energy is palpable!"},
    {'timestamp': 3103, 'name': 'GOL', 'commentary': "Aleksander finishes a brilliant chance for Team A, with Mark assisting. Their teamwork is impeccable!"},
    {'timestamp': 3310, 'name': 'POŠKODBA', 'commentary': "A pause as Davor from Team C is injured. We hope it's not too serious. The game takes a brief halt."},
    {'timestamp': 3398, 'name': 'GOL', 'commentary': "Nick executes a beautiful volley off the crossbar for Team B, assisted by Žetko. What a goal!"},
    {'timestamp': 3459, 'name': 'Tekma VII', 'commentary': "Team B and Team A are back at it. The rivalry is intense, and the fans are fully engaged."},
    {'timestamp': 3471, 'name': 'PRILOŽNOST', 'commentary': "Matija intercepts in the midfield but fails to convert. These missed opportunities might haunt them later."},
    {'timestamp': 3545, 'name': 'GOL', 'commentary': "Filip scores for Team A after a deflection, with Aleksander providing some brilliant dribbling on the left."},
    {'timestamp': 3723, 'name': 'PRILOŽNOST', 'commentary': "Matija again in the action, but his pass to Filip isn't on target. Team A needs to capitalize on these moments."},
    {'timestamp': 3735, 'name': 'GOL', 'commentary': "Hamzo scores from a tough angle for Team B! They're showing resilience and skill in equal measure."},
    {'timestamp': 3881, 'name': 'GOL', 'commentary': "Team A's Matija scores uncontested after a well-worked set-piece, assisted by Filip. They're back in it!"},
    {'timestamp': 4006, 'name': 'Tekma VIII', 'commentary': "And we're off with Team B and Team C again. The pace has not dropped one bit."},
    {'timestamp': 4409, 'name': 'Nice Dribbling', 'commentary': "Matic shows off his skills with some fine dribbling, getting the ball through the legs. The crowd appreciates the flair!"},
    {'timestamp': 4528, 'name': 'GOL', 'commentary': "Argentim intercepts a pass from Samuel and scores a perfect lob for Team C. What a way to seize the moment!"},
    {'timestamp': 4810, 'name': 'Tekma IX', 'commentary': "We're into the next match with Team A and Team C. The intensity is not letting up."},
    {'timestamp': 5268, 'name': 'PODAJA', 'commentary': "A great pass from Matija, but Mark is just unlucky not to score."},
    {'timestamp': 4690, 'name': 'Faul nad Žetkotom', 'commentary': "High tension here! Team C calls for a foul, but VAR shows Matija was first. Play continues with foul."},
    {'timestamp': 4828, 'name': 'PODAJA', 'commentary': "Erik delivers a nice pass, but Argentim can't capitalize. Team C needs to make these chances count."},
    {'timestamp': 4855, 'name': 'GOL', 'commentary': "Argentim, for Team C, finds the net after a pass from Tazzo. Teamwork makes the dream work!"},
    {'timestamp': 4928, 'name': 'GOL', 'commentary': "Team A fights back! Žan carries the ball, Mark finds Aleksander, who converts. They're not giving up!"},
    {'timestamp': 5055, 'name': 'GOL', 'commentary': "Argentim seals the win for Team C with another top-corner goal from a corner. They're asserting dominance!"},
    {'timestamp': 5250, 'name': 'Tekma X', 'commentary': "We're into the last game of the day, Team A versus Team C. It's been a rollercoaster of a match!"},
    {'timestamp': 5305, 'name': 'GOL', 'commentary': "Žetko for Team A scores after some nice passing with Kristjan. Beautiful teamwork on display!"},
    {'timestamp': 5334, 'name': 'PRILOŽNOST', 'commentary': "A chance to equalize for Team A! Filip finds himself clear, but the shot isn't accurate enough."},
    {'timestamp': 5709, 'name': 'GOL', 'commentary': "Team C scores a goal from a counterattack! Argentim scores 1v1 after a pass from Hamzo. Clinical finish!"},
    {'timestamp': 5725, 'name': 'Žan Scores', 'commentary': "Žan for Team A responds with a fantastic solo run and goal. What a response!"},
    {'timestamp': 5812, 'name': 'Piša Žan', 'commentary': "And in a delightful display of skill, Žan gets the ball through legs with some nice dribbling. The fans are loving it!"}
]


if __name__ == "__main__":
    make_highlights_reel(timestamps)
    # tts("Hello how are you today","asdas")