# Unit 13 - Robo Advisor for Retirement Plans (Option 1)

In this homework assignment, we were tasked with building an Amazon Lex chatbot that made use of a custom Lambda function running in the Python 3.7 environment. Most of the code for the lambda was provided by the instructors, however, the data validation and portfolio recommendation portion needed to be filled in by the student. The latter was simple enough. However, the former was much more difficult. In order to complete the former, I had to review the lambdas documentation. One feature I devised was to allow the user to 'try again' with the bot. This means that once the bot is done dispensing investment advice given one set of parameters, the user can type 'try again' and cycle through the dialogue over again. I also added more sample utterances that allow the user to give the bot more information up front. Finally, I cycled through all of the possible outcomes in the screen capture gif below. One way of thinking about this program is as the web-deployable equivalent to and old school MS-DOS text-based game.

![GIF of bot testing](https://github.com/ThomasJScott3/unit13-challenge/blob/main/Images/Roboadvisor_Test.gif)

Note: I have included the icons for the risk levels. Feel free to update them in my bot when reviewing. The URLs for said icons are currently pulling from the GitLab homework repository for this course.

-Thomas J. Scott
