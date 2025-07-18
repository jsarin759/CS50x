-- list the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred
SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id WHERE person_id = (
    SELECT id
    FROM people
    WHERE name = 'Bradley Cooper'
)
AND id IN (
    SELECT id
    FROM movies
    JOIN stars ON movies.id = stars.movie_id
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = 'Jennifer Lawrence'
    )
);
