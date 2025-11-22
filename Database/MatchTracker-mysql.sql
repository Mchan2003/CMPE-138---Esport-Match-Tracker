-- Match Maker Database -- 
-- DROP & CREATE TABLE --
DROP DATABASE IF EXISTS MatchTracker;
CREATE DATABASE MatchTracker;
USE MatchTracker;

-- TABLES --
CREATE TABLE UserAccount (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(50) UNIQUE NOT NULL,
    password_hash  VARCHAR(255) NOT NULL,
    role           ENUM('admin', 'user') DEFAULT 'user'
);

INSERT INTO UserAccount (username, password_hash, role)
VALUES ('admin', 'XXXXXXXXXX', 'admin');

CREATE TABLE Game(
    game_id VARCHAR(6) PRIMARY KEY, 
    game_name VARCHAR(50) NOT NULL,
    game_rules TEXT,
    game_team_size INT
);

CREATE TABLE Venue(
    venue_id       VARCHAR(9) PRIMARY KEY,
    venue_name     VARCHAR(30),
    venue_location VARCHAR(30),
    venue_capacity INT
);

CREATE TABLE PrizePool(
    prize_pool_id       VARCHAR(6) PRIMARY KEY,
    prize_pool_amount   INT,
    prize_pool_currency TEXT
);

CREATE TABLE Sponsor(
    sponsor_id      VARCHAR(6) PRIMARY KEY,
    sponsor_name    VARCHAR(50) NOT NULL,
    sponsor_type    VARCHAR(30),
    sponsor_contact VARCHAR(50)
);

CREATE TABLE Commentator(
    commentator_id         VARCHAR(6) PRIMARY KEY,
    commentator_name       VARCHAR(50) NOT NULL,
    commentator_experience VARCHAR(30),
    commentator_language   TEXT
);

CREATE TABLE Organizer(
    organizer_id           VARCHAR(6) PRIMARY KEY,
    organizer_name         VARCHAR(50) NOT NULL,
    organizer_organization VARCHAR(50),
    organizer_contact      VARCHAR(50)
);

CREATE TABLE Manager(
    manager_id      VARCHAR(6) PRIMARY KEY,
    manager_name    VARCHAR(50) NOT NULL,
    manager_contact VARCHAR(30)
);

CREATE TABLE Coach(
    coach_id        VARCHAR(6) PRIMARY KEY,
    coach_name      VARCHAR(50) NOT NULL,
    coach_specialty VARCHAR(50)
);

CREATE TABLE Team(
    team_id           VARCHAR(6)  PRIMARY KEY, 
    team_name         VARCHAR(50) NOT NULL,
    team_region       VARCHAR(30),
    team_achievements TEXT,
    team_earnings     DECIMAL(8, 2),

    manager_id VARCHAR(6),
    coach_id   VARCHAR(6),

    FOREIGN KEY (manager_id) REFERENCES Manager(manager_id),
    FOREIGN KEY (coach_id)   REFERENCES Coach(coach_id)
);

CREATE TABLE Placement(
    placement_id           VARCHAR(6) PRIMARY KEY,
    placement_rank         TEXT,
    placement_points       VARCHAR(3),
    placement_prize_amount DECIMAL(8,2)
);

CREATE TABLE Tournament(
    tournament_id VARCHAR(6) PRIMARY KEY,
    tournament_name VARCHAR(50),
    tournament_rules TEXT,
    tournament_duration VARCHAR(30),
    tournament_schedule DATETIME,
    tournament_format VARCHAR(30),

    game_id       VARCHAR(6),
    venue_id      VARCHAR(9),
    prize_pool_id VARCHAR(6),
    organizer_id  VARCHAR(6),

    FOREIGN KEY (game_id)       REFERENCES Game(game_id),
    FOREIGN KEY (venue_id)      REFERENCES Venue(venue_id),
    FOREIGN KEY (prize_pool_id) REFERENCES PrizePool(prize_pool_id),
    FOREIGN KEY (organizer_id)  REFERENCES Organizer(organizer_id)
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
);

