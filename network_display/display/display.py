from abc import abstractmethod

class Display:
    @abstractmethod
    def clear(self, color=(0, 0, 0)):
        raise NotImplementedError

    @abstractmethod
    def draw_pixel(self, x, y, color):
        raise NotImplementedError

    @abstractmethod
    def draw_line(self, x1, y1, x2, y2, color):
        raise NotImplementedError

    @abstractmethod
    def draw_text(self, x, y, text, color):
        raise NotImplementedError
    
    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def show(self):
        raise NotImplementedError
    
    @abstractmethod
    def quit(self):
        raise NotImplementedError
    
    @abstractmethod
    def draw_frame(self, framebuffer):
        raise NotImplementedError
