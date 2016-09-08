#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# To prevent injection attacks in new player registration.
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Delete matches from the database."""
    # Standard connection procedure.
    c = connect()
    cursor = c.cursor()

    cursor.execute('DELETE FROM matches')

    # Standard closing procedure.
    c.commit()
    c.close()


def deletePlayers():
    """Delete players from the database."""
    c = connect()
    cursor = c.cursor()

    cursor.execute('DELETE FROM players')

    c.commit()
    c.close()


def countPlayers():
    """Returns number of players in the database."""
    c = connect()
    cursor = c.cursor()

    cursor.execute('SELECT COUNT(*) FROM players')

    count = cursor.fetchone()[0]

    c.commit()
    c.close()

    return count


def registerPlayer(name):
    """Delete players from the database."""

    # Cleaning the passed name just in case.
    clean_name = bleach.clean(name, strip=True)

    c = connect()
    cursor = c.cursor()

    cursor.execute(
        "INSERT INTO players (player_name) VALUES (%s)", (clean_name,))

    c.commit()
    c.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = connect()
    cursor = c.cursor()

    cursor.execute("SELECT * FROM results")

    results = cursor.fetchall()
    return_val = []
    for result in results:
        # int() is required because an L is appended to each integer in the
        # results that are returned unless the number is converted.
        return_val.append(
            [result[0], result[1], int(result[2]), int(result[3])])

    c.close()

    return return_val


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = connect()
    cursor = c.cursor()

    cursor.execute(
        "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)", (winner, loser,))

    c.commit()
    c.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    c = connect()
    cursor = c.cursor()

    # Grab the rankings through the playerStandings function.
    ranking = playerStandings()

    c.close()

    pairs = []

    # Because the results view already sorts players by how many wins they have,
    # all we need to do here is drill down the list.
    while len(ranking) > 1:
        player_a = ranking.pop(0)
        player_b = ranking.pop(0)
        pairs.append((player_a[0], player_a[1], player_b[0], player_b[1]))

    return pairs
