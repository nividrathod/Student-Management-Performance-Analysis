import csv
import json
import os
from datetime import datetime
from config import CSV_FILE,JSON_FILE,SUBJECTS

def save_to_csv(students):
    if not students:
        print("No data to save")
        return

    try: 
        with open(CSV_FILE,'w',newline="",encoding='utf-8')as f:
            headers = ['Roll No','Name','Class']+ SUBJECTS + ['Total','Percentage','Grade','Result','Created Date']
            writer = csv.writer(f)

            writer.writerow(headers)
            for s in students:
                row = [s['roll_no'],s['name'],s['class']]
                row+= [s['marks'][sub] for sub in SUBJECTS]
                row+= [s['total'],s['percentage'],s['grade'],s['result'],s['created_date']]
                writer.writerow(row)

        print(f"Saved to '{CSV_FILE}'")
    except Exception as e:
        print(f"Saving Error: {e} ")

def load_from_csv():
    students = []
    if not os.path.exists(CSV_FILE):
        print("No existing data file,starting Fresh")
        return students

    try: 
        with open(CSV_FILE,'r',newline="",encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader,None)

            for row in reader:
                try:
                    marks = {sub: int(row[3+i]) for i,sub in enumerate(SUBJECTS)}
                    n = len(SUBJECTS)

                    students.append({
                        "roll_no":row[0],"name":row[1],"class":row[2],
                        "marks":marks,
                        "total":int(row[3+n]),
                        "percentage":float(row[4+n]),
                        "grade":row[5+n],
                        "result":row[6+n],
                        "created_date":row[7+n]
                    })
                except (ValueError,IndexError) as e:
                    print(f"Skipping invalid row: {e}")

        print(f"Loaded {len(students)} students(s) from '{CSV_FILE}'")
    except Exception as e:
        print(f"Error in loading: {e}")

def export_to_json(students):
    if not students:
        print("No data to export.")
        return
    try:
        report = {
            "report_generated":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_students":len(students),
            "class_average":round(sum(s['percentage'] for s in students)/len(students),2),
            "students":students
        }
        with open(JSON_FILE,"w",encoding='utf-8') as f:
            json.dump(report,f,indent=4)
        print(f"Export to:{JSON_FILE} ")

    except Exception as e:
        print(f"Error exporting: {e}")