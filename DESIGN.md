# Design considerations

The Wrestling Wizard uses Flask as a web framework and also as a server for the application. Flask is perfect for small and lightweight applications such as this one.
One drawback I discovered is that when many users tried to access the application at the same time, one of those users became corrupted and he was no longer able to log in.
What may have happened was that some fields associated with that user were entered into the database as nulls, resulting in problems for him on various screens. However,
there were no other problems with Flask, and I found it to be an effective server for my application and overall a good fit for the needs of my application.

Another design consideration I went with was using SQL Lite 3. The main reason was that this was the database introduced with the class and I did not find another
database that did much more than SQL Lite 3 and it met the needs of my application perfectly. One thing I discovered is that each 'trip' to the database had an impact on
on performance and I did everything I could to comb queries wherever possible so that page load times were as light as possible.

Lastly, I knew my users would be accessing The Wrestling Wizard primarily from mobile devices, so I did whatever I could to make sure it loaded up nicely on devices of any size.
This meant implementing many of the features from Bootstrap's extensive library as well as implementing CSS media queries in certain cases to be confident that they
loaded up correctly for a given device width. Overall, I enjoyed making the application, and the most thrilling part was when I gave the URL to my friends and watched them
compete for the 'heavyweight championship'. They gave me lots of good feedback, all of which I tried to implement as much as possible. I had also hoped to implement a search
functionality, which was a far greater effort than I realized and I ended up abandoning the pursuit after a few unsuccessful attempts. I had also hoped to implement a
feature that would allow users to bet on the outcome of a match using their points as a bank, but I never got that far as I got too bogged down
with the mechanics of the game and with making it look nice on mobile platforms. Lastly, on the night before this was due, I decided to deploy it to Heroku, which was largely unsuccessful
at first. However, after many, many, many hours of trial and error, I have the application deployed (somewhat) sucessfully. Enjoy! https://wrestling-wizard.herokuapp.com/