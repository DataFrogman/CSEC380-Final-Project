# CSEC380 Section 2 Group 3, Activities 3-7 Writeup

Adrianna Visca, Quintin Walters, Nic Brockman, and Patrick Swanson-Green

## Activity 3: Authentication
1. Provide a link to the test cases you generated for this activity.

https://github.com/DataFrogman/CSEC380-Final-Project/blob/master/tests/test1.py

2. How do you ensure that users that navigate to the protected pages cannot bypass authentication requirements?

Users cannot bypass authentication requirements because they need a valid sessionID.

3. How do you protect against session fixation?

We protect against session fixation by not passing session IDs in GET/POST variables.

4. How do you ensure that if your database gets stolen passwords aren’t exposed?

The passwords are hashed so that if the database is stolen it will be extremely difficult to figure out what the passwords are.

5. How do you prevent password brute force?

We limit the number of connections on a minutely/hourly/daily basis.

6. How do you prevent username enumeration?

We have a "Incorrect Credentials" page for if your username OR password is wrong, this way the attacker can't tell if they have a valid username or not because the response will be the same.

7. What happens if your sessionID is predictable, how do you prevent that?

If it is predictable an attacker could duplicate the ID to take over the user, you can prevent this by randomizing the sessionID each login.


## Activity 4: Content

1. How do you prevent XSS in this step when displaying the username of the user who uploaded the video?

We prevent XSS in this step by always checking for not only username but also userID.

2. How do you ensure that users can’t delete videos that aren’t their own?

Checking if the UserID of the user logged is the same as the video owner.


## Activity 5: SQL Injection

1. How would you fix your code so that these issues were no longer present (SQL Injection)?

The fix to our code would be removing any spots where the invalidcreds.html page was being rendered by sending the results database.

2. What are the limitations, if any that, of the SQL Injection issues you’ve included? 

The limitations of the SQL injection issues we've included is that the database will only be dumped if you have a correct username or completely incorrect credentials. If you have a correct password, you will see no extra data on the invalidcreds page. 


## Activity 6: SSRF

1. How would you fix your code so that this issue is no longer present (SSRF)?

Adding filename (.mp4) sanitization to the manage function would fix the code so that SSRF is no longer present.

2. How does your test demonstrate SSRF as opposed to just accessing any old endpoint?

The test demonstrates SSRF because the bash script is executed when uploaded. 


## Activity 7: Command Injection

1. How would you fix your code so that this issue is no longer present (Command Injection)?

We would fix the section of code responsible for deleting videos so that when one video is deleted it is just removed without the command rm.
