from manim import *


class One(Scene):
    def construct(self):
        mesin = VGroup(
            box := Square()
            .set_stroke(opacity=0)
            .set_fill(opacity=1, color=RED)
            .set_z_index(1),
            Triangle()
            .set_stroke(opacity=0)
            .set_fill(opacity=1, color=YELLOW)
            .rotate(PI / 6)
            .shift(LEFT * 1.1),
            Triangle()
            .set_stroke(opacity=0)
            .set_fill(opacity=1, color=YELLOW)
            .rotate(-PI / 6)
            .shift(RIGHT * 1.1),
        )
        mesin_label = MathTex("f").scale(2).next_to(mesin, UP)
        input_x = MathTex("x").next_to(mesin, LEFT)
        output_fx = MathTex("f(x)").next_to(mesin, RIGHT)
        self.play(FadeIn(mesin), Write(mesin_label))
        self.wait()
        self.play(Write(input_x))
        self.wait()
        self.play(ReplacementTransform(input_x, output_fx))
        self.wait()
        self.play(FadeOut(output_fx))
        self.play(
            Write(
                input_x := VGroup(MathTex("2"), MathTex("3"), MathTex("4"))
                .arrange(DOWN)
                .next_to(mesin, LEFT)
            )
        )
        self.wait()
        self.play(
            ReplacementTransform(
                input_x.copy(),
                output_fx := VGroup(MathTex("5"), MathTex("10"), MathTex("17"))
                .arrange(DOWN)
                .next_to(mesin, RIGHT),
            )
        )
        self.wait()

        ax = Axes(
            (0, 5),
            (0, 30, 5),
            axis_config={"numbers_to_exclude": [], "exclude_origin_tick": False},
            tips=False,
        )
        ax.add_coordinates()

        self.play(FadeOut(mesin, mesin_label))
        dots = VGroup(*[Dot(ax.c2p(i, i**2 + 1)) for i in [2, 3, 4]])
        self.play(
            Write(ax),
            ReplacementTransform(output_fx, dots),
            ReplacementTransform(input_x, dots),
        )
        self.wait()
        graf = ax.get_graph(lambda x: x**2 + 1, color=RED).set_z_index(-1)
        self.play(Create(graf), run_time=3)
        self.wait()
        parameter = ValueTracker(1)
        dot_in = always_redraw(
            lambda: Dot(ax.c2p(parameter.get_value(), 0), color=YELLOW)
        )
        dot_out = always_redraw(
            lambda: Dot(ax.c2p(0, parameter.get_value() ** 2 + 1), color=YELLOW)
        )
        self.play(FadeOut(dots, graf), FadeIn(dot_in, dot_out))
        self.wait()
        self.play(parameter.animate.set_value(5), rate_func=linear, run_time=5)
        self.wait()
        x_ax: NumberLine = NumberLine((0, 5), include_numbers=True).shift(DOWN)
        y_ax: NumberLine = NumberLine(
            (0, 30, 5), unit_size=1 / 5, include_numbers=True
        ).shift(UP)
        dot_in.clear_updaters()
        dot_out.clear_updaters()
        self.play(
            ReplacementTransform(ax.get_axes()[0], x_ax),
            ReplacementTransform(ax.get_axes()[1], y_ax),
            Transform(dot_in, Dot(x_ax.n2p(parameter.get_value()), color=YELLOW)),
            Transform(
                dot_out, Dot(y_ax.n2p(parameter.get_value() ** 2 + 1), color=YELLOW)
            ),
        )
        dot_in.add_updater(lambda mob: mob.move_to(x_ax.n2p(parameter.get_value())))
        dot_out.add_updater(
            lambda mob: mob.move_to(y_ax.n2p(parameter.get_value() ** 2 + 1))
        )
        self.wait()
        self.play(parameter.animate.set_value(0), run_time=0.5)
        self.wait()
        self.play(parameter.animate.set_value(5), run_time=5, rate_func=linear)
        self.wait()
        param_label = Tex("Parameter, $x$").scale(0.8).next_to(x_ax, LEFT)
        output_label = Tex("Fungsi, $f(x)$").scale(0.8).next_to(y_ax, LEFT)
        self.play(Write(param_label), Write(output_label))
        self.wait()


