import json

tables_path = "/Users/aarjavdesai/Documents/DBMS_proj/spider/tables.json"  
def load_schemas(tables_path):
    with open(tables_path) as f:
        tables = json.load(f)
    
    schema_map = {}
    for db in tables:
        db_id = db['db_id']
        schema_lines = []
        for i, table in enumerate(db['table_names_original']):
            cols = [
                db['column_names_original'][j][1]
                for j in range(len(db['column_names_original']))
                if db['column_names_original'][j][0] == i
            ]
            schema_lines.append(f"Table {table}: ({', '.join(cols)})")
        schema_map[db_id] = "\n".join(schema_lines)
    return schema_map

def build_prompt(question, db_id, schema_map):
    schema = schema_map[db_id]
    return f"""Given the following database schema:
{schema}

Convert this question to SQL:
Question: {question}
SQL:"""