from manim import *
from manim_physics import *


class nirseimbangan_medan(Scene):
    def construct(self):
        c1 = Charge(add_glow=False).scale(0.3)
        c2 = Charge(-1, add_glow=False).scale(0.3)
        VGroup(c1, c2).arrange(buff=0)
        efield = always_redraw(
            lambda: ElectricField(
                c1, c2, length_func=lambda norm: 0.5 * (1 - np.exp(-0.5 * norm))
            )
        )
        self.add(efield, c1, c2)
        self.wait()
        self.play(VGroup(c1, c2).animate.arrange(buff=3))
        self.wait()


class keupayaan_demo(ThreeDScene):
    def construct(self):
        c1 = Charge(2, RIGHT * 1.5)
        c2 = Charge(-1, LEFT * 1.5)

        a0 = ParametricSurface(
            lambda u, v: np.array([u, v, 0]),
            (-5, 5),
            (-5, 5),
        )
        a = ParametricSurface(
            lambda u, v: np.array([u, v, self.surface_func(u, v, c1, c2)]),
            (-5, 5),
            (-5, 5),
            color=BLUE,
            fill_opacity=0.5,
        )
        b = ParametricFunction(
            lambda t: np.array(
                [
                    t,
                    2 * np.sin(t * PI / 3 - 1.5),
                    self.surface_func(t, 2 * np.sin(t * PI / 3 - 1.5), c1, c2),
                ]
            ),
            (1, -1),
        )
        b = b.reverse_points()
        test_ch = Dot3D(b.get_start(), color=ORANGE)

        self.add(a0)
        self.wait()
        self.move_camera(PI / 3, -3 * PI / 4, added_anims=[ReplacementTransform(a0, a)])
        self.play(GrowFromCenter(test_ch))
        self.wait()
        self.play(
            MoveAlongPath(test_ch, b),
            run_time=5,
            rate_func=lambda x: 10 / 3 * (x - 0.5) ** 3 + 0.16 * x + 0.417,
        )
        self.wait()
        self.move_camera(
            0,
            -PI / 2,
            added_anims=[
                Transform(
                    a,
                    ParametricSurface(
                        lambda u, v: np.array([u, v, 0]),
                        (-5, 5),
                        (-5, 5),
                    ),
                )
            ],
        )
        self.wait()

    def surface_func(self, u, v, *charges: Charge):
        height = 0
        for c in charges:
            dist = np.linalg.norm(c.get_center() - [u, v, 0])
            height += c.magnitude / dist ** 2
        if abs(height) > 10:
            height = 10 * height / abs(height)
        return height


class fluks_demo(ThreeDScene):
    def construct(self):
        window = Square(5, color=BLUE, fill_opacity=0.5).rotate(PI / 2, UP)
        lines = VGroup(
            *[
                Arrow(LEFT, RIGHT, stroke_width=10).shift(OUT * i + UP * j)
                for i in range(-7, 8)
                for j in range(-7, 8)
            ]
        )
        lines2 = lines.copy()
        lines2.shift(np.array([0, -1, -1]) * 0.5)
        self.set_camera_orientation(PI / 3, -PI / 4)
        self.play(GrowFromCenter(window))
        self.wait()
        self.play(*[GrowArrow(l) for l in lines])
        self.wait()
        self.move_camera(PI / 3, 0)
        self.play(*[GrowArrow(l) for l in lines2])
        self.wait()
        self.play(window.animate.scale(2))
        self.wait()
        self.play(window.animate.scale(0.5))
        self.wait()
        self.move_camera(PI / 2, -PI / 2)
        self.wait()


