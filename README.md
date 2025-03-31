# 🚀 DBChat - Intelligent Database Query Assistant

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![LLM](https://img.shields.io/badge/LLM-Qwen%201.8b-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)

A powerful, AI-driven database query assistant that leverages RAG (Retrieval-Augmented Generation) to provide intelligent SQL query generation and database interaction.

## 🌟 Features

- **🤖 AI-Powered Query Generation**: Utilizes Qwen 1.8b LLM for natural language to SQL conversion
- **📊 Schema-Aware Responses**: Automatically detects and uses database structure
- **🔗 Smart Table Relationships**: Identifies and suggests proper table joins
- **📝 Query Validation**: Ensures generated queries match existing schema
- **📈 Result Export**: Automatic CSV export with metadata tracking
- **🛡️ Error Handling**: Robust error management and recovery

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/98tarunkumar/text_to_sql.git
cd text_to_sql
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database connection in `dbQuery.py`:
```python
self.db_connection = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)
```

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- Ollama with Qwen 1.8b model
- Required Python packages:
  - `mysql-connector-python`
  - `pandas`
  - `ollama`

## 🚀 Usage

1. Start the application:
```bash
python dbQuery.py
```

2. Enter your database questions in natural language:
```bash
Enter your database question: Show me all orders from the last month
```

3. Get AI-generated responses with:
- Query explanation
- SQL query
- Results in both console and CSV format

## 💡 Example Queries

```sql
-- Natural Language: "Show active users and their orders"
SELECT 
    u.username,
    o.order_id,
    o.order_date
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE u.status = 'active';
```

## 🏗️ Architecture

```
dbchat/
├── dbQuery.py          # Main application logic
├── requirements.txt    # Project dependencies
└── README.md          # Documentation
```

## 🔍 Key Components

- **DatabaseQueryAssistant**: Core class handling database interactions
- **RAG Implementation**: Schema-aware context generation
- **Query Validation**: Schema compliance checking
- **Result Management**: CSV export and metadata tracking

## 🛡️ Error Handling

- Database connection management
- Query validation
- Schema compliance checking
- JSON serialization handling
- Graceful error recovery

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Qwen LLM team for the language model
- MySQL team for the database engine
- All contributors and users of this project

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

<p align="center">
Made with ❤️ by Tarun
</p>
