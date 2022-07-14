from manim import *
from manim.opengl import *


class Scroll(AnimationGroup):
    """Animasi seperti manatal paparan. Diberi dua objek untuk bersilih ganti."""

    def __init__(
        self, mob: Mobject, target_mob: Mobject, shift: np.ndarray = UP, **kwargs
    ):
        target_mob.move_to(mob, **kwargs)
        mob.set_opacity(1).generate_target()
        mob.target.next_to(target_mob, normalize(shift), **kwargs).set_opacity(0)
        target_mob.set_opacity(1).generate_target()
        target_mob.next_to(target_mob, -normalize(shift), **kwargs).set_opacity(0)
        super().__init__(MoveToTarget(target_mob), MoveToTarget(mob))


# untuk keserasian opengl
SurroundingRectangle.deepcopy = SurroundingRectangle.copy
OpenGLMobject.align_submobjects = Mobject.align_submobjects


class ThreeDScene(ThreeDScene):
    def move_camera(
        self,
        phi: float | None = None,
        theta: float | None = None,
        gamma: float | None = None,
        zoom: float | None = None,
        focal_distance: float | None = None,
        frame_center: Mobject | Sequence[float] | None = None,
        added_anims: Iterable[Animation] = [],
        **kwargs,
    ):
        theta -= PI / 2 if config.renderer != "opengl" else 0
        # ^^ Agak susah untuk banding antara 'renderer'
        return super().move_camera(
            phi,
            theta,
            gamma,
            zoom,
            focal_distance,
            frame_center,
            added_anims,
            **kwargs,
        )


def there_and_back_with_pause(t, pause_ratio=1 / 3):
    if t < (1 - pause_ratio) / 2:
        return rate_functions.ease_in_out_sine(2 * t / (1 - pause_ratio))
    elif t > (1 + pause_ratio) / 2:
        return 1 - rate_functions.ease_in_out_sine(
            (pause_ratio - 2 * t + 1) / (pause_ratio - 1)
        )
    else:
        return 1


# tetapan opengl
config.window_monitor = 0

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
