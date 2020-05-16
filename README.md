[![Build Status](https://travis-ci.org/eruvanos/arcade_gui.svg?branch=master)](https://travis-ci.org/eruvanos/arcade_gui)

# GUI Library for Python Arcade

This project targets to offer simple to complex ui elements
to use in games and software written with the Python Arcade library.

Some UI components were copied over to adjust and fix them.

This project could also end up in a PR to integrate within Arcade.

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
    * [x] Align with UITextInput
* [x] UIButton
* [x] Focused element tracked
* [x] ID reference system for UIElements
* [x] CI/CD
* [x] UITextInput
    * [x] Basic setup
    * [x] Emit event on ENTER
    * [ ] Scroll text with cursor
    * [ ] Set max length
* [x] UIElements emit own UIEvents
    * [x] UIButton
    * [x] UITextInput
* [x] FlatButtons (https://codepen.io/maziarzamani/full/YXgvjv)
* [ ] UIImageButton
* [ ] UITexturedInputBox

* [ ] Theme support
    * [x] Load theme from yaml
    * [x] Parse arcade.color, hex and rgb
    * [x] Introduce style classes
    * [ ] Use UIElement.id to lookup special theme data
    * [ ] Use UIStyle in UIElements
      * [ ] UI3DButton
      * [x] FlatButton
      * [x] GhostFlatButton
      * [ ] Label
      * [ ] UIInputBox
    * [ ] Provide different color themes
    * [ ] Overwrite properties on UIElement 
    * [ ] Document features
      * [ ] Quickstart
      * [ ] Interactions with ids 
      * [ ] Styles
      * [ ] Style with id and classes
      * [ ] Implement own components
* [ ] Add documentation and doc strings (sphinx)
    * [x] release notes
    * [x] setup sphinx
    * [ ] choose a sphinx theme
    * [ ] setup readthedocs
* [ ] track new features and issues in Github

## Features for later

* [ ] Add hierarchy for ui_elements 
* [ ] style classes can have effect on child elements
* [ ] live refresh of loaded image
* [ ] New UIElements
  * [ ] UITextArea
  * [ ] UIContainer supporting automatic positioning (row & column) 


### Chores

* [ ] harmonize constructors `x, y` vs `center_x, center_y`
* [ ] figure out, how `UIView.find_by_id` does not produce typing warnings
* [ ] improve docs
    * [x] fix reference to examples
    * [x] include screenshots (at least one)
* [ ] make 3D Button more realistic, or change to flat buttons
* [x] support Python 3.7
* [x] test examples render the expected screen
* [x] separate button functionality from appearance 
* [ ] fix hitbox of FlatButtons 
* [x] move theme resolve logic into UIElement (now called `.parent_style()`) 

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
