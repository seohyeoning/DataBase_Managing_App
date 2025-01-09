ALTER TABLE books MODIFY COLUMN published_year INT;

INSERT INTO books (title, author, genre, published_year, availability)
VALUES 
    ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925, 'Available'),
    ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, 'Available'),
    ('1984', 'George Orwell', 'Dystopian', 1949, 'Borrowed'),
    ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 1951, 'Available'),
    ('Pride and Prejudice', 'Jane Austen', 'Romance', 1813, 'Available');

INSERT INTO members (name, email)
VALUES 
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Charlie Brown', 'charlie@example.com'),
    ('Daisy Lee', 'daisy@example.com'),
    ('Edward Green', 'edward@example.com');

INSERT INTO borrow_records (member_id, book_id, borrow_data, return_date)
VALUES 
    (1, 3, CURRENT_TIMESTAMP, '2025-01-15'), -- Alice가 1984를 빌림
    (2, 5, CURRENT_TIMESTAMP, '2025-01-20'), -- Bob이 Pride and Prejudice를 빌림
    (3, 1, CURRENT_TIMESTAMP, NULL);         -- Charlie가 The Great Gatsby를 빌림 (미반납)

INSERT INTO change_logs (user_name, change_type, table_name, details)
VALUES 
    ('Admin', 'INSERT', 'books', 'Added book: 1984 by George Orwell'),
    ('Admin', 'INSERT', 'members', 'Added member: Alice Johnson'),
    ('Admin', 'INSERT', 'borrow_records', 'Alice borrowed 1984 on 2025-01-09');