class Two(Scene):
    def construct(self):
        t_ax = NumberLine((0, 10, 2), unit_size=1 / 2, include_numbers=True)
        f_t_ax = NumberLine((-2, 2, 0.5), unit_size=1 / 0.5, include_numbers=True)
        g_t_ax = f_t_ax.copy()
        h_t_ax = f_t_ax.copy()
        axx = VGroup(t_ax, f_t_ax, g_t_ax, h_t_ax).arrange(DOWN, 1)

        labels = VGroup(
            MathTex("t").scale(0.8).next_to(t_ax, LEFT),
            MathTex("f(t)").scale(0.8).next_to(f_t_ax, LEFT),
            MathTex("g(t)").scale(0.8).next_to(g_t_ax, LEFT),
            MathTex("h(t)").scale(0.8).next_to(h_t_ax, LEFT),
        )

        t = ValueTracker(0)
        t_dot = always_redraw(lambda: Dot(t_ax.n2p(t.get_value()), color=YELLOW))
        f_dot = always_redraw(lambda: Dot(f_t_ax.n2p(np.sin(t.get_value())), color=RED))
        g_dot = always_redraw(
            lambda: Dot(g_t_ax.n2p(np.cos(t.get_value())), color=BLUE)
        )
        h_dot = always_redraw(
            lambda: Dot(h_t_ax.n2p(np.sin(2 * t.get_value())), color=GREEN)
        )
        dots = VGroup(t_dot, f_dot, g_dot, h_dot)

        self.play(Create(axx), Write(labels))
        self.wait()
        self.play(*[GrowFromCenter(i) for i in dots])
        self.wait()
        self.play(t.animate.set_value(10), run_time=10, rate_func=linear)
        self.wait()


