# PPT Submission & Analysis System

## Overview
A comprehensive document tracking system for managing PPT submissions with AI-powered analysis. The system supports both staff and student dashboards with real-time analytics and ML-based evaluation.

https://guru03-coder.github.io/SlideSense/

## Project Structure
```
Devf/
├── index.html      # Main login page (entry point)
├── staff.html      # Staff/Teacher dashboard
├── student.html    # Student dashboard
├── backend.py      # Flask backend API server
├── requirements.txt # Python dependencies
└── readme.md       # This file
```

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the backend server:**
   ```bash
   python backend.py
   ```
   The backend will run on `http://localhost:5000`

3. **Verify backend is running:**
   - Open your browser and go to `http://localhost:5000/api/staff/stats`
   - You should see JSON data with statistics

### Frontend Setup

1. **Open the application:**
   - Open `index.html` in your web browser
   - This is the main entry point for the application

2. **Login:**
   - **Staff Login:**
     - Email: `teacher@example.com`
     - Password: `password123`
   
   - **Student Login:**
     - Roll Number: `21CS001`
     - Password: `student123`

3. **Navigate:**
   - After login, you'll be redirected to:
     - Staff users → `staff.html`
     - Student users → `student.html`

## Features

### Staff Dashboard (`staff.html`)
- ✅ View all student presentations
- ✅ Filter and search presentations by student name, roll number, department
- ✅ ML-based AI analysis and scoring
- ✅ Approve/Reject submissions
- ✅ Real-time statistics dashboard
- ✅ Analytics and performance metrics
- ✅ Download presentations
- ✅ View detailed AI evaluation reports

### Student Dashboard (`student.html`)
- ✅ Upload new presentations (PPT/PPTX)
- ✅ View submission status (Pending, Approved, Rejected)
- ✅ View AI analysis and scores
- ✅ Track submission history
- ✅ Download own presentations
- ✅ View detailed feedback and recommendations
- ✅ Submission guidelines

## API Endpoints

### Authentication
- `POST /api/login` - User login (staff or student)
- `POST /api/logout` - User logout
- `POST /api/auth/verify` - Verify authentication token

### Staff Endpoints (prefix: `/api/staff`)
- `GET /presentations` - Get all presentations (with filters)
  - Query params: `search`, `department`, `status`, `min_score`, `max_score`
- `GET /presentations/<id>` - Get specific presentation with analysis
- `POST /presentations/<id>/analyze` - Get ML analysis
- `POST /presentations/<id>/approve` - Approve presentation
- `POST /presentations/<id>/reject` - Reject presentation (with reason)
- `GET /presentations/<id>/download` - Download presentation
- `GET /stats` - Get statistics (total, pending, approved, rejected)
- `GET /analytics` - Get analytics (average score, by department, etc.)
- `GET /notifications` - Get notifications

### Student Endpoints (prefix: `/api/student`)
- `GET /presentations?rollNumber=<roll>` - Get student's presentations
- `POST /upload` - Upload new presentation
- `POST /presentations/<id>/analyze` - Get ML analysis
- `GET /presentations/<id>/download` - Download own presentation
- `GET /stats?rollNumber=<roll>` - Get student statistics

## Authentication Flow

1. User opens `index.html`
2. Selects user type (Staff or Student)
3. Enters credentials
4. Backend validates credentials via `/api/login`
5. On success:
   - Authentication data stored in localStorage
   - Staff → redirected to `staff.html`
   - Student → redirected to `student.html`
6. Both dashboards check authentication on load
7. If not authenticated → redirected back to `index.html`

## Data Storage

- **Backend:** JSON file (`data.json`) for presentations and user data
- **Frontend:** localStorage for session management
- **Uploads:** Files stored in `uploads/` directory

## Demo Credentials

### Staff Accounts
- **Email:** `teacher@example.com`
- **Password:** `password123`
- **Name:** Dr. John Smith

- **Email:** `admin@example.com`
- **Password:** `admin123`
- **Name:** Admin User

### Student Accounts
- **Roll Number:** `21CS001`
- **Password:** `student123`
- **Name:** Rahul Kumar
- **Department:** CSE

- **Roll Number:** `21EE015`
- **Password:** `student123`
- **Name:** Priya Sharma
- **Department:** EEE

- **Roll Number:** `21ME023`
- **Password:** `student123`
- **Name:** Amit Patel
- **Department:** MECH

## AI Evaluation System

The system uses ML-based evaluation with the following criteria:
- **Filename Quality** (15%)
- **Content Structure** (25%)
- **Visual Design** (20%)
- **Completeness** (20%)
- **Clarity** (10%)
- **Relevance** (10%)

Each presentation receives:
- Overall score (0-100%)
- Strengths identified
- Areas for improvement
- Detailed recommendations

## Troubleshooting

### Backend not starting
- Check if Python is installed: `python --version`
- Check if port 5000 is available
- Verify all dependencies are installed: `pip list`

### Frontend not connecting to backend
- Ensure backend is running on `http://localhost:5000`
- Check browser console for errors
- Verify CORS is enabled in backend (already configured)

### Authentication issues
- Clear browser localStorage
- Check if credentials match demo accounts
- Verify backend is running and accessible

### Data not loading
- Check backend logs for errors
- Verify `data.json` file exists
- Check browser network tab for API calls

## File Structure Details

- **index.html:** Main login page with authentication logic
- **staff.html:** Staff dashboard with presentation management
- **student.html:** Student dashboard with upload and tracking
- **backend.py:** Flask server with API endpoints and ML evaluation
- **requirements.txt:** Python package dependencies

## Development Notes

- The system uses localStorage for client-side session management
- Backend uses JSON file for data persistence (can be upgraded to database)
- ML evaluation uses scikit-learn for analysis
- Frontend uses Tailwind CSS for styling
- All API calls are asynchronous using Fetch API

## Future Enhancements

- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Real file upload handling
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Multi-file upload support
- [ ] Presentation preview functionality
- [ ] Real-time updates using WebSockets

## Support

For issues or questions:
1. Check the browser console for errors
2. Check backend terminal for server errors
3. Verify all setup steps are completed
4. Ensure backend is running before accessing frontend

## License

This project is for educational/demonstration purposes.
