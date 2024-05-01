# Django Examples

A starter project for Clark's Corner. This project includes a web server and database.
Welcome to Clark’s Corner, your go-to online marketplace tailored for the Clark University community! At Clark’s Corner, users must sign in using a Clark email, ensuring that the users of this marketplace are in fact part of the Clark community, providing safety, reliability, and convenience. Users can explore a diverse range of products, categorized into things like Housing & Living and Electronics. Whether you’re searching for academic essentials or unique collectibles, our platform offers an extensive selection to cater to your needs. With features like user profiles, sellers can showcase their products, receive reviews, and manage their inventory effortlessly, like adding or removing products. Buyers can browse through seller profiles, leave reviews, and add items to their cart for a seamless shopping experience. At checkout, a receipt of the order is created, saved, and placed in the user’s “View Orders” section of their profile, so they can view their past orders and items they’ve bought. We also offer a search bar, so if there is a particular item you are looking for right off the bat, go ahead and search it and you will see all related items. Clicking on a particular item will bring you to our product page, which shows the item, its description, price, and seller. 

Notes about CRUD: 
All CRUD (Create, Read, Update, Delete) operations are supported either via the Django Admin Interface or via our web application itself. Creating a new user is supported by our web application when you click on the “sign up” button and are redirected to our sign-up page. You can read the profile information on either the web application (via the profile pages) or on the admin interface. The functionality of updating and deleting users stays within the Django Admin Interface. 

As for reviews, you are able to add a review and read the reviews on our web application (via the profile pages) but updating and deleting functionality is through the admin interface.  

For products, you can add or remove your own products from the database on the web application (via the profile page of the user who is signed in). You can also read all the products on the web page through all the different pages categorizing the products. For updating a product, you must do that through the Django Admin Interface.

For the has_in_cart table, you can add and remove items from your cart on our web app (via the “View My Cart” page on the profile page). You can view all the items of your cart in this same page. Updating the cart means adding or removing items from the cart, so that is covered, as mentioned. But again, these CRUD operations can also be done through the admin interface. 

For receipts, when a user checks out their cart, a receipt is automatically created and saved in the database, and then you can view all your receipts in the “View Orders” page of your profile page. In the real world, a user shouldn’t be able to edit or remove their past receipts, so this functionality remains in the Django Admin Interface. Also, when a user checks out, whatever items that were in their cart are removed from the product database, as they should be.

We understand that, ideally, more of the CRUD operations would be fully functional on our web application, however, given the time frame as well as the time we spent on debugging separate issues, this could be implemented in future work on this app.

Follow these steps to get started:

## Step 0: Clone This Repository

Unless otherwise specified, all commands mentioned below should be run within the root directory of this repository.

## Step 1: Install Docker

This project includes several components: 

- uWSGI, which will run your Django application code
- NGINX, a web server which will allow browsers to communicate with uWSGI
- PostgresSQL, a database which will store your application's persistent data

It could be time-consuming to install and configure all of these on your computer, but thankfully there is a better way: Docker! [Install Docker](https://docs.docker.com/get-docker/), and it will be easy to run all of these components.

## Step 2: Secure Configuration

It is a terrible idea to run software with default passwords. To configure the password for the database and other settings, you will need to write them in a `.env` file. Follow these steps:

1. Copy `dot_env_example` to `.env`
2. Run `chmod 600 .env` to prevent other users from reading your `.env` file
3. Edit `.env`, changing:
  - The text `RANDOM_PASSWORD` to a password which is actually random
  - The text `SOMETHING_LONG_AND_RANDOM` to random text, ideally generated using the Python one-liner below:

```
python3 -c "import string,random; uni=string.ascii_letters+string.digits; print(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))]))"
```

## Step 3: Ensure Installed Pillow Library and Start the Docker Services

Since we use ImageField() in one of the models for this project, you must have Pillow installed on your computer. You can follow the instructions here: https://pypi.org/project/pillow/

Once Pillow is installed, run:
```
docker compose up
```

The first time you run it, this command will take a few minutes to complete. This is because Docker needs to download the code for PostgresSQL, etc.

When you are done running the application, you can stop it by typing `Control-C`.

## Step 4: Run Migrations

Follow the instructions below to run the database migrations. This will ensure the database has the schema for the applications.

## Step 5: Load the Applications

Load <http://localhost:8080/admin> and you should be redirected to the "Django administration" login interface. Through this, you can add users and items to the database (must create a superuser first - see below).

Load <http://localhost:8080/clarkscorner> to view the web application. 


## Hints

### Creating Admin Accounts

To create a superuser, which can access the Django admin interface:

```
docker compose exec django python manage.py createsuperuser
```

To create a regular user, load `/admin/auth/user/add/` in your browser.

You can then log into the Django admin interface using this superuser account.

### Database Operations

#### Manual Commands

To interactively run SQL commands, run:

```
> docker compose exec postgres bash
# psql --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"
```

#### Migrations

When you edit Django models, the changes don't take effect until you update the database. This is done in two steps.

First, you create a migration file, which describes the changes to be made:

```
docker compose exec django python manage.py makemigrations
```

Then, you apply those changes by running the migration file:

```
docker compose exec django python manage.py migrate
```

You can read more about [Django migrations here](https://docs.djangoproject.com/en/3.2/topics/migrations/).

#### Dump

To dump the SQL commands needed to recreate a database to file, run:

```
> docker compose exec postgres bash
# pg_dump --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --file=/postgres_files/db_dump.DATE.sql
```

#### Load

To execute SQL commands from a file, run:

```
> docker compose exec postgres bash
# psql --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" --set ON_ERROR_STOP=on --file /postgres_files/db_dump.DATE.sql
```
