from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
import json
import pymysql


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://cm41785.tw1.ru/"}}, supports_credentials=True)

@app.route('/')
def home():
    return render_template('index.html')

def get_db_connection():
    try:
        conn = pymysql.connect(
            host='localhost',  
            user='cm41785_simple',  
            password='cm41785_simplec',  
            database='cm41785_simple',  
            charset='utf8mb4',  
            cursorclass=pymysql.cursors.DictCursor  
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

@app.route('/test_db', methods=['GET'])
def test_db():
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return "Соединение с базой данных успешно", 200
        else:
            return "Ошибка подключения к базе данных", 500
    except Exception as e:
        return f"Ошибка: {str(e)}", 500



@app.route('/api/add', methods=['POST'])
def add_data():
    try:
        data = request.get_json()
        print(f"Полученные данные для добавления: {data}")

        if not data or 'data' not in data:
            return jsonify({"message": "Неверный формат данных"}), 400

        file_content = data.get('data')
        print(f"Содержимое файла для добавления: {file_content}")

        conn = get_db_connection()
        cur = conn.cursor()

        for unicode_hieroglyph, parts in file_content.items():
            
            cur.execute("""
                INSERT INTO Hieroglyphs (unicode)
                VALUES (%s)
                ON DUPLICATE KEY UPDATE unicode = unicode;
            """, (unicode_hieroglyph,))

            for part in parts:
                
                cur.execute("""
                    INSERT INTO Parts_hieroglyphs (part)
                    VALUES (%s)
                    ON DUPLICATE KEY UPDATE id_part_hieroglyph=LAST_INSERT_ID(id_part_hieroglyph);
                """, (part,))
                part_id = cur.lastrowid

                
                cur.execute("""
                    INSERT INTO Hieroglyph_Parts (id_hieroglyph, id_part_hieroglyph)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE id_hieroglyph=id_hieroglyph;
                """, (unicode_hieroglyph, part_id))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Данные успешно добавлены!"}), 200

    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({"message": f"Ошибка: {str(e)}"}), 400

@app.route('/api/delete', methods=['POST'])
def delete_data():
    try:
        data = request.get_json()
        print(f"Полученные данные для удаления: {data}")

        if not data or 'data' not in data:
            return jsonify({"message": "Ошибка: Неверный формат данных"}), 400

        file_content = data.get('data')
        print(f"Содержимое файла для удаления: {file_content}")

        conn = get_db_connection()
        if conn is None:
            return jsonify({"message": "Ошибка подключения к базе данных"}), 500

        cur = conn.cursor()

        for unicode_hieroglyph, parts in file_content.items():
            print(f"Удаляем иероглиф: {unicode_hieroglyph}, Части: {parts}")

            cur.execute(
                "DELETE FROM Hieroglyph_Parts WHERE id_hieroglyph = %s;",
                (unicode_hieroglyph,)
            )

            cur.execute(
                "DELETE FROM Hieroglyphs WHERE unicode = %s;",
                (unicode_hieroglyph,)
            )

        cur.execute("""
            DELETE FROM Parts_hieroglyphs
            WHERE id_part_hieroglyph NOT IN (
                SELECT DISTINCT id_part_hieroglyph FROM Hieroglyph_Parts
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Данные успешно удалены!"}), 200

    except Exception as e:
        print(f"Ошибка: {e}")
        return jsonify({"message": f"Ошибка: {str(e)}"}), 400

@app.route('/api/upload_translations', methods=['POST'])
def upload_translations():
    try:
        data = request.get_json()
        translations = data.get('data')

        conn = get_db_connection()
        cursor = conn.cursor()

        for word, translations_by_lang in translations.items():
            for lang, translation in translations_by_lang.items():
                cursor.execute("""
                    INSERT INTO Translations (word, translation, language)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE translation = VALUES(translation);
                """, (word, translation, lang))


        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Данные успешно добавлены!"}), 200
    except Exception as e:
        return jsonify({"message": f"Ошибка: {str(e)}"}), 400

@app.route('/api/delete_translation', methods=['POST'])
def delete_translation():
    try:
        data = request.get_json()
        if not data or 'data' not in data:
            return jsonify({"message": "Ошибка: Ожидается JSON объект"}), 400
        
        translations_to_delete = data['data']
        conn = get_db_connection()
        cursor = conn.cursor()

        for word, translations in translations_to_delete.items():
            for lang in translations.keys():
                cursor.execute(
                    "DELETE FROM Translations WHERE word = %s AND language = %s",
                    (word, lang)
                )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Переводы успешно удалены!"}), 200
    except Exception as e:
        return jsonify({"message": f"Ошибка: {str(e)}"}), 400

print("Список маршрутов:")
for rule in app.url_map.iter_rules():
    print(rule)


if __name__ == '__main__':
    app.run(debug=True)