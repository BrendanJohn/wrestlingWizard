# User Manual

## Local setup steps can be ignored, the app was deployed to Heroku
https://wrestling-wizard.herokuapp.com/

## Test user
username: test
password: test

## How to register a user in The Wrestling Wizard

Use the register link to create an account. There are no complexity requirements around username and password, except that the password inputs must match.

## How to use The Wrestling Wizard

After you have created a user, log in and navigate to the create page. Here, you can create a new wrestler to begin the journey of becoming the champion.

## Matches

Matches are the bread and butter of the application. Here, you can compete against the wrestlers that other users have created. The match outcomes are randomly determined
with a slightly weighted probability that the winner is the wrestler with the higher level. Wrestlers level up and gain health as more and more matches
are completed.

## How to run The Wrestling Wizard

Open a Terminal at the root of the application, i.e., the project directory. Once there, change directory into final using this command:

cd final

Next, start the application using this command:

flask run

The Terminal window will output a URL to access a live version of the application. Copy and paste it into the URL bar of any web browser.
