from flask import Flask, request, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import io
import os

app = Flask(__name__)

# Function to create the COPUS timeline visualization
def create_copus_timeline(file_path):
    # Load and process the data (same logic as before)
    copus_data = pd.read_excel(file_path)
    copus_data.columns = ['Minute', 'Students_Activity1', 'Students_Activity2', 'Students_Activity3',
                          'Students_Activity4', 'Students_Activity5', 'Students_Activity6', 'Students_Activity7',
                          'Students_Activity8', 'Students_Activity9', 'Professor_Activity1', 'Professor_Activity2',
                          'Professor_Activity3', 'Professor_Activity4', 'Professor_Activity5', 'Professor_Activity6',
                          'Professor_Activity7', 'Professor_Activity8', 'Engagement', 'Comments']
    copus_data = copus_data.drop([0, 1]).reset_index(drop=True)
    copus_data['Minute'] = pd.to_numeric(copus_data['Minute'], errors='coerce')
    activity_columns = copus_data.columns[1:-2]
    activity_data = copus_data[activity_columns].applymap(lambda x: 1 if x == 'x' else 0)
    activity_data['Minute'] = copus_data['Minute']
    activity_data.set_index('Minute', inplace=True)

    # Define labels and colors (same as before)
    label_mapping = {
        'Students_Activity1': 'Listening',
        'Students_Activity2': 'Individual Activity Time',
        'Students_Activity3': 'Asking',
        'Students_Activity4': 'Answering',
        'Students_Activity5': 'Copying',
        'Students_Activity6': 'Creating',
        'Students_Activity7': 'Modeling (using model kit)',
        'Students_Activity8': 'Drawing Paper',
        'Students_Activity9': 'Drawing Computer',
        'Professor_Activity1': 'Lecturing',
        'Professor_Activity2': 'Asking',
        'Professor_Activity3': 'Answering',
        'Professor_Activity4': 'Teaching from Slides',
        'Professor_Activity5': 'Teaching from Chalkboard/Whiteboard',
        'Professor_Activity6': 'Teaching from Physical Model',
        'Professor_Activity7': 'Chem Visual Present',
        'Professor_Activity8': 'Mentions/Explains Visual'
    }

    professor_colors = ['#cce7ff', '#99cfff', '#66b8ff', '#339fff', '#0087ff', '#006bcc', '#004f99', '#003366']
    student_colors = ['#ffc2c2', '#ff9999', '#ff6666', '#ff4d4d', '#ff3333', '#cc0000', '#990000', '#660000']
    activity_color_mapping = {
        'Students_Activity1': student_colors[0], 'Students_Activity2': student_colors[1],
        'Students_Activity3': student_colors[2], 'Students_Activity4': student_colors[3],
        'Students_Activity5': student_colors[4], 'Students_Activity6': student_colors[5],
        'Students_Activity7': student_colors[6], 'Students_Activity8': student_colors[7],
        'Students_Activity9': student_colors[0], 'Professor_Activity1': professor_colors[0],
        'Professor_Activity2': professor_colors[1], 'Professor_Activity3': professor_colors[2],
        'Professor_Activity4': professor_colors[3], 'Professor_Activity5': professor_colors[4],
        'Professor_Activity6': professor_colors[5], 'Professor_Activity7': professor_colors[6],
        'Professor_Activity8': professor_colors[7]
    }

    # Generate the plot
    fig, ax = plt.subplots(figsize=(12, 8))
    y_pos = 0
    for col in activity_data.columns[:-2]:  # Exclude 'Engagement' and 'Comments'
        active_intervals = activity_data[activity_data[col] == 1].index.values
        for interval in active_intervals:
            ax.hlines(y=y_pos, xmin=interval, xmax=interval + 2, color=activity_color_mapping[col], linewidth=10)
        y_pos += 1
    ax.set_yticks(range(len(activity_data.columns[:-2])))
    ax.set_yticklabels([label_mapping[col] for col in activity_data.columns[:-2]])
    ax.set_xlabel('Minute')
    ax.set_title('COPUS Timeline of Student and Professor Activities')
    plt.grid(False)

    # Increase left margin to prevent label cutoff
    plt.subplots_adjust(left=0.3)  # Adjust this value as needed to add more space for labels
    plt.grid(False)

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)  # Close the figure to free memory
    return buf

@app.route('/')
def index():
    return render_template('index.html')  # Main HTML upload page

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    if file:
        buf = create_copus_timeline(file)
        return send_file(buf, mimetype='image/png', as_attachment=True, download_name='copus_timeline.png')

# Route to download the COPUS template file
@app.route('/download-template')
def download_template():
    # Path to the template file
    template_path = os.path.join(app.root_path, 'COPUS_template.xlsx')
    return send_file(template_path, as_attachment=True, download_name='COPUS_template.xlsx')

if __name__ == '__main__':
    app.run(debug=True)
