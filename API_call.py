import ollama


def few_shot_nl2sql(question, db_id, schema_map, few_shot_block):    
    
    prompt = f"""You are an expert SQL generator. Given a database schema and a question, write the correct SQL query.

Schema:
{schema_map[db_id]}

Examples:
{few_shot_block}
Now answer:
Question: {question}
SQL:"""

    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

def making_shotblock(train_examples, k=3):
    examples = train_examples[:k]
    few_shot_block = ""
    for ex in examples:
        few_shot_block += f"""Question: {ex['question']}
SQL: {ex['query']}\n\n"""
    return few_shot_block