"""Module for handling audio playback in Pygame.

This module provides a wrapper around Pygame's mixer for easier audio management,
including loading, playing, pausing, and fading audio files.
"""

import os
import pygame
import time
from pgtkb.KernelInit import audio_init
audio_init()
_cur_run_audio = []

def cleanupaudio():
    """Stop all currently playing audio instances.

    This function iterates through all tracked Audio instances and stops them.
    """
    for audio in _cur_run_audio:
        audio.stop()

class Audio:
    """Wrapper class for Pygame Sound objects.

    Provides a higher-level interface for managing audio playback, volume,
    and simple fading effects.

    Attributes:
        filepath (str): Path to the audio file.
        is_play (bool): Whether the audio is currently playing or paused.
        is_paused (bool): Whether the audio is currently paused.
        channel (pygame.mixer.Channel): The Pygame mixer channel used for playback.
    """
    __slots__ = ('filepath', '_volume', 'is_play', 'is_paused', '_loop', '_sound', 'channel')
    def __init__(self, filepath: str):
        """Initializes the Audio object.

        Args:
            filepath (str): The path to the audio file to load.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file format is not supported.
        """
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
        """Load the sound file using pygame mixer.

        This is an internal method called during initialization.
        """
        self._sound = pygame.mixer.Sound(self.filepath)

    def play(self, loop=False, volume=None):
        """Start playback of the audio file.

        Args:
            loop (bool): If True, the audio will loop indefinitely. Defaults to False.
            volume (float, optional): Initial volume setting (0.0 to 1.0).
                If None, uses the current volume. Defaults to None.
        """
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
        """Stop playback completely and reset the playback state."""
        self.is_play = False
        self._loop = False
        self.is_paused = False

        if self.channel:
            self.channel.stop()
            self.channel = None

    @property
    def duration(self) -> float:
        """Return the duration of the audio file in seconds.

        Returns:
            float: Duration in seconds.
        """
        return self._sound.get_length()

    def pause(self):
        """Pause the current playback if audio is playing."""
        if self.channel and self.channel.get_busy() and not self.is_paused:
            self.channel.pause()
            self.is_paused = True
            self.is_play = True

    def resume(self):
        """Resume playback if the audio is currently paused."""
        if self.channel and self.is_paused:
            self.channel.unpause()
            self.is_paused = False
            self.is_play = True

    def set_volume(self, volume: float):
        """Set the playback volume.

        Args:
            volume (float): The volume level to set, clamped between 0.0 and 1.0.
        """
        self._volume = max(0.0, min(1.0, volume))
        if self._sound:
            self._sound.set_volume(self._volume)

    def get_volume(self) -> float:
        """Return the current volume setting.

        Returns:
            float: The current volume (0.0 to 1.0).
        """
        return self._volume

    def fade_out(self, duration_ms: int):
        """Fade out and stop playback.

        Args:
            duration_ms (int): Duration of the fade-out in milliseconds.
        """
        if self._sound:
            self._sound.fadeout(duration_ms)
        self.is_play = False
        self.is_paused = False
        self.channel = None

    def fade_in(self, duration_ms: int, loop=False):
        """Fade in the audio over a specified duration.

        Args:
            duration_ms (int): Duration of the fade-in in milliseconds.
            loop (bool): Whether the audio should loop after fading in. Defaults to False.
        """
        self.set_volume(0.0)
        self.play(loop=loop)

        steps = 50
        step_duration = duration_ms / steps / 1000.0

        for i in range(steps):
            new_vol = self._volume * ((i + 1) / steps)
            self._sound.set_volume(new_vol)
            time.sleep(step_duration)

    def is_playing(self) -> bool:
        """Check if the audio is currently playing on its channel.

        Returns:
            bool: True if playing, False otherwise.
        """
        return self.channel is not None and self.channel.get_busy()