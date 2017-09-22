# Sturmjäger
### Stormchaser: a neural net for detecting Nazis

The code currently uses a bag of words to develop and test some basic methods (and to help bring in additional training data). Testing demonstrated 14-22% rates of Nazi detection using only name, screen_name, and profile description.

This project's goal is to develop a Twitter sign-in UI for users to assess tweets or accounts--like the [Twitter Block Chain plugin](https://github.com/satsukitv/twitter-block-chain), but enhanced with a Nazi detector.


## Use case
* User enters a username or URL of a user.
  * Sturmjäger offers to assess that user's followers and follows for potential Nazis.
  * User selects to assess followers.
* A list of followers is shown. Each row shows: picture, name, screen_name, and profile description
  * Each follower is marked with an assessment score by Sturmjäger (colored & symboled for visual recognition of tiers?)
  * User may set a cutoff level.
  * User may select all, none, or use the cutoff level. User may use checkboxes to select/deselect.
  * User may elect to block these users.
  
* User enters a tweet's URL or status ID.
  * Sturmjäger offers to assess that tweet's likes or retweets for potential Nazis.
  * ...
  
### Questions:

#### Initial, architecture questions
* How long does it take to block a list of users?
  * Current rate: approximately 250 seconds for 1000 users
* What's the best way to handle API limits here?
* In querying a list of users, should we display only the first 10, 20, 100? (Or include options?)
* Can we store everything in memory while the app churns through a long list of users to assess or block?
  * This is not possible on Heroku (dynos). We'd need to use postgres. Will we need more than 10k rows? (Probably. This would cost $9/month to upgrade Heroku postgres support.)
* Can we and should we test if users are already blocked before we assess, or before display? Should blocked users be displayed on the list, or mentioned in the UI? (e.g., "170 of 690 users are already blocked.")

#### Design questions
* What options do users want, and what options are reasonable to provide?
* How much automated behavior is useful, or feasible?
* Should the UI be reactive (e.g., display further profile information on hover)? How does that impact the UX? (e.g., can the UI still be fast and light, not sluggish?)
* How much of this is feasible on a mobile device or a tablet?
  
#### Ethics questions
* How do we identify false positives?
* What is the rate of false positives? How can we track that?
* How do we educate users about the danger of false positives and encourage responsible use of this tool?
* CAN a tool like this be used responsibly? Are false positives worth the value of a tool like Sturmjäger?
* What kind of people are false positives? Can a tool like this be used to contribute to marginalizing stigmatized people who do not deserve the stigma they bear? (As opposed to Nazis, who deserve their stigma.)
