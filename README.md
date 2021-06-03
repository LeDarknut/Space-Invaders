# Space-Invaders
Space Invaders but it's a bullet hell. The aliens shoot regularly a rocket in your spaceship's direction. You have to dodge it or protect with your shield. Rockets is loaded during rest time. You can see the current state of loading on the sprites. Longer a rocket is loaded, stronger it is. You have to shoot your current rocket in order to use your shield. Aliens move forward, destroy them before they reach your spaceship. After defeating every alien, the game ends and the statistics of the game are shown. Your highest score of each difficulty is saved, so attempt to reach the perfect game.

## Requirements
### Python 3
To actually run the script.
### Pygame
*pip install pygame*
To display the game interface.
### Pynanosvg
*pip install pynanosvg*
To generate the sprites.
### Cursor
*pip install cursor*
[Optional] To hide the cursor in the command prompt.

## Launching
Launch the file SpaceInvaders.py, then enter the level of difficulty in the prompt.

## Settings
You can edit the settings in the file Settings.conf.
* **FULLSCREEN** : [yes/no] *Display the game in fullscreen, it will disable the width and height settings.*
* **WIDTH** : [integer] *Choose the width of the window in pixel.*
* **HEIGHT** : [integer] *Choose the height of the the window in pixel.*
* **FREQUENCY** : [integer] *Choose the framerate of the game.*
* **MUSIC** : [yes/no] *Enable or disable the music.*

## Controls
The game is played on the keyboard.
* **SPACE** : Shoot a rocket then hide behind a shield until the key is released.
* **RIGHT ARROW** : Speed up right.
* **LEFT ARROW** : Speed up left.
* **ESCAPE** : Exit the game.
* **ENTER** : Reset the game.
* **BACKSPACE** : Pause the game.
