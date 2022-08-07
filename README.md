# Millenium-Falcon-Problem-Flask

## Description
Your mission is to create a web application to compute and display the odds that the Millennium Falcon reaches Endor in time and saves the galaxy.Your web application will be composed of a backend (the Millennium Falcon onboard computer), a front-end (C3PO) and a CLI (command-line interface aka R2D2). When it starts, the back-end service will read a JSON configuration file containing the autonomy, the path towards an SQLite database file containing all the routes, the name of the planet where the Millennium Falcon is currently parked (Tatooine) and the name of the planet that the empire wants to destroy (Endor). The SQLite database will contain a table named ROUTES. Each row in the table represents a space route. Routes can be travelled in any direction (from origin to destination or vice-versa). The front-end should consists of a single-page application offering users a way to upload a JSON file containing the data intercepted by the rebels about the plans of the Empire and displaying the odds (as a percentage) that the Millennium Falcon reaches Endor in time and saves the galaxy. The web page will display the probability of success as a number ranging from 0 to 100%. The command-line interface should consist of an executable that takes 2 files paths as input (respectively the paths toward the millennium-falcon.json and empire.json files) and prints the probability of success as a number ranging from 0 to 100.

## Implementation

For the following task Python programming language and Flask microframework were used. The reason behind framework selection is Flask being lightweight. It is also famous for being extensible. For the program a DFS algorithm was used to find all possible paths by recursively calling the function and checking the visited nodes (planets). The complexity of an algorithm is exponential.

* Python
* Flask

## How to run

### CLI
```bash
give-me-the-odds.py "./examples/example1/millennium-falcon.json" "./examples/example1/empire.json"
```

### Web App
```bash
(venvmf) app.py run
```