class Three(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(PI / 3, -PI / 4)
        ax = ThreeDAxes((-2, 2, 0.5), (-2, 2, 0.5), (-2, 2, 0.5), 10, 10, 10)
        t = ValueTracker(1)
        f_dot = always_redraw(
            lambda: Dot3D(ax.c2p(np.sin(t.get_value()), 0, 0), color=RED)
        )
        g_dot = always_redraw(
            lambda: Dot3D(ax.c2p(0, np.cos(t.get_value()), 0), color=BLUE)
        )
        h_dot = always_redraw(
            lambda: Dot3D(ax.c2p(0, 0, np.sin(2 * t.get_value())), color=GREEN)
        )
        sum_dot = always_redraw(
            lambda: Dot3D(
                ax.c2p(
                    np.sin(t.get_value()),
                    np.cos(t.get_value()),
                    np.sin(2 * t.get_value()),
                ),
                color=YELLOW,
            )
        )
        dots = VGroup(f_dot, g_dot, h_dot, sum_dot)

        lines = always_redraw(
            lambda: VGroup(
                DashedLine(
                    ax.c2p(np.sin(t.get_value()), 0, 0),
                    ax.c2p(np.sin(t.get_value()), np.cos(t.get_value()), 0),
                    color=BLUE,
                ),
                DashedLine(
                    ax.c2p(0, np.cos(t.get_value()), 0),
                    ax.c2p(np.sin(t.get_value()), np.cos(t.get_value()), 0),
                    color=RED,
                ),
                DashedLine(
                    ax.c2p(np.sin(t.get_value()), np.cos(t.get_value()), 0),
                    ax.c2p(
                        np.sin(t.get_value()),
                        np.cos(t.get_value()),
                        np.sin(2 * t.get_value()),
                    ),
                    color=GREEN,
                ),
            )
        )

        self.play(Create(ax))
        self.play(*[GrowFromCenter(i) for i in dots[:3]])
        self.wait()
        self.play(t.animate.increment_value(2 * PI), run_time=2 * PI, rate_func=linear)
        self.wait()
        self.play(Create(lines))
        self.play(GrowFromCenter(dots[-1]))
        self.wait()
        self.begin_ambient_camera_rotation(0.1)
        self.wait()
        self.play(t.animate.increment_value(2 * PI), run_time=2 * PI, rate_func=linear)
        self.wait()
        tp = TracedPath(sum_dot.get_center)
        self.add(tp)
        self.play(t.animate.increment_value(2 * PI), run_time=2 * PI, rate_func=linear)
        tp.clear_updaters()
        self.play(t.animate.increment_value(2 * PI), run_time=2 * PI, rate_func=linear)
        self.wait()
        tex1 = MathTex(
            "\\vec a(t)=\\left\\langle \\sin t,\\text{kos }t,\\sin 2t\\right\\rangle"
        )
        self.add_fixed_in_frame_mobjects(tex1.to_corner(UL))
        self.play(
            Write(tex1),
            t.animate(run_time=2 * PI, rate_func=linear).increment_value(2 * PI),
        )
        self.wait(2)


class Four(ThreeDScene):
    def construct(self):
        rad = 2
        self.set_camera_orientation(PI / 3, -PI / 4)
        ax = ThreeDAxes(
            (-(rad + 2), (rad + 2)),
            (-(rad + 2), (rad + 2)),
            (-(rad + 2), (rad + 2)),
            (rad + 2) * 2,
            (rad + 2) * 2,
            (rad + 2) * 2,
        )

        u_sli = NumberLine((0, PI, PI / 8), PI)
        u_sli.rotate(PI / 2)
        v_sli = NumberLine((0, 2 * PI, PI / 4), PI)
        v_sli.rotate(PI / 2)
        x_sli = NumberLine((-rad, rad, rad / 4), PI)
        x_sli.rotate(PI / 2)
        y_sli = x_sli.copy()
        z_sli = x_sli.copy()
        sliders = VGroup(u_sli, v_sli, x_sli, y_sli, z_sli)
        sliders.arrange(RIGHT, 0.75)
        labels = VGroup(*[MathTex("{}".format(i)) for i in "uvxyz"])
        for i, j in zip(labels, sliders):
            i.next_to(j, UP)

        self.add_fixed_in_frame_mobjects(sliders, labels)
        self.play(Create(sliders), Write(labels))
        self.wait()

        u_val = ValueTracker(0)
        v_val = ValueTracker(0)

        u_dot = always_redraw(lambda: Dot(u_sli.n2p(u_val.get_value()), color=ORANGE))
        v_dot = always_redraw(lambda: Dot(v_sli.n2p(v_val.get_value()), color=PURPLE))

        def x_func(u, v):
            return rad * np.cos(v.get_value()) * np.sin(u.get_value())

        def y_func(u, v):
            return rad * np.sin(v.get_value()) * np.sin(u.get_value())

        def z_func(u, v):
            return rad * np.cos(u.get_value())

        x_dot = always_redraw(lambda: Dot(x_sli.n2p(x_func(u_val, v_val)), color=RED))
        y_dot = always_redraw(lambda: Dot(y_sli.n2p(y_func(u_val, v_val)), color=BLUE))
        z_dot = always_redraw(lambda: Dot(z_sli.n2p(z_func(u_val, v_val)), color=GREEN))
        dots = VGroup(u_dot, v_dot, x_dot, y_dot, z_dot)

        self.add_fixed_in_frame_mobjects(dots)
        self.play(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.1)
        self.wait()
        self.play(VGroup(sliders, labels, dots).animate.to_corner(UL))
        self.play(Create(ax))
        self.wait()

        sum_dot = always_redraw(
            lambda: Dot3D(
                [x_func(u_val, v_val), y_func(u_val, v_val), z_func(u_val, v_val)],
                color=YELLOW,
            )
        )
        lines = always_redraw(
            lambda: VGroup(
                DashedLine(
                    [x_func(u_val, v_val), 0, 0],
                    [x_func(u_val, v_val), y_func(u_val, v_val), 0],
                    color=BLUE,
                ),
                DashedLine(
                    [0, y_func(u_val, v_val), 0],
                    [x_func(u_val, v_val), y_func(u_val, v_val), 0],
                    color=RED,
                ),
                DashedLine(
                    [x_func(u_val, v_val), y_func(u_val, v_val), 0],
                    [x_func(u_val, v_val), y_func(u_val, v_val), z_func(u_val, v_val)],
                    color=GREEN,
                ),
            )
        )

        self.play(Create(lines))
        self.wait()
        self.play(GrowFromCenter(sum_dot))
        self.wait()

        tp = TracedPath(sum_dot.get_center)

        box = SurroundingRectangle(sliders[:2] + labels[:2], RED)
        self.add_fixed_in_frame_mobjects(box)
        self.play(Create(box))
        self.wait()

        self.begin_ambient_camera_rotation(0.1)

        self.add(tp)
        self.play(u_val.animate.set_value(PI), run_time=2.5, rate_func=linear)
        self.play(u_val.animate.set_value(0), run_time=2.5, rate_func=linear)

        for _ in range(8):
            for i, j in [[u_val, v_val], [v_val, u_val]]:
                if i is u_val:
                    max_val = PI
                    other_val = PI / 4
                else:
                    max_val = 2 * PI
                    other_val = PI / 8
                ph = i.get_value()
                self.wait()
                self.play(
                    j.animate.increment_value(other_val),
                    run_time=5 / 16,
                    rate_func=linear,
                )
                self.wait()
                self.play(
                    i.animate.set_value(max_val),
                    run_time=5 / 2 * (1 - ph / max_val),
                    rate_func=linear,
                )
                self.play(i.animate.set_value(0), run_time=2.5, rate_func=linear)
                self.play(
                    i.animate.set_value(ph),
                    run_time=5 / 2 * ph / max_val,
                    rate_func=linear,
                )

        self.wait(5)
        tp.clear_updaters()
        self.play(Create(sf := Sphere(radius=rad)), run_time=5)
        self.wait(2)
