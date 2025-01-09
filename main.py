from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
import mysql.connector
from mysql.connector import Error
from kivy.lang import Builder
from func import *

Builder.load_file('app_layout.kv')


class MyApp(BoxLayout):
    def __init__(self, **kwargs): # 초기화 작업 수행
        super().__init__(**kwargs)
        self.current_action = None  # current_action 속성을 통해 현재 수행 중인 작업 저장 (insert, update, delete)

    # ---------------------------------
    # Database Connection
    # ---------------------------------
    def connect_to_db(self):
        """MySQL 데이터베이스에 연결

        mysql.connector.connect 사용해 데이터베이스 정보 설정 (host, user, password, database) 
        
        연결 실패 시 오류 메시지 출력
        """
        try:
            return mysql.connector.connect(
                host='localhost',
                user='user1',
                password='1user',
                database='library_db'
            )
        except Error as e:
            print(f"DB 연결 실패: {e}")
            return None

    # ---------------------------------
    # Animation
    # - 특정 위젯(input text 항목)을 숨기거나 표시
    # - Animation을 사용하여 height와 opacity 속성을 부드럽게 전환
    # ---------------------------------
    def hide_input_field(self, widget):
        """Hides the input field with animation."""
        anim = Animation(height=0, opacity=0, duration=0.3) 
        anim.start(widget)
        # animation 실행 종료 후 고정
        widget.size_hint_y = None 
        widget.height = 0 

    def show_input_field(self, widget):
        """Shows the input field with animation."""
        widget.size_hint_y = None
        anim = Animation(height=50, opacity=1, duration=0.3)
        anim.start(widget)

    # ---------------------------------
    # Toggle Hidden Input Box
    # - insert, update, delete 버튼 클릭 시, 관련 입력 필드 표시 및 숨기기
    # ---------------------------------
    def toggle_hidden_input_box(self, action):
        hidden_box = self.ids.hidden_input_box
        
        # 숨겨진 Input box 열기
        if hidden_box.height == 0:
            anim = Animation(height=400, opacity=1, duration=0.3)
            self.ids.hidden_label.text = f"Action: {action.capitalize()}"
            self.current_action = action
            anim.start(hidden_box)

            # 모든 위젯(입력항목) 숨기기
            input_ids = [
                "primary_key_input", "title_input",
                "author_input", "genre_input", "year_input"
            ]
            
            for input_id in input_ids:
                self.hide_input_field(self.ids.get(input_id)) # ids.get("id") : "id" ID를 가진 위젯에 대해 hide

            # action과 관련된 위젯(입력항목)만 보이기
            if action == "delete":
                self.show_input_field(self.ids.primary_key_input)
            elif action == "update":
                for input_id in ["primary_key_input", "title_input", "author_input", "genre_input", "year_input"]:
                    self.show_input_field(self.ids.get(input_id))
            elif action == "insert": 
                for input_id in ["title_input", "author_input", "genre_input", "year_input"]:
                    self.show_input_field(self.ids.get(input_id))
                    
        # 열려있는 input_box 숨기기
        else: 
            anim = Animation(height=0, opacity=0, duration=0.3)
            self.current_action = None
            anim.start(hidden_box)

            # 모든 위젯(입력항목)에 대해 숨기기
            input_ids = [
                "primary_key_input", "title_input",
                "author_input", "genre_input", "year_input"
            ]
            for input_id in input_ids:
                self.hide_input_field(self.ids.get(input_id))

    # ---------------------------------
    # Load and Display Data
    # ---------------------------------
    def load_data(self):
        connection = self.connect_to_db() # MySQL 연결
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM books") # library_db의 books 테이블 선택하는 쿼리 실행
                rows = cursor.fetchall() # fetchall(): SQL 쿼리 실행한 결과를 반환. 모든 행(튜플)에 대한 리스트로 반환
                column_names = [desc[0] for desc in cursor.description] # SQL 쿼리 결과의 열 이름 추출. cursor.description: SQL 쿼리 결과의 열 메타데이터를 포함하는 속성. 첫번째 요소(desc[0]): 열 이름
                self.update_table_display(rows, column_names) # table_display에 table 송출
            
            except Error as e:
                print(f"Failed to load data: {e}")
            
            finally:
                cursor.close()
                connection.close()

    def update_table_display(self, rows, column_names):
        """Displays the data in a formatted structure.
        """
        if not rows:
            self.ids.data_display.text = "No data found."
            return

        display_text = f"Columns:\n{tuple(column_names)}\n\n" # display_text 상단에 column_name 표시
        for row in rows:
            display_text += f"{tuple(row)}\n" # 하단에 각 row에 대한 값들 표시

        self.ids.data_display.text = display_text

    def clear_data(self):
        """Clears the displayed data."""
        self.ids.data_display.text = ""

    # ---------------------------------
    # Process Hidden Input
    # - 각 action에 해당하는 operation 수행
    # ---------------------------------
    def process_hidden_input(self):
        if self.current_action == 'insert':
            self.insert_data()
        elif self.current_action == 'update':
            self.update_data()
        elif self.current_action == 'delete':
            self.delete_data()

    # ---------------------------------
    # CRUD Operations
    # - INSERT, UPDATE, DELETE
    # ---------------------------------
    def insert_data(self):
        connection = self.connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                title = self.ids.title_input.text
                author = self.ids.author_input.text
                genre = self.ids.genre_input.text
                year = self.ids.year_input.text
                # INSERT INTO {table명} (col1, col2, ...) VALUES (val1, val2, ...)
                query = "INSERT INTO books (title, author, genre, published_year) VALUES (%s, %s, %s, %s)"
                values = (title, author, genre, year)
                cursor.execute(query, values)  # execute(query, values): SQL 쿼리를 문자열로 받고, 쿼리에 포함될 데이터를 매개변수로 전달받아 실행
                
                # SQL 쿼리로 수행된 변경 사항을 데이터베이스에 transaction 단위로 영구적으로 저장
                connection.commit() # 저장하지 않으면, transaction 종료될 때 변경 사항 사라짐
                print(f"Data inserted: {values}")
                self._update_status_text(f"Data inserted: {values}") # last update 내용 변경
                
            except Error as e:
                print(f"Insertion failed: {e}")
            finally:
                cursor.close()
                connection.close()
                
    def update_data(self):
        """특정 book_id를 기준으로 데이터 업데이트
        """
        connection = self.connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()

                # 입력값 검증
                book_id = self.ids.primary_key_input.text.strip()
                if not book_id.isdigit():  # book_id가 정수가 아니면 오류 메시지 출력
                    self._update_status_text("Invalid Book ID. Please enter a valid integer.")
                    return

                # 입력값 가져오기
                title = self.ids.title_input.text.strip()
                author = self.ids.author_input.text.strip()
                genre = self.ids.genre_input.text.strip()
                year = self.ids.year_input.text.strip()

                # 동적 쿼리 생성
                update_fields = []
                update_values = []

                if title:
                    update_fields.append("title=%s")
                    update_values.append(title)
                if author:
                    update_fields.append("author=%s")
                    update_values.append(author)
                if genre:
                    update_fields.append("genre=%s")
                    update_values.append(genre)
                if year:
                    update_fields.append("published_year=%s")
                    update_values.append(year)

                # 업데이트할 값이 없으면 중단
                if not update_fields:
                    self._update_status_text("No fields to update. Please provide at least one value.")
                    return

                # SQL 쿼리 생성
                query = f"UPDATE books SET {', '.join(update_fields)} WHERE book_id=%s"
                update_values.append(int(book_id))  # book_id 추가
                cursor.execute(query, update_values)
                connection.commit()

                # 상태 메시지
                if cursor.rowcount > 0:  # 업데이트된 행이 있는 경우
                    self._update_status_text(f"Data updated for ID {book_id}")

                else:  # 업데이트된 행이 없는 경우
                    self._update_status_text(f"No record found with ID {book_id}")

            except Error as e:
                self._update_status_text(f"Update failed: {e}")
                print(f"Update failed: {e}")
            finally:
                cursor.close()
                connection.close()


    def delete_data(self):
        """특정 book_id를 기준으로 데이터 삭제 
        """
        connection = self.connect_to_db()
        if connection:
            try:
                cursor = connection.cursor()
                book_id = self.ids.primary_key_input.text
                query = "DELETE FROM books WHERE book_id=%s"
                values = (book_id,)
                cursor.execute(query, values)
                connection.commit()
                print(f"Data deleted for ID {book_id}")
                self._update_status_text(f"Data deleted for ID {book_id}")
                
            except Error as e:
                print(f"Deletion failed: {e}")
                
            finally:
                cursor.close()
                connection.close()

    # ---------------------------------
    # Helper Methods
    # ---------------------------------
    def _update_status_text(self, message):
        """상태 메시지(update_text 레이블) 업데이트하여 사용자에게 현재 작업 상태 표시"""
        self.ids.update_text.text = message
        self.ids.update_text.height = self.ids.update_text.texture_size[1]


class LibraryApp(App):
    def build(self):
        return MyApp()


if __name__ == '__main__':
    LibraryApp().run()

