from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nunes_sports.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    price = request.form['price']
    new_product = Product(name=name, code=code, description=description, price=price)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    code = request.form['code']
    description = request.form['description']
    price = request.form['price']
    product = Product.query.get(id)
    product.name = name
    product.code = code
    product.description = description
    product.price = price
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)