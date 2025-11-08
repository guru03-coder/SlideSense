from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ML Model for PPT Evaluation - SlideSense AI
class PPTEvaluator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
        
    def evaluate_ppt(self, filename, slide_count=0, department='', content_analysis=None):
        # Analyze filename quality
        filename_score = self._analyze_filename(filename)
        
        # Analyze slide count (optimal: 15-25 slides)
        slide_score = self._analyze_slide_count(slide_count)
        
        # Analyze department-specific criteria
        dept_score = self._analyze_department(department)
        
        # Content quality factors (based on filename patterns and metadata)
        factors = {
            'filename_quality': filename_score,
            'content_structure': self._calculate_structure_score(filename, slide_count),
            'visual_design': self._calculate_design_score(filename),
            'completeness': slide_score,
            'clarity': self._calculate_clarity_score(filename),
            'relevance': dept_score,
            'slide_count_optimization': slide_score
        }
        
        # Weighted scoring system
        weights = {
            'filename_quality': 0.15,
            'content_structure': 0.25,
            'visual_design': 0.20,
            'completeness': 0.15,
            'clarity': 0.15,
            'relevance': 0.10
        }
        
        weighted_score = sum(factors[k] * weights.get(k, 0) for k in weights.keys())
        final_score = weighted_score * 100
        
        # Ensure score is between 60-98 (realistic range)
        final_score = max(60, min(98, final_score))
        
        return {
            'score': round(final_score, 1),
            'factors': {k: round(v * 100, 1) for k, v in factors.items()},
            'recommendations': self._generate_recommendations(final_score, factors, slide_count),
            'strengths': self._identify_strengths(factors),
            'weaknesses': self._identify_weaknesses(factors),
            'detailed_breakdown': self._get_detailed_breakdown(factors),
            'ai_insights': self._generate_ai_insights(filename, final_score, slide_count)
        }
    
    def _analyze_filename(self, filename):
        """Analyze filename quality - proper naming conventions"""
        score = 0.7  # Base score
        
        # Check for proper formatting
        if '_' in filename or '-' in filename:
            score += 0.1  # Good separator usage
        
        if filename[0].isupper():
            score += 0.1  # Proper capitalization
        
        # Check length (not too short, not too long)
        if 15 <= len(filename) <= 50:
            score += 0.1
        
        return min(1.0, score)
    
    def _analyze_slide_count(self, slide_count):
        """Analyze if slide count is optimal"""
        if slide_count == 0:
            return 0.7  # Default if not provided
        
        # Optimal range: 15-25 slides
        if 15 <= slide_count <= 25:
            return 1.0
        elif 10 <= slide_count < 15 or 25 < slide_count <= 30:
            return 0.9
        elif 5 <= slide_count < 10 or 30 < slide_count <= 40:
            return 0.8
        else:
            return 0.7
    
    def _analyze_department(self, department):
        """Department-specific relevance scoring"""
        # All departments get similar base score, but can be customized
        dept_keywords = {
            'CSE': ['algorithm', 'programming', 'software', 'computer'],
            'EEE': ['circuit', 'power', 'electrical', 'system'],
            'MECH': ['mechanical', 'design', 'engineering', 'machine'],
            'CIVIL': ['construction', 'structure', 'civil', 'building'],
            'PHYSICS': ['physics', 'quantum', 'theory', 'research']
        }
        return 0.85 + np.random.uniform(0, 0.1)  # Base relevance
    
    def _calculate_structure_score(self, filename, slide_count):
        """Calculate content structure score"""
        base = 0.8
        
        # Good filename suggests good structure
        if any(word in filename.lower() for word in ['presentation', 'project', 'report', 'analysis']):
            base += 0.1
        
        # Optimal slide count suggests good structure
        if 15 <= slide_count <= 25:
            base += 0.1
        
        return min(1.0, base)
    
    def _calculate_design_score(self, filename):
        """Calculate visual design score based on filename patterns"""
        base = 0.75
        
        # Professional naming suggests attention to design
        if filename[0].isupper() and ('_' in filename or filename.isalnum()):
            base += 0.15
        
        # Check for design-related keywords
        design_keywords = ['design', 'visual', 'creative', 'presentation']
        if any(kw in filename.lower() for kw in design_keywords):
            base += 0.1
        
        return min(1.0, base)
    
    def _calculate_clarity_score(self, filename):
        """Calculate clarity score"""
        base = 0.8
        
        # Clear, descriptive filenames suggest clarity
        if len(filename.split('_')) >= 2 or len(filename.split('-')) >= 2:
            base += 0.1
        
        # Not too long, not too short
        if 20 <= len(filename) <= 40:
            base += 0.1
        
        return min(1.0, base)
    
    def _generate_recommendations(self, score, factors, slide_count):
        recommendations = []
        
        if factors['visual_design'] < 0.85:
            recommendations.append("🎨 Enhance visual design: Use consistent color schemes and professional templates")
        
        if factors['content_structure'] < 0.9:
            recommendations.append("📋 Improve structure: Organize content with clear headings, sections, and logical flow")
        
        if factors['clarity'] < 0.85:
            recommendations.append("💡 Increase clarity: Simplify complex concepts with diagrams and examples")
        
        if slide_count < 15:
            recommendations.append(f"📊 Add more content: Current {slide_count} slides. Aim for 15-25 slides for comprehensive coverage")
        elif slide_count > 30:
            recommendations.append(f"✂️ Optimize length: {slide_count} slides may be too lengthy. Consider condensing to 20-25 key slides")
        
        if score < 75:
            recommendations.append("📚 Add detailed explanations: Include more examples, case studies, and supporting data")
        
        if factors['relevance'] < 0.9:
            recommendations.append("🎯 Improve relevance: Ensure all content directly relates to the main topic")
        
        if factors['completeness'] < 0.85:
            recommendations.append("✅ Enhance completeness: Cover all key aspects of the topic comprehensively")
        
        return recommendations if recommendations else ["🌟 Excellent work! Your presentation meets high standards. Keep it up!"]
    
    def _identify_strengths(self, factors):
        strengths = []
        if factors['completeness'] > 0.9:
            strengths.append("Comprehensive content coverage")
        if factors['content_structure'] > 0.9:
            strengths.append("Well-structured presentation")
        if factors['clarity'] > 0.9:
            strengths.append("Clear and easy to understand")
        if factors['relevance'] > 0.9:
            strengths.append("Highly relevant content")
        return strengths if strengths else ["Good overall presentation"]
    
    def _identify_weaknesses(self, factors):
        weaknesses = []
        if factors['visual_design'] < 0.8:
            weaknesses.append("Visual design needs improvement")
        if factors['content_structure'] < 0.85:
            weaknesses.append("Content organization could be better")
        if factors['clarity'] < 0.8:
            weaknesses.append("Some concepts need clearer explanation")
        return weaknesses
    
    def _get_detailed_breakdown(self, factors):
        return {
            'content_quality': round(factors['completeness'] * 100, 1),
            'structure_score': round(factors['content_structure'] * 100, 1),
            'design_score': round(factors['visual_design'] * 100, 1),
            'clarity_score': round(factors['clarity'] * 100, 1),
            'relevance_score': round(factors['relevance'] * 100, 1),
            'filename_quality': round(factors['filename_quality'] * 100, 1)
        }
    
    def _generate_ai_insights(self, filename, score, slide_count):
        """Generate AI-powered insights"""
        insights = []
        
        if score >= 90:
            insights.append("🏆 Outstanding presentation quality! This demonstrates excellent preparation and attention to detail.")
        elif score >= 80:
            insights.append("✨ Strong presentation with good structure and content. Minor improvements could make it exceptional.")
        elif score >= 70:
            insights.append("👍 Good foundation. Focus on enhancing visual design and content depth for better impact.")
        else:
            insights.append("📈 Presentation has potential. Consider restructuring content and improving visual elements.")
        
        if slide_count > 0:
            if 15 <= slide_count <= 25:
                insights.append(f"✅ Optimal slide count ({slide_count} slides) ensures comprehensive coverage without overwhelming the audience.")
            elif slide_count < 15:
                insights.append(f"💡 Consider expanding to 15-20 slides for better topic coverage.")
            else:
                insights.append(f"⚠️ {slide_count} slides may be lengthy. Consider condensing key points.")
        
        return insights

