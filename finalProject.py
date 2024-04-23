import psycopg2
import random

def askUser():
    checker = True
    options = ["1", "2", "3", "4", "5", "6"]
    print("Please select a number corresponding to one of the listed options")
    while checker:
        number = input("1. Add a Movie\n"
                       "2. Remove a Movie\n"
                       "3. Update a Movie\n"
                       "4. Search about a Movie\n"
                       "5. Other\n"
                       "6. Exit\n")
        if number in options:
            checker = False
        else:
            print("Please select a number corresponding to one of the listed options")
    return number

def optionsList(cursor, connection):
    number = None

    while number != "6":
        number = askUser()
        if number == "1":
            addMovie(cursor, connection)
        elif number == "2":
            removeMovie(cursor, connection)
        elif number == "3":
            updateMovie(cursor, connection)
        elif number == "4":
            searchMovie(cursor)
        elif number == "5":
            other(cursor, connection)
    print("Thank you for using the CLI")

def addMovie(cursor, connection):
    movie = input("What movie would you like to add?\n")
    real = "SELECT COUNT(*) FROM movie WHERE title ILIKE %s"
    cursor.execute(real, (movie,))
    exist = cursor.fetchone()[0]
    if exist is not None and exist != 0:
        print("That movie is already in our list.")
    else:
        try:
            cursor.execute("SELECT MAX(ID) FROM id_movie")
            id_get = cursor.fetchone()[0]
            id_get += 1
            genres = input(
                "What type of genres is this movie? Please enter your answer in a list separated by commas\n")
            genres_list = genres.split(",")
            genre_answer = []
            rand = random.randint(1, 15000)
            for genre in genres_list:
                genre_answer.append([f"id:{rand}, name:{genre}"])
            ask_over = input("Would you like to give a description of the movie? (y/n)\n")
            if ask_over == 'y':
                overview = input("Write a quick description!\n")
            else:
                overview = None

            cursor.execute("INSERT INTO movie (genres, overview, title, tagline) VALUES (%s, %s, %s, %s)",
                           (genre_answer, overview, movie, None))
            cursor.execute("INSERT INTO id_movie (id, title) VALUES (%s, %s)", (id_get, movie))
            cursor.execute("INSERT INTO id_rough (id, original_title) VALUES (%s, %s)", (id_get, movie))
            cursor.execute("INSERT INTO rough_draft (id, original_title, original_language) VALUES (%s, %s, %s)",
                           (id_get, movie, None))
            cursor.execute("INSERT INTO rating (id, popularity, vote_count, vote_average) VALUES (%s, %s, %s, %s)",
                           (id_get, None, None, None))
            cursor.execute("INSERT INTO languages (id, spoken_languages) VALUES (%s, %s)", (id_get, None))
            cursor.execute("INSERT INTO dates (id, release_date, status) VALUES (%s, %s, %s)",
                           (id_get, None, "Released"))
            cursor.execute(
                "INSERT INTO collection (id, genres, belongs_to_collection, adult, video) VALUES (%s, %s, %s, %s, %s)",
                (id_get, genre_answer, None, None, None))
            cursor.execute(
                "INSERT INTO marketing (id, homepage, tagline, release_date, poster_path, overview) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_get, None, None, None, None, overview))
            cursor.execute("INSERT INTO length (id, runtime, video) VALUES (%s, %s, %s)", (id_get, None, None))
            cursor.execute("INSERT INTO money (id, budget, revenue) VALUES (%s, %s, %s)", (id_get, 0, 0))
            cursor.execute("INSERT INTO company (id, production_companies, production_countries) VALUES (%s, %s, %s)",
                           (id_get, None, None))
            connection.commit()

            print("Movie was added to our database!")
        except Exception as message:
            connection.rollback()
            print("Error occurred. Movie was not added because: ", message)

def removeMovie(cursor, connection):
    movie = input("What movie would you like to remove?\n")
    real = "SELECT COUNT(*) FROM movie WHERE title ILIKE %s"
    cursor.execute(real, (movie,))
    exist = cursor.fetchone()[0]
    if exist is not None and exist != 0:
        try:
            action = "SELECT id FROM id_movie WHERE title ILIKE %s"
            cursor.execute(action, (movie,))
            id_grabbed = cursor.fetchone()[0]
            action = "SELECT original_title FROM id_rough WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            orig_title = cursor.fetchone()
            cursor.execute("DELETE FROM movie WHERE title ILIKE %s", (movie,))
            action = "DELETE FROM id_movie WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM id_movie WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM id_rough WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            cursor.execute("DELETE FROM rough_draft WHERE original_title ILIKE %s", (orig_title,))
            action = "DELETE FROM rating WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM languages WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM dates WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM collection WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM marketing WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM length WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM money  WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            action = "DELETE FROM company WHERE id = %s"
            cursor.execute(action, (id_grabbed,))
            connection.commit()
            print("Movie was deleted from our database!")
        except Exception as message:
            connection.rollback()
            print("Could not delete movie because: ", message)
    else:
        print("That movie doesn't exist in our database")

def updateMovie(cursor, connection):
    movie = input("What movie would you like to update?")
    real = "SELECT COUNT(*) FROM movie WHERE title ILIKE %s"
    cursor.execute(real, (movie,))
    exist = cursor.fetchone()[0]
    if exist is not None and exist != 0:
        action = "SELECT id FROM id_movie WHERE title ILIKE %s"
        cursor.execute(action, (movie,))
        id_grabbed = cursor.fetchone()[0]
        action = "SELECT original_title FROM id_rough WHERE id = %s"
        cursor.execute(action, (id_grabbed,))
        orig_title = cursor.fetchone()
        options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        table = None
        while table not in options:
            table = input("What table would you like to update related to that movie?\n"
                          "1. Collection\n"
                          "2. Company\n"
                          "3. Dates\n"
                          "4. Rough Draft\n"
                          "5. Length\n"
                          "6. Marketing\n"
                          "7. Money\n"
                          "8. Movie\n"
                          "9. Exit\n")
        try:
            if table == "1":
                column = None
                opt_list = ["1", "2", "3", "4"]
                while column not in opt_list:
                    column = input("What from categories would you like to update?\n"
                                   "1. Genres\n"
                                   "2. Collection the movie belongs to\n"
                                   "3. Should kids watch this movie\n"
                                   "4. Exit\n")
                if column == "1":
                    genres = input("What are the genres of this movie? Please separate the list by commas.\n")
                    genres_list = genres.split(",")
                    genre_answer = []
                    rand = random.randint(1, 15000)
                    for genre in genres_list:
                        genre_answer.append([f"id:{rand}, name:{genre}"])
                    cursor.execute("UPDATE collection SET genres = %s WHERE id = %s", (genre_answer, id_grabbed))
                    cursor.execute("UPDATE movie SET genres = %s WHERE title = %s", (genre_answer, movie))
                elif column == "2":
                    collection = input("What movie franchise does this movie belong to?\n")
                    cursor.execute("UPDATE collection SET belongs_to_collection = %s WHERE id = %s",
                                   (collection, id_grabbed))
                elif column == "3":
                    age_rest = input("Should kids be able to watch this movie?(y/n)\n")
                    if age_rest == 'y':
                        age_rest = True
                    else:
                        age_rest = False
                    cursor.execute("UPDATE collection SET adult = %s WHERE id = %s", (age_rest, id_grabbed))
            elif table == "2":
                column = None
                opt_list = ["1", "2", "3"]
                while column not in opt_list:
                    column = input("What from company would you like to update?\n"
                                   "1. Production Company\n"
                                   "2. Production Country\n"
                                   "3. Exit\n")
                if column == "1":
                    company = input("What company helped make the movie?\n")
                    cursor.execute("UPDATE company SET production_companies = %s WHERE id = %s", (company, id_grabbed))
                elif column == "2":
                    country = input("What country was the movie made in?\n")
                    cursor.execute("UPDATE company SET production_countries = $s WHERE id = %s", (country, id_grabbed))
            elif table == "3":
                column = None
                opt_list = ["1", "2", "3"]
                while column not in opt_list:
                    column = input("What from dates would you like to update?\n"
                                   "1. Release Date\n"
                                   "2. Status of movie\n"
                                   "3. Exit\n")
                if column == "1":
                    release = input("What should the release date be?\n")
                    cursor.execute("UPDATE dates SET release_date = %s WHERE id = %s", (release, id_grabbed))
                    cursor.execute("UPDATE marketing SET release_date = %s WHERE id = %s",(release, id_grabbed))
                elif column == "2":
                    status = input("Is the movie released or not?(y/n)")
                    if status == "y":
                        status = True
                    else:
                        status = False
                    cursor.execute("UPDATE dates SET status = %s WHERE id = %s", (status,id_grabbed))
            elif table == "4":
                column = None
                opt_list = ["1", "2", "3"]
                while column not in opt_list:
                    column = input("What from rough draft would you like to update?\n"
                                   "1. Original Title\n"
                                   "2. Original Language\n"
                                   "3. Exit\n")
                if column == "1":
                    title = input("What was the original title?\n")
                    cursor.execute("UPDATE rough_draft SET original_title = %s WHERE original_title = %s", (title, orig_title))
                    orig_title = title
                    cursor.execute("UPDATE id_rough SET original_title = %s WHERE id = %s", (title, id_grabbed))
                elif column == "2":
                    lang = input("What was the original language for the movie?\n")
                    cursor.execute("UPDATE rough_draft SET original_language = %s WHERE original_title = %s", (lang, orig_title))
            elif table == "5":
                run = input("What should the runtime be?\n")
                cursor.execute("UPDATE length SET runtime = %s WHERE id = %s", (run, id_grabbed))
            elif table == "6":
                column = None
                opt_list = ["1", "2", "3", "4", "5"]
                while column not in opt_list:
                    column = input("What from marketing would you like to update?\n"
                                   "1. Homepage\n"
                                   "2. Tagline\n"
                                   "3. Release Date\n"
                                   "4. overview"
                                   "5. Exit")
                if column == "1":
                    url = input("What is the url to the homepage?\n")
                    cursor.execute("UPDATE marketing SET homepage = %s WHERE id = %s",(url, id_grabbed))
                elif column == "2":
                    tag = input("What should the tagline of the movie be?\n")
                    cursor.execute("UPDATE marketing SET tagline = %s WHERE id = %s", (tag, id_grabbed))
                    cursor.execute("UPDATE movie SET tagline = %s WHERE title = %s", (tag, movie))
                elif column == "3":
                    release = input("What should the release date be?\n")
                    cursor.execute("UPDATE dates SET release_date = %s WHERE id = %s", (release, id_grabbed))
                    cursor.execute("UPDATE marketing SET release_date = %s WHERE id = %s",(release, id_grabbed))
                elif column == "4":
                    over = input("What should the overview of the movie be?\n")
                    cursor.execute("UPDATE marketing SET overview = %s WHERE id = %s", (over, id_grabbed))
                    cursor.execute("UPDATE movie SET overview = %s WHERE title = %s", (over, movie))
            elif table == "7":
                column = None
                opt_list = ["1", "2", "3"]
                while column not in opt_list:
                    column = input("What from money would you like to update?\n"
                                   "1. Budget\n"
                                   "2. Revenue\n"
                                   "3. Exit")
                if column == "1":
                    bud = input("What was the budget for the movie?\n")
                    cursor.execute("UPDATE money SET budget = %s WHERE id = %s", (bud, id_grabbed))
                elif column == "2":
                    rev = input("What was the revenue made for this movie?\n")
                    cursor.execute("UPDATE money SET revenue = %s WHERE id = %s", (rev, id_grabbed))
            elif table == "8":
                column = None
                opt_list = ["1", "2", "3", "4", "5"]
                while column not in opt_list:
                    column = input("What from movie would you like to update?\n"
                                   "1. Genres\n"
                                   "2. Overview\n"
                                   "3. Title\n"
                                   "4. Tagline\n"
                                   "5. Exit\n3")
                if column == "1":
                    genres = input("What are the genres of this movie? Please separate the list by commas.\n")
                    genres_list = genres.split(",")
                    genre_answer = []
                    rand = random.randint(1, 15000)
                    for genre in genres_list:
                        genre_answer.append([f"id:{rand}, name:{genre}"])
                    cursor.execute("UPDATE collection SET genres = %s WHERE id = %s", (genre_answer, id_grabbed))
                    cursor.execute("UPDATE movie SET genres = %s WHERE title = %s", (genre_answer, movie))
                elif column == "2":
                    over = input("What should the overview of the movie be?\n")
                    cursor.execute("UPDATE marketing SET overview = %s WHERE id = %s", (over, id_grabbed))
                    cursor.execute("UPDATE movie SET overview = %s WHERE title = %s", (over, movie))
                elif column == "3":
                    title = input("What is the real name of this movie?\n")
                    cursor.execute("UPDATE movie SET title = %s WHERE title = %s",(title, movie))
                    movie = title
                    cursor.execute("UPDATE id_movie SET title = %s WHERE id = %s", (title, id_grabbed))
                elif column == "4":
                    tag = input("What should the tagline of the movie be?\n")
                    cursor.execute("UPDATE marketing SET tagline = %s WHERE id = %s", (tag, id_grabbed))
                    cursor.execute("UPDATE movie SET tagline = %s WHERE title = %s", (tag, movie))
            connection.commit()
            print("Thank you for updating!")
        except Exception as message:
            connection.rollback()
            print("Could not update because: ", message)
    else:
        print("Movie is not in our database.")

def searchMovie(cursor):
    movie = input("What movie would you like to learn more about?\n")
    real = "SELECT COUNT(*) FROM movie WHERE title ILIKE %s"
    cursor.execute(real, (movie,))
    exist = cursor.fetchone()[0]
    if exist is not None and exist != 0:
        action = "SELECT id FROM id_movie WHERE title ILIKE %s"
        cursor.execute(action, (movie,))
        id_grabbed = cursor.fetchone()[0]
        action = "SELECT original_title FROM id_rough WHERE id = %s"
        cursor.execute(action, (id_grabbed,))
        orig_title = cursor.fetchone()
        options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
        table = None
        while table not in options:
            table = input("What would you like to know about the movie?\n"
                          "1. Collection\n"
                          "2. Company\n"
                          "3. Dates\n"
                          "4. Languages\n"
                          "5. Length\n"
                          "6. Marketing\n"
                          "7. Money\n"
                          "8. Movie\n"
                          "9. Rating\n"
                          "10. Rough Draft\n"
                          "11. Exit\n")
        if table == "1":
            cursor.execute("SELECT genres, belongs_to_collection, adult, video FROM collection WHERE id = %s", (id_grabbed,))
            print("The information is genres, what collection it may belong to, if kids should watch this movie, video type")
        elif table == "2":
            cursor.execute("SELECT production_companies, production_countries FROM company WHERE id = %s", (id_grabbed,))
            print("The information is the company that helped make the move, where the movie was made")
        elif table == "3":
            cursor.execute("SELECT release_date, status FROM dates WHERE id = %s", (id_grabbed,))
            print("The information is release date of the movie, if the movie is released yet or not")
        elif table == "4":
            cursor.execute("SELECT spoken_languages FROM languages WHERE id = %s", (id_grabbed,))
            print("The information is languages the movie is in")
        elif table == "5":
            cursor.execute("SELECT runtime, video FROM length WHERE id = %s", (id_grabbed,))
            print("The information is the runtime of the movie, and video type")
        elif table == "6":
            cursor.execute("SELECT homepage, tagline, release_date, poster_path, overview FROM marketing WHERE id = %s", (id_grabbed,))
            print("The information is the homepage, tagline, release date of the movie, poster path, overview of the movie")
        elif table == "7":
            cursor.execute("SELECT budget, revenue FROM money WHERE id = %s", (id_grabbed,))
            print("The information is the budget, revenue")
        elif table == "8":
            cursor.execute("SELECT genres, overview, title, tagline FROM movie WHERE title ILIKE %s", (movie,))
            print("The information is genres, overview, title, and tagline")
        elif table == "9":
            cursor.execute("SELECT popularity, vote_count, vote_average FROM rating WHERE id = %s", (id_grabbed,))
            print("The information is the popularity, vote count and average of the movie")
        elif table == "10":
            cursor.execute("SELECT original_title, original_language FROM rough_draft WHERE original_title ILIKE %s", (orig_title,))
            print("The information is the original title and language of the movie")
        results = cursor.fetchall()
        print(results, "\n")
        print("Hope you found what you were looking for!")
    else:
        print("Movie is not in our database.")

def other(cursor, connection):
    options = ["1", "2", "3", "4"]
    num = None
    while num not in options:
        num = input("What are you looking for?\n"
                    "1. Movies by most profit\n"
                    "2. Movie profit based off of runtime\n"
                    "3. Movie profit higher than average profit\n"
                    "4. Exit\n")
    if num == "1":
        lim = input("How long would you like the list to be?\n")
        try:
            lim = int(lim)
            check = lim + 1
        except:
            lim = 5
        cursor.execute("SELECT t.title, (m.revenue - m.budget) AS profit FROM id_movie AS t JOIN money AS m ON t.id = m.id ORDER BY profit DESC LIMIT %s", (lim,))
        profit_lis = cursor.fetchall()
        for movie in profit_lis:
            print(movie)
    elif num == "2":
        lim = input("How long would you like the list to be?\n")
        try:
            lim = int(lim)
            check = lim + 1
        except:
            lim = 5
        cursor.execute("SELECT l.runtime, AVG(m.revenue - m.budget) AS avg_profit FROM length AS l JOIN money AS m ON l.id = m.id GROUP BY l.runtime ORDER BY avg_profit DESC LIMIT %s", (lim,))
        avg_prof_time = cursor.fetchall()
        print("Min | Profit")
        for ans in avg_prof_time:
            ans0 = ans[0]
            ans0 = str(ans0)
            ans0 = ans0.replace('Decimal', '')
            ans0 = ans0.replace('(', '')
            ans0 = ans0.replace(')', '')
            ans1 = ans[1]
            ans1 = float(ans1)
            ans1 = str(ans1)
            ans1 = ans1.replace('Decimal', '')
            ans1 = ans1.replace('(', '')
            ans1 = ans1.replace(')', '')
            print(ans0,"|",ans1)

    elif num == "3":
        lim = input("How long would you like the list to be?\n")
        try:
            lim = int(lim)
            check = lim + 1
        except:
            lim = 5
        cursor.execute("SELECT t.title, (m.revenue - m.budget) AS profit FROM id_movie AS t JOIN money AS m on t.id = m.id WHERE (m.revenue - m.budget) > (SELECT AVG(revenue - budget) FROM money) ORDER BY profit ASC LIMIT %s", (lim,))
        movies = cursor.fetchall()
        for ans in movies:
            print(ans)
    print("Cool stuff, right!")

def user_hookup():
    database_hookup = {"dbname": "finalProject", "user": "postgres", "password": "meateater2", "host": "localhost",
                       "port": "5432"}
    connection = psycopg2.connect(**database_hookup)
    connection.autocommit = False
    cursor = connection.cursor()
    optionsList(cursor, connection)
    cursor.close()
    connection.close()


if __name__ == '__main__':
    user_hookup()
