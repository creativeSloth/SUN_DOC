import os
import re

import directories.document_helpers as helpers
from directories.constants import (
    DIRS,
    DOC_1,
    DOC_1_NAME,
    DOC_2,
    DOC_2_NAME,
    SOURCE,
    TARGET_1,
    TARGET_2,
    TEMPLATE_1,
)


class _FakeUi:
    def __init__(self, project_name):
        self._project = project_name

    class _Project:
        def __init__(self, text):
            self._text = text

        def toPlainText(self):
            return self._text

    @property
    def project(self):
        return self._Project(self._project)


class _FakeSelf:
    def __init__(self, project_name):
        self.ui = _FakeUi(project_name)


def test_get_docs_paths_uses_target_2_and_embeds_template_names(reset_dirs):
    reset_dirs.paths[TARGET_2] = "/tmp/store"
    doc_1, doc_2 = helpers.get_docs_paths(project="MRS 19-001")

    assert doc_1.startswith("/tmp/store")
    assert DOC_1_NAME in doc_1
    assert "MRS 19-001" in doc_1
    assert doc_1.endswith(".odt")

    assert DOC_2_NAME in doc_2
    assert doc_2.endswith(".odt")


def test_get_docs_paths_includes_timestamp(reset_dirs):
    reset_dirs.paths[TARGET_2] = "/tmp/store"
    doc_1, _ = helpers.get_docs_paths(project="X")
    # timestamp pattern YYYYMMDDHHMMSS appears between dashes
    assert re.search(r"\d{14}", os.path.basename(doc_1)) is not None


def test_set_doc_1_dir_writes_into_DIRS(reset_dirs):
    reset_dirs.paths[TARGET_2] = "/tmp/store"
    helpers.set_doc_1_dir(_FakeSelf("Proj-A"))
    assert reset_dirs.paths[DOC_1].startswith("/tmp/store")
    assert "Proj-A" in reset_dirs.paths[DOC_1]


def test_set_doc_2_dir_writes_into_DIRS(reset_dirs):
    reset_dirs.paths[TARGET_2] = "/tmp/store"
    helpers.set_doc_2_dir(_FakeSelf("Proj-B"))
    assert reset_dirs.paths[DOC_2].startswith("/tmp/store")
    assert "Proj-B" in reset_dirs.paths[DOC_2]


def test_set_source_dir_updates_DIRS(reset_dirs):
    helpers.set_source_dir("/data/source")
    assert reset_dirs.paths[SOURCE] == "/data/source"


def test_set_target_1_dir_updates_DIRS(reset_dirs):
    helpers.set_target_1_dir("/data/target1")
    assert reset_dirs.paths[TARGET_1] == "/data/target1"


def test_set_target_2_dir_updates_DIRS(reset_dirs):
    helpers.set_target_2_dir("/data/target2")
    assert reset_dirs.paths[TARGET_2] == "/data/target2"


def test_set_template_dir_writes_to_provided_key(reset_dirs):
    helpers.set_template_dir(TEMPLATE_1, "/data/templates/t1.odt")
    assert DIRS.paths[TEMPLATE_1] == "/data/templates/t1.odt"
