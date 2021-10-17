CREATE DATABASE IF NOT EXISTS `soc` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE soc;
CREATE TABLE IF NOT EXISTS `course` (
    `code` varchar(10) NOT NULL,
    `name` varchar(100) NOT NULL,
    `info` varchar(250),
    `preq` varchar(100),
    `text` varchar(100),
    PRIMARY KEY (`code`, `name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `class` (
    `number` int(10),
    `ccode` varchar(10) NOT NULL,
    `cname` varchar(100) NOT NULL,
    `instructor` varchar(50),
    `location` varchar(10),
    `day` varchar(10),
    `period` varchar(5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `code` (
    `short` varchar(10) NOT NULL,
    `full` varchar(100) NOT NULL,
    PRIMARY KEY (`short`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
