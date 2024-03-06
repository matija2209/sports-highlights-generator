from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip,concatenate,VideoClip
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip,ImageClip,AudioFileClip,CompositeAudioClip
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip,concatenate_audioclips
import numpy as np
from lib.openai import tts
from moviepy.audio.fx.all import volumex
from utils.convertTimestampToSeconds import convert_to_seconds
import pandas as pd
from models.Timestamp import FootballEvent,TopPlayer
from typing import List
from datetime import datetime
from utils.getMatchStats import calculate_match_scores,get_top_players
import math




def create_teamsheet(table_name: str, data, file_path: str):
    # Font settings (adjust the path and size as needed)
    try:
        # Regular font for table content
        font_regular = ImageFont.truetype("arial.ttf", 45)
        font_regular = ImageFont.truetype("arial.ttf", 45)
        # Larger font for the table name
        font_large = ImageFont.truetype("arial.ttf", 96)  # Larger font size for the table name
    except IOError:
        # Fallback to default font if specific font file is not found
        font_regular = ImageFont.load_default(55)
        font_medium = ImageFont.load_default(70)
        font_large = ImageFont.load_default(120)
    
    # Enhanced layout settings
    image_width = 1600
    row_height = 130  # Increased row height for better readability
    header_height = 180  # Increased header height for emphasis
    column_padding = 70  # Padding for columns
    image_height = header_height + row_height * (len(data) + 1)  # +1 for the header row
    
    # Create an image with white background
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw table header
    draw.text((10, 10), table_name, fill="black", font=font_large)
    # Draw column titles
    # draw.text((10, header_height - 25), "Mesto", fill="black", font=font_regular)
    draw.text((60, header_height), "Ime", fill="black", font=font_medium)
    
    # Draw horizontal line after the header
    draw.line((0, header_height, image_width, header_height), fill="black", width=4)
    
    # Draw each top player row
    for i, player in enumerate(data, start=1):
        y_position = header_height + row_height * i
        # Draw horizontal line after each row
        draw.line((0, y_position, image_width, y_position), fill="gray", width=1)
        # Rank
        draw.text((10, y_position + 5), str(i), fill="black", font=font_regular)
        # Player Name
        draw.text((60, y_position + 5), player.name, fill="black", font=font_regular)
        # Score/Count

    
    # Save the image
    image.save(f"app/assets/{table_name}-{file_path}.png")




def create_table_image(table_name: str, data: List[TopPlayer], file_path: str,type="goals"):
    # Font settings (adjust the path and size as needed)
    try:
        # Regular font for table content
        font_regular = ImageFont.truetype("arial.ttf", 45)
        font_regular = ImageFont.truetype("arial.ttf", 45)
        # Larger font for the table name
        font_large = ImageFont.truetype("arial.ttf", 96)  # Larger font size for the table name
    except IOError:
        # Fallback to default font if specific font file is not found
        font_regular = ImageFont.load_default(55)
        font_medium = ImageFont.load_default(70)
        font_large = ImageFont.load_default(120)
    
    # Enhanced layout settings
    image_width = 1600
    row_height = 130  # Increased row height for better readability
    header_height = 180  # Increased header height for emphasis
    column_padding = 70  # Padding for columns
    image_height = header_height + row_height * (len(data) + 1)  # +1 for the header row
    
    # Create an image with white background
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw table header
    draw.text((10, 10), table_name, fill="black", font=font_large)
    # Draw column titles
    # draw.text((10, header_height - 25), "Mesto", fill="black", font=font_regular)
    draw.text((60, header_height), "Igralec", fill="black", font=font_medium)

    if type=="goals":
        draw.text((image_width - 750, header_height), "Dosezeni goli", fill="black", font=font_medium)
    elif type=="assists":
        draw.text((image_width - 750, header_height), "Stevilo asistenc", fill="black", font=font_medium)
    elif type=="xpg":
        draw.text((image_width - 750, header_height), "xPG", fill="black", font=font_medium)
    
    # Draw horizontal line after the header
    draw.line((0, header_height, image_width, header_height), fill="black", width=4)
    
    # Draw each top player row
    for i, player in enumerate(data, start=1):
        y_position = header_height + row_height * i
        # Draw horizontal line after each row
        draw.line((0, y_position, image_width, y_position), fill="gray", width=1)
        # Rank
        draw.text((10, y_position + 5), str(i), fill="black", font=font_regular)
        # Player Name
        draw.text((60, y_position + 5), player.name.capitalize(), fill="black", font=font_regular)
        # Score/Count
        draw.text((image_width - 750, y_position + 5), str(player.count), fill="black", font=font_regular)
    
    # Save the image
    image.save(f"app/assets/{table_name}-{file_path}.png")



