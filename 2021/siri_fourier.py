import os, sys

sys.path.append(os.path.abspath("."))
from manim_advanced import *


class Intro(Scene):
    """Pengenalan."""

    def construct(self):
        quote = Tex(
            "Sebarang fungsi ",
            "antara dua had mampu ditulis\\\\dengan hanya ",
            "hasil tambah fungsi-fungsi sinus dan kosinus.",
        ).scale_to_fit_width(config.frame_width - 2)
        quote[0].set_color(YELLOW)
        quote[-1].set_color(YELLOW)

        self.play(Write(quote), run_time=3)
        self.wait()
        self.play(FadeOut(quote))

        segue = VGroup(
            Title("Siri Fourier"),
            Tex("Keserenjangan Fungsi"),
            Tex("Gerak Kerja Siri Fourier"),
            Tex("Visualisasi Siri Fourier"),
            Tex("????"),
            Tex("Nombor Kompleks"),
        )
        segue[1:].arrange(DOWN, aligned_edge=LEFT)
        segue[1:].set_color(color=GREY_E)
        segue[-1].move_to(segue[-2], LEFT).set_color(WHITE)

        self.play(*(Write(i) for i in segue[:-1]))
        self.play(segue[1].animate.set_color(WHITE), run_time=3)
        self.play(segue[2].animate.set_color(WHITE), run_time=3)
        self.play(segue[3].animate.set_color(WHITE), run_time=3)
        self.play(segue[4].animate.set_color(WHITE), run_time=3)
        self.play(ReplacementTransform(segue[4], segue[5]), run_time=3)
        self.wait()


class Keserenjangan1(Scene):
    def construct(self):
        plane = NumberPlane()
        theta = 2 * PI / 3
        vec1 = Vector(3 * np.array([np.cos(theta), np.sin(theta), 0]), color=YELLOW)
        vec2 = Vector(
            2 * np.array([np.cos(theta - PI / 2), np.sin(theta - PI / 2), 0]), color=RED
        )
        rangle = always_redraw(
            lambda: RightAngle(
                Line(ORIGIN, vec1.get_end()), Line(ORIGIN, vec2.get_end())
            )
        )
        vec1_label = always_redraw(
            lambda: MathTex("\\va u", color=YELLOW).next_to(vec1.get_end(), UR)
        )
        vec2_label = always_redraw(
            lambda: MathTex("\\va v", color=RED).next_to(vec2.get_end(), UR)
        )
        dot_formula = MathTex(
            "\\va u",
            "\\cdot",
            "\\va v",
            "=0",
            tex_to_color_map={"\\va u": YELLOW, "\\va v": RED},
        ).to_corner(UL)
        self.play(Create(plane))
        self.wait()
        self.play(GrowArrow(vec1), GrowArrow(vec2))
        self.play(Create(rangle))
        self.wait()
        self.play(Write(vec1_label), Write(vec2_label))
        self.wait()
        self.play(
            ReplacementTransform(vec1_label.copy(), dot_formula[0]),
            ReplacementTransform(vec2_label.copy(), dot_formula[2]),
            Write(dot_formula[1]),
            Write(dot_formula[3]),
        )
        self.wait()
        self.play(
            Transform(vec1, Vector([0, 2], color=YELLOW)),
            Transform(vec2, Vector([5, 0], color=RED)),
        )

        coord1 = vec1.coordinate_label(color=YELLOW)
        coord2 = vec2.coordinate_label(color=RED)

        self.play(
            ReplacementTransform(vec1_label, coord1),
            ReplacementTransform(vec2_label, coord2),
        )
        self.wait()

        dot_calc = MathTex("(0)(5)+(2)(0)=0").next_to(
            dot_formula, DOWN, aligned_edge=LEFT
        )
        dot_calc[0][1].set_color(YELLOW)
        dot_calc[0][8].set_color(YELLOW)
        dot_calc[0][4].set_color(RED)
        dot_calc[0][11].set_color(RED)

        self.play(
            AnimationGroup(
                Write(
                    VGroup(
                        dot_calc[0][0],
                        dot_calc[0][2:4],
                        dot_calc[0][5:8],
                        dot_calc[0][9:11],
                        dot_calc[0][12],
                    )
                ),
                AnimationGroup(
                    ReplacementTransform(coord1[0][0].copy(), dot_calc[0][1]),
                    ReplacementTransform(coord2[0][0].copy(), dot_calc[0][4]),
                    run_time=3,
                ),
                AnimationGroup(
                    ReplacementTransform(coord1[0][1].copy(), dot_calc[0][8]),
                    ReplacementTransform(coord2[0][1].copy(), dot_calc[0][11]),
                    run_time=3,
                ),
                Write(dot_calc[0][13:]),
                lag_ratio=1,
            )
        )
        self.wait()


