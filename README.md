# chore_log

*Earn minutes, play games*

## Distinctiveness and Complexity

- **Different types of users with relationships between them**: This is the first project I've done that has two different types of users. Models for `Parent` and `Child` both extend `User` but get different experiences with different permissions. (In the social network assignment, users could follow each other but each user was based on the same model and each user's permissions were identical.)
- **Customizing the experience by user type**: This was the first project I've done where a view delivers a drastically different template based on what type of user is logged in.
- **More complicated permissions**: Parents can view their own index page and their children's pages, but not the pages of other parents or other parents' children. This was more complicated than previous projects, where the permissions were basically "you must be logged in to see this" and "you can only see your own stuff."
- **Aggregating data from different models**: My web application allows users to log "work" and "play" and view the balance between the two. However, work and play are by necessity modeled differently: child users can log play of any title and duration, while the work they log is from a preset list defined by their parent. This meant that I needed to do some trickery involving `annotation`s and `union`s in order to make "work" and "play" something that could be presented in the same ledger and added together for a balance. This is the first time I've had to make two different models work together like that.
- **New front end techniques**: The front end is where I have the most experience, and I wanted to try some new techniques that I have been reading about. In contrast to the previous homework projects, I eschewed Bootstrap in favor of Flexbox and Grid for layout and [Open Props](https://open-props.style) for other styling. I used view transitions to see if I could provide an SPA-like experience with a traditional multi-page architecture. This is the first time I have tried out browser-native modals using the `dialog` element. I'm also leaning on the [new browser support for `datalist`](https://adactio.com/journal/21445) to provide browser-native autocomplete.

## File By File

### models.py

- The `User` model has two different types of users: Parent and Child. Child users reference Parent users.
- The `Chore_Definition` defines chores that a child users can do. Each one is worth a certain number of minutes.
- The `Work` model captures a chore done by a specific child at a specific time.
- The `Play` model captures play done by a child. It has fewer restrictions on it: Rather than referencing specific set of definitions of play (like `Work` does with `Chore_Definition`) a child user can log play of any title for any length of time.

### views.py

- I define three forms using `ModelForm`: one for logging work, one for logging play, and one for defining chores.
- `get_log_and_balance` is the most complicated function in the project. It uses two different models, `Work` and `Play`, and brings them together so that I can present them in one unified ledger, and also add up the values to provide a balance.
- The `index` function provides a different homepage for a parent user than for a child user. (See `index-for-children.html` and `index-for-parents.html`.)
- There are separate registration views/pages for parents and children. The parent registration takes an email address, username, and password. But children are not expected to have an email address. Instead, the specify their parent's email address, a username, and a password. Taking the parent's email address establishes the relationship between the child user and their parent user.
- `full_log` get the ledger and balance of work and play for a given user. Permissions are important here: Children can only see their own log. Parents can see their children's logs. The log uses Django's paginator.
- `log_chore`, `log_play`, and `define_chore` all use the `ModelForm` forms defined at the top.
- `login_view` and `logout_view` are standard.

### tests.py

I use `TestCase` to test that the relationship between `Parent` and `Child` users works as intended, that `is_valid_play` is successfully catching problems, that various pages load with the correct data, and one child is not able to access another child's log.

### tests_selenium.py

Tests registering as a parent, registering as a child of that parent, and logging play.

### /templates

Logged out users get `start.html` where a list of links lets them choose between logging in, registering as a parents, or registering as a child.

Because there are two different types of user, we have two different registration pages: `register-child.html` and `register-parent.html`. If a user is already registered, they use `login.html`.

Once logged in, each type of user has their own homepage: `index-for-children.html` and `index-for-parents.html`. Children get a summary view of their balance the last five log entries they have made. Parents see a list of their children and a list of chores they have defined. These views are where I used `dialog` elements to provide browser-native modals to bring up forms for defining chores (parents) and logging work and play (children). 

The form for logging play includes a **JavaScript timer**: a child user can start the timer, go play their game, and then when they come back and stop the timer, the minutes field is automatically filled out for them.

`full-log.html` displays a paginated view of a user's full ledger.

`layout.html` is basically what we did in the homework assignments, but with the addition of a custom favicon.

### /static

- CSS: The most complicated stuff in here is the view transitions. The header is kept in place while the `main` element of the page slides in and out. Everything else is familiar styling, though based on custom properties defined by [Open Props](https://open-props.style) rather than Bootstrap.
- JS: Two JavaScript functions work together to listen for clicks and and then assign a view transition type of `forwards` or `backwards` as appropriate. This ended up being a little more complicated than I hoped because, while Safari now supports view transitions, it doesn't support view transition *types* yet, so I had to set and retrieve those in `localStorage` as a workaround.
- Favicon files: Courtesy of [RealFaviconGenerator](https://realfavicongenerator.net).

## How to run the application

1. Install dependencies using `pip install -r requirements.txt`
2. Set up database using `python3 manage.py makemigrations` and `python3 manage.py migrate`
3. Run server using `python3 manage.py runserver`
4. Run tests using `python3 manage.py test`
