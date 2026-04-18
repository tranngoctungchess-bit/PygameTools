import os
import pygame
import time

_cur_run_audio = []

def cleanupaudio():
    """Stop all currently playing audio instances."""
    for audio in _cur_run_audio:
        audio.stop()

class Audio:
    def __init__(self, filepath: str):
        ext = os.path.splitext(filepath)[1].lower()
        valid_exts = ('.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac')

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file not found: {filepath}")
        if ext not in valid_exts:
            raise ValueError(f"Unsupported format: {ext}. Supported: {valid_exts}")

        self.filepath = filepath
        self._volume = 1.0
        self.is_play = False
        self.is_paused = False
        self._loop = False

        self._sound = None
        self.channel = None

        self._load()
        _cur_run_audio.append(self)

    def _load(self):
        """Load the sound file using pygame mixer."""
        self._sound = pygame.mixer.Sound(self.filepath)

    def play(self, loop=False, volume=None):
        """Start playback of the audio file."""
        if volume is not None:
            self.set_volume(volume)
        self._loop = loop
        if not self.is_paused:
            self.stop()
        else:
            if self.channel:
                self.channel.unpause()
                self.is_paused = False
                self.is_play = True
                return

        self._sound.set_volume(self._volume)
        self.channel = self._sound.play(-1 if loop else 0)
        self.is_play = True
        self.is_paused = False

    def stop(self):
        """Stop playback completely."""
        self.is_play = False
        self._loop = False
        self.is_paused = False

        if self.channel:
            self.channel.stop()
            self.channel = None

    @property
    def duration(self) -> float:
        """Return the duration of the audio file in seconds."""
        return self._sound.get_length()

    def pause(self):
        """Pause playback."""
        if self.channel and self.channel.get_busy() and not self.is_paused:
            self.channel.pause()
            self.is_paused = True
            self.is_play = True

    def resume(self):
        """Resume paused playback."""
        if self.channel and self.is_paused:
            self.channel.unpause()
            self.is_paused = False
            self.is_play = True

    def set_volume(self, volume: float):
        """Set the playback volume (0.0 to 1.0)."""
        self._volume = max(0.0, min(1.0, volume))
        if self._sound:
            self._sound.set_volume(self._volume)

    def get_volume(self) -> float:
        """Return the current volume."""
        return self._volume

    def fade_out(self, duration_ms: int):
        """Fade out over duration_ms milliseconds and stop playback."""
        if self._sound:
            self._sound.fadeout(duration_ms)
        self.is_play = False
        self.is_paused = False
        self.channel = None

    def fade_in(self, duration_ms: int, loop=False):
        """Fade in over duration_ms milliseconds, starting from volume 0."""
        self.set_volume(0.0)
        self.play(loop=loop)

        steps = 50
        step_duration = duration_ms / steps / 1000.0

        for i in range(steps):
            new_vol = self._volume * ((i + 1) / steps)
            self._sound.set_volume(new_vol)
            time.sleep(step_duration)

    def is_playing(self) -> bool:
        return self.channel is not None and self.channel.get_busy()