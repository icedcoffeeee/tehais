from manim import *

config.background_color = "#333"


class LoadedSpring(VGroup):
    def __init__(
        self,
        length=3,
        pivot_point=LEFT * 3,
        mass=1,
        spring_const=10,
        load_style={"side_length": 1, "fill_opacity": 1, "color": RED},
        spring_style={},
        **kwargs,
    ):
        self.length = length
        self.pivot_point = pivot_point
        self.mass = mass
        self.spring_const = spring_const
        self.omega = (self.spring_const / self.mass) ** 0.5
        self.damping = self.spring_const / (self.mass * 60)
        self.displacement = 0
        self.velocity = 0

        super().__init__(**kwargs)

        self.load = Square(**load_style).move_to(self.pivot_point + self.length * RIGHT)
        self.spring = ParametricFunction(
            lambda t: np.array([t, 0.3 * np.sin(4 * PI * t), 0]),
            t_range=[0, self.length],
            **spring_style,
        ).next_to(self.pivot_point, RIGHT, 0)
        self.spring.add_updater(
            lambda mob: mob.stretch_to_fit_width(
                np.linalg.norm(self.load.get_left() - self.spring.get_left()),
                about_point=self.spring.get_left(),
            )
        )

        self.add(self.spring, self.load)

    def add_displacement(self, displacement):
        self.displacement += displacement
        self.load.shift(RIGHT * displacement)

    @override_animate(add_displacement)
    def _add_displacement_animation(self, displacement, anim_args={}):
        self.displacement += displacement
        return ApplyMethod(self.load.shift, RIGHT * displacement, **anim_args)

    def oscilating(self, dt):
        d_displacement = 0
        d_velocity = 0
        nspf = 100
        for _ in range(nspf):
            d_displacement += self.velocity * dt / nspf
            d_velocity += (
                (-self.omega ** 2 * self.displacement - self.damping * self.velocity)
                * dt
                / nspf
            )
        self.velocity += d_velocity
        self.add_displacement(d_displacement)

    def start_osc(self, damping=None):
        if damping is not None:
            self.damping /= 1 - damping
        self.add_updater(LoadedSpring.oscilating)

    def end_osc(self):
        self.remove_updater(LoadedSpring.oscilating)

    def add_frictional_ground(self):
        self.ground = VGroup(
            Line(
                self.load.get_bottom() + LEFT * 2,
                self.load.get_bottom() + RIGHT * 2,
            )
        )
        self.ground.add(
            *[
                Line(ORIGIN, DL * 0.2).shift(self.load.get_bottom() + RIGHT * i)
                for i in np.arange(-1.5, 2, 0.5)
            ]
        )
        self.add(self.ground)
        return self


class CircuitTex(MathTex):
    def __init__(self, *tex_strings, **kwargs):
        circuit_preamble = TexTemplate(preamble="\\usepackage{circuitikz}")
        super().__init__(
            *tex_strings,
            arg_separator=" ",
            tex_environment="circuitikz",
            tex_template=circuit_preamble,
            stroke_width=3,
            fill_opacity=0,
            **kwargs,
        )


class Questioning(Scene):
    def construct(self):

        a = CircuitTex(
            """
            \\draw 
            (0,0) to[battery]
            (0,2) to[R]
            (2,2) to[L]
            (2,0) to[C]
            (0,0)
            ;
            """
        ).shift(RIGHT * 3.5)
        ls = LoadedSpring().add_frictional_ground()
        darrow = DoubleArrow(LEFT, RIGHT).set_color(YELLOW)
        qm = Tex("?").next_to(darrow, UP).scale(1.5)

        self.play(Create(ls))
        self.wait()
        self.play(ls.animate.add_displacement(1))
        self.wait()
        ls.start_osc()
        self.wait(6)
        ls.end_osc()
        self.wait()
        self.play(ls.animate.shift(3.5 * LEFT), Create(a))
        self.wait()
        self.play(Create(darrow))
        self.wait()
        self.play(Write(qm), run_time=4)
        self.wait()


