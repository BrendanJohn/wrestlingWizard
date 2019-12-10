# User Manual

## What is the The Wrestling Wizard?
The Wrestling wizard is a web-based application that allows authenticated users the ability to create wrestlers and compete in matches. Wrestlers level up as they complete matches which
improves attributes like speed, strength, and health. The goal of the game is to acquire the world heavyweight championship, which is tracked on a leaderboard.

## How to register a new user in The Wrestling Wizard

Use the register link to create an account. There are no complexity requirements around username and password, except that the password inputs must match.

## How to use The Wrestling Wizard

After you have created a user, log in and navigate to the create page. Here, you can create a new wrestler to begin the journey of becoming the champion.

## Matches

Matches are the bread and butter of the application. Here, you can compete against the wrestlers that other users have created. The match outcomes are randomly determined
with a slightly weighted probability that the winner is the wrestler with the higher level. Wrestlers level up and gain health as more and more matches
are completed.

## Test user
username: test
password: test

## Local setup steps below can be ignored, the app was deployed to Heroku
https://wrestling-wizard.herokuapp.com/


## How to run The Wrestling Wizard locally

Open a Terminal at the root of the application, i.e., the project directory. Once there, change directory into final using this command:

cd final

Next, start the application using this command:

flask run

The Terminal window will output a URL to access a live version of the application. Copy and paste it into the URL bar of any web browser.
