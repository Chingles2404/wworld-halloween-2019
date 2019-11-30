# Whatever World Halloween Event (Oct 30 2019 - Nov 3 2019)
The code above was used for a Telegram bot during an event in a group, [@whateverworld](https://t.me/whateverworld), in order to facilitate the recording of the players' scores after each game played using [@werewolfbot](https://t.me/werewolfbot).

This bot uses the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library.

## About
This event was created for Halloween. There were 3 sub-events, where players spent one day collecting candy corn through playing games. At the end of the day, the event narrator, [@snailandstars](https://t.me/snailandstars), announced that the candy corn has formed a monster, aptly nicknamed the "candy corn monster". The players then spent the next 2 days playing games to deal damage to the monster to bring its health points down to 0. (Note: The players did not know how many health points the monster had, and the group admins planned to make it dynamic, to suit the activity in the group) On the fourth day, the players played games to collect a 1000 rune tags collectively to seal the monster away.

## Bot functions
###### connect_candy_corn / connect_damage / connect_rune_tag
These functions would be used later on in the candy_corn, damage, and rune_tag functions. It was used to calculate the number of candy corn/amount of damage dealt to a monster/number of rune tags a player won from a particular round, and recorded them in the database.

###### candy_corn / damage / rune_tag
For these functions to be used, a log group should be created, where the end-game messages from [@werewolfbot](https://t.me/werewolfbot) should be forwarded. The admins during the event logged the scores in their own log group by replying a forward slash ("/") with the function name to the end-game message, depending on which sub-event was going on at that point in time. The functions parse the end-game messages to determine who won or lost and who remained alive or died, before calling the functions above for the calculations.

###### candy_corn_scores / damage_scores / rune_tag_scores
These functions were to enable players to see the top 10 scorers for each sub-event, and for the damage_scores and rune_tag_scores, to show the progress of the group in defeating the candy corn monster and in collecting rune tags respectively. These functions could be called by sending a forward slash ("/") with the function name in the group.

###### find
This function was used in the log group to allow admins to search for a player and their current scores.

###### add_candy_corn / add_damage / add_rune_tag
This function allowed the admins to create a new player entry in the database manually in the log group, since some players' ID's cannot be read from the end-game messages due to their privacy settings.

###### update_candy_corn / update_damage / update_rune_tags
This function allowed the admins to add the scores of a player manually in the log group, since some players' ID's cannot be read from the end-game messages due to their privacy settings.

###### health
This function allowed the admins in the log group to check the health of the monster by sending "/health" or to add or subtract health points from the monster by sending "/health [integer]"

## Special thanks
This event could not have been executed successfully without the help of the event and general group admins, Pandora and Anonymous, and [Fallen Angel](https://t.me/maykurasaki). 