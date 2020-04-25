# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Qt-specific implementation of the text field class """


from traits.api import Trait, provides

from pyface.fields.i_text_field import ITextField, MTextField
from pyface.qt.QtCore import Qt
from pyface.qt.QtGui import QLineEdit
from .field import Field


ECHO_TO_QT_ECHO_MODE = {
    "normal": QLineEdit.Normal,
    "password": QLineEdit.Password,
    "none": QLineEdit.NoEcho,
    "when_editing": QLineEdit.PasswordEchoOnEdit,
}
QT_ECHO_MODE_TO_ECHO = {
    value: key for key, value in ECHO_TO_QT_ECHO_MODE.items()
}

# mapped trait for Qt line edit echo modes
Echo = Trait("normal", ECHO_TO_QT_ECHO_MODE)

ALIGNMENT_TO_QALIGNMENT = {
    "default": Qt.AlignLeft | Qt.AlignVCenter,
    "left": Qt.AlignLeft | Qt.AlignVCenter,
    "center": Qt.AlignHCenter | Qt.AlignVCenter,
    "right": Qt.AlignRight | Qt.AlignVCenter,
}
QALIGNMENT_TO_ALIGNMENT = {
    0: "default",
    Qt.AlignLeft: "left",
    Qt.AlignHCenter: "center",
    Qt.AlignRight: "right",
}
ALIGNMENT_MASK = Qt.AlignLeft | Qt.AlignHCenter | Qt.AlignRight


@provides(ITextField)
class TextField(MTextField, Field):
    """ The Qt-specific implementation of the text field class """

    #: Display typed text, or one of several hidden "password" modes.
    echo = Echo

    # ------------------------------------------------------------------------
    # IWidget interface
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create the toolkit-specific control that represents the widget. """
        control = QLineEdit(parent)
        return control

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    def _get_control_value(self):
        """ Toolkit specific method to get the control's value. """
        return self.control.text()

    def _set_control_value(self, value):
        """ Toolkit specific method to set the control's value. """
        self.control.setText(value)
        # fire update
        if self.update_text == "editing_finished":
            self.control.editingFinished.emit()
        else:
            self.control.textEdited.emit(value)

    def _observe_control_value(self, remove=False):
        """ Toolkit specific method to change the control value observer. """
        if remove:
            self.control.textEdited.disconnect(self._update_value)
        else:
            self.control.textEdited.connect(self._update_value)

    def _get_control_placeholder(self):
        """ Toolkit specific method to set the control's placeholder. """
        return self.control.placeholderText()

    def _set_control_placeholder(self, placeholder):
        """ Toolkit specific method to set the control's placeholder. """
        self.control.setPlaceholderText(placeholder)

    def _get_control_echo(self):
        """ Toolkit specific method to get the control's echo. """
        return QT_ECHO_MODE_TO_ECHO[self.control.echoMode()]

    def _set_control_echo(self, echo):
        """ Toolkit specific method to set the control's echo. """
        self.control.setEchoMode(ECHO_TO_QT_ECHO_MODE[echo])

    def _get_control_read_only(self):
        """ Toolkit specific method to get the control's read_only state. """
        return self.control.isReadOnly()

    def _set_control_read_only(self, read_only):
        """ Toolkit specific method to set the control's read_only state. """
        self.control.setReadOnly(read_only)

    def _get_control_alignment(self):
        """ Toolkit specific method to get the control's read_only state. """
        alignment = int(self.control.alignment() & ALIGNMENT_MASK)
        return QALIGNMENT_TO_ALIGNMENT[alignment]

    def _set_control_alignment(self, alignment):
        """ Toolkit specific method to set the control's read_only state. """
        self.control.setAlignment(ALIGNMENT_TO_QALIGNMENT[alignment])

    def _observe_control_editing_finished(self, remove=False):
        """ Change observation of whether editing is finished. """
        if remove:
            self.control.editingFinished.disconnect(self._editing_finished)
        else:
            self.control.editingFinished.connect(self._editing_finished)
