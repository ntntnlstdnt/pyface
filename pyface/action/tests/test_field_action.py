# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from pyface.fields.api import ComboField, SpinField, TextField
from pyface.gui import GUI
from pyface.window import Window
from pyface.util.gui_test_assistant import GuiTestAssistant
from ..field_action import FieldAction


class TestFieldAction(GuiTestAssistant, unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.parent = Window()
        self.parent._create()

    def tearDown(self):
        self.parent.destroy()
        self.gui.process_events()
        del self.parent
        super().tearDown()

    def test_combo_field_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform(value):
            memo.append(value)

        action = FieldAction(
            name="Dummy",
            field_type=ComboField,
            field_defaults={
                "values": ["a", "b", "c"],
                "value": "a",
                "tooltip": "Dummy",
            },
            on_perform=perform,
        )
        control = action.create_control(self.parent.control)
        try:
            self.gui.process_events()

            control._field.value = "b"
            self.gui.process_events()

            self.assertEqual(memo, ["b"])
        finally:
            control._field.destroy()
            self.gui.process_events()

    def test_text_field_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform(value):
            memo.append(value)

        action = FieldAction(
            name="Dummy",
            field_type=TextField,
            field_defaults={"value": "a", "tooltip": "Dummy"},
            on_perform=perform,
        )
        control = action.create_control(self.parent.control)

        try:
            self.gui.process_events()

            control._field.value = "b"
            self.gui.process_events()

            self.assertEqual(memo, ["b"])
        finally:
            control._field.destroy()
            self.gui.process_events()

    def test_spin_field_action(self):
        # test whether function is called by updating list
        # XXX should really use mock
        memo = []

        def perform(value):
            memo.append(value)

        action = FieldAction(
            name="Dummy",
            field_type=SpinField,
            field_defaults={
                "value": 1,
                "bounds": (0, 100),
                "tooltip": "Dummy",
            },
            on_perform=perform,
        )
        control = action.create_control(self.parent.control)

        try:
            self.gui.process_events()

            control._field.value = 5
            self.gui.process_events()

            self.assertEqual(memo, [5])
        finally:
            control._field.destroy()
            self.gui.process_events()
