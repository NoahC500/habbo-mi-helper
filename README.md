# Habbo MI Helper

## Intro

### Operation Cleanup
In this branch will be a full restructuring of the code to make it less spaghetti like

This is a script I've created to aid me in my role as Director General of Military Intelligence at [HabboUK](https://habbouk.com/).

Currently, it includes:

- An activity checker which uses Habbo's API to report when a user last logged in

- The ability to download user's avatars (used for our weekly newsletter showcasing the Leadership team)

- The ability to open up the task completion pages for staff (DQ)

- An inbuilt editor for names used in the aforementioned features

Usernames are fetched from a file named `habbo-eedb-names.txt` located in a folder named `.Habbo-Name-List` in the user's home directory (should work on Windows, Linux and Mac).

Images downloaded are sent to the same `.Habbo-Name-List` folder.

These will both likely need to be created before the script is run. This won't be necessary in future.

## Libraries used

- Requests

- JSON

- DateTime

- OS

- TKInter

- WebBrowser

- PIL

- IO

- Subprocess
