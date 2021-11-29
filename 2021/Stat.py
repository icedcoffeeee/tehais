from manim import *
import random as rn


class Mean(Scene):
    def construct(self):
        bg = NumberPlane().set_opacity(0.1)
        base = Line([-5, 0, 0], [5, 0, 0])
        COG = (
            Triangle(color=WHITE, fill_opacity=1)
            .scale(0.4)
            .next_to(base, DOWN, buff=0.1)
        )
        weight = Dot(color=BLUE).scale(2).next_to(ORIGIN, UP, buff=0.1)
        force = Arrow(
            weight.get_center(),
            weight.get_center() + DOWN,
            color=RED,
        )
        weights = VGroup()
        forces = VGroup()
        data = [0, 1, -2, 4.5, -3.5, 2.8]
        data_weights = [1, 3, 1, 1, 2, 4]
        nom_purata = (
            Variable(COG.get_center()[0], "\\overline{x}").scale(0.7).to_corner(UL)
        )
        nom_purata.value.add_updater(lambda p: p.set_value(COG.get_center()[0]))

        self.play(Create(bg), Create(base), Create(force), Create(COG))
        self.wait()
        self.play(GrowFromCenter(weight))
        self.wait()
        self.play(Write(nom_purata))
        self.wait()
        for i in range(1, len(data)):
            self.play(
                GrowFromCenter(
                    weight2 := weight.copy()
                    .scale(data_weights[i])
                    .next_to(RIGHT * (data[i]), UP, buff=0.1)
                ),
                GrowArrow(
                    force2 := force.copy()
                    .scale(np.abs(data_weights[i]), about_point=ORIGIN)
                    .shift(RIGHT * (data[i]))
                ),
                COG.animate.next_to(
                    [
                        np.average(data[0 : i + 1], weights=data_weights[0 : i + 1]),
                        0,
                        0,
                    ],
                    DOWN,
                    buff=0.1,
                ),
            )
            self.wait(max([0.5, min([1, 2 - i])]))
            weights += weight2
            forces += force2
        self.wait(1.5)


class Var(GraphScene):  # kelas GraphScene dibuang menjelang manim v0.10.0
    Square_Dict = {"color": BLUE, "stroke_opacity": 0, "fill_opacity": 0.4}

    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            x_min=0,
            x_max=11,
            x_axis_label="$n$",
            x_labeled_nums=range(11),
            y_min=0,
            y_max=11,
            y_axis_label="$x_n$",
            y_labeled_nums=range(11),
            **kwargs,
        )

    def construct(self):
        self.setup_axes(animate=True)
        self.wait()
        data = []
        dots = VGroup()
        rn.seed(30)
        for i in range(10):
            data.append([i + 1, rn.random() * 10])
        for x, y in data:
            dots += Dot(self.coords_to_point(x, y))
        self.play(Create(d := Dot()))
        self.play(
            AnimationGroup(
                *[ReplacementTransform(d.copy(), dots[i]) for i in range(9)],
                ReplacementTransform(d, dots[-1]),
                lag_ratio=0.2,
                run_time=1,
            ),
        )
        self.wait()
        meanline = Line(
            self.coords_to_point(-1, mean := np.average([i[1] for i in data])),
            self.coords_to_point(11, np.average([i[1] for i in data])),
            color=YELLOW,
        )
        meanline_label = MathTex("\\overline{x}", color=YELLOW).next_to(meanline, LEFT)
        self.play(
            AnimationGroup(
                Create(meanline),
                Write(meanline_label),
                lag_ratio=1,
            )
        )
        self.wait()
        varlines = VGroup()
        for i in range(10):
            varlines += DashedLine(
                dots[i].get_center(),
                self.coords_to_point(i + 1, mean),
                color=BLUE,
            )
        self.play(Create(varlines))
        self.wait()
        varsquares = VGroup()
        growvarsquares = []
        for i in range(len(varlines)):
            varsquares += Square(varlines[i].get_length(), **self.Square_Dict)
            if dots[i].get_y() > meanline.get_y():
                varsquares[i].next_to(dots[i].get_center(), DL, buff=0)
                growvarsquares.append(GrowFromEdge(varsquares[i], UR))
            else:
                varsquares[i].next_to(dots[i].get_center(), UL, buff=0)
                growvarsquares.append(GrowFromEdge(varsquares[i], DR))
        self.play(AnimationGroup(*growvarsquares, lag_ratio=0.2))
        self.wait()
        variance = np.average(
            [
                (varlines[i].get_length() / self.space_unit_to_y) ** 2
                for i in range(len(varlines))
            ]
        )
        bigvarsquare = Square(
            ((variance * 10) ** 0.5) * self.space_unit_to_y, **self.Square_Dict
        )
        self.play(
            FadeOut(self.axes),
            FadeOut(VGroup(meanline, meanline_label, dots, varlines)),
            ReplacementTransform(varsquares, bigvarsquare),
        )
        self.wait()
        smallvarsquares = VGroup()
        for i in range(10):
            smallvarsquares += Rectangle(
                height=bigvarsquare.side_length / 5,
                width=bigvarsquare.side_length / 2,
                **self.Square_Dict,
            )
        smallvarsquares.arrange_in_grid(5, 2, buff=0)
        self.remove(bigvarsquare)
        self.add(smallvarsquares)
        self.play(
            *[
                smallvarsquares[i].animate.shift(smallvarsquares[i].get_center() * 0.1)
                for i in range(10)
            ]
        )
        self.wait()
        smallvarsquare = smallvarsquares[4]
        smallvarsquares -= smallvarsquares[4]
        self.play(
            AnimationGroup(
                FadeOut(smallvarsquares),
                Transform(
                    smallvarsquare,
                    Square(
                        (smallvarsquare.height * smallvarsquare.width) ** 0.5,
                        **self.Square_Dict,
                    ),
                ),
                lag_ratio=1,
            )
        )
        self.wait()
        self.play(smallvarsquare.animate.shift(LEFT))
        t1 = Tex("Luas = ", "Varians").set_color_by_tex("V", YELLOW)
        t1.next_to(smallvarsquare, RIGHT)
        sdbrace = Brace(smallvarsquare)
        t2 = sdbrace.get_tex("\\text{Sisihan Piawai}").set_color_by_tex("s", YELLOW)
        self.play(AnimationGroup(Write(t1), Write(VGroup(t2, sdbrace)), lag_ratio=2))
        self.wait()