def wipe_effect(get_frame, t, transition_duration):
    """ Generates a frame for a wipe effect mask using NumPy for efficiency """
    frame = get_frame(t)
    frame_width = frame.shape[1]
    wipe_width = int(frame_width * (t / transition_duration))
    # Use numpy to create the mask efficiently
    mask = np.zeros((frame.shape[0], frame.shape[1]))
    mask[:, :wipe_width] = 1
    return mask
    
def add_image_to_clip(clip, image_path):
    image = f"app/assets/{image_path}.png"
    banner_image = ImageClip(image)

    # Position the image in the center of the video clip
    x_center = (clip.size[0] - banner_image.size[0]) / 2
    y_center = (clip.size[1] - banner_image.size[1]) / 2
    banner_image = banner_image.set_position((x_center, y_center))

    # Set the duration of the image clip to match the duration of the video clip
    banner_image = banner_image.set_duration(clip.duration)

    # Composite the image onto the video clip
    final_clip = CompositeVideoClip([clip, banner_image])

    return final_clip


def add_highlight_banner(clip, text):
    # Banner settings
    banner_duration = 6
    banner_image_path = "app/assets/banner.png"
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

def make_highlights_reel(top_scorer_name,top_assists_name,top_opportunities,source_file_name,highlights:List[FootballEvent],scores,highlight_type):
    # Load your video
    video = VideoFileClip(f"app/source/{source_file_name}.mp4")

    # List of highlights
    # Duration of each clip in seconds
    duration_before = 1  # 5 seconds before the timestamp
    duration_after = 11  # 12 seconds after the timestamp

    # Duration of the transition (in seconds)
    transition_duration = 0.5

    # List to hold all the clips
    clips = []

    intro_clip = video.subclip(20, 30)
    clip_top_scorers = add_image_to_clip(intro_clip, f"{top_scorer_name}-{source_file_name}")

    intro_assists_clip = video.subclip(30, 40)
    clip_top_assists = add_image_to_clip(intro_assists_clip, f"{top_assists_name}-{source_file_name}")


    intro_second_clip = video.subclip(40, 45)
    clip_top_opps = add_image_to_clip(intro_second_clip, f"{top_opportunities}-{source_file_name}")
    
    clips.append(clip_top_scorers)
    clips.append(clip_top_assists)
    clips.append(clip_top_opps)
    frame = clip_top_scorers.get_frame(1)
    Image.fromarray(frame).save("preview.jpg")

    for index, highlight in enumerate(highlights):
        if highlight_type == "goals":
            if highlight["eventType"] == "opp":
                continue
        text_commentary = highlight.get("commentary")
        timestamp = highlight['timestamp']
        event_type = highlight["eventType"]
        player_name = highlight["scorer"]
        team = highlight.get("team")
        game = highlight.get("game")
        assist = highlight.get("assist")
        audio_file_name = f"highlight_{index}"

        if text_commentary is not None:
            tts(text_commentary, audio_file_name)  # Assuming
            commentary_audio = AudioFileClip(f"app/highlights/commentary/{audio_file_name}.mp3")

        start = max(0, timestamp - duration_before)
        end = min(timestamp + duration_after, video.duration)
        clip = video.subclip(start, end)

        if event_type == "start":
            try:
                game,teamOneGoals,teamTwoGoals = list(filter(lambda x:x["game"]==game,scores))[0].values()
            except:
                game,teamOneGoals,teamTwoGoals = game,0,0
            overlay_text = f"Tekma: {player_name.capitalize()} proti {assist.capitalize()} ({teamOneGoals}:{teamTwoGoals})"
        else:
            if isinstance(assist, str):
                overlay_text = f"{event_type.upper()}: {player_name.capitalize()} podajalec: {assist.capitalize()} ({team.upper()})"
            else:
                overlay_text = f"{event_type.upper()}: {player_name.capitalize()} ({team.upper()})"

        clip_with_banner = add_highlight_banner(clip, overlay_text)
        # Combine the video clip with the audio commentary
        if text_commentary:
            clip_with_audio = clip_with_banner.set_audio(commentary_audio)
            clips.append(clip_with_audio)
        else:
            clips.append(clip_with_banner)

    # Adding transitions between clips
    print(f"There are total of {len(clips)} clips")

    custom_padding = 2
    final_clips = [clips[0]]
    for clip in clips[1:]:
        final_clips.append(clip.crossfadein(3))
    final_video = concatenate_videoclips(final_clips, padding=-custom_padding, method="chain")

    # final_video_duration = final_video.duration

    # background_audio = AudioFileClip("app/assets/stadion-sound.mp3")
    # loop_count = int(final_video_duration / background_audio.duration) + 1
    
    # background_audio = background_audio.fx(volumex, 0.02)
    
    # extended_background_audio = concatenate_audioclips([background_audio] * loop_count)
    # extended_background_audio = extended_background_audio.set_duration(final_video_duration)

    final_audio = CompositeAudioClip([final_video.audio]) #extended_background_audio
    final_video = final_video.set_audio(final_audio)

    # Write the result to a file
    final_video.write_videofile(
    f"app/highlights/{source_file_name}-{highlight_type}-{datetime.now().strftime('%H-%M')}.mp4", 
        codec="libx265", 
        fps=24, 
        ffmpeg_params=['-vcodec', 'hevc_videotoolbox', '-tag:v', 'hvc1', '-quality', '54', 
                    '-acodec', 'aac', '-b:a', '64k']
    )

