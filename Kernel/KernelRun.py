from typing import Union, Callable, List
import concurrent.futures
import pygame
class BreakThread(Exception):
    def __init__(self, message):
        super().__init__(message)
class Thread:
    def __init__(self, functions: list, quitcondition: Union[int, Callable[..., bool], None] = pygame.QUIT, fps=60):
        self.functions = functions
        self.quitcondition = quitcondition
        self.running = True
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.break_requested = False
    def threadstart(self):
        if self.quitcondition or self.fps > 0:
            try:
                while self.running and not self.break_requested:
                    for event in pygame.event.get():
                        if isinstance(self.quitcondition, int) and (event.type == self.quitcondition):
                            self.running = False

                    if callable(self.quitcondition):
                        self.running = False
                    for func in self.functions:
                        func()
                    self.clock.tick(self.fps)
            except BreakThread:
                self.running = False
            except Exception as e:
                print(f"Thread error: {e}")
                raise
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