"""
class Norm(Scene):
    def construct(self):
        ax1 = Axes(
            x_range=[-4,4,0.5],
            x_axis_config={
                "include_numbers":True,
                "decimal_number_config" : {
                    "num_decimal_places" : 1
                }
            },
            y_range=[0,0.5,0.1],
            y_axis_config={
                "include_numbers":True,
                "decimal_number_config" : {
                    "num_decimal_places" : 1
                }
            },
            )\
                .shift(UP*0.5)
        ax2 = Axes(
            x_range=[4,12],
            x_axis_config={
                "include_numbers":True,
            }
            )
        ax3 = ax2.get_axis(0).next_to(ax1.c2p(0,0),DOWN,buff=1)
        label1 = ax1.get_axis_label("Z",ax1.get_axis(0),RIGHT,UR+UP*3)
        label2 = ax2.get_axis_label("X",ax2.get_axis(0),RIGHT,UR+UP*3)
        normgr = ax1.get_graph(lambda x:(1/(2*PI)**0.5)*np.exp(-0.5*x**2))\
            .set_color(YELLOW)
        # prob = ax1.get_area
        self.add(
            ax1,ax3,normgr,label1,label2
            )
"""


class Intro(Scene):
    def construct(self):
        t1 = Tex("Memahami ", "Statistik").set_color_by_tex("S", YELLOW)
        t2 = BulletedList("Purata", "Varians", "Sisihan Piawai", "Z-Skor").shift(LEFT)
        self.play(Write(t1))
        self.wait(2)
        self.play(t1.animate.to_edge(UP))
        self.wait(2)
        self.play(Write(t2[0]))
        self.wait(2)
        self.play(Write(t2[1]))
        self.play(Write(t2[2]))
        self.wait(2)
        self.play(Write(t2[3]))
        self.wait(2)
        self.play(Create(box := SurroundingRectangle(t2[0])))
        self.wait(2)
        self.play(
            Create(
                box2 := VGroup(
                    SurroundingRectangle(t2[1]),
                    SurroundingRectangle(t2[2]),
                )
            ),
            FadeOut(box),
        )
        self.wait(2)
        self.play(Create(box := SurroundingRectangle(t2[3])), FadeOut(box2))
        self.wait(2)
        self.play(FadeOut(box))
        self.wait(2)
        self.clear()
        self.wait()
        set_purata = Tex("data\\\\= \\{0,1,1,1,-2,4.5,-3.5,-3.5,2.8,2.8,2.8,2.8\\}")

        self.play(Write(set_purata))
        self.wait()
        self.play(
            Create(
                box := SurroundingRectangle(set_purata[0][8:13]),
            )
        )
        self.wait(2)
        self.clear()

        formula_ave = MathTex(
            "\\overline{x}={\\sum_{i=1}^{N} {x_i\\cdot w_i}\\over\\sum_{i=1}^{N} {w_i}}"
        )
        formula_var = MathTex(
            "\\sigma",
            "^2",
            "=",
            "{\\sum_{i=1}^{N}\\left(x_i-\\overline{x}\\right)^2\\over N}",
            "}",
        )
        formula_sis = MathTex(
            "\\sigma",
            "=",
            "\\sqrt{",
            "{\\sum_{i=1}^{N}\\left(x_i-\\overline{x}\\right)^2\\over N}",
            "}",
        )
        formula_z = MathTex("Z={X-\\mu\\over\\sigma}")

        self.play(Write(formula_ave))
        self.wait(2)
        self.play(FadeOut(formula_ave))
        self.wait()
        self.play(Write(formula_var))
        self.wait(2)
        self.play(
            TransformMatchingTex(
                formula_var, formula_sis, key_map={"^2": "\\sqrt{"}, path_arc=PI / 2
            ),
        )
        self.wait(2)
        self.play(FadeOut(formula_sis))
        self.wait()
        self.play(Write(formula_z))
        self.wait(2)
        self.play(FadeOut(formula_z))
        self.wait()