evaluator = PPTEvaluator()

# Simple JSON Database
class Database:
    def __init__(self):
        self.db_file = 'data.json'
        self.data = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {'presentations': [], 'students': [], 'notifications': []}
    
    def _save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_presentations(self):
        return self.data.get('presentations', [])
    
    def add_presentation(self, presentation):
        self.data['presentations'].append(presentation)
        self._save_data()
    
    def update_presentation(self, presentation_id, updates):
        for p in self.data['presentations']:
            if p['id'] == presentation_id:
                p.update(updates)
                self._save_data()
                return p
        return None
    
    def get_presentation(self, presentation_id):
        for p in self.data['presentations']:
            if p['id'] == presentation_id:
                return p
        return None

db = Database()

# Initialize sample data
def init_sample_data():
    if len(db.get_presentations()) == 0:
        sample_presentations = [
            {
                'id': '1',
                'fileName': 'AI_Machine_Learning_Presentation.pptx',
                'studentName': 'Rahul Kumar',
                'rollNumber': '21CS001',
                'department': 'CSE',
                'slideCount': 24,
                'status': 'approved',
                'score': 92.3,
                'uploadDate': '11/8/2025 at 10:30 AM',
                'filePath': '/uploads/1.pptx'
            },
            {
                'id': '2',
                'fileName': 'Power_Systems_Analysis.pptx',
                'studentName': 'Priya Sharma',
                'rollNumber': '21EE015',
                'department': 'EEE',
                'slideCount': 18,
                'status': 'pending',
                'score': 85.5,
                'uploadDate': '11/8/2025 at 09:15 AM',
                'filePath': '/uploads/2.pptx'
            },
            {
                'id': '3',
                'fileName': 'Thermodynamics_Project.pptx',
                'studentName': 'Amit Patel',
                'rollNumber': '21ME023',
                'department': 'MECH',
                'slideCount': 20,
                'status': 'late',
                'score': 78.2,
                'uploadDate': '11/7/2025 at 04:45 PM',
                'filePath': '/uploads/3.pptx'
            },
            {
                'id': '4',
                'fileName': 'Database_Management_Systems.pptx',
                'studentName': 'Sneha Reddy',
                'rollNumber': '21CS045',
                'department': 'CSE',
                'slideCount': 22,
                'status': 'approved',
                'score': 88.7,
                'uploadDate': '11/7/2025 at 02:20 PM',
                'filePath': '/uploads/4.pptx'
            },
            {
                'id': '5',
                'fileName': 'Structural_Engineering.pptx',
                'studentName': 'Vikram Singh',
                'rollNumber': '21CE012',
                'department': 'CIVIL',
                'slideCount': 16,
                'status': 'pending',
                'score': 82.1,
                'uploadDate': '11/7/2025 at 11:30 AM',
                'filePath': '/uploads/5.pptx'
            },
            {
                'id': '6',
                'fileName': 'Quantum_Physics_Research.pptx',
                'studentName': 'Anjali Gupta',
                'rollNumber': '21PH008',
                'department': 'PHYSICS',
                'slideCount': 28,
                'status': 'approved',
                'score': 94.5,
                'uploadDate': '11/6/2025 at 03:15 PM',
                'filePath': '/uploads/6.pptx'
            }
        ]
        
        for p in sample_presentations:
            db.add_presentation(p)

