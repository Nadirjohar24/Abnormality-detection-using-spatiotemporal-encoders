from flask import Flask, request, render_template, redirect, url_for
import os
from your_existing_code import process_video

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        video = request.files['video']
        if video:
            # Create a unique filename for the uploaded video
            video_filename = os.path.join("static/uploads", video.filename)
            video.save(video_filename)

            # Process the video and get abnormal event timestamps
            abnormal_events = process_video(video_filename)

            # Write the abnormal_events to a log file
            log_filename = "static/uploads/abnormal_events.log"
            with open(log_filename, "w") as log_file:
                for timestamp in abnormal_events:
                    log_file.write(f"Abnormal Event at {timestamp} ms\n")

            # Redirect to the results page
            return redirect(url_for('results'))

    return render_template('upload.html')



@app.route('/results')
def results():
    log_filename = "static/uploads/abnormal_events.log"
    if os.path.exists(log_filename):
        with open(log_filename, "r") as log_file:
            log_contents = log_file.read()
    else:
        log_contents = "No abnormal events detected."

    return render_template('results.html', log_contents=log_contents)

if __name__ == '__main__':
    app.run(debug=True)
