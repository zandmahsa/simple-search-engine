# The Simple Search Engine



## Introduction

Welcome to "The Simple Search Engine" – our first project for the course "Artificial Intelligence and the Web." This project is a demonstration of integrating AI concepts with web technologies to create a basic search engine. Our aim is to provide a simplified but functional example of how search engines operate, leveraging artificial intelligence for data crawling and retrieval.

https://gitlab.gwdg.de/m.zandkhanehshahri/aiweb-project-mm1.git



## Getting Started

To get started with "The Simple Search Engine," follow the steps outlined below. Make sure you have all the necessary dependencies installed before proceeding.

### Prerequisites

python 
requests
beautifulsoup4
flask
woosh


## Running the Application

To run the application, follow these steps in the given order:

### 1-Start the Crawler

Run the crawler.py script to crawl and index the data.

```
python crawler.py

```

### 2-Configure the Application:

Next, run the config.py script to configure the application settings.

```
python config.py

```

### 3-Launch the Flask Application:

Finally, start the Flask application by running flask_app.py.

```
python flask_app.py

```


Upon successful execution, the Flask server will start, and you can access the application through your web browser at the address provided in the console (usually http://localhost:5000).


## Usage

After launching the application, use the web interface to submit search queries. The application will display results based on the data indexed by the crawler.

## Contributing
We welcome contributions and suggestions to improve this project. Please feel free to fork the repository and submit pull requests.