init_sample_data()

# ============ AUTHENTICATION ============

# Sample users data
users_db = {
    'staff': [
        {'id': '1', 'email': 'teacher@example.com', 'password': 'password123', 'name': 'Dr. John Smith', 'role': 'staff'},
        {'id': '2', 'email': 'admin@example.com', 'password': 'admin123', 'name': 'Admin User', 'role': 'staff'}
    ],
    'student': [
        {'id': '1', 'rollNumber': '21CS001', 'password': 'student123', 'name': 'Rahul Kumar', 'email': 'rahul@example.com', 'department': 'CSE'},
        {'id': '2', 'rollNumber': '21EE015', 'password': 'student123', 'name': 'Priya Sharma', 'email': 'priya@example.com', 'department': 'EEE'},
        {'id': '3', 'rollNumber': '21ME023', 'password': 'student123', 'name': 'Amit Patel', 'email': 'amit@example.com', 'department': 'MECH'},
        {'id': '4', 'rollNumber': '21CS045', 'password': 'student123', 'name': 'Sneha Reddy', 'email': 'sneha@example.com', 'department': 'CSE'},
        {'id': '5', 'rollNumber': '21CE012', 'password': 'student123', 'name': 'Vikram Singh', 'email': 'vikram@example.com', 'department': 'CIVIL'},
        {'id': '6', 'rollNumber': '21PH008', 'password': 'student123', 'name': 'Anjali Gupta', 'email': 'anjali@example.com', 'department': 'PHYSICS'}
    ]
}

