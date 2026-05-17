from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QPlainTextEdit, QTableWidget, QTableWidgetItem, QWidget

from events.utils import (
    enter_key_pressed,
    is_pushbutton,
    is_search_box,
    lmbutton_presses,
    lmbutton_releases_pb,
    mouse_enters_pb,
    mouse_leaves_pb,
)


def event_Filter(self, source: QWidget = None, event: QEvent = None) -> bool:

    if is_pushbutton(source):
        if mouse_enters_pb(event):
            source.setIcon(source.hover_icon)
        elif mouse_leaves_pb(event):
            source.setIcon(source.normal_icon)
        elif lmbutton_presses(event):
            source.setIcon(source.click_icon)
        elif lmbutton_releases_pb(event):
            source.setIcon(source.hover_icon)

    # Prüfe, ob das Ereignis von einem QTextEdit kommt
    if is_search_box(source):
        if enter_key_pressed(event):
            table = getattr(source, "table", None)
            if table is not None:
                func = getattr(source, "func", None)
                if func:
                    func(self, table=table, text_edit=source)
                    return True

    if isinstance(source, QTableWidget):
        if event.type() == QEvent.Paint:
            # print(event)

            rect = event.rect()

            row = source.rowAt(rect.bottom()) - 1
            amount_item: QTableWidgetItem = source.item(row, 3)
            if amount_item:
                count: float = float(amount_item.text())
            # print(row)

            # Prüfen, ob amount_item vorhanden ist und den Wert 0 hat
            if amount_item is None or count != 0:
                return False

            # Alle Zellen in der Zeile färben
            for column in range(source.columnCount()):
                item = source.item(row, column)
                if item:
                    source.item(row, column).setForeground(QColor("#e20000"))

            return True

    return False
