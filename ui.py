from ursina import *


class UiObject(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def multiplyScale(self, i):
        after = self.scale * i
        yd = self.scale_y * (i-1)
        self.scale = after
        self.scale_z = 1

        x = self.position.x
        y = self.position.y + yd

        cool = (x, y)

        return cool

class MyButton(Button):
    def __init__(self, text='', **kwargs):
        if 'origin' not in kwargs:
            kwargs['origin'] = (0, 0)

        if 'scale' not in kwargs:
            kwargs['scale'] = (0.25, 0.1)

        super().__init__(text, **kwargs)

        self.kwargs = {}
        self.selected = False

    def on_click(self):
        if self.disabled:
            return

        if callable(self._on_click) and self.kwargs:
            action = self._on_click
            action(self.kwargs)
        else:
            super().on_click()

    def set_selected(self):
        self.selected = True
        self.color = self.highlight_color

        for c in self.parent.children:
            if isinstance(c, MyButton) and c != self:
                if c.selected:
                    c.deselect()

    def deselect(self):
        self.selected = False
        self.color = Button.color

    def on_mouse_enter(self):
        if not self.disabled and self.model:
            self.model.setColorScale(self.highlight_color)

            if self.highlight_scale != 1:
                self.model.setScale(Vec3(self.highlight_scale, self.highlight_scale, 1))

        if hasattr(self, 'tooltip'):
            self.tooltip.enabled = True
            if not hasattr(self.tooltip, 'original_scale'):
                self.tooltip.original_scale = 1

            self.tooltip.animate_scale(self.tooltip.original_scale)


class MyText(Text):
    def __init__(self, text='', **kwargs):
        if 'origin' not in kwargs:
            kwargs['origin'] = (0, 0)

        super().__init__(text, **kwargs)


# class MyText2(UiObject):
#     def __init__(self, **kwargs):
#         super().__init__()
#
#         self.textEntity = MyText(**kwargs)
#         self.text
#
#     def update(self):
#         self.textEntity.text
