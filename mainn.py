import tkinter as tk
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from database_connector import DatabaseConnector

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Set NLTK data path (modify the path accordingly)
nltk.data.path.append('/path/to/nltk_data')

class NLPDatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("NLP Database Interface")

        self.db_connector = DatabaseConnector()

        self.create_widgets()

    def create_widgets(self):
        # Entry widget for user input
        self.input_entry = tk.Entry(self.master, width=40)
        self.input_entry.grid(row=0, column=0, padx=10, pady=10)

        # Button to trigger the query
        self.query_button = tk.Button(self.master, text="Query Database", command=self.execute_query)
        self.query_button.grid(row=0, column=1, padx=10, pady=10)

        # Text widget to display results
        self.result_text = tk.Text(self.master, height=10, width=50)
        self.result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def execute_query(self):
        user_input = self.input_entry.get()
        sql_query = self.convert_to_sql(user_input)

        if sql_query:
            results = self.db_connector.execute_query(sql_query)

            if results:
                result_text = "\n".join(map(str, results))
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, result_text)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No results found.")
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Could not generate a valid SQL query from the input.")

    def convert_to_sql(self, query):
        tokens = word_tokenize(query)
        stop_words = set(stopwords.words('english'))
    
        # Use any word that is not a stop word as a keyword
        keywords = [word for word in tokens if word.lower() not in stop_words]

        print("Input Keywords:", keywords)

        if not keywords:
            return None

        # Simple mapping of keywords to database columns (case-insensitive)
        column_mapping = {
            'title': 'title',
            'author': 'author',
            'year': 'year'
        }

        conditions = []
        for keyword in keywords:
            for column, field in column_mapping.items():
                if column.lower() in keyword.lower():
                    conditions.append(f"{field} LIKE '%{keyword}%'")

        if not conditions:
            return None

        sql_query = f"SELECT * FROM books WHERE {' AND '.join(conditions)};"
        print("Generated SQL Query:", sql_query)
        return sql_query

if __name__ == "__main__":
    root = tk.Tk()
    app = NLPDatabaseApp(root)
    root.mainloop()
