from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip,concatenate
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

# Function to create a crossfade transition
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

def add_premier_league_style_banner(clip, text, banner_duration=5):
    # Calculate banner size and position
    padding = 10
    fadeout_duration = 0.5
    banner_height = int(clip.h / 5)
    banner_width = clip.w
    banner_pos = (0, clip.h - banner_height)

    # Create a color clip (banner background)
    banner = ColorClip(size=(banner_width, banner_height), color=(255, 255, 255), duration=banner_duration)

    # Create a text clip with simplified parameters
    txt_clip = TextClip(text, fontsize=110, color='black', font='Arial')

    # Calculate vertical position for the text to be aligned at the bottom of the banner with some padding
    vertical_pos_for_text = banner_height - txt_clip.h - padding

    # Calculate horizontal position for the text to be aligned to the left side of the banner with some padding
    horizontal_pos_for_text = padding

    # Set the position and duration of the text clip
    txt_clip = txt_clip.set_position((horizontal_pos_for_text, vertical_pos_for_text)).set_duration(banner_duration)

    # Overlay the banner and text on the original clip
    banner_clip = CompositeVideoClip([banner, txt_clip.set_position((horizontal_pos_for_text, vertical_pos_for_text))], size=clip.size)
    banner_clip_duration = min(banner_duration, clip.duration)
    banner_clip = banner_clip.set_duration(banner_clip_duration).fadeout(fadeout_duration)

    # Overlay the banner clip on the original clip
    final_clip = CompositeVideoClip([clip, banner_clip.set_position(('left', 'bottom'))])

    return final_clip.set_duration(clip.duration)

def mehe(highlights):
    file_name = input("Finished highlights video name?\n")
    source_file_name == input("Source file name",) # "Nogomet 18-2-2024.mp4"
    # Load your video
    video = VideoFileClip(f"./source/{file_name}")

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
    {'timestamp': 860, 'name': 'Tekma II'},
    {'timestamp': 1365, 'name': 'Tekma III'},
    {'timestamp': 1581, 'name': 'PRILOŽNOST'},
    {'timestamp': 1665, 'name': 'GOL'},
    {'timestamp': 1788, 'name': 'GOL (Mark)'},
    {'timestamp': 1880, 'name': 'Tekma IV'},
    {'timestamp': 2265, 'name': 'GOL (Tim)'},
    {'timestamp': 2325, 'name': 'GOL (Aleks...)'},
    {'timestamp': 2350, 'name': 'PRILOŽNOST'},
    {'timestamp': 2355, 'name': 'PRILOŽNOST'},
    {'timestamp': 2414, 'name': 'Tekma V'},
    {'timestamp': 2503, 'name': 'Izbijanje NM'},
    {'timestamp': 2780, 'name': 'GREAT GOL'},
    {'timestamp': 2930, 'name': 'Tekma VI'},
    {'timestamp': 3103, 'name': 'GOL'},
    {'timestamp': 3310, 'name': 'POŠKODBA'},
    {'timestamp': 3398, 'name': 'GOL'},
    {'timestamp': 3459, 'name': 'Tekma VII'},
    {'timestamp': 3545, 'name': 'GOL (Filip)'},
    {'timestamp': 3723, 'name': 'PRILOŽNOST'},
    {'timestamp': 3735, 'name': 'GOL'},
    {'timestamp': 3881, 'name': 'GOL'},
    {'timestamp': 4006, 'name': 'Tekma VIII'},
    {'timestamp': 4409, 'name': 'Piša Matic'},
    {'timestamp': 4528, 'name': 'GOL'},
    {'timestamp': 4570, 'name': 'Tekma IX'},
    {'timestamp': 4668, 'name': 'PODAJA'},
    {'timestamp': 4690, 'name': '"Faul" nad Žetkotom'},
    {'timestamp': 4855, 'name': 'GOL'},
    {'timestamp': 4928, 'name': 'GOL'},
    {'timestamp': 5055, 'name': 'GOL'},
    {'timestamp': 5250, 'name': 'Tekma X'},
    {'timestamp': 5812, 'name': 'Piša Žan'}
    ]



if __name__ == "__main__":
    mehe(timestamps)