class One(Scene):
    def construct(self):
        ansatz = MathTex("x=x_0e^{\\alpha t}")
        alpha = MathTex("\\alpha=\\frac{-\\mu\\pm\\sqrt{\\mu^2-4\\omega^2} }{2}")
        mu = MathTex("\\mu=\\frac{b}{m}")
        mu[0][0].set_color(YELLOW)
        mu[0][2].set_color(YELLOW)
        om = MathTex("\\omega^2=\\frac{k}{m}")
        om[0][0].set_color(YELLOW)
        om[0][3].set_color(YELLOW)
        VGroup(mu, om).arrange(buff=2).shift(DOWN * 2)
        VGroup(ansatz, alpha).arrange(DOWN, 0.5)
        self.play(Write(ansatz.move_to(ORIGIN)))
        self.wait()
        self.play(Write(alpha), ansatz.animate.next_to(alpha, UP, 0.5))
        self.wait()
        self.play(
            Indicate(alpha[0][3], rate_func=there_and_back_with_pause, run_time=3),
            Indicate(alpha[0][7], rate_func=there_and_back_with_pause, run_time=3),
            Write(mu),
        )
        self.play(
            Indicate(alpha[0][11], rate_func=there_and_back_with_pause, run_time=3),
            Write(om),
        )
        self.wait()
        self.play(FadeOut(mu, om))
        self.wait()
        self.play(
            alpha[0][7].animate.scale(1 / 1.5).set_color(BLUE),
            alpha[0][11].animate.scale(1.5).set_color(RED),
            run_time=5,
        )
        self.play(
            alpha[0][7].animate.scale(1.5).set_color(WHITE),
            alpha[0][11].animate.scale(1 / 1.5).set_color(WHITE),
            run_time=5,
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                alpha,
                alpha := MathTex(
                    "\\alpha=\\frac{-\\mu\\pm\\sqrt{-\\left(4\\omega^2-\\mu^2\\right)} }{2}"
                ).move_to(alpha),
            )
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                alpha,
                alpha := MathTex(
                    "\\alpha=\\frac{-\\mu\\pm\\sqrt{-1}\\sqrt{4\\omega^2-\\mu^2} }{2}"
                ).move_to(alpha),
            )
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                alpha,
                alpha := MathTex("\\alpha=\\frac{-\\mu\\pm i\\omega' }{2}").move_to(
                    alpha
                ),
            )
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                alpha.copy(),
                answer := MathTex(
                    "x=Ae^{\\frac{-\\mu+i\\omega' }{2}t}+Be^{\\frac{-\\mu-i\\omega' }{2}t}"
                )
                .move_to(alpha)
                .shift(DOWN),
            ),
            TransformMatchingShapes(ansatz.copy(), answer),
        )
        self.wait()
        self.play(FadeOut(ansatz, alpha), answer.animate.move_to(ORIGIN))
        self.wait()
        self.play(
            TransformMatchingShapes(
                answer,
                answer := MathTex(
                    """
                    x=Ae^{-\\frac{\\mu}{2}t}e^{i\\frac{\\omega\' }{2}t}+
                    Be^{-\\frac{\\mu}{2}t}e^{-i\\frac{\\omega\' }{2}t}
                    """
                ),
            )
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                answer,
                answer := MathTex(
                    """
                    x=e^{-\\frac{\\mu}{2}t}\\left(Ae^{i\\frac{\\omega\' }{2}t}+
                    """,
                    "B",
                    """
                    e^{-i\\frac{\\omega\' }{2}t}\\right)
                    """,
                ),
            )
        )
        self.wait()
        self.play(
            Indicate(answer[0][10:17], rate_func=there_and_back_with_pause, run_time=3),
            Indicate(answer[2][0:8], rate_func=there_and_back_with_pause, run_time=3),
        )
        self.wait()
        konj = MathTex("B=", "A^*").next_to(answer, DOWN, 1)
        label = (
            Tex("konjugat nombor\\\\kompleks")
            .set_color(BLUE)
            .next_to(konj[1], DOWN, 0.5)
        )
        self.play(Write(konj))
        self.wait()
        self.play(ReplacementTransform(konj[1].copy(), label))
        self.wait()
        self.play(
            TransformMatchingTex(
                answer,
                answer := MathTex(
                    """
                    x=e^{-\\frac{\\mu}{2}t}\\left(Ae^{i\\frac{\\omega\' }{2}t}+
                    """,
                    "A^*",
                    """
                    e^{-i\\frac{\\omega\' }{2}t}\\right)
                    """,
                ),
            ),
            ReplacementTransform(konj[1], answer[1]),
            FadeOut(konj[0], label),
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                answer,
                answer := MathTex(
                    "x=",
                    "e^{-\\frac{\\mu}{2}t}",
                    "\\left(",
                    "2|A|",
                    "\\text{ kos }\\frac{\\omega'}{2}t",
                    "\\right)",
                ),
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                answer,
                answer := MathTex(
                    "x=",
                    "C",
                    "e^{-\\frac{\\mu}{2}t}",
                    "\\text{ kos }\\frac{\\omega'}{2}t",
                ),
            )
        )
        self.wait()
        self.play(
            answer[2].animate.set_color(YELLOW),
            answer[3].animate.set_color(RED),
        )
        self.wait()


