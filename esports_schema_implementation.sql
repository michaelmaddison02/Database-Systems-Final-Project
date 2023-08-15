-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema esports
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema esports
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esports` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `esports` ;

-- -----------------------------------------------------
-- Table `esports`.`teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esports`.`teams` (
  `team_name` VARCHAR(45) NOT NULL,
  `team_wins` INT NULL DEFAULT NULL,
  `team_losses` INT NULL DEFAULT NULL,
  `team_games_played` INT NULL DEFAULT NULL,
  `team_kills` INT NULL DEFAULT NULL,
  `team_deaths` INT NULL DEFAULT NULL,
  `team_combined_kills_per_min` INT NULL DEFAULT NULL,
  PRIMARY KEY (`team_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `esports`.`players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esports`.`players` (
  `player_name` VARCHAR(45) NOT NULL,
  `team_name` VARCHAR(45) NOT NULL,
  `player_position` VARCHAR(45) NULL DEFAULT NULL,
  `player_kills` INT NULL DEFAULT NULL,
  `player_deaths` INT NULL DEFAULT NULL,
  `player_assists` INT NULL DEFAULT NULL,
  PRIMARY KEY (`player_name`),
  INDEX `team_name_idx` (`team_name` ASC) VISIBLE,
  CONSTRAINT `team_name`
    FOREIGN KEY (`team_name`)
    REFERENCES `esports`.`teams` (`team_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `esports`.`player_share`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esports`.`player_share` (
  `player_name` VARCHAR(45) NOT NULL,
  `player_kill_share` DECIMAL(3,1) NULL DEFAULT NULL,
  `player_death_share` DECIMAL(3,1) NULL DEFAULT NULL,
  `player_gold_diff_by_10` INT NULL DEFAULT NULL,
  `player_xp_diff_by_10` INT NULL DEFAULT NULL,
  PRIMARY KEY (`player_name`),
  CONSTRAINT `player_name`
    FOREIGN KEY (`player_name`)
    REFERENCES `esports`.`players` (`player_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
