CSEC380 Section 2 Group 3
Adrianna Visca, Quintin Walters, Nic Brockman, and Patrick Swanson-Green
Activities 3-7 Writeup

Activity 3:
1. Provide a link to the test cases you generated for this activity.

ANSWER

2. How do you ensure that users that navigate to the protected pages cannot bypass authentication requirements?

ANSWER

3. How do you protect against session fixation?

ANSWER

4. How do you ensure that if your database gets stolen passwords aren’t exposed?

The passwords are hashed so that if the database is stolen it will be extremely difficult to figure out what the passwords are.

5. How do you prevent password brute force?

We limit the number of connections on a minutely/hourly/daily basis.

6. How do you prevent username enumeration?

We have a "Incorrect Credentials" page for if your username OR password is wrong, this way the attacker can't tell if they have a valid username or not because the response will be the same.

7. What happens if your sessionID is predictable, how do you prevent that?

ANSWER


Activity 4:

1. How do you prevent XSS in this step when displaying the username of the user who uploaded the video?

ANSWER

2. How do you ensure that users can’t delete videos that aren’t their own?

ANSWER


Activity 5:

1. How would you fix your code so that these issues were no longer present SQL Injection)?

ANSWER

2. What are the limitations, if any that, of the SQL Injection issues you’ve included? 

ANSWER


Activity 6:

1. How would you fix your code so that this issue is no longer present (SSRF)?

ANSWER

2. How does your test demonstrate SSRF as opposed to just accessing any old endpoint?

ANSWER


Activity 7:

1. How would you fix your code so that this issue is no longer present (Command Injection)?

ANSWER
