import pygame
import miniaudio
import os

class Audio:
    def __init__(self, filepath: str):
        ext = os.path.splitext(filepath)[1].lower()
        valid_exts = ('.mp3', '.wav', '.ogg', '.flac', '.m4a', '.aac')
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file not found: {filepath}")
        if ext not in valid_exts:
            raise ValueError(f"Unsupported format: {ext}. Supported: {valid_exts}")
        self.filepath = filepath
        self.backend = self._detect_backend()
        self._load()
        self._stream = None
        self._paused = False
        self._volume = 1.0
    def _detect_backend(self):
        try:
            import miniaudio
            return 'miniaudio'
        except ImportError:
            return 'pygame'

    def _load(self):
        if self.backend == 'miniaudio':
            self._info = miniaudio.get_file_info(self.filepath)
            self._stream = None
        else:  # pygame
            self._sound = pygame.mixer.Sound(self.filepath)

    def play(self, loop=False, volume=None):
        play_volume = volume if volume is not None else self._volume

        if self.backend == 'miniaudio':
            self._stream = miniaudio.play_file(
                self.filepath,
                loop=loop,
                volume=play_volume
            )
        else:  # pygame
            self._sound.set_volume(play_volume)
            self._sound.play(-1 if loop else 0)

        self._paused = False
    def stop(self):
        if self.backend == 'miniaudio' and self._stream:
            self._stream.stop()
            self._stream = None
        else:
            self._sound.stop()

    @property
    def duration(self):
        if self.backend == 'miniaudio':
            return self._info.duration
        else:
            return self._sound.get_length()
    def pause(self):
        if self.backend == 'miniaudio' and self._stream:
            self._stream.pause()
            self._paused = True
        elif self.backend == 'pygame':
            pygame.mixer.pause()
    def resume(self):
        if self.backend == 'miniaudio' and self._stream and self._paused:
            self._stream.resume()
            self._paused = False
        elif self.backend == 'pygame':
            pygame.mixer.unpause()

    def set_volume(self, volume: float):
        self._volume = max(0.0, min(1.0, volume))

        if self.backend == 'miniaudio' and self._stream:
            self._stream.volume = self._volume
        elif self.backend == 'pygame' and hasattr(self, '_sound'):
            self._sound.set_volume(self._volume)

    def get_volume(self) -> float:
        return self._volume

    def fade_out(self, duration_ms: int):
        if self.backend == 'miniaudio' and self._stream:
            self._stream.fade_out(duration_ms)
        elif self.backend == 'pygame':
            self._sound.fadeout(duration_ms)

    def fade_in(self, duration_ms: int, loop=False):
        if self.backend == 'miniaudio':
            self._stream = miniaudio.play_file(
                self.filepath,
                loop=loop,
                volume=0.0
            )
            self._stream.fade_in(duration_ms, target_volume=self._volume)