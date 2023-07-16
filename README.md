# Pawcation

Pawcation is a website addressed to dog owners offering hotel services for dogs. Having a dog is wonderful but we all know how hard it can be, at times,  to find a safe place for our furry friends when we are not around.Enters Pawcation, a small business that offer safe stays so that our dogs are treated well until we get back. 

The live version of my project can be found here: 
___
## UX Design

### Wireframes 
Wireframes for the project were created using Figma and can be viewed on Figma [here](https://www.figma.com/file/G1KsEzPmiHHn6TrtWUEKh2/Pawcation-Wireframes?type=design&node-id=4%3A376&mode=design&t=t87crDcdStwRB99v-1)

![Wireframes 1](readme-images/wireframes-1.png)
![Wireframes 2](readme-images/wireframes-2.png)
![Wireframes 3](readme-images/wireframes-3.png)

## Database Design 
I designed the Database using LucidChard. A link to the document is [here](https://lucid.app/lucidchart/2d227d87-755c-4bae-a0cb-cd0d41d74134/edit?viewport_loc=-720%2C-515%2C1875%2C903%2C0_0&invitationId=inv_8b495c89-08df-4f9f-bb0c-868687f2bdb8)

![Database Diagram](readme-images/database.png)

## Agile 
A link to the Github project and stories can be found [here](https://github.com/users/ilaria-barletta/projects/2/views/1)

## Technologies Used
* Django 
* HTML5 
* CSS 
* Bootstrap 5 
* Python 
* ElephantSQL 
* Cloudinary 
* FontAwesome 

___
## Features 
__Homepage__: ![Welcome page and request to log in or register](add pic)

This is the main page that the user sees before registering or logging in. 
The content is centered and the style is clean and simple. 
There is a navigation bar and a footer.
The navigation bar at this stage contains only the name of the website (it works as a link to the homepage as well if the buttons present in the page are clicked and the user wants to go back to the main screen).
The navigation bar will change and provide links to additional pages only after the user has registered or logged in to their account.
A quick but clear in the scope message to the user informs them of what pawcation is. 
The message contains a link that if clicked will show reviews left by other customers.
There are then 2 buttons that let the user register if they are new or log in if they are known users. 

__Register__: ![Registration form] (add pic)

This is the first option the user has and can click on in order to provide their details to access the service. 
When clicked the user will be taken to a form page where some details will be requested. 
In particular they will be asked to provide username and password. An email can be also provided but that's optional. 
The password needs to be selected once and then typed it again for confirmation. 

__Successfully registered__: ![message showing registration successfull, user is in the system] (add pic)
When the process is complete and the user selects register they are shown a screen where options are listed in the nav bar. 
A pop up message saying "succesfully signed in" is showed to them  

__Log in__: ![log in form] (add pic)

Alternatively the user that already has an accound can just log in into it selecting the relevant button. 
In such case they will be asked to type in their username and password and both fields are mandatory. 

__Succesfully logged in__: ![message showing registration successfull, user is in the system] (add pic)

___
## Testing 

### Manual testing 

responsivness testing
browser compatibility testing
bugs (resolved and unresolved)
lighthouse testing
code validation testing 
user stories testing
features testing

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

### User stories testing
1. Site registration [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30571231): 

| Test        | Outcome     |
| ----------- | ----------- |
| From homepage the register button takes user to registration form      | Pass        |
| Form has username, password and email fields       | Pass        |
| Username and password are mandatory fields       | Pass        |
| If pass and confirm pass do not match, error msg shows       | Pass        |
| Button to register present and working       | Pass        | 
| Register button takes to bookings       | Pass        | 
| Button to cancel present and working       | Pass        | 
| cancel button takes user to homepage       | Pass        | 

2. Site login: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30571430):

| Test        | Outcome     |
| ----------- | ----------- |
| From homepage the login button takes user to login form       | Pass        |
| Username and password are mandatory fields       | Pass        |
| if user provides wrong username/password, error msg shows   | Pass        |
| Button to  Login present and working      | Pass        |
| Login button takes to bookings       | Pass        |
| Button to cancel present and working | Pass        |
| Cancel button takes user to  Homepage      | Pass        |

3. Add Pet Details: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30571658):

| Test        | Outcome     |
| ----------- | ----------- |
| Name, age, breed, allergies, notes are all mandatory fields in form      | Pass        |
| The image field in the form is not mandatory and a placeholder will be used if user doesn't add one       | Pass        |
| Dogs can be max 12 years old to use pawcation services, error msg shows if age selected is >12       | Pass        |
| Button to submit is present and creates the pet and takes the user back to the pet list where the newly added pet is shown when clicked | Pass        |
| Button to cancel is present and takes the user back to the pet list when clicked       | Pass        |

4. View Pet List: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=31068112):

| Test        | Outcome     |
| ----------- | ----------- |
| Every pet the user has registered is shown       | Pass        |
| Pet name and profile picture are shown      | Pass        |
| If a pet doesn't have a profile picture a placeholder is shown       | Pass        |
| Pets that other users have registered should not be shown to the user      | Pass        |
| The user should have the option to edit or delete pets    | Pass        |
| The "edit" option on a pet should take the user to the pet details form with the pets details filled in    | Pass        |
| The "delete" option on a pet should take the user to the delete pet page    | Pass        |

5. Update Per Details: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30571798):

