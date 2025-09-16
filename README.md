This project will automatically import your Sorcery TCG decklist into Tabletop Simulator.

Getting Started:
----------------------------------------
1. Create a text file containing your Sorcery decklist. Follow the format shown in sampleDeck.txt
2. Edit sorcery_config.py to contain the path to your decklist. (PATH_TO_DECK_LIST="")
3. Run the Python script.
4. Open Tabletop Simulator and check your saved objects. You should have three new saved objects: An avatar, an atlas deck, and a spell deck.

Have fun!

Troubleshooting
----------------------------------------

1. Script does not run
    - Make sure python is installed
    - Run the following command in your console: ```pip install pillow```, then try again.
2. Files do not appear in Tabletop Simulator browser
    - Try specifying a custom path to Tabletop Simulator in the config file. 
        - e.g. ```CUSTOM_TTS_PATH=C:/Users/x/Documents/My Games/Tabletop Simulator/Saves/Saved Objects```
    - Try setting ```SAVE_TO_TTS_PATH=False``` and specify a different path in ```CUSTOM_OUTPUT_PATH```.
        - The files can then be copy/pasted to the correct folder.
3. Tabletop Simulator will not load the files
    - It is possible the image links have changed; the /res folder will need to be updated
4. Other issues
    - Make sure all card names are spelled correctly in the deck list
    - Make sure you are not trying to overwrite a file that already exists; I disabled this to prevent accidents