def prepare_timestamp(file_path):
    # Load the CSV file
    data = pd.read_csv(f"app/timestamps/{file_path}.csv")
    
    # Define a helper function to convert timestamps to seconds
    # Initialize the list to store the objects
    objects_list = []
    
    # Add a new column to identify the game each event belongs to
    data['game'] = 0  # Initialize the 'Game' column
    current_game = 0  # Counter for the current game

    # Iterate through each row to update the 'Game' column
    for index, row in data.iterrows():
        if row['eventType'] == 'start':
            current_game += 1  # Increment game counter when a new starts
        data.at[index, 'game'] = current_game

    # Iterate through each row in the dataframe to construct the object
    for index, row in data.iterrows():
        obj = {
            'timestamp': convert_to_seconds(row['timestamp']),
            'eventType': row['eventType'],
            'scorer': row['scorer'],
            'team': row['team'],
            'assist': row['assist'],
            'game': row['game']  # Include the game identification
        }
        objects_list.append(obj)
    
    return objects_list

if __name__ == "__main__":
    file_path = input("What is the name of the file?\n")
    timestamps = prepare_timestamp(file_path)
    scores = calculate_match_scores(timestamps)
    top_goal_scorers, top_opportunity_creators,top_assists_creators = get_top_players(timestamps)

    top_scorer_name = "Strelci"
    top_assists_name = "Asistence"
    top_opportunities = "Priloznosti"

    create_table_image(top_scorer_name,top_goal_scorers,file_path,"goals")
    create_table_image(top_assists_name,top_assists_creators,file_path,"assists")
    create_table_image(top_opportunities,top_opportunity_creators,file_path,"xpg")

    highlight_types = ["goals","all"]
    for highlight_type in highlight_types:
        make_highlights_reel(top_scorer_name,top_assists_name,top_opportunities,file_path,timestamps,scores,highlight_type)
    # tts("Hello how are you today","asdas")