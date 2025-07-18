-- Keep a log of any SQL queries you execute as you solve the mystery.

-- the theft took place on July 28, 2023 and that it took place on Humphrey Street

-- This query is used to see all of the crimes that took place on July 28, 2023 on Humphrey Street
-- and hopefully find the crime scene report that matches the date and location of the crime.
SELECT *
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
-- Description: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today.
-- with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
-- id number of the crime: 295

-- Since we know there are three witnesses, we should next check the transcripts of the interviews that took place on the day of the crime.
SELECT *
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28;
-- These are the transcripts to the three interviews.

-- Ruth, id = 161: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you
-- have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- Eugene, id = 162: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
-- I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- Raymond, id = 163: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard
-- the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other
-- end of the phone to purchase the flight ticket.

-- Now, lets take a chronological approach to solving the murder. First, we should identify all of the people that withdrew from an ATM on
-- Leggett Street. This query will allow us to see the account numbers of the people who withdrew money. Since the thief withdrew money on
-- the day of the murder at this ATM, one of these accounts belongs on the thief.
SELECT *
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Now we need to find the people associated with the account numbers. This can be done in two steps. The first step is to identify the
-- ids of the people who withdrew accounts at the ATM on Leggett Street on the day of the crime. Then we can identify the people's actual
-- names associated with those ids. This query identifies ids of the people who withdrew at the ATM on Leggett Street on the day of the crime.
SELECT *
FROM bank_accounts
WHERE account_number IN (
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
);

-- This query idenifies the actual people that withdrew at the ATM on Leggett Street on the day of the crime.
SELECT *
FROM people
WHERE id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN (
        SELECT account_number
        FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
    )
);

-- After completing this query, we now have eight suspects that could be the thief. However, more work needs to be done. Based on Ruth's testimony,
-- the thief left the bakery via car shortly after 10:15 am. Since we know the license plates for each individual, we can compare these license plates
-- to those found by the bakery's security logs to see if any of these plates overlap. The thief's license plate should overlap since they were at both
-- the ATM and bakery.

-- This query shows the bakery security logs on day of crime. Ruth mentioned that within ten minutes of the theft (10:15 am), the thief left the bakery,
-- meaning that the thief's activity would have taken place on any time between 10:05 am and 10:25 am.
SELECT *
FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 ORDER BY minute;

-- Now that we have all license plates that entered or existed the bakery from 10:05 am to 10:25 am, we can compare these plates to the plates who belong
-- to the people at the ATM. This query completes such comparison.
SELECT *
FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
    SELECT license_plate
    FROM people WHERE id IN (
        SELECT person_id
        FROM bank_accounts
        WHERE account_number IN (
            SELECT account_number
            FROM atm_transactions
            WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
        )
    )
)
ORDER BY minute;

-- Now, we have the license plates of the people who were at both the bakery and ATM on Leggett Street. This query identifies the people associated with
-- those license plates.
SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
        SELECT license_plate
        FROM people
        WHERE id IN (
            SELECT person_id
            FROM bank_accounts
            WHERE account_number IN (
                SELECT account_number
                FROM atm_transactions
                WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
            )
        )
    )
    ORDER BY minute
);

-- Now, we have four suspects: Iman, Luca, Diana, and Bruce. However, we are not done yet. Raymond's testimony mentions that the thief made a call
-- that was less than a minute in length. To identify the specific call, we should first look at all calls from the suspects that took place on the
-- day of the crime that were under a minute in length. This query shows all of the calls that meet such criteria.
SELECT *
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (
    SELECT phone_number
    FROM people
    WHERE license_plate IN (
        SELECT license_plate
        FROM bakery_security_logs
        WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
            SELECT license_plate
            FROM people
            WHERE id IN (
                SELECT person_id
                FROM bank_accounts
                WHERE account_number IN (
                    SELECT account_number
                    FROM atm_transactions
                    WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                )
            )
        )
        ORDER BY minute
    )
);

-- Based on the result of that query, there are two calls that were made from people that were at both the ATM and bakery. This query identifies the
-- people that initiated the conversation (they were the callers).
SELECT *
FROM people
WHERE phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (
        SELECT phone_number
        FROM people
        WHERE license_plate IN (
            SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
                SELECT license_plate
                FROM people WHERE id IN (
                    SELECT person_id
                    FROM bank_accounts
                    WHERE account_number IN (
                        SELECT account_number
                        FROM atm_transactions
                        WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                    )
                )
            )
            ORDER BY minute
        )
    )
);

-- Now, we have two suspects: Diana and Bruce. Unfortunately, there is not much left we can do with just the phone numbers and license plates, so the
-- next step is to identify the accomplices for each suspect. We can assume that each accomplice was on the receiving end of the conversations (they
-- were the receiver).

