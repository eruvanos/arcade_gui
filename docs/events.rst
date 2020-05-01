.. _events:

UIEvents
===========

Some of the UI Elements produce a :py:func:`arcade_gui.UIEvent <arcade_gui:arcade_gui.core.UIEvent>` when they are interacted with. These events
all follow a common structure that looks something like this:

 - **'type'** : String representing the type of the event
 - **'ui_element'** : The UIElement that fired this event.
 - **'ui_id'** : Shortcut to event.ui_element.id, could be None as the id is not a required attribute of an UIElement

Though some of the events also have additional data relevant to that event.

Event list
----------

A list of all the different events by element.

:class:`UIButton <arcade_gui.UIButton>` - MOUSE_PRESS
....................................................................

Fired when a user presses a button by left clicking on it with a mouse, and releasing the mouse button while still
hovering over it.

 - **'type'** : arcade_gui.MOUSE_PRESS
 - **'x'** : Mouse position x
 - **'y'** : Mouse position y
 - **'button'** : Mouse button
 - **'modifiers'** : Modifier keys pressed.

**Example usage**:

.. code-block:: python
   :linenos:

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == test_button:
                    print('Test button pressed')

:class:`UIButton <pygame_gui.elements.UIButton>` - UI_BUTTON_DOUBLE_CLICKED
...........................................................................

MOUSE_PRESS = 'MOUSE_PRESS'
MOUSE_RELEASE = 'MOUSE_RELEASE'
MOUSE_SCROLL = 'MOUSE_SCROLL'
MOUSE_MOTION = 'MOUSE_MOTION'
KEY_PRESS = 'KEY_PRESS'
KEY_RELEASE = 'KEY_RELEASE'

TEXT_INPUT = 'TEXT_INPUT'
TEXT_MOTION = 'TEXT_MOTION'
TEXT_MOTION_SELECTION = 'TEXT_MOTION_SELECTION'