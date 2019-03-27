# nettbureauCase
Instructions on how to run the project is included in the *Backend* and *Frontend* folders.

## Ideas for improvements

### Additional measures for spam prevention
This form of spam prevention (ip-based) can be circumvented by malicious actors by using proxies nad only sending a few requests from each uniqe ip. This is hard to prevent, but can be done for example by using captchas.

### Cookies
I was uncertain if the email and phone fields should be unique in the DB or not. If they are not supposed to be unique and the system is meant to allow multiple submissions per user, a simple cookie can be used to store the contents of the last used name, email and phone number to make it easier for the user next time they visit.

### Analytics
Another approach for improving the utility of this app for the providers is to collect information from the requests, like the agent used to connect, time of day, country of origin etc. This information can be analyzed to identify a more specific user base and tailor make the service for them.