-- This query identifies the possible accomplices based on the possible suspects.
SELECT *
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (
        SELECT phone_number
        FROM people
        WHERE license_plate IN (
            SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
                SELECT license_plate
                FROM people WHERE id IN (
                    SELECT person_id
                    FROM bank_accounts
                    WHERE account_number IN (
                        SELECT account_number
                        FROM atm_transactions
                        WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                    )
                )
            )
            ORDER BY minute
        )
    )
);

-- Now, we have to accomplices: Philip and Robin. Based on some cross examination we can do ourselves from the last three SQL queries, it is clear
-- that Diana called Philip and Bruce called Robin. However, we still don't know definitively who the thief and accomplices are. To figure that out,
-- we need look more deeply into the flight information. We know that the thief went on a plane, so the first thing we can do next is to see which
-- airport the thief left from.

-- This query identifies all of the airports in Fiftyville. Since the thief was already in Fiftyville, it is likely that they will go to an airport
-- in Fiftyville to catch their flight.
SELECT *
FROM airports
WHERE city = 'Fiftyville'; -- id: 8

-- There is only one airport in Fiftyville named 'Fiftyville Regional Airport.' Since there is only one airport, this means that the thief went
-- here to catch their flight. Based on Raymond's testimony, the thief would take the first flight the next day. We should next look at all of
-- the flights that left Fiftyville on the next day (July 29, 2023) since the earliest flight the flight  the thief took.

-- This query identifies all of the flights leaving Fiftyville on July 29, 2023.
SELECT *
FROM flights
WHERE origin_airport_id = (
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
) AND year = 2023 AND month = 7 AND day = 29;

-- Based on the result, the earliest flight was at 8:20 am and headed to an airport with an id of 4. Since this was the earliest flight of the
-- day, this is the flight the thief took. However, we don't know what airport has an id of 4. Also, lets take note that the id of the flight
-- is 36, as we will need it later.

-- This query identifies the airport that has an id of 4.
SELECT *
FROM airports
WHERE id = 4;

-- The LaGuardia Airport in New York City has an id of 4. This means that the thief was headed to New York City. However, we still don't know
-- the identity of the thief. We can solve for that by identifying the passport numbers for the passengers on the flight and cross examining
-- them to the passport numbers of Diana and Bruce, our two suspects. Whichever individual's passport numbers match across the two queries
-- means that they are the thief.

-- people on the flight
-- This query identifies the people on the flight by their passport number. Notice how we use the flight id of 36 here because we need the
-- passport numbers on a specific flight, which can be called by using the flight id, which is unique to that specific flight.
SELECT *
FROM passengers
WHERE flight_id = 36;

-- Now that we have the passport numbers of all of the passengers on the flight, we can cross examine them with Diana's and Bruce's passports
-- to see if either of them are the thief.

-- This query identifies the passport number that belongs to the individual who was at the ATM, bakery, and on the flight.
-- This is the thief's passport number.
SELECT * FROM passengers WHERE passport_number IN (
    SELECT passport_number
    FROM people
    WHERE phone_number IN (
        SELECT caller
        FROM phone_calls
        WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (
            SELECT phone_number
            FROM people
            WHERE license_plate IN (
                SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
                    SELECT license_plate
                    FROM people WHERE id IN (
                        SELECT person_id
                        FROM bank_accounts
                        WHERE account_number IN (
                            SELECT account_number
                            FROM atm_transactions
                            WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                        )
                    )
                )
                ORDER BY minute
            )
        )
    )
) AND flight_id = 36;

-- Now, we can finally indenify the thief based on their passport number. This query idenifies the thief based on their passport number.
SELECT name FROM people WHERE passport_number IN (
    SELECT passport_number FROM passengers WHERE passport_number IN (
        SELECT passport_number
        FROM people
        WHERE phone_number IN (
            SELECT caller
            FROM phone_calls
            WHERE year = 2023 AND month = 7 AND day = 28 AND duration <= 60 AND caller IN (
                SELECT phone_number
                FROM people
                WHERE license_plate IN (
                    SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND license_plate IN (
                        SELECT license_plate
                        FROM people WHERE id IN (
                            SELECT person_id
                            FROM bank_accounts
                            WHERE account_number IN (
                                SELECT account_number
                                FROM atm_transactions
                                WHERE year = 2023 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'
                            )
                        )
                    )
                    ORDER BY minute
                )
            )
        )
    ) AND flight_id = 36
);

-- This reveals our thief, who is Bruce. This also means that Robin is his accomplice since Bruce called Robin for the plane ticket.

-- This is the final result:
-- The THIEF is: Bruce
-- The city the thief ESCAPED TO: New York City
-- The ACCOMPLICE is: Robin
