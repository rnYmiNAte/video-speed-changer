import ffmpeg
from typing import Optional

def change_video_speed(
    input_path: str,
    output_path: str,
    speed: float = 1.0,           # overall rate (video + audio duration)
    tempo: Optional[float] = None, # audio tempo (speed) independent
    pitch_scale: Optional[float] = None,  # e.g. 1.2 = +20% pitch up
    preserve_pitch: bool = True,
    quality: str = "medium"       # ultrafast, medium, veryslow
):
    if speed <= 0:
        raise ValueError("speed must be > 0")

    stream = ffmpeg.input(input_path)

    # Video: change presentation timestamp → changes speed
    video = stream.video.filter('setpts', f"{1/speed}*PTS")

    audio = stream.audio

    # Audio tempo adjustment (changes speed without pitch by default if using rubberband)
    if tempo is not None or (preserve_pitch and speed != 1.0):
        effective_tempo = tempo if tempo is not None else speed
        if effective_tempo > 0.1:
            # rubberband is highest quality but slow; atempo is fast but limited (0.5–2.0)
            if 0.4 <= effective_tempo <= 2.0:
                audio = audio.filter('atempo', effective_tempo)
            else:
                # chain multiple atempo or use rubberband (needs lib)
                audio = audio.filter('rubberband', tempo=effective_tempo, pitch=pitch_scale or 1.0)

    # Independent pitch shift (after tempo)
    if pitch_scale is not None and pitch_scale != 1.0:
        audio = audio.filter('rubberband', pitch=pitch_scale)

    # Merge & output
    joined = ffmpeg.output(
        video, audio,
        output_path,
        vcodec='libx264', acodec='aac',
        preset=quality,
        map_metadata=1  # keep original metadata
    )

    ffmpeg.run(joined)
