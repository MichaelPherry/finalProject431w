Create Table full_movie_tab (adult bool, belongs_to_collection text, 
							 budget bigint,	genres text, homepage text, 
							 id int, imdb_id varchar,original_language varchar, 
							 original_title text,overview text, popularity float,
							 poster_path text, production_companies text, 
							 production_countries text, release_date date,
							 revenue bigint, runtime decimal, spoken_languages text,
							 status varchar, tagline text, title text, 
							 video bool, vote_average float, vote_count int);
select * from full_movie_tab

Copy full_movie_tab
from 'C:\Users\mj202\Desktop\School\Cmpsc 431W\Final_Project\movies_metadata.csv'
DELIMITER ','
CSV HEADER;

create table id_movie as
select id, title
from full_movie_tab;

alter table id_movie
add primary key (id);

create table id_rough as
select id, original_title
from full_movie_tab;

alter table id_rough
add primary key(id);

Create table Movie as
select genres, overview, title, tagline
from full_movie_tab;

alter table Movie
add primary key(title);

create table rough_draft as 
select original_title, original_language
from full_movie_tab;

alter table rough_draft
add primary key(original_title)

create table rating as
select id, popularity, vote_count, vote_average
from full_movie_tab;

alter table rating
add primary key(id)

create table languages as
select id, spoken_languages
from full_movie_tab;

alter table languages
add primary key(id)

create table dates as
select id, release_date, status
from full_movie_tab;

alter table dates
add primary key(id)

create table collection as
select id, genres, belongs_to_collection, adult, video
from full_movie_tab;

alter table collection
add primary key(id)

create table marketing as
select id, homepage, tagline, release_date, poster_path, overview
from full_movie_tab;

alter table marketing
add primary key(id)

create table length as
select id, runtime, video
from full_movie_tab;

alter table length
add primary key(id)

create table money as
select id, budget, revenue, revenue - budget
from full_movie_tab;

alter table money
add primary key(id)

create table company as
select id, production_companies, production_countries
from full_movie_tab;

alter table company
add primary key(id)
