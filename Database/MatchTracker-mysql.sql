-- If the database exists, drop it
-- Then create the new database
-- And use it
DROP DATABASE IF EXISTS MatchTracker;
CREATE DATABASE MatchTracker;
USE MatchTracker;

CREATE TABLE Game(
    game_id VARCHAR(6) PRIMARY KEY, 
    game_name VARCHAR(50) NOT NULL,
    game_rules TEXT,
    game_team_size INT
    -- INSERT DERIVED -- 
);


CREATE TABLE Tournament(
    tournament_id VARCHAR(6) PRIMARY KEY,
    tournament_name VARCHAR(50),
    tournament_rules TEXT,
    tournament_duration VARCHAR(30),
    tournament_schedule DATETIME,
    tournament_format VARCHAR(30)
    -- INSERT DERIVED --
);


CREATE TABLE MatchInfo(
    match_id        VARCHAR(6) PRIMARY KEY,
    match_rounds    INT,
    match_date_time DATETIME,
    match_results   TEXT
    -- INSERT DERIVED --  
);


CREATE TABLE Team(
    team_id           VARCHAR(6)  PRIMARY KEY, 
    team_name         VARCHAR(50) NOT NULL,
    team_region       VARCHAR(30),
    team_achievements TEXT,
    team_earnings     DECIMAL(8, 2)
    -- INSERT DERIVED --  
);


CREATE TABLE Player(
    player_id        VARCHAR(6)   PRIMARY KEY,
    player_username  VARCHAR (30) NOT NULL,
    player_real_name VARCHAR (50),
    player_role      VARCHAR(30),
    player_rank      VARCHAR(20),
    player_aliases   TEXT,
    player_age       INT,
    player_games     TEXT
    -- INSERT DERIVED --  
);


CREATE TABLE Placement(
    placement_id           VARCHAR(6) PRIMARY KEY,
    placement_rank         TEXT,
    placement_points       VARCHAR(3),
    placement_prize_amount DECIMAL(6,2)
    -- INSERT DERIVED --  
);


CREATE TABLE Venue(
    venue_id       VARCHAR(9) PRIMARY KEY,
    venue_name     VARCHAR(30),
    venue_location VARCHAR(30),
    venue_capacity INT
    -- INSERT DERIVED --  
);


CREATE TABLE PrizePool(
    prize_pool_id          VARCHAR(6),
    prize_pool_id_amount   INT,
    prize_pool_id_currency TEXT
    -- INSERT DERIVED --
);


CREATE TABLE Sponsor(
    sponsor_id      VARCHAR(6) PRIMARY KEY,
    sponsor_name    VARCHAR(50) NOT NULL,
    sponsor_type    VARCHAR(30),
    sponsor_contact VARCHAR(50)
    -- INSERT DERIVED --
);


CREATE TABLE Commentator(
    commentator_id         VARCHAR(6) PRIMARY KEY,
    commentator_name       VARCHAR(50) NOT NULL,
    commentator_experience VARCHAR(30),
    commentator_language   TEXT
    -- INSERT DERIVED --
);


CREATE TABLE Organizer(
    organizer_id           VARCHAR(6) PRIMARY KEY,
    organizer_name         VARCHAR(50) NOT NULL,
    organizer_organization VARCHAR(50),
    organizer_contact      VARCHAR(50)
    -- INSERT DERIVED --
);


CREATE TABLE Manager(
    manager_id             VARCHAR(6) PRIMARY KEY,
    manager_name           VARCHAR(50) NOT NULL,
    manager_contact        VARCHAR(30)
    -- INSERT DERIVED --
);


CREATE TABLE Coach(
    coach_id        VARCHAR(6) PRIMARY KEY,
    coach_name      VARCHAR(50) NOT NULL,
    coach_specialty VARCHAR(50)
    -- INSERT DERIVED --
);