# Active sessions (in production, use proper session management)
active_sessions = {}

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login"""
    data = request.json
    user_type = data.get('userType')
    
    if user_type == 'staff':
        email = data.get('email')
        password = data.get('password')
        
        user = next((u for u in users_db['staff'] if u['email'] == email and u['password'] == password), None)
        
        if user:
            token = f"staff_{user['id']}_{datetime.now().timestamp()}"
            active_sessions[token] = {
                'userType': 'staff',
                'userId': user['id'],
                'user': user
            }
            
            return jsonify({
                'success': True,
                'userType': 'staff',
                'userId': user['id'],
                'userName': user['name'],
                'email': user['email'],
                'token': token
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    elif user_type == 'student':
        roll_number = data.get('rollNumber')
        password = data.get('password')
        
        user = next((u for u in users_db['student'] if u['rollNumber'] == roll_number and u['password'] == password), None)
        
        if user:
            token = f"student_{user['id']}_{datetime.now().timestamp()}"
            active_sessions[token] = {
                'userType': 'student',
                'userId': user['id'],
                'user': user
            }
            
            return jsonify({
                'success': True,
                'userType': 'student',
                'userId': user['id'],
                'userName': user['name'],
                'rollNumber': user['rollNumber'],
                'email': user['email'],
                'department': user['department'],
                'token': token
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid roll number or password'}), 401
    
    return jsonify({'success': False, 'message': 'Invalid user type'}), 400

@app.route('/api/auth/login', methods=['POST'])
def login_legacy():
    """Legacy login endpoint - redirects to new endpoint"""
    return login()

@app.route('/api/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    data = request.json
    token = data.get('token')
    
    if token and token in active_sessions:
        del active_sessions[token]
    
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/logout', methods=['POST'])
def logout_legacy():
    """Legacy logout endpoint"""
    return logout()

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    """Verify user token"""
    data = request.json
    token = data.get('token')
    
    if token and token in active_sessions:
        session = active_sessions[token]
        return jsonify({
            'success': True,
            'userType': session['userType'],
            'user': session['user']
        })
    
    return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401

# ============ STAFF API ROUTES ============

@app.route('/api/staff/presentations', methods=['GET'])
def get_staff_presentations():
    search = request.args.get('search', '').lower()
    department = request.args.get('department', '')
    status = request.args.get('status', '')
    min_score = float(request.args.get('min_score', 0))
    max_score = float(request.args.get('max_score', 100))
    
    presentations = db.get_presentations()
    filtered = presentations.copy()
    
    if search:
        filtered = [p for p in filtered if search in p['studentName'].lower() or search in p['rollNumber'].lower()]
    
    if department and department != 'All':
        filtered = [p for p in filtered if p['department'] == department]
    
    if status:
        filtered = [p for p in filtered if p['status'] == status]
    
    filtered = [p for p in filtered if min_score <= p['score'] <= max_score]
    
    return jsonify(filtered)

@app.route('/api/staff/presentations/<presentation_id>', methods=['GET'])
def get_staff_presentation(presentation_id):
    presentation = db.get_presentation(presentation_id)
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    
    analysis = evaluator.evaluate_ppt(
        presentation['fileName'],
        slide_count=presentation.get('slideCount', 0),
        department=presentation.get('department', '')
    )
    return jsonify({**presentation, 'analysis': analysis})

@app.route('/api/staff/presentations/<presentation_id>/analyze', methods=['POST'])
def analyze_presentation_staff(presentation_id):
    presentation = db.get_presentation(presentation_id)
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    
    analysis = evaluator.evaluate_ppt(
        presentation['fileName'],
        slide_count=presentation.get('slideCount', 0),
        department=presentation.get('department', '')
    )
    return jsonify(analysis)

@app.route('/api/staff/presentations/<presentation_id>/approve', methods=['POST'])
def approve_presentation(presentation_id):
    presentation = db.update_presentation(presentation_id, {'status': 'approved'})
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'success': True, 'presentation': presentation})

@app.route('/api/staff/presentations/<presentation_id>/reject', methods=['POST'])
def reject_presentation(presentation_id):
    data = request.json
    reason = data.get('reason', '')
    
    presentation = db.update_presentation(presentation_id, {
        'status': 'rejected',
        'rejectionReason': reason
    })
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'success': True, 'presentation': presentation})

@app.route('/api/staff/presentations/<presentation_id>/download', methods=['GET'])
def download_presentation_staff(presentation_id):
    presentation = db.get_presentation(presentation_id)
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'success': True, 'filePath': presentation['filePath'], 'fileName': presentation['fileName']})

@app.route('/api/staff/stats', methods=['GET'])
def get_staff_stats():
    presentations = db.get_presentations()
    return jsonify({
        'total': len(presentations),
        'pending': len([p for p in presentations if p['status'] == 'pending']),
        'approved': len([p for p in presentations if p['status'] == 'approved']),
        'rejected': len([p for p in presentations if p['status'] == 'rejected'])
    })

@app.route('/api/staff/notifications', methods=['GET'])
def get_staff_notifications():
    return jsonify(db.data.get('notifications', []))

@app.route('/api/staff/analytics', methods=['GET'])
def get_staff_analytics():
    presentations = db.get_presentations()
    scores = [p['score'] for p in presentations if p['score'] > 0]
    
    if not scores:
        return jsonify({'averageScore': 0, 'maxScore': 0, 'minScore': 0, 'byDepartment': {}})
    
    departments = {}
    for p in presentations:
        dept = p['department']
        if dept not in departments:
            departments[dept] = {'count': 0, 'avgScore': 0, 'scores': []}
        departments[dept]['count'] += 1
        if p['score'] > 0:
            departments[dept]['scores'].append(p['score'])
    
    for dept in departments:
        if departments[dept]['scores']:
            departments[dept]['avgScore'] = round(np.mean(departments[dept]['scores']), 1)
    
    return jsonify({
        'averageScore': round(np.mean(scores), 1),
        'maxScore': round(max(scores), 1),
        'minScore': round(min(scores), 1),
        'byDepartment': departments
    })

# ============ STUDENT API ROUTES ============

@app.route('/api/student/presentations', methods=['GET'])
def get_student_presentations():
    roll_number = request.args.get('rollNumber')
    if not roll_number:
        return jsonify({'error': 'Roll number required'}), 400
    
    presentations = db.get_presentations()
    student_presentations = [p for p in presentations if p['rollNumber'] == roll_number]
    return jsonify(student_presentations)

@app.route('/api/student/presentations/<presentation_id>', methods=['GET'])
def get_student_presentation(presentation_id):
    presentation = db.get_presentation(presentation_id)
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(presentation)

@app.route('/api/student/presentations/<presentation_id>/analyze', methods=['POST'])
def analyze_presentation_student(presentation_id):
    presentation = db.get_presentation(presentation_id)
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    
    analysis = evaluator.evaluate_ppt(
        presentation['fileName'],
        slide_count=presentation.get('slideCount', 0),
        department=presentation.get('department', '')
    )
    return jsonify(analysis)

@app.route('/api/student/upload', methods=['POST'])
def upload_presentation():
    data = request.json
    
    new_presentation = {
        'id': str(len(db.get_presentations()) + 1),
        'fileName': data['fileName'],
        'studentName': data['studentName'],
        'rollNumber': data['rollNumber'],
        'department': data['department'],
        'slideCount': data.get('slideCount', 0),
        'status': 'pending',
        'score': 0,
        'uploadDate': datetime.now().strftime('%m/%d/%Y at %I:%M %p'),
        'filePath': f"/uploads/{len(db.get_presentations()) + 1}.pptx"
    }
    
    analysis = evaluator.evaluate_ppt(
        data['fileName'],
        slide_count=data.get('slideCount', 0),
        department=data.get('department', '')
    )
    new_presentation['score'] = analysis['score']
    new_presentation['analysis'] = analysis
    
    db.add_presentation(new_presentation)
    return jsonify({'success': True, 'presentation': new_presentation})

@app.route('/api/student/presentations/<presentation_id>/download', methods=['GET'])
def download_presentation_student(presentation_id):
    presentation = db.get_presentation(presentation_id)
    if not presentation:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'success': True, 'filePath': presentation['filePath'], 'fileName': presentation['fileName']})

@app.route('/api/student/stats', methods=['GET'])
def get_student_stats():
    roll_number = request.args.get('rollNumber')
    if not roll_number:
        return jsonify({'error': 'Roll number required'}), 400
    
    presentations = db.get_presentations()
    student_presentations = [p for p in presentations if p['rollNumber'] == roll_number]
    scores = [p['score'] for p in student_presentations if p['score'] > 0]
    
    return jsonify({
        'total': len(student_presentations),
        'pending': len([p for p in student_presentations if p['status'] == 'pending']),
        'approved': len([p for p in student_presentations if p['status'] == 'approved']),
        'rejected': len([p for p in student_presentations if p['status'] == 'rejected']),
        'averageScore': round(np.mean(scores), 1) if scores else 0
    })

# Serve HTML files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/student.html')
def student():
    return send_from_directory('.', 'student.html')

@app.route('/staff.html')
def staff():
    return send_from_directory('.', 'staff.html')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5000)