# chore_log

*Earn minutes, play games*

## Distinctiveness and Complexity

### Models

This is the first project I've done that has two different types of users (apart from the standard Django admin). Models for `Parent` and `Child` both extend `User` but get different experiences with different permissions. This was a good opportunity for me to learn about [inheritance](https://docs.djangoproject.com/en/5.2/topics/db/models/#model-inheritance) and [why previous CS50 projects used `AbstractUser`](https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#extending-the-existing-user-model).

### Views

- **Delivering different templates**: This was the first project I've done where a view delivers a drastically different template based on what type of user is logged in. Parents and children get entirely different index pages.
- **More complicated permissions**: Parents can view their own index page and their children's pages, but not the pages of other parents or other parents' children. This was more complicated than previous projects, where the permissions were basically "you must be logged in to see this" and "you can only see your own stuff."
- Merging two different models (work and play) in one view - liberal `annotation` to support a `union`. In retrospect I wonder whether I should have had a single `transaction` model using fields to differentiate between `work` and `play`, but that would have been difficult when kids pick work from a pre-defined list but can define any game they want for themselves.

### Front end

The front end is where I have the most experience, and I enjoy keeping things light and concise. I did several things on the front end that previous homework projects did not call for:

- **No Bootstrap**: In contrast to the previous homework projects, I eschewed Bootstrap in favor of Flexbox and Grid for layout and [Open Props](https://open-props.style) for other styling.
- **Local storage for timer**:
- **View transitions to/from parent page to child page**:
- **Modals for log entries**: Small, simple bits of content often don't need their own page. I've been reading about using `dialog` to create modals where the browser takes care of semantics, keyboard accessibility, etc., but this was my first opporunity to experiment with it. Between this and view transitions, I'm getting most of the feel of an SPA without the complexity.
- **Lightweight autocomplete for game titles**: I didn't want to have to specify a list of games ahead of time, because my kids discover new games all the time. But just presenting the user an empty input field would require them to type the same game titles over and over again—annoying! Luckily, support for `datalist` is [now good enough](https://adactio.com/journal/21445) that I can progressively enhance a regular old `input type="text"` to provide autocomplete without restricting the user to predefined values.

## File By File

- models.py: 
- views.py: first time returning two values from one function, first time rendering different templates based on user type, first time limiting querysets
- forms.py
- tests.py
- templates

## How to run the application

