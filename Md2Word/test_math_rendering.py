import unittest
from docx import Document
from docx.oxml.ns import qn
import build_report


class MathRenderingTests(unittest.TestCase):
    def test_inline_latex_becomes_native_omml(self):
        doc = Document()
        paragraph = doc.add_paragraph()
        build_report.add_inline(paragraph, r"Pearson $r_{ij}$ correlation", {})
        math_nodes = list(paragraph._p.iter(qn('m:oMath')))
        self.assertEqual(len(math_nodes), 1)
        self.assertIn('Pearson ', paragraph.text)
        self.assertIn(' correlation', paragraph.text)

    def test_fraction_and_sum_convert_to_omml(self):
        doc = Document()
        paragraph = doc.add_paragraph()
        build_report.add_math(paragraph, r"\frac{\sum_i x_i}{n}")
        self.assertEqual(len(list(paragraph._p.iter(qn('m:oMath')))), 1)

    def test_invalid_latex_raises_clear_error(self):
        doc = Document()
        with self.assertRaisesRegex(ValueError, "Không chuyển đổi được công thức LaTeX"):
            build_report.add_math(doc.add_paragraph(), r"\notAValidCommand{abc}")


if __name__ == '__main__':
    unittest.main()
