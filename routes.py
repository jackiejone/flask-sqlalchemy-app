import os 

from flask import Flask, render_template, request, redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "backpack_database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Backpack(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    item = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return self.item

db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        item = Backpack(item=request.form.get("item"))
        db.session.add(item)
        db.session.commit()
    backpack_items = Backpack.query.all()
    return render_template("home.html", backpack_items=backpack_items)

@app.route('/delete', methods=["POST"])
def delete():
    item_name = request.form.get("item")
    backpack_item = Backpack.query.filter_by(item=item_name).first()
    if backpack_item == None:
        print("no such item in db")
    else:
        db.session.delete(backpack_item)
        db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)