-- 공공 도서관 데이터베이스 설계
CREATE DATABASE library_db;
USE library_db;

-- 1. 도서 정보 테이블
CREATE TABLE books (
	book_id INT AUTO_INCREMENT PRIMARY KEY, -- 도서 ID (고유값)
    title VARCHAR(225) NOT NULL,            -- 도서 제목
    author VARCHAR(255) NOT NULL,           -- 저자 
    genre VARCHAR(100),                     -- 장르
	published_year YEAR,					-- 출판 연도
    availability ENUM('Available', 'Borrowed') DEFAULT 'Available'  -- 대출 가능 여부 
);

-- 2. 회원 정보 테이블
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY, -- 회원 ID (고유값)
    name VARCHAR(100) NOT NULL,               -- 회원 이름
    email VARCHAR(255) NOT NULL UNIQUE,       -- 이메일
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP       -- 가입 날짜
);

-- 3. 대출 기록 테이블 
CREATE TABLE borrow_records (
	record_id INT AUTO_INCREMENT PRIMARY KEY, -- 대출 기록 ID (고유값)
    member_id INT NOT NULL, 				  -- 회원 ID (참조)
    book_id INT NOT NULL, 					  -- 도서 ID (참조)
    borrow_data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 대출 날짜
    return_date DATE, 							-- 반납 날짜
    FOREIGN KEY (member_id) REFERENCES members(member_id), # members 테이블의 member_id를 참조
    FOREIGN KEY (book_id) REFERENCES books(book_id) # books 테이블의 book_id를 참조
);

-- 4. 로그 테이블 (옵션, 데이터 변경 추적)
CREATE TABLE change_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,    -- 로그 ID (고유값)
    user_name VARCHAR(100),                   -- 변경한 사용자 이름
    change_type ENUM('INSERT', 'UPDATE', 'DELETE'), -- 변경 유형
    table_name VARCHAR(100),                  -- 변경된 테이블 이름
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 변경 시간
    details TEXT                              -- 변경 내용
);


