import json
from telegram.ext import ContextTypes
from repository.common_sql import create_connection, execute_query, execute_query_with_param
import user_state


def create_user_states_table():
    user_states_table = """
        CREATE TABLE user_states (
            user_id INTEGER PRIMARY KEY,
            stage INT,
            stage_1_selection TEXT[],
            stage_2_selection TEXT[],
            stage_3_selection TEXT[],
            stage_4_selection TEXT[],
            stage_5_selection TEXT[],
            stage_6_selection TEXT[],
            user_data JSONB
        );
        """
    connection = create_connection()
    execute_query(connection, user_states_table)


def save_user_state(context: ContextTypes.DEFAULT_TYPE):
    try:
        connection = create_connection()
        cur = connection.cursor()

        user_data_json = json.dumps(context.user_data['data'].to_dict()) if context.user_data.get('data') else '{}'

        cur.execute("""
            INSERT INTO user_states (user_id, stage, stage_1_selection, stage_2_selection, stage_3_selection, stage_4_selection, stage_5_selection, stage_6_selection, user_data) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                stage = EXCLUDED.stage,
                stage_1_selection = EXCLUDED.stage_1_selection,
                stage_2_selection = EXCLUDED.stage_2_selection,
                stage_3_selection = EXCLUDED.stage_3_selection,
                stage_4_selection = EXCLUDED.stage_4_selection,
                stage_5_selection = EXCLUDED.stage_5_selection,
                stage_6_selection = EXCLUDED.stage_6_selection,
                user_data = EXCLUDED.user_data;
        """, (user_state.get_data(context).common_data.chat_id,
              context.user_data['stage'],
              context.user_data['stage_1_selection'],
              context.user_data['stage_2_selection'],
              context.user_data['stage_3_selection'],
              context.user_data['stage_4_selection'],
              context.user_data['stage_5_selection'],
              context.user_data['stage_6_selection'],
              user_data_json))
        connection.commit()
        cur.close()
        connection.close()
    except Exception as e:
        print(f"Ошибка при сохранении состояния пользователя: {e}")


def save_stage_options():
    try:

        with open('/Users/raisatramazanova/development/python_bot/python_pro_bot/data/unique_codes.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split(' - ')

                sql = """
                     INSERT INTO stage_options (stage_id, name)
                     VALUES (%s, %s)
                     """
                if str(value)[:1] == '1':
                    val = ((4, key),)
                elif str(value)[:1] == '2':
                    val = ((3, key),)
                elif str(value)[:1] == '3':
                    val = ((2, key),)
                elif str(value)[:1] == '4':
                    val = ((5, key),)
                connection = create_connection()
                execute_query_with_param(connection, sql, val)
    except Exception as e:
        print(f"Ошибка при сохранении состояния пользователя: {e}")