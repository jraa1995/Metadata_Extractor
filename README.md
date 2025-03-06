# Metadata_Extractor

Extracts metadata from dataset files like .csv, .xlsx, and more.

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/jraa1995/Metadata_Extractor```

2. **Make sure to set up venv (Virtual Env)**
    ```sh
    1. python -m venv venv
    2. venv\Scripts\Activate
    ```
4. **Install dependencies (requirements.txt)**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the MCP Pipeline**
    ```sh
    python src/main.py data/YOUR_CSV_OR_DATAFILE_NAME.type
    ```

### **Structure**
- **Modularity** - Separates concerns (CLI, logic, utils) for easier maintenance
- **Testing** - Dedicateed 'tests/' folder for validation
- **Scalability** - Ready for adding new features such as web app in 'src/web/'..
- **Organization** - keeps data, logs, and code separate

Let me know if you'd like to tweak this further or add sample files to `data/` for testing!
