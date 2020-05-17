[![Build Status](https://travis-ci.org/eruvanos/arcade_gui.svg?branch=master)](https://travis-ci.org/eruvanos/arcade_gui)
[![Documentation Status](https://readthedocs.org/projects/arcade-gui/badge/?version=latest)](https://arcade-gui.readthedocs.io/en/latest/?badge=latest)

# GUI Library for Python Arcade

This project targets to offer simple to complex ui elements
to use in games and software written with the Python Arcade library.

Some UI components were copied over to adjust and fix them.

This project could also end up in a PR to integrate within Arcade.

## The vision - WIP

ArcadeGui enables you to build this UI in 15 minutes:
![Kenney 1 - UI Base Pack](docs\_static\UIBasePackPreview.png)


## Basic Components

#### UIView
Central class to manager the ui components.
Converts `on_` callback functions into events, so that UIElements
just have to contain one method to interact with user input.

#### UIElement
A general interface of an UI element.

## Examples

Examples providing an overview of features, there will be dedicated documentation soon.

* [UILabel](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uilabel.py)
* [UIButton](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uibutton.py)
* [UIInputBox](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_uiinputbox.py)
* [Example with ID](https://github.com/eruvanos/arcade_gui/blob/master/examples/show_id_example.py)

### Screenshots

![Example with ID Screenshot](https://github.com/eruvanos/arcade_gui/blob/master/docs/_static/ProGramer.png)


## Features for first release

* [x] UILabel
    * [x] Align with UITextBox
* [x] UIButton
* [x] Focused element tracked
* [x] ID reference system for UIElements
* [x] CI/CD
* [x] UITextBox
    * [x] Basic setup
    * [x] Emit event on ENTER
    * [ ] Scroll text with cursor
    * [ ] Set max length
* [x] UIElements emit own UIEvents
    * [x] UIButton
    * [x] UITextInput
* [x] FlatButtons (https://codepen.io/maziarzamani/full/YXgvjv)
* [x] UIImageButton
* [ ] UITexturedInputBox (maybe include in UIInputBox)
* [ ] Theme support
    * [x] Load style from yaml
    * [x] Parse arcade.color, hex and rgb
    * [x] Introduce style classes
    * [x] Style attributes can be set as global fallback under class `globals`
    * [x] Use UIElement.id to lookup special style data
    * [ ] Use UIStyle in UIElements
      * [x] UI3DButton
      * [x] FlatButton
      * [x] GhostFlatButton
      * [x] UILabel
      * [x] UIInputBox
      * [ ] UIImageButton (images)
      * [ ] Read font attributes from style
    * [ ] Provide different color styles
    * [x] Overwrite properties on UIElement 
* [ ] Add documentation and doc strings (sphinx)
    * [x] release notes
    * [x] setup sphinx
    * [ ] choose a sphinx theme
    * [ ] setup readthedocs
    * [ ] Document features
      * [ ] Quickstart
      * [ ] Interactions with ids 
      * [ ] Styles
      * [ ] Style with id and classes
      * [ ] Implement own components
* [ ] track new features and issues in Github

## Features for later

* [ ] Add hierarchy for ui_elements 
* [ ] style classes can have effect on child elements
* [ ] live refresh of loaded image
* [ ] New UIElements
  * [ ] UITextArea
  * [ ] UIContainer supporting automatic positioning (row & column) 
* [ ] Layouting in general


### Chores

* [ ] improve docs
    * [x] fix reference to examples
    * [x] include screenshots (at least one)
* [x] support Python 3.7
* [x] test examples render the expected screen
* [x] separate button functionality from appearance 
* [x] move theme resolve logic into UIElement (now called `.parent_style()`) 
* [x] make 3D Button more realistic, or change to flat buttons
* [x] harmonize constructors `x, y` vs `center_x, center_y`
* [ ] fix hitbox of FlatButtons 
* [ ] add example for custom styles for all elements (perfect for test coverage)
* [ ] figure out, how `UIView.find_by_id` does not produce typing warnings

### Thoughts on themes (now called style)

* UIView should hold a UIStyle that is used by all components, added to this view
* UIElements have a _style attribute to overwrite style properties
* Maybe supporting a hierarchy would be nice 

## Background information and other frameworks

## Decisions

* UIView is central component
* One UIStyle object per UIView  
  seems to be easier to implement a live refresh later
* UIStyle information can be loaded from file or set programmatically
* Themes vs Style  
  talking to my younger brother gave me the impression, that 'style' or 'design' are more understandable then 'theme'
* Events vs o 'on_'-callbacks  
  Implementing new UIElements is way easier (less typing) if there is a central on_event method.  
  Furthermore subclassing of UIElements to add custom actions like butten is pressed feels not as easy as it should be,
  an alternative could have been a signal/slot mechanism like in QT


### Reference Pygame GUI projects

[Overview](https://www.pygame.org/wiki/gui)

* ThorPy
    * http://www.thorpy.org/index.html
* Phil's pyGame Utilities
    * https://www.pygame.org/project/108
* OcempGUI
    * https://www.pygame.org/project/125
* PyGVisuals
    * https://github.com/Impelon/PyGVisuals
* Pygame GUI
    * [Homepage](https://github.com/MyreMylar/pygame_gui)
    * [Examples](https://github.com/MyreMylar/pygame_gui_examples)
    * [QuickStart Example](https://github.com/MyreMylar/pygame_gui_examples/blob/master/quick_start.py)
    * Concept
        * UIManager manages every interaction, new elements get the UIManager on creation
        * Elements create events and hook into pygames event system
        * Themes can be read from JSON files
* CSS Layout Engine: [Colosseum](https://colosseum.readthedocs.io/en/latest/index.html)
* Tkinter Geometry Manager: [doc](https://effbot.org/tkinterbook/pack.htm)