| Test        | Outcome     |
| ----------- | ----------- |
| Name, age, breed, allergies, notes are all mandatory fields in form      | Pass        |
| The image field in the form is not mandatory and a placeholder will be used if user doesn't add one     | Pass        |
| The form has each field pre-filled with the existing details of the pet to update      | Pass        |
| The submit button should take the user back to the pet list and save the changes made to the data in the form       | Pass        |
| The cancel button should take the user back to the pet list without saving any of the changes they did to the data in the form     | Pass        |

6. Delete Pet: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=33380253):

| Test        | Outcome     |
| ----------- | ----------- |
| The page confirms if the user would like to delete the pet and shows the name of the pet to be deleted       | Pass        |
| The delete button will delete the pet and will take the user back to the pet list where the pet just deleted will no longer be visible       | Pass        |
| The cancel button will take the user back to the pet list ignoring the previous delete request.       | Pass        |


7. Booking type selection: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=33381567):

| Test        | Outcome     |
| ----------- | ----------- |
| Start a new booking presents the user with two options: pre-visit or full booking       | Pass        |
| Each option is briefly described and has a choose button       | Pass        |
| The choose button in the previsit box takes the user to the new pre-visit form       | Pass        |
| The choose button in the full booking box takes the user to the new full booking form     | Pass        |


8. Create a pre-visit booking: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30571928):

| Test        | Outcome     |
| ----------- | ----------- |
| The user can select the start date and the time for their previsit       | Pass        |
| The start date must not be in the past     | Pass        |
| The user can select the pet they are booking the pre-visit for from the dropdow list showing all the pet that particular user has registered on the platform       | Pass        |
| The user can book only one previsit per pet. If the pet has already completed a previsit or has one booked and not yet completed then an error message will be shown giving information regaring the policy (just one previsit per pet) and the instruction to edit the future pre-visit already booked       | Pass        |
| The submit button should take the user back to bookings where the new pre-visit booked will be visible       | Pass        |
| The cancel button will take the user back to bookings   | Pass        |



9. Create a stay booking: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30571943):

| Test        | Outcome     |
| ----------- | ----------- |
| The user can select the start date, end date (date and time) for their booking     | Pass        |
| The user can select the pet they're planning to book for from the dropdown list of pets. The list of pets shows all the pets the logged is user has added to their account.        | Pass        |
| The user cannot book a stay for more than 30 days        | Pass        |
| The user cannot book a stay for less than 1 hour     | Pass        |
| The user cannot book a stay for a pet that has not yet completed a pre-visit      | Pass        |
| The user cannot book a stay if there are already 2 bookings present in the system for that same date they're trying to book for     | Pass        |
| The submit button will take the user to the booking page where the new booking will be listed along with the other bookings the user mighy have       | Pass        |
| The cancel button will take the user back to the booking page       | Pass        |

10. Create a stay booking - date validation: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30572301)
& Create a stay booking - pet capacity validation: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30572465):

| Test        | Outcome     |
| ----------- | ----------- |
| clicking on submit, if the date the user is booking for is not available due to limited capacity, an error message is shown and the user is asked to book for a different date        | Pass        |

11. View booking list: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=31068173):

| Test        | Outcome     |
| ----------- | ----------- |
| The booking page shows all the booking a user has in their account past and future       | Pass        |
| The completed bookings cannot be edited or modified       | Pass        |
| The bookings show the name of the pet they are for and the time they are for       | Pass        |
| Bookings that are not completed yet present the option to be edited       | Pass        |
| Booking that are not completed yet present the option to be deleted       | Pass        |


12. Update a booking: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=33384945):

| Test        | Outcome     |
| ----------- | ----------- |
| All the bookings that are not completed yet in the booking page present the option do be edited      | Pass        |
| the edit button takes the user to the update booking form       | Pass        |
| the field in the update booking form are prefilled with the choices the user originally made. they can be edited.       | Pass        |
| The submit button takes the user back to bookings and shows the updated details of the booking       | Pass        |
| The cancel button takes the user back to bookings     | Pass        |

13. Delete a booking: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=33380250):

| Test        | Outcome     |
| ----------- | ----------- |
| All the bookings that are not completed yet in the booking page present the option to be deleted.         | Pass        |
| The page confirms if the user would like to delete the booking and shows the name of the pet, the type of bookings and the time to be deleted       | Pass        |
| The delete button will delete the booking and take the user back to the bookings page where the deleted booking will no longer be visible       | Pass        |
| The cancel button will take the user back to the booking page       | Pass        |


14. Create a property review: [Github Story](https://github.com/users/ilaria-barletta/projects/2/views/1?pane=issue&itemId=30573214):

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |



15. View property reviews: []():

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

16. Update a property review: []():

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

17. Delete a property review: []():

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

18. View other users review: []():

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

19.  []():

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

20.  []():

| Test        | Outcome     |
| ----------- | ----------- |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |
| Title       | Pass        |

### Automated testing

## Deployment, Forking and Cloning 
The project has been deployed using Heroku. Here are the step to follow for the deployement:

1. Access your Heroku account and click on "create a new app", name the app and select the region before hitting the create app button.   
2. Navigate to the settings tab and create config vars for cloudinary, the database, and the secret key
3. Navigate to the deploy section and select Github as deployment method. After confirming that we want to connect to Github we can then search for the Github repository name. Once we find it we can click on connect. 
5. Scroll down and select enable automatic deploys

The live link to my project is here: https://pawcation.herokuapp.com/



### Forking & Cloning
To fork this repository click on the "Fork" button in the top right of the repository in Github. 

To clone this repository:
1. Click the "Code" button in the repository. 
2. Copy the clone link.
3. Use git to clone the copied link: `git clone LINK`. 

___
## References