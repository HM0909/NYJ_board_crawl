# nyj_board_crawl
남양주시립박물관 사이트 크롤링

Table Script
```
CREATE TABLE `board_nyi` (
  `SEQ` int(11) NOT NULL COMMENT '시퀀스',
  `TITLE` varchar(200) NOT NULL COMMENT '제목',
  `READ_COUNT` int(11) NOT NULL COMMENT '조회수',
  `LINK_URL` varchar(200) DEFAULT NULL COMMENT 'URL',
  `ATTACH_URL` varchar(2000) DEFAULT NULL COMMENT '첨부파일 URL',
  `WRITER` varchar(50) DEFAULT NULL COMMENT '작성자',
  `CONTENT` text COMMENT '내용',
  `REG_DATE` varchar(20) NOT NULL COMMENT '등록일',
  PRIMARY KEY (`SEQ`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
