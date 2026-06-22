from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
from mysql.connector import Error
from neurofuzzy_model import NeuroFuzzyModel
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'heart_disease_db'
}


def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        connection = get_db_connection()
        if connection is None:
            return render_template('register.html', error="Database connection failed. Please try again later.")

        cursor = connection.cursor(dictionary=True)
        try:
            # Check if user already exists
            cursor.execute("SELECT id, name FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                # Existing user → log them in
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                # New user → insert and log in
                cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
                connection.commit()
                user_id = cursor.lastrowid
                session['user_id'] = user_id
                session['user_name'] = name
                return redirect(url_for('dashboard'))
        except Error as e:
            error_msg = f"Database error: {e}"
            return render_template('register.html', error=error_msg)
        finally:
            cursor.close()
            connection.close()

    # GET request
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    return render_template('dashboard.html', user_name=session.get('user_name'))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        # Get form data
        features = {
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'cp': int(request.form['cp']),
            'trestbps': int(request.form['trestbps']),
            'chol': int(request.form['chol']),
            'fbs': int(request.form['fbs']),
            'restecg': int(request.form['restecg']),
            'thalach': int(request.form['thalach']),
            'exang': int(request.form['exang']),
            'oldpeak': float(request.form['oldpeak']),
            'slope': int(request.form['slope']),
            'ca': int(request.form['ca']),
            'thal': int(request.form['thal'])
        }

        # Make prediction
        model = NeuroFuzzyModel()
        risk_percentage, result = model.predict(features)

        # Store in database
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                               INSERT INTO predictions
                               (user_id, age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                                exang, oldpeak, slope, ca, thal, risk_percentage, prediction_result)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                               """, (session['user_id'], features['age'], features['sex'], features['cp'],
                                     features['trestbps'], features['chol'], features['fbs'], features['restecg'],
                                     features['thalach'], features['exang'], features['oldpeak'], features['slope'],
                                     features['ca'], features['thal'], risk_percentage, result))
                connection.commit()
            except Error as e:
                print(f"Database error: {e}")
            finally:
                cursor.close()
                connection.close()

        return render_template('predict.html', prediction={
            'risk_percentage': risk_percentage,
            'result': result,
            'features': features
        })

    return render_template('predict.html', prediction=None)


@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    connection = get_db_connection()
    predictions = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                           SELECT *
                           FROM predictions
                           WHERE user_id = %s
                           ORDER BY prediction_date DESC
                           """, (session['user_id'],))
            predictions = cursor.fetchall()
        except Error as e:
            print(f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()

    return render_template('history.html', predictions=predictions)


@app.route('/download_report')
def download_report():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    # Fetch all predictions for the user
    connection = get_db_connection()
    predictions = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                           SELECT *
                           FROM predictions
                           WHERE user_id = %s
                           ORDER BY prediction_date DESC
                           """, (session['user_id'],))
            predictions = cursor.fetchall()
        except Error as e:
            print(f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()

    # Create PDF report
    filename = f"heart_disease_report_{session['user_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24,
                                 textColor=colors.HexColor('#2c3e50'))
    story.append(Paragraph("Heart Disease Detection Report", title_style))
    story.append(Spacer(1, 0.3 * inch))

    # User info
    story.append(Paragraph(f"User Name: {session.get('user_name')}", styles['Normal']))
    story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    # Summary statistics
    if predictions:
        avg_risk = sum(p['risk_percentage'] for p in predictions) / len(predictions)
        high_risk_count = sum(1 for p in predictions if p['risk_percentage'] > 50)

        story.append(Paragraph("Summary Statistics", styles['Heading2']))
        story.append(Paragraph(f"Total Predictions: {len(predictions)}", styles['Normal']))
        story.append(Paragraph(f"Average Risk: {avg_risk:.2f}%", styles['Normal']))
        story.append(Paragraph(f"High Risk Predictions: {high_risk_count}", styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))

        # Predictions table
        story.append(Paragraph("Prediction History", styles['Heading2']))

        table_data = [['Date', 'Age', 'BP', 'Chol', 'Risk %', 'Result']]
        for pred in predictions:
            table_data.append([
                pred['prediction_date'].strftime('%Y-%m-%d'),
                str(pred['age']),
                str(pred['trestbps']),
                str(pred['chol']),
                f"{pred['risk_percentage']}%",
                pred['prediction_result']
            ])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)

    doc.build(story)

    return send_file(filename, as_attachment=True, download_name=filename)


@app.route('/accuracy')
def show_accuracy():
    if 'user_id' not in session:
        return redirect(url_for('register'))

    model = NeuroFuzzyModel()
    try:
        metrics = model.evaluate_accuracy()
        return render_template('accuracy.html', metrics=metrics)
    except Exception as e:
        return render_template('accuracy.html', error=str(e))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)