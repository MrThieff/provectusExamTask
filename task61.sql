-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Авг 20 2013 г., 14:40
-- Версия сервера: 5.5.31
-- Версия PHP: 5.4.4-14+deb7u2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `task61`
--

-- --------------------------------------------------------

--
-- Структура таблицы `coments`
--

CREATE TABLE IF NOT EXISTS `coments` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET koi8r NOT NULL,
  `coment` text NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=89 ;

--
-- Дамп данных таблицы `coments`
--

INSERT INTO `coments` (`id`, `username`, `coment`, `time`) VALUES
(1, 'firs', 'my first comment: ASDFGHJKL!', '2013-08-13 04:00:00'),
(3, '123', 'asdaqweq', '2013-08-13 04:00:00'),
(6, 'DIMA', '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', '2013-08-13 04:00:00'),
(18, 'Dima', 'Declares the BLOCK or the rest of the compilation unit as being in the given namespace. The scope of the package declaration is either the supplied code BLOCK or, in the absence of a BLOCK, from the declaration itself through the end of current scope (the enclosing block, file, or eval).', '2013-08-14 19:29:00'),
(19, 'MyNameIs', 'From the comparions presented here, one might conclude that selection sort should never be used. It does not adapt to the data in any way (notice that the four animations above run in lock step), so its runtime is always quadratic.', '2013-08-14 19:29:00'),
(20, 'MyNameIs', 'From the comparions presented here, one might conclude that selection sort should never be used. It does not adapt to the data in any way (notice that the four animations above run in lock step), so its runtime is always quadratic.', '2013-08-14 19:29:00'),
(21, '111', '222', '2013-08-14 19:29:00'),
(38, '111', '222', '2013-08-14 19:29:00'),
(39, '111', '222', '2013-08-14 19:29:00'),
(40, '111', '222', '2013-08-14 19:29:00'),
(41, '222', '3333', '2013-08-14 19:29:00'),
(42, '333', '4444', '2013-08-14 19:29:00'),
(43, '333', '4444', '2013-08-14 19:29:00'),
(44, '444', '5555', '2013-08-14 05:11:38'),
(48, 'me', 'What a studid thing =P', '2013-08-14 05:50:30'),
(49, '123', '123', '2013-08-14 07:02:24'),
(50, '123', '123', '2013-08-14 07:16:54'),
(52, '123', '123123123123', '2013-08-14 20:32:44'),
(53, 'NEW', '&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;', '2013-08-14 20:37:11'),
(54, 'NEW', '&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;', '2013-08-14 20:39:28'),
(55, 'NEW', '&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;', '2013-08-14 20:39:29'),
(56, 'NEW', '&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;', '2013-08-14 20:39:30'),
(57, 'NEW', '&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;', '2013-08-14 20:39:32'),
(58, 'NEW', '&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;_&#1058;&#1059;&#1062;', '2013-08-14 20:40:35'),
(59, '123', '123', '2013-08-14 20:40:44'),
(60, '123', '123', '2013-08-14 20:40:52'),
(61, '123', '123', '2013-08-14 20:40:52'),
(62, '123', '123', '2013-08-14 20:40:52'),
(63, '123', '123', '2013-08-14 20:40:53'),
(64, '123', '123', '2013-08-14 20:40:53'),
(65, '123', '123', '2013-08-14 20:40:53'),
(66, '123', '123', '2013-08-14 20:40:53'),
(67, '123', '123', '2013-08-14 20:40:53'),
(68, '123', '123', '2013-08-14 20:40:54'),
(69, '123', '123', '2013-08-14 20:43:15'),
(70, '123', '123', '2013-08-14 20:43:16'),
(71, '123', '123', '2013-08-14 20:43:21'),
(72, '11111111111111111111', '111111111111111111111111', '2013-08-14 20:43:34'),
(73, '2222222222222222222', '222222222222222222222222222', '2013-08-14 20:44:09'),
(74, '123', '123', '2013-08-15 02:50:07'),
(75, '111', '<H1>=P</H1>', '2013-08-20 15:16:10'),
(76, 'aaa', '<img style="margin: 2px;" alt="" src="http://jenkins.dins.ru:8080/static/fa82ce0d/images/24x24/clock.gif" height="24" width="24">', '2013-08-20 15:18:49'),
(78, '";Drop database;', '";Drop database;', '2013-08-20 15:19:48'),
(79, 'ss', '";Drop database;', '2013-08-20 15:20:06'),
(80, 'sad', 'asd', '2013-08-20 15:20:16'),
(81, '11', '11', '2013-08-20 15:20:47'),
(82, '1233', '1233', '2013-08-20 16:17:19'),
(83, '1111', '!@#$%^&*()_+', '2013-08-20 16:17:32'),
(85, '12333', '<!', '2013-08-20 16:41:36'),
(86, '12333', 'qweeeqweqweasdasfc\r\nasfasfas\r\nasfasfasfasfasff\r\nasfasfasf', '2013-08-20 16:44:15'),
(87, '12334', '< b > 111 </ b >', '2013-08-20 16:46:51'),
(88, 'mememe', '&#1058;&#1059;&#1062;\r\n&#1058;&#1059;&#1062;\r\n&#1058;&#1059;&#1062;-&#1058;&#1059;&#1062;-&#1058;&#1059;&#1062;', '2013-08-20 16:53:34');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
