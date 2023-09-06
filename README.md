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
1. First, clone this repository on your computer
>git clone git@github.com:hothanhtuan1209/mini_supermarket_project.git

2. Next, move into the directory containing this file:
>cd training_python
>cd Django

3. Checkout to branch develop
> git checkout develop

4. Create database
> py manage.py migrate

5. Running server
>py manage.py server
 - Go to Web browser and search localhost:8000

6. Create new Role and Permission first
 - Roles and permissions need to be created before the account

7. Create superuser
> py manage.py createsuperuser

8. Login superuser account
 - Log in with account superuser to check the newly created Roles and Permissions
 
 ## Contribute
 - If you want to contribute to this project, please create a pull request and clearly describe the changes you propose