class Keserenjangan2(Scene):
    def construct(self):
        fungsi_f = MathTex("f(x)=\\sin(x)")
        fungsi_g = MathTex("g(x)=\\sin(2x)")
        VGroup(fungsi_f, fungsi_g).arrange(buff=2)

        self.play(Write(fungsi_f), Write(fungsi_g))
        self.wait()

        ax = Axes((-PI / 4, 2 * PI + PI / 4, PI / 4), (-1, 1, 0.25))
        graph_f = ax.plot(lambda x: np.sin(x), [0, 2 * PI, 0.01], color=RED)

        self.play(
            AnimationGroup(
                AnimationGroup(FadeOut(fungsi_g), fungsi_f.animate.to_corner(UR)),
                Create(ax),
                lag_ratio=1,
            )
        )
        self.play(Create(graph_f))

        samples = ValueTracker(8)
        dots_f = always_redraw(
            lambda: VGroup(
                *[
                    Dot(ax.c2p(i, np.sin(i)), 0.05, color=RED)
                    for i in np.arange(
                        0,
                        2 * PI + 2 * PI / samples.get_value(),
                        2 * PI / samples.get_value(),
                    )
                ]
            )
        )

        self.play(
            AnimationGroup(*[GrowFromCenter(i) for i in dots_f], lag_ratio=0.5),
            graph_f.animate.set_stroke(opacity=0.3),
        )
        self.add(dots_f)
        self.wait()
        self.play(VGroup(ax, graph_f).animate.scale(0.5).to_edge(LEFT))
        self.wait()

        mat_f = []
        mat_f += [
            [np.sin(i)]
            for i in np.arange(
                0, 2 * PI + 2 * PI / samples.get_value(), 2 * PI / samples.get_value()
            )
        ]
        vektor_f = (
            Matrix(
                mat_f,
                element_to_mobject=DecimalNumber,
                element_to_mobject_config=dict(num_decimal_places=2),
                left_bracket="(",
                right_bracket=")",
            )
            .shift(RIGHT * 3.5)
            .scale_to_fit_height(5)
        )

        self.play(Write(vektor_f))
        vektor_f.save_state()
        self.wait()

        graph_g = ax.plot(
            lambda x: np.sin(2 * x), [0, 2 * PI, 0.01], color=YELLOW, stroke_opacity=0.3
        )
        dots_g = always_redraw(
            lambda: VGroup(
                *[
                    Dot(ax.c2p(i, np.sin(2 * i)), 0.05, color=YELLOW)
                    for i in np.arange(
                        0,
                        2 * PI + 2 * PI / samples.get_value(),
                        2 * PI / samples.get_value(),
                    )
                ]
            )
        )
        mat_g = []
        mat_g += [
            [np.sin(2 * i)]
            for i in np.arange(
                0, 2 * PI + 2 * PI / samples.get_value(), 2 * PI / samples.get_value()
            )
        ]
        vektor_g = (
            Matrix(
                mat_g,
                element_to_mobject=DecimalNumber,
                element_to_mobject_config=dict(num_decimal_places=2),
                left_bracket="(",
                right_bracket=")",
            )
            .shift(RIGHT * 3.5)
            .scale_to_fit_height(5)
        )
        graph_f.save_state()

        self.play(
            ReplacementTransform(fungsi_f, fungsi_g.to_corner(UR)),
            ReplacementTransform(graph_f, graph_g),
            ReplacementTransform(dots_f, dots_g),
            ReplacementTransform(vektor_f, vektor_g),
        )
        self.wait()

        vektor_g.save_state()
        vektor_f.restore()
        VGroup(vektor_f, dot_sym := MathTex("\\cdot"), vektor_g).arrange()
        vektor_g.restore()

        self.play(
            FadeOut(ax, graph_g, dots_g, fungsi_g),
            FadeIn(vektor_f, dot_sym),
            vektor_g.animate.next_to(dot_sym),
        )

        moving_gr = VGroup(vektor_f, dot_sym, vektor_g)
        moving_gr.save_state()
        VGroup(moving_gr, eq := MathTex("=0")).arrange()
        moving_gr.restore()

        self.play(moving_gr.animate.next_to(eq, LEFT), Write(eq))
        self.wait()
        self.clear()
        graph_f.restore()
        self.add(ax, graph_f, dots_f)
        self.play(VGroup(ax, graph_f).animate.scale(2).move_to(ORIGIN))
        self.wait()
        self.play(samples.animate.set_value(500), run_time=5)
        self.wait()

        integ_form = MathTex("\\sum", "\\sin(x)\\sin(2x)")

        self.clear()
        self.play(Write(integ_form))
        self.wait()
        self.play(
            TransformMatchingTex(
                integ_form,
                integ_form := MathTex(
                    "\\int_0^{2\\pi}", "\\sin(x)\\sin(2x)", "\\dd{x}"
                ),
            )
        )
        self.wait()

        integ_form.save_state()
        VGroup(integ_form, eq).arrange()
        integ_form.restore()

        self.play(Write(eq), integ_form.animate.next_to(eq, LEFT))
        self.wait()
        self.clear()
        self.wait()

        set_serenjang = VGroup(
            MathTex("\\{\\sin(nx)\\}_\\perp", "\\qdiberi n=0,1,2,..."),
            MathTex("\\{\\kos(nx)\\}_\\perp", "\\qdiberi n=0,1,2,..."),
            MathTex("\\kos(nx)\\sin(mx)_\\perp\\qdiberi n,m=0,1,2,..."),
        ).arrange(DOWN, 1)

        self.play(Write(set_serenjang))
        self.wait()
        self.play(Indicate(set_serenjang[0][0]), Indicate(set_serenjang[1][0]))
        self.wait()
        self.clear()

        serenjang = MathTex("\\int_0^{2\\pi}\\kos(x)", "\\kos(3x)", "\\dd{x}", "=", "0")
        nirserenjang = MathTex(
            "\\int_0^{2\\pi}\\kos(x)", "\\kos(x)", "\\dd{x}", "=", "\\pi"
        )

        self.play(Write(serenjang[:-2]))
        self.wait()
        self.play(Write(serenjang[-2:]))
        self.wait()
        self.play(
            TransformMatchingTex(
                serenjang[:-1], nirserenjang[:-1], transform_mismatches=True
            ),
            Unwrite(serenjang[-1]),
        )
        self.wait()
        self.play(Write(nirserenjang[-1]))

        dot_same_vec = MathTex("\\va u\\cdot\\va u=\\norm{\\va u}^2")
        nirserenjang.save_state()
        VGroup(nirserenjang, dot_same_vec).arrange(DOWN)
        nirserenjang.restore()

        self.play(nirserenjang.animate.next_to(dot_same_vec, UP), Write(dot_same_vec))
        self.wait()

        self.play(*[Unwrite(i) for i in [nirserenjang, dot_same_vec]])
        self.wait()