class fluks_demo_2d(Scene):
    def construct(self):
        ang_val = ValueTracker(0)
        a = Line(DOWN, UP, color=BLUE).scale(2.5)
        a.add_updater(
            lambda mob: mob.rotate(
                ang_val.get_value() - angle_between_vectors(a.get_vector(), UP)
            )
        )
        b = VGroup(
            *[Line(LEFT, RIGHT).scale(7).shift(UP * i) for i in np.arange(-4, 4.5, 0.5)]
        )
        for i in b:
            i.add_updater(
                lambda mob: mob.set_color(RED)
                if 2.5 * abs(np.cos(ang_val.get_value())) < abs(mob.get_center()[1])
                else mob.set_color(GREEN)
            )
            self.add(i)
        self.add(a)
        self.wait()
        self.play(ang_val.animate.set_value(3 * PI / 4), run_time=5)
        self.wait()
        normal_vect = always_redraw(
            lambda: Vector(
                2
                * np.array(
                    [-np.cos(ang_val.get_value()), -np.sin(ang_val.get_value()), 0]
                ),
                color=YELLOW,
            )
        )
        field_vect = Vector(RIGHT * 3, color=PURPLE)
        label_S = MathTex("\\va{S}", color=YELLOW).next_to(normal_vect.get_end())
        label_E = MathTex("\\va{E}", color=PURPLE).next_to(field_vect.get_end())
        self.play(
            GrowArrow(normal_vect),
            GrowArrow(field_vect),
        )
        self.wait()
        mag_brace = BraceBetweenPoints(ORIGIN, normal_vect.get_end())
        self.play(GrowFromCenter(mag_brace))
        self.wait()
        self.play(ShrinkToCenter(mag_brace))
        self.wait()
        self.play(
            Write(label_E),
            Write(label_S),
        )
        formula = MathTex(
            "\\phi_E=",
            "\\va E",
            "\\vdot",
            "\\va S",
            "=",
            "|\\va E|",
            "|\\va S|",
            "\\text{kos }\\theta",
        ).to_corner(UL)
        formula[1:].to_corner(UL)
        self.play(Write(formula[1:4]), b.animate.set_opacity(0.5))
        self.wait()
        efield_brace = Brace(field_vect, UP)
        self.play(
            Write(efield_brace),
            Write(formula[4:6]),
        )
        self.play(FadeOut(efield_brace))
        self.wait()
        proj_vect = always_redraw(
            lambda: Vector(RIGHT * normal_vect.get_end()[0], color=ORANGE)
        )
        proj_vect_label = MathTex("\\va{S'}", color=ORANGE).next_to(proj_vect, UP)
        dash = always_redraw(
            lambda: DashedLine(normal_vect.get_end(), proj_vect.get_end(), color=ORANGE)
        )
        self.play(
            Create(dash),
            ReplacementTransform(normal_vect.copy(), proj_vect),
            Write(proj_vect_label),
        )
        ang_arc = always_redraw(lambda: Angle(normal_vect, field_vect, 0.5))
        ang_arc_label = always_redraw(
            lambda: MathTex("\\theta").move_to(ang_arc.point_from_proportion(0.5) * 1.5)
        )
        self.play(Create(ang_arc), Write(ang_arc_label))
        self.play(ReplacementTransform(proj_vect_label, formula[6:]))
        self.wait()
        self.play(
            Write(formula[0]),
            formula[1:].animate.next_to(formula[0]),
        )
        self.wait()
        self.play(ang_val.animate.set_value(PI / 2), run_time=2)
        self.wait()
        self.play(ang_val.animate.set_value(PI / 4), run_time=2)
        self.wait()


