# Repository for Jon Martin's personal python projects
Updated 7/27/2022

## Most Notable Overall (and why)
 - Apache Kafka
   - Real-time data streaming experience
   - I built it out end-to-end myself (lots of reading the docs)
   - Find it under ./data_engineering/apache_kafka
 - Playlist Curator
   - Utilizes Spotify's API
   - Applied cosine distance for recommending songs
   - Find it under ./ml/playlist_curator
 - DB Search
   - No-code solution for SQL queries
   - Shows understanding of SQL
   - There's even functionality for exporting to Excel
   - Find it under ./tkinter
 - Prefect
   - Similar to Airflow, Prefect is a ETL pipeline in python
   - Find it under ./data_engineering/prefect

## Layout Guide
Here's how I organize my projects. I've bolded the projects mentioned above in Most Notable Overall.

#### Cybernetics
 - Python implementations of cybernetics principles (like transformers) from *An Introduction to Cybernetics* by W. Ross Ashby
  - The smallest directory
  
#### Data Engineering
 - Projects using different 3rd party "pipelines":
   - **Apache Kafka** &mdash; all of the groundwork I laid for my implementation in Docker created for my senior capstone at Kansas State University (an autonomous agroponics system)
   - **Prefect** &mdash; a light version of Airflow, incredibly cool to utilize and try to structure my code in a new way
 - And an ETL example I made to show to some underclassmen (the bare bones basics)
 
 #### Fun
  - My catch-all for code that didn't fall into a specific category
  - The notable ones:
    - Monopoly Bank &mdash; I wanted to automate the Monopoly bank functionality for when I'm playing with my friends
    - Query Compare &mdash; I was comparing a couple of SQL queries for some Excel reports I had to make
    - Page Editor &mdash; One of my first ever pieces of code in python :)

#### General Data
 - Two main components:
   - Stocks &mdash; I made a command line app to refresh data for specified ticker symbols
   - Data Viz &mdash; Just a notebook for trying out new plotting functions I read about. Uses OWID COVID data
   
#### ML
 - A pretty wide variety of projects here:
   - **Playlist Curator** &mdash; not implemented with ML yet, but uses cosine distance to recommend songs utilizing Spotify's API
   - Pycaret &mdash; cool new auto-ML python library, you should give it a look if you haven't heard of it
   - COVID &mdash; my first ever attempt at ML, before I took a course in ML or anything so it's a mess
   - Wikipedia NLP &mdash; I webscraped some data from Wikipedia and wanted to try out tf-idf, something I'd read about but never utilized
   - Exercises &mdash; just some practice exercises from a Udemy course I did, *Data Science Bootcamp*
   
#### Tkinter
 - One of the first libraries I ever used in python, Tkinter remains an old love of mine
 - Many, many projects here:
   - **DB Search** &mdash; I wanted to create a no-code solution for building SQL queries. Kind of works, missing some small but crucial details on how tables relate to each other (only uses set intersections currently)
   - SWSE Business Management &mdash; I play as a "businessman" in a DnD campaign with friends and wanted to create a POS system for my character.
   - RPG &mdash; a fun ascii RPG that you can move around in (has a cool implementation for that, if you've got time)

#### Utility Testing
 - Niche testing stuff that I didn't want to bog down the Fun directory with

#### Web
 - Web related things, of course, ranging from websites to webscraping
 - I keep a lot of these for reference with new projects
 - Quick explanation:
   - Django Test &mdash; a simple example django tutorial I followed
   - Flask Test &mdash; same as Django Test, just trying out Flask
   - Streamlit &mdash; trying out streamlit (very very cool python library, check it out)
   - Webscraping &mdash; a sub-directory for various one-off webscrape attempts
