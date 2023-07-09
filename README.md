# Auto Attendance System using Face Recognition in Django

This is an auto attendance system developed using Django framework and integrated with face recognition technology. The system automates the attendance tracking process by utilizing facial recognition algorithms.

## Features

- Face Detection: The system employs face detection algorithms to identify and locate faces within images or live video streams.
- Face Recognition: It utilizes face recognition techniques to recognize and match faces with pre-registered student identities.
- Attendance Tracking: The system tracks attendance by matching detected faces with the database of registered students and marking their presence.
- User-Friendly Interface: The application provides a user-friendly web interface for easy interaction and monitoring of attendance records.
- Performance Optimization: The system is optimized for efficient face detection and recognition, ensuring accurate and timely attendance tracking.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/rohittelgote23/Auto_Attendance.git
   ```

2. Navigate to the project directory:

   ```shell
   cd Auto_Attendance
   ```

3. Create and activate a virtual environment:

   ```shell
   virtualenv env
   source env/bin/activate  # For Linux/Mac
   env\Scripts\activate  # For Windows
   ```

4. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

5. Run the database migrations:

   ```shell
   python manage.py migrate
   ```

6. Start the development server:

   ```shell
   python manage.py runserver
   ```

7. Access the application locally via `http://localhost:8000` in your web browser.

## Usage

1. Register student information by capturing their images and storing them in the system.
2. Start the attendance session, either by uploading an image.
3. The system will detect faces, match them with registered students, and mark their attendance.
4. View and manage attendance records through the user-friendly web interface.

## Acknowledgements

- The project utilizes the [Django](https://www.djangoproject.com/) web framework and face recognition libraries.
- Special thanks to the developers and contributors of the dependencies used in this project.
