# Flag Guessing Game

![title_page](https://user-images.githubusercontent.com/71076769/211027034-c69062b2-5ae5-4807-975a-abd273bb57b6.png)

> This repository contains a flag guessing game for a user to play in Discord.

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [Demonstration](#demonstration)
- [Author Info](#author-info)

---

## Description

This repository provides the user a flag guessing game which is integrated into Discord. It uses the **Flagpedia API** to collect the images of the flags and send them into Discord for the user to guess. 

The game provides **solo** and **team play**, tracking and recording scores within the game and stroring them  in a leaderboard which can be viewed using `!leaderboard` ([Leaderboard](#leaderboard)).

If the user inputs inputs the correct name for the flag the game will continue ([Correct answer screen](#correct-answer)) however if the user's input is incorrect the game will end and they will be prompted to play again through  a simple **yes** or **no** button system ([Incorrect answer screen](#incorrect-answer)).

### Technologies / Packages

- Python
    - **requests** package
    
        Used to call the API and collect the image of the flag.
    - **nextcord** package

        Used to integrate the flag guessing game into Discord.  
- API
    - **Flagpedia** API [https://flagpedia.net/]

        Used to collect the images of the flags.

[Back To The Top](#flag-guessing-game)

---

## How To Use

### Commands

`!flag` - This opens a unique channel for the user to play the game.

`!flag-team` - This allows a group of people to play the game. It begins the game in the channel this command was called in.
(This is also represented as **team** on the scoreboard)

`!leaderboard` - This provides a visual leaderbaord with the top scores achieved in the game for that server.

[Back To The Top](#flag-guessing-game)

---
## Demonstration

### **Correct Answer**

Below you can see a screenshot of the user correctly guessing the name of the flag.

![correct_answers_edited](https://user-images.githubusercontent.com/71076769/211026184-58e2a573-dcd7-469d-8b24-8743ced2ba32.png)

### **Incorrect Answer**

Below you can see a screenshot of the user incorrectly guessing the name of the flag. The game will end and their **score** will be displayed with the **correct answer** and a link to the Wikipedia page.

The  user is also prompted whether they would like to play again.

![incorrect_answeres_edited](https://user-images.githubusercontent.com/71076769/211026212-bedb0bb9-d1ad-4a89-8125-7a1971e33025.png)

### **Leaderboard**

Below you can see a screenshot of the user calling the leaderboard to view the top scores in the game.

![leaderboard_edited](https://user-images.githubusercontent.com/71076769/211026243-8cd43a0d-4028-45df-acef-e2176c63bce7.png)

[Back To The Top](#flag-guessing-game)

---

## Author Info

LinkedIn - [George Lopez](https://www.linkedin.com/in/george-benjamin-lopez/)

[Back To The Top](#flag-guessing-game)