class Intro(Scene):
    def construct(self):
        # Cas sama menolak
        charge_1 = Charge(5, point=RIGHT * 0.5, add_glow=False).scale(0.5)
        charge_2 = Charge(5, point=LEFT * 0.5, add_glow=False).scale(0.5)

        e_field_1 = always_redraw(
            lambda: ElectricField(charge_1, length_func=lambda x: x)
        )
        e_field_2 = always_redraw(
            lambda: ElectricField(charge_2, length_func=lambda x: x)
        )

        force_12 = always_redraw(lambda: e_field_2.get_vector(charge_1.get_center()))
        force_21 = always_redraw(lambda: e_field_1.get_vector(charge_2.get_center()))

        self.add(force_12, force_21, charge_1, charge_2)
        self.wait()
        charge_1.add_updater(e_field_2.get_nudge_updater())
        charge_2.add_updater(e_field_1.get_nudge_updater())
        self.wait(3)
        charge_1.clear_updaters()
        charge_2.clear_updaters()
        self.play(FadeOut(charge_1, charge_2, force_12, force_21))

        # Cas lain menarik
        charge_1 = Charge(5, point=RIGHT * 2.25, add_glow=False).scale(0.5)
        charge_2 = Charge(-5, point=LEFT * 2.25, add_glow=False).scale(0.5)
        charge_1.magnitude = -5

        e_field_1 = always_redraw(
            lambda: ElectricField(charge_1, length_func=lambda x: x)
        )
        e_field_2 = always_redraw(
            lambda: ElectricField(charge_2, length_func=lambda x: x)
        )

        force_12 = always_redraw(lambda: e_field_2.get_vector(charge_1.get_center()))
        force_21 = always_redraw(lambda: e_field_1.get_vector(charge_2.get_center()))

        self.add(force_12, force_21, charge_1, charge_2)
        self.wait()
        charge_1.add_updater(e_field_2.get_nudge_updater())
        charge_2.add_updater(e_field_1.get_nudge_updater())
        self.wait(3)
        charge_1.clear_updaters()
        charge_2.clear_updaters()
        self.wait()


class Coulomb(Scene):
    def construct(self):
        formula = MathTex(
            "\\va{F}=",
            "\\frac{Qq}{4\\pi\\varepsilon_0}",
            "\\frac{1}{|\\va{r}|^2}",
            "\\vu{r}",
        )

        self.play(Write(formula))
        self.wait()
        self.play(Indicate(formula[1], rate_func=there_and_back_with_pause), run_time=3)
        self.wait()
        self.play(Indicate(formula[2], rate_func=there_and_back_with_pause), run_time=3)
        self.wait()
        self.play(Indicate(formula[3], rate_func=there_and_back_with_pause), run_time=3)
        self.wait()
        self.clear()
        self.wait()
        ax = Axes((-1, 5), (-1, 5), 7, 5)
        c1 = Charge(point=ax.c2p(0, 0), add_glow=False)
        c2 = Charge(point=ax.c2p(4, 3), add_glow=False)
        pos_vec = Arrow(c1, c2, buff=0.2, color=BLUE)
        pos_vec_label = MathTex("\\va{r}", color=BLUE).next_to(pos_vec.get_center(), UP)
        unit_vec = (
            pos_vec.copy()
            .set_color(ORANGE)
            .scale(
                1 / np.linalg.norm(pos_vec.get_length()),
                about_point=pos_vec.get_start(),
            )
        )
        unit_vec_label = MathTex("\\vu{r}", color=ORANGE).next_to(
            unit_vec.get_center(), UP
        )
        self.play(*[Write(i) for i in [ax, c1, c2]])
        self.wait()
        self.play(GrowArrow(pos_vec), Write(pos_vec_label))
        self.wait()
        self.play(
            ReplacementTransform(pos_vec.copy(), unit_vec),
            ReplacementTransform(pos_vec_label.copy(), unit_vec_label),
        )
        self.play(
            VGroup(unit_vec, unit_vec_label).animate.shift(
                c2.get_center() - c1.get_center()
            )
        )
        self.wait()


