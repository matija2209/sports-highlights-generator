from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip,concatenate,VideoClip
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip,ImageClip
from PIL import Image
# Function to create a crossfade transition
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
import numpy as np

def wipe_effect(get_frame, t):
    """ Generates a frame for a wipe effect mask """
    frame = get_frame(t)
    frame_width, frame_height = frame.shape[1], frame.shape[0]
    wipe_width = int(frame_width * t / 10)  # Adjust the 10 for speed
    mask = np.zeros((frame_height, frame_width))
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
    txt_clip = TextClip(text, fontsize=110, color='white', font='Montserrat-Regular')
    
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

def mehe(highlights):
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

    for highlight in highlights:
        timestamp = highlight['timestamp']
        name = highlight["name"]
        start = max(0, timestamp - duration_before)
        end = min(timestamp + duration_after, video.duration)
        clip = video.subclip(start, end)
        overlay_text = name  # Customize your text
        clip_with_banner = add_premier_league_style_banner(clip, overlay_text)

        clips.append(clip_with_banner)
    # Adding transitions between clips
    print(f"There are total of {len(clips)} clips")

    custom_padding = 2
    final_clips = [clips[0]]

    # Loop through the remaining clips, adding each with a crossfade
    for clip in clips[1:]:
        final_clips.append(clip.crossfadein(custom_padding))
    final_video = concatenate_videoclips(final_clips, padding=-custom_padding, method="chain")

    # Write the result to a file
    final_video.write_videofile(
    f"highlights/{file_name}.mp4", 
        codec="libx265", 
        fps=24, 
        ffmpeg_params=['-vcodec', 'hevc_videotoolbox', '-tag:v', 'hvc1', '-quality', '54', 
                    '-acodec', 'aac', '-b:a', '128k']
    )


timestamps = [
    {'timestamp': 318, 'name': 'Tekma I'},
    {'timestamp': 612, 'name': 'PRILOŽNOST'},
    {'timestamp': 775, 'name': 'GOL'},
    # {'timestamp': 860, 'name': 'Tekma II'},
    # {'timestamp': 1365, 'name': 'Tekma III'},
    # {'timestamp': 1581, 'name': 'PRILOŽNOST'},
    # {'timestamp': 1665, 'name': 'GOL'},
    # {'timestamp': 1788, 'name': 'GOL (Mark)'},
    # {'timestamp': 1880, 'name': 'Tekma IV'},
    # {'timestamp': 2265, 'name': 'GOL (Tim)'},
    # {'timestamp': 2325, 'name': 'GOL (Aleks...)'},
    # {'timestamp': 2350, 'name': 'PRILOŽNOST'},
    # {'timestamp': 2355, 'name': 'PRILOŽNOST'},
    # {'timestamp': 2414, 'name': 'Tekma V'},
    # {'timestamp': 2503, 'name': 'Izbijanje NM'},
    # {'timestamp': 2780, 'name': 'GREAT GOL'},
    # {'timestamp': 2930, 'name': 'Tekma VI'},
    # {'timestamp': 3103, 'name': 'GOL'},
    # {'timestamp': 3310, 'name': 'POŠKODBA'},
    # {'timestamp': 3398, 'name': 'GOL'},
    # {'timestamp': 3459, 'name': 'Tekma VII'},
    # {'timestamp': 3545, 'name': 'GOL (Filip)'},
    # {'timestamp': 3723, 'name': 'PRILOŽNOST'},
    # {'timestamp': 3735, 'name': 'GOL'},
    # {'timestamp': 3881, 'name': 'GOL'},
    # {'timestamp': 4006, 'name': 'Tekma VIII'},
    # {'timestamp': 4409, 'name': 'Piša Matic'},
    # {'timestamp': 4528, 'name': 'GOL'},
    # {'timestamp': 4570, 'name': 'Tekma IX'},
    # {'timestamp': 4668, 'name': 'PODAJA'},
    # {'timestamp': 4690, 'name': '"Faul" nad Žetkotom'},
    # {'timestamp': 4855, 'name': 'GOL'},
    # {'timestamp': 4928, 'name': 'GOL'},
    # {'timestamp': 5055, 'name': 'GOL'},
    # {'timestamp': 5250, 'name': 'Tekma X'},
    # {'timestamp': 5812, 'name': 'Piša Žan'}
    ]



if __name__ == "__main__":
    mehe(timestamps)