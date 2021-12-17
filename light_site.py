from flask import Flask, render_template, request #flask includes
import subprocess, time, psutil                   #includes for multiprocessing, timing etc...   

#create the actual flask server 'object'
app = Flask(__name__)
global process
process = None

def show_effect(effect, color1, color2, color3): #create a subprocess that will run the light effect in the bakground... if not the flask server would crash upon the use of infinite loops running effects
    global process
    process = subprocess.Popen(["sudo", "python3", "light_functs.py", str(effect), str(color1), str(color2), str(color3)]) 
    
def kill_proc(proc_id): #kill the previously running process via psutil...
    p = psutil.Process(proc_id)
    for proc in p.children(recursive=True):
        proc.kill()
    p.kill()


#run initialization of hardware directly before the first ping on the server
@app.before_first_request
def before_first_request():
    show_effect("SOLID", "BLACK", "BLACK", "BLACK")
    #set strip to black here 
    

#route handling for homepage... its just static html so nothing crazy here
@app.route("/", methods=['POST', 'GET'])
def home(name=None):
    return render_template("home.html", name=name)


#route handling for the form page 
@app.route("/form", methods=['POST', 'GET'])
def form(name=None):
    global process
    if request.method == 'POST': #if the html is of type post
        if process is not None:  #kill the old process if it exists
            kill_proc(process.pid)
            
        effect = request.form.get('Effect') #parse effects from the html form
        color1 = request.form.get('Color1')
        color2 = request.form.get('Color2')
        color3 = request.form.get('Color3')
        print(str(effect) + "\n" + str(color1) + "\n" + str(color2) + "\n" + str(color3))
        
        show_effect(effect, color1, color2, color3) #run the external python script with the new parameters
        
        return render_template("form.html", name=name, effect=effect, color1=color1, color2=color2, color3=color3) #render the html template

    else: #if the html is of type get
        effect = request.form.get('Effect') 
        color1 = request.form.get('Color1')
        color2 = request.form.get('Color2')
        color3 = request.form.get('Color3')
        return render_template("form.html", name=name, effect=effect, color1=color1, color2=color2, color3=color3) #return html template


if __name__ == "__main__": #actually run the server
    app.run(debug=True, host='0.0.0.0', port=8000, threaded=True)
