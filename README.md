# JKLM BombParty bot

This is a bot for the BombParty game from https://jklm.fun.
The bot is based on automated web browser interactions with the Selenium package.

## Disclaimer
The aim of this project is not to ruin online games by cheating. It is simply a use case for the Selenium package, designed to familiarize myself with it.

## Behavior
Unlike existing solutions, this bot does not rely on graphical coordinates to locate various game elements such as text boxes, text inputs and buttons.

Instead, it uses the Selenium package and the HTML code of the page to locate and interact with these elements.
Obviously, if the HTML code of the website is modified, the bot will be broken. Nevertheless, it is a practical solution that requires no preparation to operate.

## Languages
By default, the supported languages are the ones in the "data" folder. Feel free to add your own word list. To that end, you must create a ".txt" file with one word per row.  
The name of that file should be of the format "\<LANGUAGE\>_words.txt". Do not forget to modify the "LANGUAGE" parameter in the configuration file accordingly.

## Configuration
To play the game, you can either create a new lobby or join an existing one. This is controlled by the "CREATE" parameter in the configuration file ('True' to create a lobby, 'False' to join one).

- If you want to create a new lobby, you must also specify whether this lobby will be public or private. This is controlled by the "PRIVATE" parameter in the configuration file ("True" to create a private lobby, "False" to create a public one).

- If you want to join an existing lobby, do not forget to modify the "ROOM_CODE" parameter in the configuration file accordingly.