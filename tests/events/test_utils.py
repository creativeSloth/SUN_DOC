from types import SimpleNamespace

import pytest
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTextEdit

from events.utils import (
    enter_key_pressed,
    is_pushbutton,
    is_search_box,
    is_table,
    lmbutton_presses,
    lmbutton_releases_pb,
    mouse_enters_pb,
    mouse_leaves_pb,
)


def _ev(event_type):
    return SimpleNamespace(type=lambda: event_type)


def test_mouse_enters_pb_matches_enter_event():
    assert mouse_enters_pb(_ev(QEvent.Enter)) is True
    assert mouse_enters_pb(_ev(QEvent.Leave)) is False


def test_mouse_leaves_pb_matches_leave_event():
    assert mouse_leaves_pb(_ev(QEvent.Leave)) is True
    assert mouse_leaves_pb(_ev(QEvent.Enter)) is False


def test_lmbutton_presses_requires_press_and_left_button():
    event = SimpleNamespace(
        type=lambda: QEvent.MouseButtonPress,
        buttons=lambda: Qt.LeftButton,
    )
    assert lmbutton_presses(event) is True

    wrong_button = SimpleNamespace(
        type=lambda: QEvent.MouseButtonPress,
        buttons=lambda: Qt.RightButton,
    )
    assert lmbutton_presses(wrong_button) is False


def test_lmbutton_releases_pb_requires_release_and_left_button():
    event = SimpleNamespace(
        type=lambda: QEvent.MouseButtonRelease,
        button=lambda: Qt.LeftButton,
    )
    assert lmbutton_releases_pb(event) is True

    not_release = SimpleNamespace(
        type=lambda: QEvent.MouseButtonPress,
        button=lambda: Qt.LeftButton,
    )
    assert lmbutton_releases_pb(not_release) is False


def test_enter_key_pressed_matches_return_key():
    event = SimpleNamespace(
        type=lambda: QEvent.KeyPress,
        key=lambda: Qt.Key_Return,
    )
    assert enter_key_pressed(event) is True

    other_key = SimpleNamespace(
        type=lambda: QEvent.KeyPress,
        key=lambda: Qt.Key_Escape,
    )
    assert enter_key_pressed(other_key) is False


def test_is_pushbutton_recognises_qpushbutton(qapp):
    assert is_pushbutton(QPushButton()) is True
    assert is_pushbutton(QTextEdit()) is False


def test_is_table_recognises_qtablewidget(qapp):
    assert is_table(QTableWidget()) is True
    assert is_table(QPushButton()) is False


def test_is_search_box_requires_text_edit_type_attribute(qapp):
    text_edit = QTextEdit()
    assert is_search_box(text_edit) is False

    text_edit.text_edit_type = "search"
    assert is_search_box(text_edit) is True


def test_is_search_box_false_for_non_textedit(qapp):
    assert is_search_box(QPushButton()) is False
