# LSTMAnomalyDetection
## How to run
This project requires Docker, specifically Docker Compose. To start the application, simply run docker compose up. This process can be managed through the included Makefile. At any time, you can type make help in the terminal to view a list of available commands and usage instructions.

'''Bash
compose                        Run the docker compose
database                       Start only the database
help                           Show this help
loader                         Load the dataset into the database
'''

After you have run the loader and have the database, you can use the notebook to run network database models. If you have all the packages installed, which can be found in 'requirments.txt', you can run all to get all the model results. 