-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2.1
-- http://www.phpmyadmin.net
--
-- Host: localhost:80
-- Czas generowania: 24 Maj 2020, 14:56
-- Wersja serwera: 5.7.29-0ubuntu0.16.04.1
-- Wersja PHP: 7.0.33-0ubuntu0.16.04.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `systemy_zintegrowane`
--
CREATE DATABASE IF NOT EXISTS `systemy_zintegrowane` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `systemy_zintegrowane`;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Status_NIP`
--

CREATE TABLE `Status_NIP` (
  `nip` varchar(10) NOT NULL,
  `data` date NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `Status_rachunek_bankowy`
--

CREATE TABLE `Status_rachunek_bankowy` (
  `nip` varchar(10) NOT NULL,
  `rachunek_bankowy` varchar(26) NOT NULL,
  `data` date NOT NULL,
  `status` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `Status_NIP`
--
ALTER TABLE `Status_NIP`
  ADD PRIMARY KEY (`nip`,`data`);

--
-- Indexes for table `Status_rachunek_bankowy`
--
ALTER TABLE `Status_rachunek_bankowy`
  ADD PRIMARY KEY (`nip`,`rachunek_bankowy`,`data`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
