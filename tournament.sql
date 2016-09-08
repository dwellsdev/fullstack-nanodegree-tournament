-- Table definitions for the tournament project.

-- Makes resetting the database easier.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

-- Create players table.
CREATE TABLE players(
  player_id serial PRIMARY KEY,
  player_name text
);

-- Create matches table.
CREATE TABLE matches(
  match_id serial PRIMARY KEY,
  winner_id INTEGER,
  loser_id INTEGER,
  FOREIGN KEY(winner_id) REFERENCES players(player_id),
  FOREIGN KEY(loser_id) REFERENCES players(player_id)
);

-- Create view for results. The built-in sorting greatly simplifies the work
-- done in the python file. Items in the table are in the order required by
-- tests.
CREATE VIEW results AS
SELECT player.player_id AS player_id,
player.player_name AS player_name,
(SELECT COUNT(*) FROM matches
WHERE matches.winner_id = player.player_id) AS matches_won,
(SELECT COUNT(*) FROM matches
WHERE player.player_id IN (winner_id, loser_id)) AS matches_played
FROM players player GROUP BY player.player_id ORDER BY matches_won DESC;

-- Added rounds table for adding later functionality.
-- -- Create rounds table.
-- CREATE TABLE rounds(
--   round_id serial PRIMARY KEY,
--   player_id INTEGER,
--   player_name TEXT,
--   matches_won INTEGER,
--   FOREIGN KEY(player_id) REFERENCES players(player_id),
--   FOREIGN KEY(player_name) REFERENCES players(player_name),
--   FOREIGN KEY(matches_won) REFERENCES results(matches_won)
-- );
