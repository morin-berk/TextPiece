# TextPiece 
This is a student micro-project, a web service that can save, organize and search for pieces of text among already saved results. 
The aim is to learn FastAPI framework, Elasticsearch.

The service consists of two endpoints. The first saved a text piece object to the storage, 
the second allows searching text pieces. 

## Installation
The service uses Docker.

**docker-compose up --build** to build the image and run the web service for the first time.

**docker-compose down** to stop the container.

**docker-compose up -d** to run the container the next time.

## Getting started 
The web service runs on *localhost:8080*

Documentation: *localhost:8080/docs*

## Searching
Elasticsearch is used as a storage and a search system. 

If no params are specified, it returns list of all text pieces. 
Optional params allow filtering results. Can be used in any combination.
- *text* - search similar text;
- *text_type* - either "paragraph" or "title";
- *page_number*;
- *document_name*.

## Saving
Text piece is a json object, consisting of:
- *document_id* - also used as id for saving to index
- *text*
- *text_type*
- *page_number*
- *document_name*
