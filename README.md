# PROJECT MINI SUPERMARKET APP
This is a project to build mini supermarket management software, including Account, Role, Permission, Invoice, Product, Receipt, Purchase Order, Supplier, Product Categories, Lot, Goods delivery note models and models with role as mediator.
- Account: this model is used to manage users and their accounts, each user has a unique account
- Role: this is a model for managing employee positions
- Permission: this is the model for managing the rights that users can do on the system
- Invoice: this is the model for managing sales invoices
- Product: this is the model to manage the products sold in the supermarket
- Receipt: this is the model for managing the receipt of goods in the warehouse
- Purchase Order: this is the model for managing orders from suppliers
- Supplier: this is the model for managing suppliers
- Product Categories: this is a model for managing goods such as dry food, alcoholic beverages, soft drinks,...
- Lot: this is a model to manage the lot number of goods, ensuring that goods are imported and exported according to the FIFO . principle
- Goods delivery note: this is the model to manage the delivery note out of the warehouse  

## Required
- To run the project, you need to install python version 3.11 or higher and install the environments to use python.
- Install django
 >pip install django 

## How to use
### For Linux or MacOS operating systems, replace py with python
1. First, clone this repository on your computer
> git clone git@github.com:hothanhtuan1209/mini_supermarket_project.git

2. Next, move into the directory containing this file:
> cd mini_supermarket_project
> cd myproject

3. Checkout to branch develop
> git checkout develop

4. Create database
> py manage.py makemigrations supermarket_manager 
> py manage.py migrate

5. Create role and permission
> py manage.py create_permissions_and_role

6. Create superuser
> py manage.py createsuperuser

7. Running server
>py manage.py runserver
 - Go to Web browser and search localhost:8000

8. Login superuser account
 - Login with account superuser

## How to fix csrf token error in Postman (403 forbidden)
 - In Headers of request, enter key = 'X-CSRFToken' and value '{{csrftoken}}'
 - Create a environment with name is 'Token' and Variable is 'csrftoken'
 - In Tests of request, enter 'var xsrfCookie = postman.getResponseCookie("csrftoken"); postman.setEnvironmentVariable('csrftoken', xsrfCookie.value);'

## Contribute
 - If you want to contribute to this project, please create a pull request and clearly describe the changes you propose