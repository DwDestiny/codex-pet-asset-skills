import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


repo_root = Path(__file__).resolve().parents[1]


class effect_artifact_tests(unittest.TestCase):
    def test_sample_pptx_has_multiple_editable_slides(self):
        pptx_path = (
            repo_root
            / "demos"
            / "visual-ppt-deck-builder"
            / "sample-visual-ppt-deck.pptx"
        )
        self.assertTrue(pptx_path.is_file())
        with zipfile.ZipFile(pptx_path) as pptx_zip:
            entries = pptx_zip.namelist()
            slide_entries = [
                entry
                for entry in entries
                if entry.startswith("ppt/slides/slide") and entry.endswith(".xml")
            ]
            media_entries = [entry for entry in entries if entry.startswith("ppt/media/")]
            self.assertGreaterEqual(len(slide_entries), 5)
            self.assertGreaterEqual(len(media_entries), 1)

            slide_xml = "\n".join(
                pptx_zip.read(entry).decode("utf-8", errors="ignore")
                for entry in slide_entries
            )
            self.assertIn("<a:t>", slide_xml)
            self.assertIn("<p:sp>", slide_xml)
            self.assertLess(slide_xml.count("<p:pic>"), 6)

    def test_sample_spec_slide_count_matches_pptx(self):
        spec_path = (
            repo_root
            / "demos"
            / "visual-ppt-deck-builder"
            / "sample-deck-spec.json"
        )
        pptx_path = (
            repo_root
            / "demos"
            / "visual-ppt-deck-builder"
            / "sample-visual-ppt-deck.pptx"
        )
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        with zipfile.ZipFile(pptx_path) as pptx_zip:
            slide_entries = [
                entry
                for entry in pptx_zip.namelist()
                if entry.startswith("ppt/slides/slide") and entry.endswith(".xml")
            ]
        self.assertEqual(len(slide_entries), len(spec["slides"]))

    def test_title_slide_text_does_not_span_into_visual_panel(self):
        helper_path = (
            repo_root
            / "skills"
            / "visual-ppt-deck-builder"
            / "scripts"
            / "build_visual_pptx.js"
        )
        content = helper_path.read_text(encoding="utf-8")
        self.assertIn("w: 6.75", content)
        self.assertNotIn("w: 10.9", content)

    def test_quicklook_can_render_sample_pptx_thumbnail(self):
        qlmanage = Path("/usr/bin/qlmanage")
        if not qlmanage.is_file():
            self.skipTest("qlmanage is not available on this machine")

        pptx_path = (
            repo_root
            / "demos"
            / "visual-ppt-deck-builder"
            / "sample-visual-ppt-deck.pptx"
        )
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = subprocess.run(
                [
                    str(qlmanage),
                    "-t",
                    "-s",
                    "1000",
                    "-o",
                    tmp_dir,
                    str(pptx_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            thumbnails = list(Path(tmp_dir).glob("*.png"))
            self.assertTrue(thumbnails)
            self.assertGreater(thumbnails[0].stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
