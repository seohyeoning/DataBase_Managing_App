-- 공공 도서관 데이터베이스 설계

-- 1. 도서 정보 테이블
CREATE TABLE books (
	book_id INT AUTO_INCREMENT PRIMARY KEY, -- 도서 ID (고유값)
    title VARCHAR(225) NOT NULL,            -- 도서 제목
    author VARCHAR(255) NOT NULL,           -- 저자 
    genre VARCHAR(100),                     -- 장르
	published_year YEAR,
    availability ENUM('Available', 'Borrowed') DEFAULT 'Available'  -- 대출 가능 여부 
);

