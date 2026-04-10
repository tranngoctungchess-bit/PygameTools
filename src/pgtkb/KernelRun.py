from typing import Union

from collections.abc import Callable
import concurrent.futures
import pygame

from pgtkb import PygameRender, MainScreen, EventDispatcher

quitnow = pygame.QUIT
class BreakThread(Exception):
    def __init__(self, message):
        super().__init__(message)
class Thread:
    def __init__(self, screen: MainScreen, functions: list,
                 quitcondition: int | Callable[..., bool] | None = pygame.QUIT, fps: int| float=60):
        self.functions = functions
        self.quitcondition = quitcondition
        self.running = True
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.break_requested = False
        self.event_manager = EventDispatcher(screen)
        self.dt = 1.0 / fps if fps > 0 else 0.016
    def _loop_start(self):
        while self.running and not self.break_requested:
            self.dt = self.clock.tick(self.fps) / 1000.0
            if self.quitcondition == pygame.QUIT:
                self.running = self.event_manager.event_passdown()
            if callable(self.quitcondition) and self.quitcondition():
                self.running = False
            for func in self.functions:
                func()
    def threadstart(self):
        if self.quitcondition is not None or self.fps > 0:
            try:
                self._loop_start()
            except BreakThread:
                self.running = False
        else:
            for func in self.functions:
                func()
            self.running = False
    def threadbreak(self):
        self.break_requested = True
    def immediate_break(self):
        self.running = False
    def run_parallel(self, cpu_func, *args):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(cpu_func, *args)
            return future
    def check_future(self, future):
        if future.done():
            return future.result()
        return None
    def get_event(self):
        return self.event_manager.event
class MainApplication(Thread):
    def __init__(self, screen_size, screen_flags=0, screen_bg = (0,0,0),
                 fixed = False, quitcondition: int | Callable[..., bool] | None = quitnow,
                 fps: int | float=60, render_engine = PygameRender, caption = None, functions = None):
        user_functions = functions if functions is not None else []
        screen = MainScreen(screen_size, screen_flags, screen_bg, fixed)
        screen.set_common_engine(render_engine)
        if caption:
            screen.set_caption(caption)
        super().__init__(screen, user_functions, quitcondition, fps)
        self.screen = screen
        self.functions.append(self._main_render)

    def _main_render(self):
        for widget in self.screen.child.values():
            self._recursive_update(widget, self.dt)
        for widget in self.screen.child.values():
            widget.render()
            if widget.child:
                self._recursive_render(widget)
        pygame.display.flip()

    def _recursive_update(self, parent_widget, dt):
        if hasattr(parent_widget, 'update'):
            parent_widget.update(dt)
        for widget in parent_widget.child.values():
            self._recursive_update(widget, dt)
    def add_action(self, func):
        self.functions.append(func)
    def _recursive_render(self, parent_widget):
        for widget in parent_widget.child.values():
            widget.render()
            if widget.child:
                self._recursive_render(widget)