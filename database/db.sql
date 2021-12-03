CREATE USER IF NOT EXISTS shiv@localhost IDENTIFIED BY 'bang';
CREATE DATABASE IF NOT EXISTS soc DEFAULT CHARACTER SET = 'utf8';
GRANT ALL on soc.* to 'shiv'@'localhost' IDENTIFIED BY 'bang';
USE soc;
CREATE TABLE IF NOT EXISTS `course` (
    `code` varchar(10) NOT NULL,
    `name` varchar(100) NOT NULL,
    `info` varchar(1000),
    `preq` varchar(250),
    `text` varchar(250),
    `isbn` varchar(20),
    `last` varchar(10),
    PRIMARY KEY (`code`, `name`)
);

CREATE TABLE IF NOT EXISTS `class` (
    `number` int(10),
    `ccode` varchar(10) NOT NULL,
    `cname` varchar(100) NOT NULL,
    `instructor` varchar(50),
    `location` varchar(10),
    `day` varchar(10),
    `btime` time,
    `etime` time,
    `final` varchar(50)
);

CREATE TABLE IF NOT EXISTS `prof` (
    `name` varchar(50) NOT NULL,
    `rate` varchar(10) NOT NULL,
    PRIMARY KEY (`name`)
);