CREATE TABLE TeamPlayer(
    team_id   VARCHAR(6),
    player_id VARCHAR(6),

    PRIMARY KEY (team_id, player_id),

    FOREIGN KEY (team_id)   REFERENCES Team(team_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

CREATE TABLE PlayerGame(
    player_id VARCHAR(6),
    game_id   VARCHAR(6),

    PRIMARY KEY (player_id, game_id),

    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id)   REFERENCES Game(game_id)
);

CREATE TABLE MatchInfo(
    match_id        VARCHAR(6) PRIMARY KEY,
    match_rounds    INT,
    match_date_time DATETIME,
    match_results   TEXT,

    tournament_id VARCHAR(6),
    game_id       VARCHAR(6),
    team1_id      VARCHAR(6),
    team2_id      VARCHAR(6),

    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
    FOREIGN KEY (game_id)       REFERENCES Game(game_id),
    FOREIGN KEY (team1_id)      REFERENCES Team(team_id),
    FOREIGN KEY (team2_id)      REFERENCES Team(team_id)
);

CREATE TABLE MatchCommentator(
    match_id       VARCHAR(6),
    commentator_id VARCHAR(6),
    
    PRIMARY KEY (match_id, commentator_id),
    FOREIGN KEY (match_id)       REFERENCES MatchInfo(match_id),
    FOREIGN KEY (commentator_id) REFERENCES Commentator(commentator_id)
);

CREATE TABLE TournamentTeam(
    tournament_id VARCHAR(6),
    team_id       VARCHAR(6),
    placement_id  VARCHAR(6),

    PRIMARY KEY (tournament_id, team_id),

    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
    FOREIGN KEY (team_id)       REFERENCES Team(team_id),
    FOREIGN KEY (placement_id)  REFERENCES Placement(placement_id)
);

CREATE TABLE TournamentSponsor(
    tournament_id VARCHAR(6),
    sponsor_id    VARCHAR(6),

    PRIMARY KEY (tournament_id, sponsor_id),

    FOREIGN KEY (tournament_id) REFERENCES Tournament(tournament_id),
    FOREIGN KEY (sponsor_id)    REFERENCES Sponsor(sponsor_id)
);

CREATE TABLE TournamentCommentator(
    tournament_id  VARCHAR(6),
    commentator_id VARCHAR(6),

    PRIMARY KEY (tournament_id, commentator_id),

    FOREIGN KEY (tournament_id)  REFERENCES Tournament(tournament_id),
    FOREIGN KEY (commentator_id) REFERENCES Commentator(commentator_id)
);

-- Populating The Tables --
-- Games -- 
INSERT INTO Game (game_id, game_name, game_rules, game_team_size) VALUES
('G001', 'League of Legends', 'MOBA with 3 lanes, destroy enemy nexus to win', 5),
('G002', 'Counter-Strike 2', 'Tactical FPS, plant/defuse bomb or eliminate enemies', 5),
('G003', 'Dota 2', 'MOBA with ancient defense objective', 5),
('G004', 'Valorant', 'Tactical shooter with agent abilities', 5),
('G005', 'Overwatch 2', 'Team-based hero shooter with objective modes', 5);

-- Tournaments --
INSERT INTO Tournament (tournament_id, tournament_name, tournament_rules, tournament_duration, tournament_schedule, tournament_format) VALUES
('T001', 'Worlds Championship 2024', 'Double elimination bracket, best of 5 finals', '30 days', '2024-10-15 09:00:00', 'Double Elimination'),
('T002', 'CS2 Major Berlin', 'Swiss system into single elimination playoffs', '14 days', '2024-11-20 10:00:00', 'Swiss + Single Elim'),
('T003', 'The International 2024', 'Group stage into double elimination bracket', '21 days', '2024-09-01 12:00:00', 'Double Elimination'),
('T004', 'Valorant Champions', 'Group stage into single elimination bracket', '18 days', '2024-08-10 11:00:00', 'Single Elimination'),
('T005', 'Overwatch League Finals', 'Best of 7 grand finals', '10 days', '2024-10-05 14:00:00', 'Playoffs');

-- Matches --
INSERT INTO MatchInfo (match_id, match_rounds, match_date_time, match_results) VALUES
('M001', 5, '2024-10-15 15:00:00', 'Team A won 3-2 against Team B'),
('M002', 3, '2024-10-16 18:00:00', 'Team C won 2-1 against Team D'),
('M003', 5, '2024-11-20 16:00:00', 'Team E won 3-1 against Team F'),
('M004', 3, '2024-09-01 13:00:00', 'Team G won 2-0 against Team H'),
('M005', 7, '2024-08-10 17:00:00', 'Team I won 4-3 against Team J');

-- Teams --
INSERT INTO Team (team_id, team_name, team_region, team_achievements, team_earnings) VALUES
('TM001', 'Cloud9', 'North America', 'Multiple LCS titles, Worlds semifinals', 500000.00),
('TM002', 'T1', 'South Korea', '4x World Champions, numerous LCK titles', 850000.00),
('TM003', 'FaZe Clan', 'Europe', 'CS Major winners, multiple tournament victories', 620000.00),
('TM004', 'Team Liquid', 'North America', 'TI winners, multiple regional championships', 780000.00),
('TM005', 'Fnatic', 'Europe', 'World Champions S1, multiple regional titles', 450000.00),
('TM006', 'Gen.G', 'South Korea', 'Worlds 2024 Champions, LCK titles', 680000.00);

-- Players -- 
INSERT INTO Player (player_id, player_username, player_real_name, player_role, player_rank, player_aliases, player_age, player_games) VALUES
('P001', 'Faker', 'Lee Sang-hyeok', 'Mid Laner', 'Challenger', 'The Unkillable Demon King', 28, 'League of Legends'),
('P002', 's1mple', 'Oleksandr Kostyliev', 'AWPer', 'Global Elite', 'The Ukrainian Star', 27, 'Counter-Strike 2'),
('P003', 'N0tail', 'Johan Sundstein', 'Support', 'Immortal', 'BigDaddy', 31, 'Dota 2'),
('P004', 'TenZ', 'Tyson Ngo', 'Duelist', 'Radiant', 'TenZ the Prodigy', 23, 'Valorant'),
('P005', 'Deft', 'Kim Hyuk-kyu', 'ADC', 'Challenger', 'Korean Marksman', 28, 'League of Legends'),
('P006', 'ZywOo', 'Mathieu Herbaut', 'AWPer', 'Global Elite', 'French Phenom', 24, 'Counter-Strike 2'),
('P007', 'Ceb', 'Sébastien Debs', 'Offlaner', 'Immortal', '7ckngMad', 32, 'Dota 2'),
('P008', 'Chronicle', 'Timofey Khromov', 'Initiator', 'Radiant', 'The Russian Wall', 21, 'Valorant');

-- Placements --
INSERT INTO Placement (placement_id, placement_rank, placement_points, placement_prize_amount) VALUES
('PL001', '1st', '100', 50000.00),
('PL002', '2nd', '75', 25000.00),
('PL003', '3rd', '50', 150000.00),
('PL004', '4th', '40', 100000.00),
('PL005', '5th-6th', '30', 75000.00),
('PL006', '7th-8th', '20', 50000.00);

-- Venues --
INSERT INTO Venue (venue_id, venue_name, venue_location, venue_capacity) VALUES
('V001', 'Madison Square Garden', 'New York, USA', 20000),
('V002', 'Mercedes-Benz Arena', 'Berlin, Germany', 17000),
('V003', 'Climate Pledge Arena', 'Seattle, USA', 18000),
('V004', 'Gocheok Sky Dome', 'Seoul, South Korea', 16000),
('V005', 'Accor Arena', 'Paris, France', 20300);

-- Prize Pools --
INSERT INTO PrizePool (prize_pool_id, prize_pool_amount, prize_pool_currency) VALUES
('PP001', 2000000, 'USD'),
('PP002', 1500000, 'USD'),
('PP003', 40000000, 'USD'),
('PP004', 2250000, 'USD'),
('PP005', 3500000, 'USD');

-- Sponsors --
INSERT INTO Sponsor (sponsor_id, sponsor_name, sponsor_type, sponsor_contact) VALUES
('S001', 'Red Bull', 'Energy Drink', 'esports@redbull.com'),
('S002', 'Logitech G', 'Gaming Peripherals', 'partnerships@logitech.com'),
('S003', 'Intel', 'Technology', 'esports@intel.com'),
('S004', 'Mastercard', 'Financial Services', 'gaming@mastercard.com'),
('S005', 'HyperX', 'Gaming Hardware', 'esports@hyperx.com');

-- Commentators --
INSERT INTO Commentator (commentator_id, commentator_name, commentator_experience, commentator_language) VALUES
('C001', 'Trevor Henry', '10 years', 'English'),
('C002', 'Alex Richardson', '8 years', 'English, Spanish'),
('C003', 'Kim Min-ah', '6 years', 'Korean, English'),
('C004', 'Mitch Leslie', '12 years', 'English'),
('C005', 'OD Pixel', '9 years', 'English');

-- Organizers --
INSERT INTO Organizer (organizer_id, organizer_name, organizer_organization, organizer_contact) VALUES
('O001', 'John Martinez', 'Riot Games', 'j.martinez@riotgames.com'),
('O002', 'Sarah Chen', 'ESL Gaming', 's.chen@eslgaming.com'),
('O003', 'Erik Johnson', 'Valve Corporation', 'e.johnson@valvesoftware.com'),
('O004', 'Anna Petrov', 'Blast Premier', 'a.petrov@blast.tv'),
('O005', 'Marcus White', 'DreamHack', 'm.white@dreamhack.com');

-- Managers --
INSERT INTO Manager (manager_id, manager_name, manager_contact) VALUES
('MG001', 'Jack Etienne', 'jack@cloud9.gg'),
('MG002', 'Steve Arhancet', 'steve@teamliquid.com'),
('MG003', 'Sam Mathews', 'sam@fnatic.com'),
('MG004', 'Carlos Rodriguez', 'carlos@g2esports.com'),
('MG005', 'Andy Dinh', 'andy@tsm.gg');

-- Coaches --
INSERT INTO Coach (coach_id, coach_name, coach_specialty) VALUES
('CO001', 'Kim Jeong-gyun', 'Draft Strategy and Team Coordination'),
('CO002', 'Danny Sorensen', 'Tactical Analysis and Map Control'),
('CO003', 'Andreas Hoejsleth', 'Hero Selection and Game Theory'),
('CO004', 'Chet Singh', 'Agent Composition and Utility Usage'),
('CO005', 'Fabian Broich', 'Team Synergy and Communication');