class medan_definisi(Scene):
    def construct(self):
        c1 = Charge(add_glow=False)
        c2 = Charge(add_glow=False).shift(UP)
        medan = ElectricField(c1, length_func=lambda x: x * 3)
        force_vec = always_redraw(lambda: medan.get_vector(c2.get_center()))
        self.add(c1, c2)
        self.wait()
        self.play(GrowArrow(force_vec))
        self.wait()
        self.play(c2.animate.shift(RIGHT * 2), run_time=2)
        self.play(c2.animate.shift(DOWN * 2), run_time=2)
        self.play(c2.animate.move_to(LEFT * 2), run_time=3)
        self.wait()
        x_range = np.arange(medan.x_min, medan.x_max, medan.delta_x)
        y_range = np.arange(medan.y_min, medan.y_max, medan.delta_y)
        self.t = 0
        medan_pseudo = VGroup()
        from itertools import product as pd

        for x, y in pd(x_range, y_range):
            self.play(c2.animate.move_to([x, y, 0]), run_time=0.05, rate_func=linear)
            medan_pseudo += force_vec.copy()
            self.add(medan_pseudo)

        self.wait()
        self.remove(medan_pseudo)
        self.add(medan)
        self.play(Transform(medan, ElectricField(c1)))
        self.wait()
        self.clear()
        self.wait()
        formula = MathTex(
            "\\va{E}=",
            "{Q\\over",
            "4\\pi\\varepsilon_0}",
            "\\frac{1}{|\\va{r}|^2}",
            "\\vu{r}",
        )
        formula[1][0].set_color(YELLOW)
        self.play(Write(formula))
        self.wait()


class keupayaan_2d(Scene):
    def construct(self):
        c1 = Charge(2).shift(LEFT * 4)
        c2 = Charge().shift(LEFT * 2)
        medan = ElectricField(c1, length_func=lambda x: sigmoid(x))
        force = always_redraw(lambda: medan.get_vector(c2.get_center()))
        force_label = always_redraw(lambda: MathTex("\\va{F}").next_to(force))

        self.add(c1, c2)
        self.wait()
        self.play(GrowArrow(force), Write(force_label))
        c2.add_updater(medan.get_nudge_updater(3))
        self.wait(2)
        c2.clear_updaters()
        force_label.clear_updaters()

        dist = BraceBetweenPoints(LEFT * 2, c2.get_center(), UP)
        phold = c2.get_center()
        dist_label = dist.get_tex("\\va{s}")

        self.wait()
        self.play(Write(dist), Write(dist_label))

        formula = MathTex("W=", "\\va{F}", "\\cdot", "\\va{s}").to_edge(UP)

        self.wait()
        self.play(
            ReplacementTransform(force_label, formula[1]),
            ReplacementTransform(dist_label, formula[3]),
            Write(formula[0]),
            Write(formula[2]),
            FadeOut(dist),
        )
        self.wait()

        formula.add_background_rectangle()
        self.add_foreground_mobjects(formula)
        self.play(Create(medan))
        self.wait()
        work_1 = MathTex("W").add_background_rectangle().next_to(LEFT * 2, DOWN)
        work_2 = MathTex("W", ">", "W").shift(UP).add_background_rectangle()
        work_2[-1].scale(0.6)
        work_3 = (
            MathTex("W", "=", "W", "+\\Delta W").shift(UP).add_background_rectangle()
        )
        work_3[3].scale(0.6)

        self.play(medan.animate.set_opacity(0.5))
        self.play(
            c2.animate.move_to(LEFT * 2),
            FadeIn(work_1[0]),
            ReplacementTransform(formula[1][0].copy(), work_1[1]),
        )
        self.add(c3 := c2.copy(), force_copy := force.copy(), work_4 := work_1.copy())
        c2.add_updater(medan.get_nudge_updater(3))
        self.play(
            work_1.animate.next_to(phold, DOWN).scale(0.6),
            run_time=2,
            rate_func=rush_from,
        )
        c2.clear_updaters()
        self.wait()
        self.add(work_2[0], work_1[1], work_4[1])
        self.play(
            FadeOut(work_4[0]),
            FadeOut(work_1[0]),
            Write(work_2[2]),
            ReplacementTransform(work_4[1], work_2[1]),
            ReplacementTransform(work_1[1], work_2[3]),
        )
        self.remove(work_2[0])
        self.add(work_3[0], work_2[1:])
        self.play(
            Write(work_3[4]),
            ReplacementTransform(work_2[1], work_3[1]),
            ReplacementTransform(work_2[2], work_3[2]),
            ReplacementTransform(work_2[3], work_3[3]),
        )
        self.wait()
        self.play(Create(sr := SurroundingRectangle(work_3[4][1:])))
        self.wait()
        self.play(FadeOut(sr), Create(cr := Cross(work_3[4][1:])))
        volt_formula = MathTex("V=\\frac {\\Delta W}q")
        volt_formula.next_to(work_3[4], buff=2).add_background_rectangle()
        self.wait()
        self.add(volt_formula[0])
        self.play(FadeOut(cr), Write(volt_formula[1:]))
        self.wait()
        self.clear()

        self.wait()
        c4 = Charge(2, RIGHT * 1.5)
        c5 = Charge(-1, LEFT * 1.5)
        medan_2 = ElectricField(c4, c5)
        self.play(FadeIn(c4, c5))
        self.wait()
        self.play(Create(medan_2))
        self.wait()


