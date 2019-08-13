

### Licencing System

Simple subscription system emulating buying a yearly plan and attaching website(s) to it.

There are 3 business entities :

- Customer - has a name, a password an email address, a subscription and a subscription renewal date.
- Plan - has a name, a price, and a number of websites allowance.
- Website - has an URL, and a customer


Customer Actions
- Subscribe to plan
- Move from a plan to another
- Manage websites (add/update/remove)

###  Setting Up Project
- Setup virtual enviroment with python 3 and activate the enviroment
- clone the repository
    ```
    git clone https://github.com/tonyguesswho/Licencing-System.git
    ```

-   Install dependencies from requirements.txt file: (This is optional since it contains just linting packages)

    ```
    pip install -r requirements.txt
    ```
## Running tests
cd into the application folder and run

    ```
    python -m unittest discover  -v
    ```



