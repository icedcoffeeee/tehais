from manim import *
from manim_editor import PresentationSectionType


class FungsiMatriks(Scene):
    def construct(self):
        nplane = NumberPlane()
        nplane_ghost = NumberPlane().set_opacity(0.1)
        i_hat = Vector(color=RED)
        j_hat = Vector(UP, color=GREEN)
        mat = np.array([[2, -1], [-1, 2]])
        vec_mat = np.array([[3], [2]])
        vec = Vector([3, 2, 0], color=ORANGE)
        answer = mat @ vec_mat
        equation = (
            VGroup(
                Matrix(mat),
                Matrix(vec_mat),
                MathTex("="),
                Matrix(answer),
            )
            .arrange()
            .to_corner(UL)
        )
        equation[:2].center()
        space = VGroup(nplane, i_hat, j_hat)

        self.play(Write(equation[:2]))
        self.next_section("Pendahuluan", PresentationSectionType.NORMAL)
        self.play(
            Create(nplane_ghost),
            Create(space),
            FadeIn(bgrec := BackgroundRectangle(equation[:2].copy().to_corner(UL))),
            equation[:2].animate.to_corner(UL).scale(0.9),
        )
        self.wait()
        self.play(Create(vec))
        space.add(vec)
        self.wait()
        # Matrix.get_columns

        self.next_section("Ricihan", PresentationSectionType.NORMAL)
        self.play(
            Create(
                surround := SurroundingRectangle(VGroup(equation[0].get_columns()[0]))
            ),
            Indicate(i_hat),
        )
        self.wait()
        space.save_state()
        self.play(
            space.animate.apply_matrix(
                mat_1 := np.array([[mat[0][0], 0], [mat[1][0], 1]])
            ),
            run_time=3,
        )
        self.wait()

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(
            Transform(
                surround, SurroundingRectangle(VGroup(equation[0].get_columns()[1]))
            ),
            Indicate(j_hat),
        )
        self.wait()
        space.save_state()
        self.play(
            space.animate.apply_matrix(mat @ np.linalg.inv(mat_1)),
            run_time=3,
        )
        self.wait()

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(
            FadeIn(bgrec2 := BackgroundRectangle(equation[2:])),
            Write(equation[2:]),
            nplane_ghost.animate.set_opacity(1),
            nplane.animate.set_opacity(0.1),
        )
        self.wait()

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(
            space.animate.apply_matrix(np.linalg.inv(mat)),
            FadeOut(bgrec),
            FadeOut(bgrec2),
            Unwrite(equation),
            Uncreate(surround),
        )
        self.play(
            Uncreate(vec),
            nplane_ghost.animate.set_opacity(0.1),
            nplane.animate.set_opacity(1),
        )
        space.remove(vec)

        self.next_section("Eigenvektor")
        eig_vec_1 = Vector([1, 1, 0], color=PURPLE)
        eig_vec_2 = Vector([-1, 1, 0], color=PURPLE)

        self.play(
            ReplacementTransform(i_hat.copy(), eig_vec_1),
            ReplacementTransform(j_hat.copy(), eig_vec_2),
        )
        space.add(eig_vec_1, eig_vec_2)

        self.next_section(type=PresentationSectionType.SUB_NORMAL)

        eigen_span = VGroup(
            Line(UR * 8, DL * 8, color=PURPLE),
            Line(UL * 8, DR * 8, color=PURPLE),
        )

        self.play(
            space.animate.apply_matrix(mat),
            run_time=3,
        )
        self.play(GrowFromCenter(eigen_span))

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        eigen_equation = MathTex("A\\va v=\\lambda \\va v").to_corner(UL)
        eigen_equation[0][1:3].set_color(PURPLE)
        eigen_equation[0][5:].set_color(PURPLE)
        eigen_equation[0][4].set_color(MAROON)
        bgrec = BackgroundRectangle(eigen_equation)

        self.play(
            FadeIn(bgrec),
            Write(eigen_equation),
        )
        self.wait()
        eigen_val = VGroup(
            BraceBetweenPoints(ORIGIN, eig_vec_1.get_end(), color=MAROON),
            BraceBetweenPoints(ORIGIN, eig_vec_2.get_end(), DL, color=MAROON),
        )
        self.play(*(GrowFromCenter(i) for i in eigen_val))

        self.next_section(type=PresentationSectionType.SUB_NORMAL)

        self.play(Uncreate(eigen_val))
        self.play(space.animate.apply_matrix(np.linalg.inv(mat)))

        all_eigen_vecs = VGroup(
            *(Vector(np.array([1, 1, 0]) * i, color=PURPLE) for i in range(-5, 5)),
            *(Vector(np.array([-1, 1, 0]) * i, color=PURPLE) for i in range(-5, 5)),
        )
        all_eigen_vecs.set_z_index(-1)

        self.play(*(GrowArrow(i) for i in all_eigen_vecs))

        self.next_section(type=PresentationSectionType.SUB_NORMAL)

        self.play(
            space.animate.apply_matrix(mat),
            all_eigen_vecs.animate.apply_matrix(mat),
            run_time=3,
        )

        self.next_section(type=PresentationSectionType.SUB_NORMAL)

        self.play(
            space.animate.apply_matrix(np.linalg.inv(mat)),
            all_eigen_vecs.animate.apply_matrix(np.linalg.inv(mat)),
        )
        self.play(
            *(
                Uncreate(i)
                for i in [
                    eig_vec_1,
                    eig_vec_2,
                    all_eigen_vecs,
                    eigen_span,
                    bgrec,
                    eigen_equation,
                ]
            )
        )
        self.wait()

        self.next_section("Penentu Matriks", PresentationSectionType.NORMAL)

        det_equation = MathTex("\\det(A)", "=").to_corner(UL)
        bgrec = BackgroundRectangle(det_equation)
        self.play(
            FadeIn(bgrec),
            Write(det_equation[0]),
        )

        det_kwarg = {
            "color": YELLOW,
            "fill_opacity": 0.7,
        }
        det_init = Square(1, **det_kwarg).next_to(ORIGIN, UR, 0)
        self.play(GrowFromPoint(det_init, ORIGIN))
        space.add(det_init)

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(
            space.animate.apply_matrix(mat),
            run_time=3,
        )
        det_text = Tex("Luas").set_color(YELLOW).next_to(det_equation)
        bgrec2 = BackgroundRectangle(det_text)
        self.play(
            FadeIn(bgrec2),
            Write(det_equation[1]),
            ReplacementTransform(det_init.copy(), det_text),
        )
        bgrec.add(bgrec2)

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(FadeOut(det_init))

        ad = VGroup(
            DashedLine(i_hat.get_end(), [mat[0][0], mat[1][1], 0], color=BLUE_E),
            DashedLine(j_hat.get_end(), [mat[0][0], mat[1][1], 0], color=BLUE_E),
            ar := Polygon(
                ORIGIN,
                RIGHT * mat[0][0],
                [mat[0][0], mat[1][1], 0],
                UP * mat[1][1],
                color=BLUE_E,
                fill_opacity=det_kwarg["fill_opacity"],
            ),
            Text("+").move_to(ar),
        )
        bc = VGroup(
            DashedLine(i_hat.get_end(), [mat[0][1], mat[1][0], 0], color=RED_E),
            DashedLine(j_hat.get_end(), [mat[0][1], mat[1][0], 0], color=RED_E),
            ar := Polygon(
                ORIGIN,
                RIGHT * mat[0][1],
                [mat[0][1], mat[1][0], 0],
                UP * mat[1][0],
                color=RED_E,
                fill_opacity=det_kwarg["fill_opacity"],
            ),
            Text("-").move_to(ar),
        )
        self.play(
            *(Create(i) for i in ad[:2]),
            *(Create(i) for i in bc[:2]),
        )
        self.play(
            GrowFromPoint(ad[2], ORIGIN),
            GrowFromPoint(bc[2], ORIGIN),
        )
        self.play(Write(ad[3]), Write(bc[3]))

        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(Unwrite(ad[3]), Unwrite(bc[3]))
        self.play(*(Uncreate(i) for i in [*ad[:2], *bc[:2]]))
        self.play(
            ReplacementTransform(ad, det_init),
            ReplacementTransform(bc, det_init),
        )
        self.wait()
        self.next_section(type=PresentationSectionType.SUB_NORMAL)
        self.play(
            FadeOut(bgrec),
            FadeOut(bgrec2),
            *(Unwrite(i) for i in [det_equation, det_text]),
        )
        self.play(space.animate.apply_matrix(np.linalg.inv(mat)))
        self.remove(nplane_ghost)
        self.play(Uncreate(space))

        # self.interactive_embed()
