<h1>FastApi Backend</h1>

<h3>Setting up the application</h3>

Start a <a href="https://qdrant.tech/">Qdrant</a> instance with docker
```
docker pull qdrant/qdrant
docker run -p 6333:6333 qdrant/qdrant
```
Create a .env file and define the environment variable to connect to the databse
```
QDRANT_URL='http://localhost:6333'
QDRANT_COLLECTION_NAME=... # Not necessary for running the tests
```
Create a virtual environment
```bash
python -m venv .venv
```
Activate it
```
.venv\Scripts\activate.bat # on Windows
source .venv/bin/activate  # on Linux
```
Install pip-tools
```bash
python -m pip install pip-tools
```
Install requirements
```bash
pip-sync requirements.txt dev-requirements.txt
```
(Optional) Run the application
```
python -m src.main
```
<i>You can view the endpoints on `/docs`</i>


<h3>Running the tests</h3>

Run the following command in the root of the backend directory

```
pytest
```



<h1>React Frontend</h1>

<h3>Running the Frontend App</h3>

To start the Music Information Retrieval Web App Frontend, use the following command at the root of the frontend app:
```
npm start
```
This will launch the development server, and you can access the app at http://localhost:3000 in your web browser.


<h3>Running the tests</h3>

Tests are located in the ```__tests__``` folder at the root of the frontend app. To run the tests, use the following command:
```
npm test
```
This will execute the test suite and provide feedback on the test results.