class Zero(Scene):
    def construct(self):
        ls = LoadedSpring()
        self.play(Create(ls))
        self.wait()
        self.play(ls.animate.add_displacement(1))
        self.wait()
        ls.start_osc()
        self.wait(6)
        ls.end_osc()
        self.play(FadeOut(ls))
        ls = LoadedSpring().add_frictional_ground()
        self.play(Create(ls))
        self.wait()
        self.play(ls.animate.add_displacement(1))
        self.wait()
        ls.start_osc(0.99)
        self.wait(6)
        ls.end_osc()
        self.play(FadeOut(ls))
        ls = LoadedSpring().add_frictional_ground()
        self.play(Create(ls))
        self.wait()
        self.play(ls.animate.add_displacement(1))
        self.wait()
        ls.start_osc(0.8)
        self.wait(6)
        ls.end_osc()
        self.wait(2)


class Two(Scene):
    def construct(self):
        f1 = MathTex("\\text{kos }\\theta=\\frac{e^{i\\theta}+e^{-i\\theta}}{2}")
        f2 = MathTex("\\sin\\theta=\\frac{e^{i\\theta}-e^{-i\\theta}}{2i}")
        VGroup(f1, f2).arrange(buff=2)
        huk_eu = MathTex("e^{i\\theta}=\\text{kos }\\theta+i\\sin\\theta").shift(UP * 2)
        self.play(Write(VGroup(f1, f2)))
        self.wait()
        self.play(Write(huk_eu))
        self.wait()
        self.play(
            TransformMatchingShapes(
                f1,
                f1 := MathTex(
                    "2\\text{ kos }\\theta=e^{i\\theta}+e^{-i\\theta}"
                ).move_to(f1),
            ),
            TransformMatchingShapes(
                f2,
                f2 := MathTex("2i\\sin\\theta=e^{i\\theta}-e^{-i\\theta}").move_to(f2),
            ),
        )
        self.wait()
        self.play(
            Circumscribe(f1[0][6:9], run_time=3),
            Circumscribe(f1[0][10:], run_time=3),
            Circumscribe(f2[0][7:10], run_time=3),
            Circumscribe(f2[0][11:], run_time=3),
        )
        self.wait()
        self.play(
            Circumscribe(f1[0][:5], run_time=3),
            Circumscribe(f2[0][:6], run_time=3),
        )
        self.wait()


class Three(Scene):
    def construct(self):
        pl = ComplexPlane().add_coordinates()
        self.play(Create(pl))

        vec1 = Vector([2, 3, 0], color=YELLOW)
        labelvec1 = MathTex("z=2+3i").next_to(pl.n2p(2 + 3j), UR)
        vec2 = Vector([2, -3, 0], color=RED)
        labelvec2 = MathTex("z^*=2-3i").next_to(pl.n2p(2 - 3j), DR)

        self.wait()
        self.play(GrowArrow(vec1), Write(labelvec1))
        self.wait()
        self.play(ReplacementTransform(vec1.copy(), vec2), Write(labelvec2))

        self.wait()
        self.play(FadeOut(labelvec1, labelvec2), vec2.animate.shift([2, 3, 0]))

        br = BraceBetweenPoints(ORIGIN, RIGHT * 4, DOWN)
        t1 = br.get_tex("2|z|\\text{ kos }\\theta")

        self.wait()
        self.play(Write(br), Write(t1))
        self.wait()


class Four(Scene):
    def construct(self):
        ax = Axes([0, 10], [-1, 1.5, 0.5])
        ax.scale(0.6).to_edge(UP)
        ax.add_coordinates()
        labels = ax.get_axis_labels(MathTex("x"), MathTex("t"))

        ls = LoadedSpring().add_frictional_ground()

        self.play(Create(ls))
        self.wait()
        self.play(Create(ax), ls.animate.shift(DOWN * 2))
        self.wait()

        self.play(ls.animate.add_displacement(1))
        self.wait()

        graph = VGroup(
            Line(ax.c2p(0, ls.displacement), ax.c2p(0, ls.displacement), color=RED)
        )

        def update_graph(mob: VGroup, dt):
            line = Line(
                mob[-1].get_end(),
                ax.c2p(ax.p2c(mob[-1].get_end())[0] + dt, ls.displacement),
                color=RED,
            )
            mob.add(line)

        self.add(graph)
        graph.add_updater(update_graph)
        ls.start_osc(0.8)
        self.wait(10)
        graph.remove_updater(update_graph)
        ls.end_osc()
        self.wait()

        exp_gr = DashedVMobject(ax.get_graph(lambda x: np.exp(-0.3 * x), color=YELLOW))

        self.play(Create(exp_gr))
        self.wait()


class Outro(Scene):
    def construct(self):
        a = Rectangle(height=9, width=16)
        a.scale_about_point(0.25, a.get_corner(UR)).move_to([3.5, -2, 0])
        b = a.copy().move_to([3.5, 2, 0])
        c = Circle(1.25, color=WHITE).move_to([-3.5, 2, 0])

        self.play(FadeIn(a, b, c))
        self.wait()