class Slash(Line):
    def __init__(self, mobject: Mobject, color=YELLOW, **kwargs):
        start = mobject.get_critical_point(DL)
        end = mobject.get_critical_point(UR)
        super().__init__(start=start, end=end, color=color, **kwargs)


class fluks_calc(Scene):
    def construct(self):
        f0 = MathTex("\\phi_E=")
        f1 = MathTex("\\int \\va E\\cdot \\text d\\va S")
        VGroup(f0, f1).arrange().move_to(ORIGIN)
        f2 = MathTex("\\va E\\cdot\\int \\text d\\va S").next_to(
            f1, DOWN, aligned_edge=LEFT
        )
        f3 = MathTex("\\va E\\cdot \\left(4\\pi r^2\\right)").next_to(
            f1, DOWN, aligned_edge=LEFT
        )
        f4 = MathTex(
            "\\left(\\frac{Q}{4\\pi\\varepsilon_0}\\frac{1}{r^2}\\right)\\cdot \\left(4\\pi r^2\\right)"
        ).next_to(f1, DOWN, aligned_edge=LEFT)
        f5 = MathTex("\\frac{Q}{\\varepsilon_0}").next_to(f1, DOWN, aligned_edge=LEFT)

        self.play(Write(f0), Write(f1))
        self.wait()
        self.play(TransformMatchingShapes(f1.copy(), f2))
        self.wait()
        self.play(FadeOut(f1), f2.animate.next_to(f0))
        self.wait()
        self.play(TransformMatchingShapes(f2.copy(), f3, True))
        self.wait()
        self.play(FadeOut(f2), f3.animate.next_to(f0))
        self.wait()
        self.play(
            ReplacementTransform(f3[:2].copy(), f4[:12]),
            TransformMatchingShapes(f3[2:].copy(), f4[12:]),
        )
        self.wait()
        self.play(FadeOut(f3), f4.animate.next_to(f0))
        self.wait()
        self.play(
            AnimationGroup(
                Create(
                    VGroup(
                        s1 := Slash(f4[0][3:5]),
                        s2 := Slash(f4[0][14:16]),
                    )
                ),
                Create(
                    VGroup(
                        s3 := Slash(f4[0][9:11]),
                        s4 := Slash(f4[0][16:18]),
                    )
                ),
                lag_ratio=0.75,
            )
        )
        self.wait()
        self.play(FadeOut(s1, s2, s3, s4), TransformMatchingShapes(f4.copy(), f5))
        self.wait()
        self.play(FadeOut(f4), f5.animate.next_to(f0))
        self.wait()
        self.play(Indicate(f0[0][:2], rate_func=there_and_back_with_pause), run_time=3)
        self.play(Indicate(f5[0][0], rate_func=there_and_back_with_pause), run_time=3)
        self.wait()


