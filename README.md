[![Build Status](https://travis-ci.org/eruvanos/arcade_gui.svg?branch=master)](https://travis-ci.org/eruvanos/arcade_gui)

# GUI Library for Python Arcade

This library contained a first draft of GUI components for arcade game library.
These components are now fully integrated into python arcade.

# Experimental GUI Components

Starting with the version `0.2.0` all components that are included
in arcade will be removed.

Starting with version `0.2.0` this library will
contain experimental components, that could move into the arcade standard. 
Consider them as alpha, so breaking changes could happen in every version update.  


## Basic Components until version `0.1.0`

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

![Example with ID Screenshot](https://github.com/eruvanos/arcade_gui/blob/master/docs/assets/ProGramer.png)


## Features planned to work on

* [ ] Enhancements
    * [ ] layered UI
* [ ] Layout
    * [ ] Modal 
        * [ ] open 
        * [ ] close 
        * [ ] colour background 
        * [ ] image background 
* [ ] New Components
    * [ ] UITextArea
    * [ ] Scrollbar

### Chores

* [ ] 

## Background information and other frameworks

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
