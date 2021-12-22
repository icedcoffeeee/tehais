from manim import *
from manim.opengl import *


class Scroll(AnimationGroup):
    def __init__(
        self, mob: Mobject, target_mob: Mobject, shift: np.ndarray = UP, **kwargs
    ):
        """Animasi seperti manatal paparan. Diberi dua objek untuk bersilih ganti."""
        target_mob.move_to(mob, **kwargs)
        mob.generate_target()
        mob.target.next_to(target_mob, normalize(shift), **kwargs).set_opacity(0)
        target_mob.generate_target()
        target_mob.next_to(target_mob, -normalize(shift), **kwargs).set_opacity(0)
        super().__init__(
            MoveToTarget(target_mob),
            MoveToTarget(mob),
        )


# untuk keserasian opengl
SurroundingRectangle.deepcopy = SurroundingRectangle.copy
OpenGLMobject.align_submobjects = Mobject.align_submobjects

# tetapan opengl
config.window_monitor = 1

# untuk penulisan formula yang kerap digunakan
from manim.utils.tex_templates import _3b1b_preamble

config["tex_template"] = TexTemplate(
    preamble=_3b1b_preamble
    + r"""
\DeclareMathOperator{\kos}{kos}
\DeclareMathOperator{\qjika}{\quad\text{jika}\quad}
\DeclareMathOperator{\qdiberi}{\quad\text{diberi}\quad}
"""
)

# singkatan untuk mudahkan penggunaan
@property
def c(self: Mobject):
    return self.get_center()


Mobject.c = c
OpenGLMobject.c = c


@property
def v(self: ValueTracker):
    return self.get_value()


ValueTracker.v = v

ARR = lambda x, y, z=0: np.array([x, y, z])