class Extras(Scene):
    def construct(self):
        self.part1()
        self.part2()
        self.part3()
        self.part4()
        self.part5()

    def part1(self):
        elektron = Tex("(Ilustrasi Awanan Kebarangkalian\\\\Elektron)")
        self.play(Write(elektron))
        self.wait()
        self.clear()
        self.wait()

    def part2(self):
        cas1 = Charge(point=RIGHT * 1.5)
        cas2 = Charge(-1, point=LEFT * 1.5)
        label1 = Tex("negatif").next_to(cas2, DOWN)
        label2 = Tex("positif").next_to(cas1, DOWN)
        self.play(
            FadeIn(cas1, cas2),
            Write(label1),
            Write(label2),
        )
        self.wait()
        self.play(
            label1.animate(path_arc=PI / 4).next_to(cas1, DOWN),
            label2.animate(path_arc=PI / 4).next_to(cas2, DOWN),
        )
        self.wait()
        self.clear()
        self.wait()

    def part3(self):
        soalan = Tex("Cas?")
        tanda = Tex("?").scale(1.5)
        circ = Circle(color=ORANGE, fill_opacity=1)
        self.play(Write(soalan))
        self.wait()
        self.play(soalan.animate.shift(UP * 1.5), FadeIn(circ))
        self.wait()
        self.clear()
        self.wait()
        self.play(FadeIn(Charge().scale(3)))
        self.wait()
        self.play(Write(tanda.shift(UP * 1.5)))
        self.wait()
        self.play(Create(Cross(tanda)))
        self.wait()
        self.clear()
        self.wait()

    def part4(self):
        charge1 = Charge().move_to([-3.5, 0, 0])
        charge2 = Charge().move_to([3.5, 0, 0])
        medan1 = ElectricField(
            charge1,
            x_max=0,
        )
        medan2 = ElectricField(
            charge2, x_min=0.5, length_func=lambda x: sigmoid(x) * 0.25
        )
        vakum = Tex("Vakum").next_to(charge1, UP).to_edge(UP)
        vakum.add_background_rectangle()
        air = Tex("Air").next_to(charge2, UP).to_edge(UP)
        air.add_background_rectangle()
        air_medium = Square(10, color=BLUE, fill_opacity=0.3).next_to(ORIGIN, buff=0)
        air_medium.set_z_index(-2)
        air_medium.shift(DOWN * 10)
        self.play(
            FadeIn(charge1, charge2),
            Create(line := Line(UP * 4, DOWN * 4)),
            air_medium.animate.shift(UP * 10),
            FadeIn(vakum[0], air[0]),
            Write(vakum[1:]),
            Write(air[1:]),
        )
        self.wait()
        self.play(
            AnimationGroup(*[GrowArrow(i) for i in medan1]),
            AnimationGroup(*[GrowArrow(i) for i in medan2]),
        )
        self.wait()
        senang = (
            Tex("senang")
            .next_to(charge1, DOWN)
            .to_edge(DOWN)
            .add_background_rectangle()
        )
        susah = (
            Tex("susah").next_to(charge2, DOWN).to_edge(DOWN).add_background_rectangle()
        )
        self.play(FadeIn(senang[0], susah[0]), Write(senang[1:]), Write(susah[1:]))
        self.wait()
        self.clear()
        self.wait()

    def part5(self):
        ax = Axes((-1, 5), (-1, 10, 2))
        ax.add_coordinates()
        fungsi = ax.get_graph(lambda x: x * (x - 3) ** 2 + 3, color=RED)
        area = ax.get_riemann_rectangles(fungsi, [1, 3], 0.5)
        area2 = ax.get_riemann_rectangles(fungsi, [1, 3], 0.1)
        area3 = ax.get_riemann_rectangles(fungsi, [1, 3], 0.02)
        self.add(ax, fungsi)
        self.wait()
        self.play(Create(area))
        self.wait()
        self.play(ReplacementTransform(area, area2))
        self.wait()
        self.play(ReplacementTransform(area2, area3))
        self.wait()
        self.clear()
        self.wait()


class Extras3(Scene):
    def construct(self):
        self.keabadian_cas()

    def keabadian_cas(self):
        t = Tex("Keabadian Cas")
        t1 = Tex("Dicipta").shift(LEFT * 2)
        t2 = Tex("Dimusnah").shift(RIGHT * 2)

        self.play(Write(t))
        self.wait()
        self.play(t.animate.shift(UP))
        self.play(Write(t1), Write(t2))
        self.play(
            Create(Cross(t1)),
            Create(Cross(t2)),
        )
        self.wait()
