# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from traits.api import Constant, HasTraits, Instance

from pyface.fields.i_field import IField
from .action import Action


class TraitsUIWidgetAction(Action):
    """ A widget action containing a TraitsUI.

    If a object is supplied, then the UI is generated from the object's view,
    otherwise the ui is generated on using the Action object.

    Notes
    -----
    This is currently only supported by the Qt backend.
    """

    # TraitsUIWidgetAction traits -------------------------------------------

    #: The underlying traits model to be displayed, or None.
    object = Instance(HasTraits)

    # Action traits ---------------------------------------------------------

    #: This is a widget action.
    style = Constant("widget")

    # ------------------------------------------------------------------------
    # Action interface
    # ------------------------------------------------------------------------

    def create_control(self, parent):
        """ Called when creating a "widget" style action.

        This constructs an IField-based control directly and binds changes to
        the value to the `value_updated` method.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control, usually a toolbar.

        Returns
        -------
        control : toolkit control
            A toolkit control or None.
        """
        if self.object is not None:
            ui = self.object.edit_traits(kind='subpanel', parent=parent)
        else:
            ui = self.edit_traits(kind='subpanel', parent=parent)
        control = ui.control
        control._ui = ui
        return control

    # ------------------------------------------------------------------------
    # HasTraits interface
    # ------------------------------------------------------------------------

    def trait_context(self):
        """ Use the model object for the Traits UI context, if appropriate.
        """
        if self.object:
            context = self.model.trait_context()
            context['action'] = self
            return context
        return super(TraitsUIWidgetAction, self).trait_context()