class GerakKerja1(Scene):
    def construct(self):
        formula_am = MathTex(
            "f(x)",
            "=\\sum_{n=0}^\\infty",
            "a_n",
            "\\kos(nx)",
            "+",
            "\\sum_{n=0}^\\infty",
            "b_n",
            "\\sin(nx)",
        )

        self.play(Write(formula_am))
        self.wait()
        self.play(
            Indicate(formula_am[2], rate_func=there_and_back_with_pause),
            Indicate(formula_am[6], rate_func=there_and_back_with_pause),
            run_time=3,
        )
        self.wait()
        self.play(
            Indicate(formula_am[3], rate_func=there_and_back_with_pause),
            Indicate(formula_am[7], rate_func=there_and_back_with_pause),
            run_time=3,
        )
        self.wait()
        self.play(formula_am.animate.shift(LEFT * 20), rate_func=rush_into)
        self.wait()
        Part1.construct_(self)  # malas nak tulis balik :/
        self.wait()
        self.clear()

        formula_a_n = MathTex(
            "f(x)",
            "\\kos(mx)",
            "=\\sum_{n=0}^\\infty",
            "a_n",
            "\\kos(nx)",
            "\\kos(mx)",
            "+",
            "\\sum_{n=0}^\\infty",
            "b_n",
            "\\sin(nx)",
            "\\kos(mx)",
        ).scale_to_fit_width(config.frame_width - 2)

        self.play(formula_am.animate.shift(RIGHT * 20), rate_func=rush_from)
        self.wait()
        self.play(formula_am.animate.scale_to_fit_height(formula_a_n.height))
        self.play(TransformMatchingTex(formula_am, formula_a_n))
        self.wait()

        formula_a_n2 = MathTex(
            "\\int_0^{2\\pi}",
            "f(x)",
            "\\kos(mx)",
            "\\dd{x}",
            "=\\sum_{n=0}^\\infty",
            "\\int_0^{2\\pi}",
            "a_n",
            "\\kos(nx)",
            "\\kos(mx)",
            "\\dd{x}",
            "+",
            "\\sum_{n=0}^\\infty",
            "\\int_0^{2\\pi}",
            "b_n",
            "\\sin(nx)",
            "\\kos(mx)",
            "\\dd{x}",
        ).scale_to_fit_width(config.frame_width - 2)

        self.play(formula_a_n.animate.scale_to_fit_height(formula_a_n2.height))
        self.play(TransformMatchingTex(formula_a_n, formula_a_n2))
        self.wait()

        brace1 = Brace(formula_a_n2[5:10])
        tbrace1 = (
            VGroup(
                MathTex("0\\qjika n\\neq m"),
                MathTex("\\pi\\qjika n=m\\neq 0"),
                MathTex("2\\pi\\qjika n=m=0"),
            )
            .arrange(DOWN)
            .scale(0.7)
            .next_to(brace1.get_tip(), DOWN)
        )
        brace2 = Brace(formula_a_n2[12:])
        tbrace2 = brace2.get_tex("=0").scale(0.7)

        self.play(AnimationGroup(Write(brace1), Write(tbrace1), lag_ratio=2))
        self.wait()
        self.play(
            ReplacementTransform(brace1, brace2), FadeOut(tbrace1), FadeIn(tbrace2)
        )
        self.wait()
        self.play(FadeOut(brace2, tbrace2, formula_a_n2))
        self.wait()

        long_siries = MathTex(
            "\\int_0^{2\\pi}f(x)\\kos(2x)\\dd{x}=",
            "a_1\\int_0^{2\\pi}\\kos(x)\\kos(2x)\\dd{x}+",
            "a_2\\int_0^{2\\pi}\\kos(2x)\\kos(2x)\\dd{x}+",
            "a_3\\int_0^{2\\pi}\\kos(3x)\\kos(2x)\\dd{x}+",
            "...+",
            "b_1\\int_0^{2\\pi}\\sin(x)\\kos(2x)\\dd{x}+",
            "b_2\\int_0^{2\\pi}\\sin(2x)\\kos(2x)\\dd{x}+",
            "b_3\\int_0^{2\\pi}\\sin(3x)\\kos(2x)\\dd{x}+",
            "...+",
            "a_0\\int_0^{2\\pi}\\kos(0x)\\kos(2x)\\dd{x}",
        ).to_edge(LEFT)
        decl_n = MathTex("n=2").to_edge(UP)

        self.play(
            AnimationGroup(Write(decl_n), Write(long_siries, run_time=1), lag_ratio=1)
        )

        def scroll(n=1):
            t = long_siries.copy()
            t[n].center()
            t[:n].next_to(t[n], LEFT)
            t[n + 1 :].next_to(t[n], RIGHT)
            return t

        def cross_item(n=1, m=2):
            if n != m:
                cross = Cross(long_siries[n]).center()
                an = AnimationGroup(Wait(), Create(cross), lag_ratio=1)
                long_siries[n].add(cross)
            else:
                an = Wait()
            return an

        for n in range(1, 4):
            self.play(Transform(long_siries, scroll(n)))
            self.play(cross_item(n))

        self.wait()

        for n in range(5, 8):
            self.play(Transform(long_siries, scroll(n)))
            self.play(cross_item(n))

        self.wait()

        self.play(Transform(long_siries, scroll(9)))
        self.wait()
        self.play(cross_item(9))
        self.wait()

        lsc = VGroup(
            bgn := long_siries[0].copy(),
            (end := long_siries[2].copy()).remove(end[-1]).next_to(bgn),
        ).center()

        self.play(ReplacementTransform(long_siries, lsc))
        self.wait()
        self.remove(lsc)
        lsc = MathTex(
            "\\int_0^{2\\pi}f(x)\\kos(2x)\\dd{x}",
            "=",
            "a_2",
            "\\int_0^{2\\pi}\\kos(2x)\\kos(2x)\\dd{x}",
        )
        self.add(lsc)

        self.play(
            TransformMatchingTex(
                lsc,
                lsc := MathTex(
                    "\\int_0^{2\\pi}f(x)\\kos(2x)\\dd{x}", "=", "a_2", "\\pi"
                ),
                transform_mismatches=True,
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                lsc,
                lsc := MathTex(
                    "{1\\over",
                    "\\pi",
                    "}",
                    "\\int_0^{2\\pi}f(x)\\kos(2x)\\dd{x}",
                    "=",
                    "a_2",
                ),
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                lsc,
                lsc := MathTex(
                    "a_2",
                    "=",
                    "{1\\over",
                    "\\pi",
                    "}",
                    "\\int_0^{2\\pi}f(x)\\kos(2x)\\dd{x}",
                ),
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                lsc,
                lsc := MathTex(
                    "a_n",
                    "=",
                    "{1\\over",
                    "\\pi",
                    "}",
                    "\\int_0^{2\\pi}f(x)\\kos(nx)\\dd{x}",
                ),
                transform_mismatches=True,
            )
        )
        self.wait()
        self.play(
            Write(cond := Tex("bagi $n\\ge 1$").next_to(lsc, DOWN)), Unwrite(decl_n)
        )
        lsc_cosine0 = MathTex(
            "a_0=\\frac 1{2\\pi}\\int_0^{2\\pi}f(x)", "\\kos(0x)", "\\dd{x}"
        )
        lsc.save_state()
        VGroup(lsc_cosine0, lsc).arrange(DOWN)
        lsc.restore()
        self.wait()
        self.play(
            FadeOut(cond, shift=DOWN),
            Write(lsc_cosine0),
            lsc.animate.next_to(lsc_cosine0, DOWN),
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                lsc_cosine0,
                lsc_cosine0 := MathTex(
                    "a_0=\\frac 1{2\\pi}\\int_0^{2\\pi}f(x)", "\\dd{x}"
                ).next_to(lsc, UP),
                fade_transform_mismatches=True,
            )
        )
        self.wait()

        lsc_sine = MathTex("b_n=\\frac 1\\pi\\int_0^{2\\pi}f(x)\\sin(nx)\\dd{x}")
        lsc.save_state()
        lsc_cosine0.save_state()
        VGroup(lsc_cosine0, lsc, lsc_sine).arrange(DOWN)
        lsc.restore()
        lsc_cosine0.restore()

        self.play(
            Write(lsc_sine), VGroup(lsc, lsc_cosine0).animate.next_to(lsc_sine, UP)
        )
        self.wait()


