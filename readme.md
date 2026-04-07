# NVDA Layered Commands

* Author: Matthew Duffell-Hoffman

This NVDA add-on implements a layered command interface to give alternative access to many NVDA keystrokes. The purpose of this add-on is to ease the transition from JAWS, providing access to keystrokes JAWS users are more familiar with.

## Usage

Pressing NVDA + alt + space activates layered command mode. A beep is played on activation.
The activation keystroke can be configured in the Input category of Input Gestures

While in layered command mode, press one of the following keystrokes to perform the action. Pressing any other key will exit layered command mode. A lower pitch beep is played on exit.
Some commands exit layered command mode, and some do not. A low pitch beep is always played on exit.

Press slash (/) on any layer to open a list of commands for that layer.

## Commands

* NVDA + alt + space: Activate layered command mode
* slash: Opens help message for current layer

### First Layer

The following commands are available in the first layer:

* F11: Toggles temporary screen curtain on/off
* C: Speaks the text on the clipboard
* D: Toggles audio ducking on/off
* H: Opens speech history window
* control + N: Toggles notification announcements
* S: Toggles between speech mode on demand and speech mode talk
* shift + S: Toggles between speech mode on demand and speech mode off
* T: Activates the table navigation layer
* V: Activates the volume adjustment layer

### Table Layer

The table layer can only be activated while the focus is on a navigable table.

The following commands are available in the table layer:

* down arrow: Moves to next row
* up arrow: Moves to previous row
* right arrow: Moves to next column
* left arrow: Moves to previous column
* page up or control + up arrow: Moves to first row
* page down or control + down arrow: Moves to last row
* home or control + left arrow: Moves to first column
* end or control + right arrow: Moves to last column
* NVDA + right arrow or shift + page up: Reads from current cell to end of row
* NVDA + down arrow or shift + page down: Reads from current cell to end of column
* NVDA + left arrow or shift + up arrow: Reads entire current row
* NVDA + up arrow or shift + numpad 5: Reads entire current column
* numpad 5: Reads current cell
* control + home: Moves to first cell
* control + end: moves to last cell
* control + enter: Moves to next table
* control + shift + enter: Moves to previous table

### Volume Layer

The following commands are available in the volume layer:

* B: Activates the sound splitting/balance layer
* C: Activates the sound card layer
* N: Activates the NVDA volume layer
* S: Activates the system sound layer

#### Sound Splitting Layer

The following commands are available in the sound splitting layer:

* left arrow: NVDA sound on left and system sound on right
* right arrow: NVDA sound on right and system sound on left
* up arrow: Disables sound splitting

#### Sound Card Layer

The following commands are available in the sound card layer

* down arrow: Moves NVDA audio to the next sound card
* up arrow: moves NVDA sound to the previous sound card

#### NVDA Volume Layer

Volume adjustments are clamped between 10% and 100% while using this layer.
The following commands are available in the NVDA sound layer:

* down arrow: decreases NVDA volume by 2%
* up arrow: Increases NVDA volume by 2%
* page down: Decreases NVDA volume by 10%
* page up: Increases NVDA volume by 10%
* end: Sets NVDA volume to 10^
* home: sets NVDA volume to 100%

#### System Volume Layer

Volume adjustments are clamped between 10% and 100% while using this layer.
The following commands are available in the System sound layer:

* down arrow: decreases NVDA volume by 2%
* up arrow: Increases System volume by 2%
* page down: Decreases System volume by 10%
* page up: Increases System volume by 10%
* end: Sets System volume to 10^
* home: sets System volume to 100%
* M: toggles system mute on/off
