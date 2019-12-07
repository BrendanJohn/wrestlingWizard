# Design consideration

The wrestling wizard uses flask as a web framework and also as a server for the application. Flask is perfect for small and lightweight applications such as this one.
One drawback I discovered that when many users tried to access the application at the same time, one of those users became corrupted and he was no longer able to log in.
What may have happened was some fields associated with that user were entered into the database as nulls, resulting in problems for him on various screens. However,
there were no other large problems with Flask, and I found it to be a good fit for the needs of my application.

Another design consideration I went with was using SQL lite 3. The main reason was that this was the database introduced with the class and I did not find another
database that did much more than SQL lite and it met the needs of my application perfectly. One thing I discovered is that each 'trip' to the database had an impact on
on performance and I did everything I could to combing queries wherever possible so that page load times were as light as possible.

Lastly, I knew my users would be accesing the wrestling wizard primarily from mobile devices so I did whatever I could to make sure it loaded up nicely on devices of any size.
This mean implementing many of the features from bootstraps extensive library as well as implementing css media queries in certain cases to be confident that they
loaded up correctly for a given device. Overall I enjoyed making the application, and the most thrilling part was when I gave the url to my friends watching them
compete for the 'heavyweight championship. They gave me lots of good feedback, which I tried to implement as much as possible. I had also hoped to implement a search
functionality which was a far greater effor than I realized and I endedup up abandoning the pursuit after a few unsuccussful attempts. I had also hoped to implement a
feautre that would allow users to bet on the outcome of a match using their points as a bank, however I never even got that far as I got too bogged down
with the mechanics of the game and making it look nice on molbile platforms.