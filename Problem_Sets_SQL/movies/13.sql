-- list the names of all people who starred in a movie in which Kevin Bacon also starred
SELECT name
FROM people
JOIN stars ON people.id = stars.person_id
WHERE movie_id IN (
    SELECT movies.id
    FROM movies
    JOIN stars ON movies.id = stars.movie_id
    JOIN people ON stars.person_id = people.id
    WHERE name = 'Kevin Bacon' AND birth = 1958
)
AND people.name != 'Kevin Bacon';
