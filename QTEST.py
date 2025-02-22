from flask import Flask, render_template_string
import getpass
import pytz
from datetime import datetime
import psutil
import platform
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>System Information</title>
    <style>
        body {
            font-family: monospace;
            padding: 20px;
        }
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h3>Name: {{ name }}</h3>
    <h3>User: {{ username }}</h3>
    <h3>Server Time (IST): {{ server_time }}</h3>
    <h3>TOP output:</h3>
    <pre>{{ top_output }}</pre>
</body>
</html>
'''

def get_system_info():
    try:
        # Basic system info
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        output = "System Information:\n"
        output += f"CPU Usage: {cpu_percent}%\n"
        output += f"Memory Total: {memory.total/1024/1024:.1f}MB\n"
        output += f"Memory Available: {memory.available/1024/1024:.1f}MB\n"
        output += f"Memory Used: {memory.used/1024/1024:.1f}MB\n\n"
        
        # Process list
        output += "Process Information:\n"
        output += f"{'PID':>7} {'CPU%':>6} {'MEM%':>6} {'NAME':>15}\n"
        
        for proc in psutil.process_iter(['pid', 'cpu_percent', 'memory_percent', 'name']):
            try:
                info = proc.info
                output += f"{info['pid']:7d} {info.get('cpu_percent', 0):6.1f} {info.get('memory_percent', 0):6.1f} {info.get('name', 'unknown'):15}\n"
            except Exception as e:
                app.logger.error(f"Error getting process info: {e}")
                continue
                
        return output
    except Exception as e:
        app.logger.error(f"Error in get_system_info: {e}")
        return "Error getting system information"

@app.route('/htop')
def htop():
    try:
        # Get system username
        username = getpass.getuser()
        
        # Get current time in IST
        ist = pytz.timezone('Asia/Kolkata')
        server_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
        
        # Get system information
        top_output = get_system_info()

        return render_template_string(HTML_TEMPLATE, 
            name="Naresh Kumar",
            username=username,
            server_time=server_time,
            top_output=top_output
        )
    except Exception as e:
        app.logger.error(f"Error in htop route: {e}")
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)