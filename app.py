#
from flask import Flask, request, jsonify
import os
import subprocess
import json
import glob
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    
    try:
        # A1: Install uv and run the data generation script
        if "install uv" in task_description:
            user_email = os.getenv('USER_EMAIL')
            subprocess.run(['pip', 'install', 'uv'], check=True)
            subprocess.run(['python', 'https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py', user_email], check=True)
            return jsonify({"message": "Data generated successfully."}), 200
        
        # A2: Format the contents of /data/format.md
        elif "format" in task_description:
            subprocess.run(['prettier', '--write', '/data/format.md'], check=True)
            return jsonify({"message": "File formatted successfully."}), 200
        
        # A3: Count the number of Wednesdays in /data/dates.txt
        elif "count Wednesdays" in task_description:
            with open('/data/dates.txt', 'r') as f:
                dates = f.readlines()
            wednesdays = sum(1 for date in dates if datetime.strptime(date.strip(), '%Y-%m-%d').weekday() == 2)
            with open('/data/dates-wednesdays.txt', 'w') as f:
                f.write(str(wednesdays))
            return jsonify({"message": "Counted Wednesdays successfully."}), 200
        
        # A4: Sort contacts in /data/contacts.json
        elif "sort contacts" in task_description:
            with open('/data/contacts.json', 'r') as f:
                contacts = json.load(f)
            sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
            with open('/data/contacts-sorted.json', 'w') as f:
                json.dump(sorted_contacts, f)
            return jsonify({"message": "Contacts sorted successfully."}), 200
        
        # A5: Write the first line of the 10 most recent .log files
        elif "recent logs" in task_description:
            log_files = sorted(glob.glob('/data/logs/*.log'), key=os.path.getmtime, reverse=True)[:10]
            with open('/data/logs-recent.txt', 'w') as f:
                for log_file in log_files:
                    with open(log_file, 'r') as lf:
                        first_line = lf.readline()
                        f.write(first_line)
            return jsonify({"message": "Recent logs written successfully."}), 200
        
        # A6: Create an index of H1 titles from Markdown files
        elif "index markdown" in task_description:
            index = {}
            for md_file in glob.glob('/data/docs/*.md'):
                with open(md_file, 'r') as f:
                    for line in f:
                        if line.startswith('# '):
                            index[os.path.basename(md_file)] = line[2:].strip()
                            break
            with open('/data/docs/index.json', 'w') as f:
                json.dump(index, f)
            return jsonify({"message": "Index created successfully."}), 200
        
        # A7: Extract sender's email from /data/email.txt using LLM
        elif "extract email" in task_description:
            with open('/data/email.txt', 'r') as f:
                email_content = f.read()
            # Call LLM to extract email (pseudo-code)
            sender_email = call_llm_to_extract_email(email_content)
            with open('/data/email-sender.txt', 'w') as f:
                f.write(sender_email)
            return jsonify({"message": "Email extracted successfully."}), 200
        
        # A8: Extract credit card number from image
        elif "extract credit card" in task_description:
            # Call LLM to extract card number from image (pseudo-code)
            card_number = call_llm_to_extract_card_number('/data/credit-card.png')
            with open('/data/credit-card.txt', 'w') as f:
                f.write(card_number.replace(" ", ""))
            return jsonify({"message": "Credit card number extracted successfully."}), 200
        
        # A9: Find the most similar pair of comments
        elif "similar comments" in task_description:
            with open('/data/comments.txt', 'r') as f:
                comments = f.readlines()
            # Use embeddings to find the most similar comments (pseudo-code)
            similar_comments = find_most_similar_comments(comments)
            with open('/data/comments-similar.txt', 'w') as f:
                f.write('\n'.join(similar_comments))
            return jsonify({"message": "Similar comments found successfully."}), 200
        
        # A10: Calculate total sales for "Gold" ticket type
        elif "total sales gold" in task_description:
            conn = sqlite3.connect('/data/ticket-sales.db')
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
            total_sales = cursor.fetchone()[0]
            with open('/data/ticket-sales-gold.txt', 'w') as f:
                f.write(str(total_sales))
            conn.close()
            return jsonify({"message": "Total sales calculated successfully."}), 200
        
        else:
            return jsonify({"error": "Task not recognized."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path')
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({"content": content}), 200
    else:
        return jsonify({"error": "File not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
