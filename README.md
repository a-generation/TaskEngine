# TaskEngine

**TaskEngine** is application that allows you to view current processes on your computer, update process data, and manage processes. You can terminate or restart processes and create new tasks from within the application.

## Key Features

- **View Processes**: Display a list of running processes with their PID, name, and username.
- **Manage Processes**: Terminate or restart selected processes.
- **Create Tasks**: Launch new tasks from the interface.
- **Update Interval**: Choose the interval for updating process data (1 sec, 3 sec, 5 sec, or no updates).
- **About**: An information dialog with details about the author and a link to the GitHub repository.

## Installation

To run TaskEngine on your computer, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/a-generation/TaskEngine.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd TaskEngine
    ```

3. **Install required dependencies**:

    Ensure you have Python 3 and pip installed. Then, install the necessary libraries using:

    ```bash
    pip install pyqt5 psutil
    ```

4. **Run the application**:

    Execute the script `main.py`:

    ```bash
    python main.py
    ```

## Usage

1. **Updating Data**: Choose the update interval from the "Update Interval" menu.
2. **Managing Processes**: Select a process in the table and use the buttons in the "Processes" menu to terminate or restart the process.
3. **Creating Tasks**: Use the "Create Task" button to start new tasks by entering a command in the dialog that appears.
4. **About**: Find information about the author, the program's name, and the repository link in the "About" menu.

## Screenshots

(Add screenshots of your application here, if available)

## Notes

**TaskEngine** can be particularly useful in situations where your Task Manager is blocked or disabled by a virus. It allows you to monitor and manage processes even if your system's default task management tools are inaccessible.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
