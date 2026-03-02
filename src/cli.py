import argparse
from .processor import change_video_speed

def main():
    parser = argparse.ArgumentParser(description="Video Speed / Tempo / Pitch Changer")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("--speed", type=float, default=1.0, help="Overall speed multiplier")
    parser.add_argument("--tempo", type=float, help="Audio tempo (independent)")
    parser.add_argument("--pitch", type=float, help="Pitch scale (e.g. 1.2 = higher voice)")
    parser.add_argument("--preserve-pitch", action="store_true", default=True)
    parser.add_argument("--fast", action="store_true", help="Use ultrafast preset")

    args = parser.parse_args()

    change_video_speed(
        args.input, args.output,
        speed=args.speed,
        tempo=args.tempo,
        pitch_scale=args.pitch,
        preserve_pitch=args.preserve_pitch,
        quality="ultrafast" if args.fast else "medium"
    )