class Part1(Scene):
    def construct_(self):
        asas = VGroup(MathTex("f(x)=", "a_1", "\\kos(x)+", "b_1", "\\sin(x)+"))
        asas.add(
            *VGroup(
                *[
                    MathTex(f"a_{i}", f"\\kos({i}x)+", f"b_{i}", f"\\sin({i}x)+")
                    for i in range(2, 5)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(asas[0][1], DOWN, aligned_edge=LEFT)
        )
        asas.add(MathTex("...").next_to(asas[-1], DOWN, aligned_edge=LEFT))

        mod_1 = VGroup(MathTex("\\sin(x)=", "0", "\\kos(x)+", "1", "\\sin(x)+"))
        mod_1.add(
            *VGroup(
                *[
                    MathTex(f"0", f"\\kos({i}x)+", f"0", f"\\sin({i}x)+")
                    for i in range(2, 5)
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(mod_1[0][1], DOWN, aligned_edge=LEFT)
        )
        mod_1.add(MathTex("...").next_to(mod_1[-1], DOWN, aligned_edge=LEFT))
        [i.center() for i in [asas, mod_1]]

        self.play(Write(asas))
        self.wait()

        self.play(*[TransformMatchingTex(i, j) for i, j in zip(asas, mod_1)])
        self.wait()

        mod_2 = VGroup(MathTex("\\kos(3x)="), MathTex("1"), MathTex("0"))
        self.play(
            Scroll(mod_1[0][0], mod_2[0], aligned_edge=RIGHT),
            Scroll(mod_1[0][3], mod_2[2]),
            Scroll(mod_1[2][0], mod_2[1]),
        )
        self.wait()

        special_1 = VGroup(MathTex("-\\frac{x^2}{5}(x-5)="), Tex("?"))
        self.play(
            Scroll(mod_2[0], special_1[0], aligned_edge=RIGHT),
            Scroll(mod_1[0][1], special_1[1].copy()),
            Scroll(mod_2[2], special_1[1].copy()),
            *[
                Scroll(i[j], special_1[1].copy())
                if n != 1
                else Scroll(mod_2[1], special_1[1].copy())
                if j != 2
                else Scroll(i[j], special_1[1].copy())
                for n, i in enumerate(mod_1[1:4])
                for j in [0, 2]
            ],
        )
        self.wait()
        self.play(*(FadeOut(i) for i in self.mobjects))


class Example1(Scene):
    def construct(self):
        plane1 = Axes((0, 2 * PI, PI / 2), (-2, 2))
        x_coord = [MathTex(i) for i in ["\\pi/2", "\\pi", "3\\pi/2", "2\\pi"]]
        plane1.add_coordinates(
            dict(zip(np.arange(PI / 2, 2 * PI + PI / 2, PI / 2), x_coord))
        )
        func = lambda x: -x / 5 * (x - 5)
        main_graph = plane1.plot(func, color=YELLOW)
        main_tex = MathTex("f(x)=-\\frac x5(x-5)").to_corner(UR).set_color(YELLOW)

        self.play(
            AnimationGroup(
                Create(plane1),
                AnimationGroup(Create(main_graph), Write(main_tex)),
                lag_ratio=1,
            )
        )
        self.wait()

        iterations = 100 + 1
        A = [self.get_coeff(func, n=n) for n in range(iterations)]
        A = [A[0] / 2, *A[1:]]
        B = [self.get_coeff(func, "b", n=n) for n in range(iterations)]
        component_graphs_cosine = VGroup(
            *[plane1.plot(lambda x: A[n] * np.cos(n * x), color=BLUE) for n in range(8)]
        ).save_state()
        component_graphs_sine = VGroup(
            *[plane1.plot(lambda x: B[n] * np.sin(n * x), color=RED) for n in range(8)]
        ).save_state()
        component_graphs_cosine.scale(0.4).arrange().to_edge(LEFT)
        component_graphs_sine.scale(0.4).arrange().next_to(
            component_graphs_cosine, DOWN, aligned_edge=LEFT
        )

        self.play(
            VGroup(plane1, main_graph).animate.scale(0.4).to_edge(UP), Unwrite(main_tex)
        )
        self.play(
            *[
                ReplacementTransform(main_graph.copy(), i)
                for i in component_graphs_cosine
            ],
            *[
                ReplacementTransform(main_graph.copy(), i)
                for i in component_graphs_sine
            ],
        )
        self.wait()
        self.play(
            *[Uncreate(i) for i in component_graphs_cosine],
            *[Uncreate(i) for i in component_graphs_sine],
            VGroup(plane1, main_graph).animate.scale(1 / 0.4).move_to(ORIGIN),
        )
        component_graphs_cosine.restore()
        component_graphs_sine.restore()
        var = Variable(0, "n", Integer).to_edge(UP)
        self.play(Write(var))
        for i in range(len(component_graphs_cosine)):
            self.play(
                var.tracker.animate.set_value(i),
                Create(component_graphs_cosine[i]),
                Create(component_graphs_sine[i]),
            )
            self.wait()
            graph = plane1.plot(
                lambda x: self.get_fourier_approx(x, i, A, B), color=PURPLE
            )
            self.play(
                ReplacementTransform(component_graphs_cosine[i], graph),
                ReplacementTransform(component_graphs_sine[i], graph),
            )
            if i != len(component_graphs_cosine) - 1:
                self.play(graph.animate.set_stroke(opacity=0.2))

        self.wait()

        for i in range(len(component_graphs_cosine), iterations):
            var.tracker.set_value(i)
            graph.set_stroke(opacity=0.2)
            graph = plane1.plot(
                lambda x: self.get_fourier_approx(x, i, A, B), color=PURPLE
            )
            self.add(graph)
            self.wait(0.1)
        self.wait(2)

    def get_coeff(
        self, func: Callable[[float], float], a_b: str = "a", n: int = 1
    ) -> float:
        from sympy import integrate, sin, cos, pi
        from sympy.abc import x

        f = func(x)
        if a_b == "a":
            return float(integrate(f * cos(n * x), (x, 0, 2 * pi))) / PI
        if a_b == "b":
            return float(integrate(f * sin(n * x), (x, 0, 2 * pi))) / PI
        else:
            raise ValueError("a_b is either 'a' or 'b'")

    def get_fourier_approx(
        self, x: float, n: int, A: Sequence[float], B: Sequence[float]
    ) -> float:
        ans = 0
        for i in range(n + 1):
            ans += A[i] * np.cos(i * x) + B[i] * np.sin(i * x)
        return ans


class Extras1(Scene):
    def construct(self):
        tex1 = MathTex(
            "a_n",
            "=",
            "{1\\over",
            "\\pi",
            "}",
            "\\int_0^{",
            "2\\pi",
            "}f(x)\\kos(",
            "nx",
            ")\\dd{x}",
        )
        tex2 = MathTex(
            "a_n",
            "=",
            "{1\\over",
            "L",
            "}",
            "\\int_0^{",
            "2L",
            "}f(x)\\kos(",
            "{",
            "nx",
            "\\pi\\over L}",
            ")\\dd{x}",
        )
        self.add(tex1)
        self.wait()
        self.play(
            AnimationGroup(
                ShowPassingFlashWithThinningStrokeWidth(
                    SurroundingRectangle(tex1[6][1]), time_width=1
                ),
                AnimationGroup(
                    ShowPassingFlashWithThinningStrokeWidth(
                        SurroundingRectangle(VGroup(tex1[5][-1], tex1[6][0])),
                        time_width=1,
                    )
                ),
                lag_ratio=1,
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(tex1, tex2, key_map={"\\pi": "L", "2\\pi": "2L"})
        )
        self.wait()


class Complex1(Scene):
    def construct(self):
        teorem_euler = MathTex("z=e^{ix}=\kos(x)+i\sin(x)")
        teorem_euler.generate_target()
        teorem_euler.k = MathTex("z^*=e^{-ix}=\kos(x)-i\sin(x)")
        VGroup(teorem_euler.target, teorem_euler.k).arrange(DOWN)
        self.play(Write(teorem_euler))
        self.wait()
        self.play(MoveToTarget(teorem_euler), Write(teorem_euler.k))
        permudah = VGroup(
            MathTex("\kos(x)=\\frac{z+z^*}2"), MathTex("\sin(x)=\\frac{z-z^*}{2i}")
        ).arrange(DOWN)
        self.wait()
        self.play(Scroll(VGroup(teorem_euler, teorem_euler.k), permudah))
        self.wait()
        self.play(Unwrite(permudah))
        form1 = VGroup(
            MathTex("f(x)="),
            MathTex("\\sum_{n=0}^\\infty"),
            MathTex("a_n", "\\kos(nx)", "+"),
            MathTex("\\sum_{n=0}^\\infty"),
            MathTex("b_n", "\\sin(nx)"),
        ).arrange()
        form2 = VGroup(
            MathTex("f(x)="),
            MathTex("\\sum_{n=0}^\\infty"),
            MathTex("a_n", "{e^{inx}", "+", "e^{-inx}", "\\over 2}", "+"),
            MathTex("\\sum_{n=0}^\\infty"),
            MathTex("b_n", "{e^{inx}", "-", "e^{-inx}", "\\over 2i}"),
        ).arrange()
        self.play(Write(form1))
        self.play(
            TransformMatchingTex(form1[2], form2[2]),
            TransformMatchingTex(form1[4], form2[4]),
            ReplacementTransform(form1[:2], form2[:2]),
            ReplacementTransform(form1[3], form2[3]),
            run_time=3,
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                form2,
                MathTex("f(x)=", "\sum_{n=-\infty}^\infty", "c_n", "e^{inx}"),
                transform_mismatches=True,
                key_map={
                    "\\sum_{n=0}^\\infty": "\sum_{n=-\infty}^\infty",
                    "a_n": "c_n",
                    "b_n": "c_n",
                    "e^{inx}": "e^{inx}",
                    "e^{-inx}": "e^{inx}",
                },
            ),
            run_time=2,
        )
        self.wait()
