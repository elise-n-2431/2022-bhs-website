from flask import Flask, render_template, redirect, request
app=Flask(__name__)

@app.route('/divpoints',methods=['POST','GET'])
def divpoints():
    if request.method=='POST':
        idk=[request.form.get("North"),request.form.get("Password")]
        print(idk)
    return render_template('divisionalpoints.html')
if __name__=="__main__":
    app.run(debug=True)