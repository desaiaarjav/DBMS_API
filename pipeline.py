import sqlite3
import re
import API_call
import building_schema
import json
import sqlite3




def normalize_sql(sql):
    sql = sql.lower().strip()
    sql = re.sub(r'\s+', ' ', sql)  # collapse whitespace
    sql = sql.rstrip(';')
    return sql

def extract_sql(text):
    import re
    # Extract from code block
    match = re.search(r'```sql\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Take first SELECT statement found
    match = re.search(r'(SELECT.*?)(?:;|$)', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()

def exact_match(predictions, gold_queries):
    correct = sum(
        normalize_sql(p) == normalize_sql(g)
        for p, g in zip(predictions, gold_queries)
    )
    return correct / len(gold_queries)

def execution_accuracy(predictions, gold_queries, db_ids, db_base_path="spider/database"):
    correct = 0
    total = 0
    
    for pred, gold, db_id in zip(predictions, gold_queries, db_ids):
        db_path = f"{db_base_path}/{db_id}/{db_id}.sqlite"
        try:
            conn = sqlite3.connect(db_path)
            pred_result = set(conn.execute(pred).fetchall())
            gold_result = set(conn.execute(gold).fetchall())
            if pred_result == gold_result:
                correct += 1
        except Exception as e:
            pass  # invalid SQL = wrong
        finally:
            total += 1
            conn.close()
    
    return correct / total

tables_path = "/Users/aarjavdesai/Documents/DBMS_proj/spider/tables.json"  
schema_map = building_schema.load_schemas(tables_path)


train_data_path = "/Users/aarjavdesai/Documents/DBMS_proj/spider/train_spider.json"
with open(train_data_path, 'r', encoding='utf-8') as file:
    train_data = json.load(file)

shot_block = API_call.making_shotblock(train_data, k=1)

def evaluate(dev_data, schema_map,size, db_base_path="spider/database"):
    predictions = []
    gold_queries = []
    db_ids = []
    shot_block = API_call.making_shotblock(train_data, k=1)
    dev_data = dev_data[:size]
    for example in dev_data:
        question = example['question']
        db_id = example['db_id']
        gold_sql = example['query']

        pred_sql = extract_sql(API_call.few_shot_nl2sql(question, db_id, schema_map, shot_block))

        predictions.append(pred_sql)
        gold_queries.append(gold_sql)
        db_ids.append(db_id)

    em = exact_match(predictions, gold_queries)
    ex = execution_accuracy(predictions, gold_queries, db_ids, db_base_path)
    
    return em, ex

accuracy=evaluate(train_data, schema_map,350)
print("Exact Match Accuracy:", accuracy[0])
print("Execution Accuracy:", accuracy[1])







    


