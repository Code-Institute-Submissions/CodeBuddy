# Code Buddy

## Python and Data Centric Development Milestone Project
A demo of this project can be viewed [here](https://jyf-codebuddy.herokuapp.com/).

This website has been designed for the budding community, to share personal articles and tips on how to get started on coding and sofware development. Users may come here to read articles, create content,or post questions. In a sense, the concept is similar to Reddit / Quora. Any user can visit this website, create articles, and post comments, without any login required. Articles or comments may also be deleted, but has to be deleted by the same email input that was used to create the content.

## UX

### Strategy - User Stories
Members of the public would use the website to:
- Browse articles on software development topics to learn how to get started / or how to get better on coding.
- Post articles to share tips and experiences to the community
- Post questions to ask for help on a certain topic in coding / software development.
- Post comments to share personal experiences and opinions on coding / software development.
- Help the budding community members with any troubleshooting problems they may have encountered.
- Edit their own articles / comments if they wish to make amendments.
- Delete their own articles / comments if find the material outdated / inappropriate or as they deem fit. 

Owners of the website may use this website for display ads revenue in the future if there is high enough traffic of software community visitors.

![Main thread page](report/screenshots/desktop.png "Desktop thread page")
![Mobile view of the thread page](report/screenshots/mobile.png "Mobile thread page")


### Structure and intended user behavior
- The website has a hierarchy where all threads are displayed as cards on the main page
- Each thread can be accessed by the thread_id as the URL route
- Each thread contains comments, which can be accessed by the thread_id and the comment_id as the URL route
- when user first enter the website, they will land on the "about page" which explains the background, objectives, and content of the website
- may then choose to browse articles, or create a new article as next step, followed by interacting with the rest of the content on the website

### Skeleton
Wireframes for Code Buddy can be viewed [here](report/wireframes). Wireframes were built on figma. The wireframes were used as a guide. Ultimately, some slight design changes were implemented, such as splitting the about page and search functionality from the main threads page into their individual pages, to ensure easier code maintenance.

### Surface
Functionality and clarity was the main focus and reason behind the colour scheme and typography choice. Comfortable colors schemes were chosen and used to improve reading experience. If time and resource permits, the colour scheme and styling should be revisited and improved to offer something unique for the community. 

## Features

### Current Features
#### Generic Browsing and Viewing of Website
- Ability to browse all content on the website without the need to sign up for a user account.
- Ability to search for articles based on keywords in each article's titles
- Ability to see timestamp of post to understand when the post was made, and its recency or relevancy
- Ability to see who was the author who made the post, to take note of credibility of poster in the community

#### Thread Creation / Edit / Deletion with User Validation
- Creation of article by any user, with all fields being mandatory. If fields are empty, there will be an error message prompting user to fill in all fields. 
- Update, delete articles that were written by the article owner, by email validation. If the email input does not match the original record's email input, there will be an error message to tell the user that the content is not allowed for editing or deleting, and the user may return to the article. 
- There is also additional logic to ensure email input and verification will not fail due to human error, such as upper / lower case sensitivity, and accidental keyboard spaces added by user. This is done by parsing the email input as lowercase, and also using python .strip() function.

#### Comments Creation / Edit / Deletion with User Validation
- Creation of comments by any user, with all fields being mandatory. If fields are empty, there will be an error message prompting user to fill in all fields. 
-  Update, delete comments that were written by the comment's owner, by email validation.  If the email input does not match the original record's email input, there will be an error message to tell the user that the content is not allowed for editing or deleting, and the user may return to the article. 
-  There is also additional logic to ensure email input and verification will not fail due to human error, such as upper / lower case sensitivity, and accidental keyboard spaces added by user. This is done by parsing the email input as lowercase, and also using python .strip() function.

### Potential Features to Further Implement:
- Adding of categories as tags, for better content organisation and searching if the number of articles scale up
- Adding of user login accounts, to ensure better security of content (as email addresses can be guessed to manipulate others' content on the website)
- Adding of like and comment counter, which helps users decide which post to read based on popularity
- Adding of text editor to allow users to format and display article or comments content in a more visually appealing way.

## Technologies Used
- Python
- HTML
- CSS
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for cloud hosted database
- [Flask 1.1.2](https://flask.palletsprojects.com/en/1.1.x/) to create the web app
- [Jinja 2.11.2](https://jinja.palletsprojects.com/en/2.11.x/) for templating
- [pymongo 3.11.0](https://pymongo.readthedocs.io/) to communicate with MongoDB database using Python
- [dotenv](https://pypi.org/project/python-dotenv/) to use environment variables
- [Bootstrap 4.5](https://getbootstrap.com/docs/4.5/getting-started/introduction/) for web page styling
- [Heroku](https://www.heroku.com/) to host the web app
- [gunicorn 20.0.4](https://gunicorn.org/) as the Python WSGI HTTP Server for deployment
- [GitHub](https://github.com/) for source control

## Programming Methodologies
- .env file was used to store environment variables so that Flask secret key and database credentials were not publicly viewable.

## Database Design
Two MongoDB collections were used:
1. Threads
2. Comments - which is nested under threads, using thread_id is the foreign key

### Sample MongoDB documents
Sample database document for threads collection:

```
{
	"_id": {
		"$oid": "5fb0d803e5af892300cfc22b"
	},
	"thread_title": "What is Fullstack Programming?",
	"thread_article": "A full stack developer needs to know the following technologies:HTML/CSSThe web is built on these technologies. HTML is the tool that helps developers input content into a website and CSS is a designing tool used to alter the appearance of web applications. Both are essential tools for a full stack developer and are taught in all courses, whether online or in-person.JavaScriptThis is a must-have for any full stack developer.",
	"thread_author": "Alex",
	"thread_author_email": "alex@gmail.com",
	"thread_datetime": {"$date":{"$numberLong":"1605425155684"}},
	"thread_datetime_edited": {"$date":{"$numberLong":"1605461439304"}},
}
```

Sample database document comments collection:
```
{
	"_id": {
		"$oid": "5fb13285a867615b495f2f41"
	},
	"thread_id": "5fb0d803e5af892300cfc22b",
	"comment": "Thanks for sharing, that was a really insightful post. May I know what are the best books and resources you recommend to get started?",
	"commenter_name": "Johnny",
	"commenter_email": "johnny@gmail.com",
	"commenter_datetime": {"$date":{"$numberLong":"1605613135844"}},
	"commenter_datetime_edited": {"$date":{"$numberLong":"1605448325621"}},
}
```

## Testing
All testing was done manually, with the following tests performed:
|  # | Event | Expected Outcome | Actual Outcome |
|----|-------|------------------|----------------|
|  1 | enter website without going to any specific route, will be redirected to "about" page (also labelled as the "Hello World" page)| About Page / Hello World page loads | As expected |
|  2 | create a new question / article by clicking top right hand corner button "Post an Article / Question" | loads article creation page | As expected |
|  3 | Search by category | Only results matching category should show. Search criteria should also be retained in the input form. | As expected |
|  4 | in create new question / article page, don't fill in all fields (ensure 1 or more fields are missing) and click submit | flash error message appears, stating "please ensure all fields are filled!" | As expected |
|  5 | in create new question / article page, fill in all fields, click submit | article is created succesfully, with the flash message staying "article created successfully". user is redirected to all articles page. article as appended to the bottom of the cards. | As expected |
|  6 | from all article page, visit single article page, by clicking on the created article's title, or clicking "read more" in the article's card body | proceeds to individual article page, with the URL route as the article's _id  | As expected |
|  7 | in single article page, add a comment. first, don't fill in all fields in the comment, and click submit | flash error message shows in single article page "please ensure all comments fileld are filled!" | As expected |
|  8 | in single article page, now add comment, by filling in all fields | flash message in single article page shows "comment posted succesfully!". comment is appended to the bottom of the article, in chronological order | As expected |
|  9 | while looking at the comment, click edit comment, visit edit comment page | user enters edit comment page | As expected |
| 10 | in comment edit page, fill in any random email address (that was not the original email used to post the comment), and try to edit comment content, and click submit | flash error message says "your email does not match the original record for this comment. edit was unsuccessful, changes were not saved" | As expected |
| 11 | in comment edit page, fill in the original email address used to create the comment, but remove all contents in the comment, and click submit | flash error message says "please ensure all fields are filled! your changes were not saved." | As expected |
| 12 | in comments edit page, fill in the original email address used to create the comment, and this time, edit the contents of the comment, and click submit | flash message says "comment updated successfully!" user is redirected to single article page, and the comment appended under the article has its contents updated. | As expected |
| 13 | go back to the same comments card, this time, click delete comment | user enters delete comment page | As expected |
| 14 | in delete comment page, enter a random email (not used to create the comment), and click "confirm" delete button | flash error message says "your email does not match the original record for this comment. Delete was unsuccessful." | As expected |
| 15 | in delete comment page, now enter the same email used to create the comment, click "confirm" delete button | flash message says "comment deleted successfully!" scroll down to the comments section under the article page, and find that the comment card has been deleted. | As expected |
| 16 | now in single article page, visit the article card, click edit post, and visit the edit article page | user enters edit article page | As expected |
| 17 | in article edit page, fill in any random email address (that was not the original email used to post the comment), and try to edit any other fields, and click submit | flash error message says "your email does not match the original record for this comment. edit was unsuccessful, changes were not saved" | As expected |
| 18 | in article edit page, fill in the original email address used to create the article, but leave some fields empty, and click submit | flash error message says "please ensure all fields are filled! your changes were not saved."| As expected |
| 19 | in article edit page, fill in the original email address used to create the comment, and this time, edit the fields of the article, and click submit | flash message says "article updated successfully!" user is redirected to single article page, and the article's card has its content updated accordingly. | As expected |
| 20 | in the same article's card this time, click delete post | user enters delete article page | As expected |
| 21 | in delete article page, enter a random email (not used to create the article), and click "confirm" delete button | flash error message says "your email does not match the original record for this article. Delete was unsuccessful." | As expected |
| 22 | in delete article page, now enter the same email used to create the article, click "confirm" delete button | flash message says "article deleted successfully!". user is led to the allnavigate to search feature from the navbar, click on search	search page is launched | As expected |
| 24 | in search page, dont key in any input, hit submit | search result page display all articles | As expected |
| 25 | go back to the search page, this time, key in a keyword present in only some article titles, i.e "fullstack", click submit | display search result page shows all article titles with the keyword entered i.e. "fullstack" as cards| As expected |

## Deployment Steps
A live demo of this project can be viewed [here](https://jyf-codebuddy.herokuapp.com/).
All the source code for this project is available [here](https://github.com/jyfoo213/CodeBuddy) on GitHub.

Code for the project was committed to GitHub in the following manner:
- Individual files were added to the next commit staging area by executing the `git add [filename]` command in a command-line interface.
- All changes in the working directory were added to the next commit (stage) by executing the `git add .` command in a command-line interface.
- Staged content was committed as new commit snapshot by executing the `git commit -m “[message]"` command in a command-line interface.
- Local branch commits were pushed to the remote repository master branch by executing the `git push -u origin master` command in a command-line interface.
- Subsequent local branch commits were pushed to the remote repository master branch by executing the `git push` command in a command-line interface.

Deployment to Heroku was performed in the following manner:
- Ensure requirements.txt file is installed, if not use `pip3 install -r requirements.txt`
- Install Heroku on local machine with `sudo snap install heroku --classic`, skip this step if it is already installed
- Log in into Heroku using `heroku login -i`
- Create a new app on Herkou `heroku create <app-name>` , as app name needs to be unique throughout the web, it is suggested to put initials before the app name
- Verify remotes that have been added with `git remote -v`
- Install Gunicorn with `pip3 install gunicorn`
- Create a `Procfile` (no extenstion) and add in to file the first line only `web gunicorn <your main app name without .py>:app`
- Freeze imports and dependencies with `pip3 freeze --local > requirement.txt`
- Commit changes and push to Heroku using `git add.` `git commit -m "<msg>"` then `git push heroku master`
- Proceed to the [Heroku](https://www.heroku.com/ "Heroku Cloud Application Platform") webpage and login to your dash board
    - Choose the correct application made previously
    - Under the Settings Tab --> Config Vars (Reveal Config Vars)
    - Add in your Var keys like `MONGO_URL` and `SECRET_KEY` and their respective values
    - Click `Open App` at the navbar above to see your webpage

## Run locally on PC
- Clone the [repository](https://github.com/jyfoo213/CodeBuddy)
- Setup a python virtual environment in the root folder of the project: `python3 -m venv venv`
- Activate the python virtual environment whilst in the root folder of the project: `source venv\bin\activate`
- Install the dependencies: `pip install -r requirements.txt`
- In root folder of project, create a `.env` file and set the following environment variables: `export SECRET_KEY = <your own key>`, `export MONGO_URI = <your MongoDB URI>`, `export PORT = <your chosen port>`
- Run the web app `python app.py`
- Use a web browser to navigate to `localhost:<your chosen port>`

## Credits
- Code institues instructor Paul Chor for guidance on backend development
- Teaching assistant John Benedict for helping with troubleshooting of bugs
- Reddit / Quora / Stackoverflow as project inspiration
